"""Endpoints de IA: autenticação, validação e controle local de volume."""
from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from flask import Blueprint, g, jsonify, request
from services.orientador_ia_service import FalhaOrientador, OrientadorIAService

orientador_controller = Blueprint("orientador_controller", __name__)
_pedidos = defaultdict(deque)
_lock = Lock()


def _limitado(usuario_id):
    agora = monotonic()
    with _lock:
        # Proteção simples para o protótipo. Em produção, usar rate limit compartilhado.
        if len(_pedidos) > 2000:
            for chave in list(_pedidos):
                if not _pedidos[chave] or agora - _pedidos[chave][-1] > 600:
                    del _pedidos[chave]
        historico = _pedidos[usuario_id]
        while historico and agora - historico[0] > 600:
            historico.popleft()
        if len(historico) >= 8:
            return True
        historico.append(agora)
        return False


@orientador_controller.get("/api/orientador/status")
def status():
    import os
    chave = os.getenv("GEMINI_API_KEY", "").strip()
    pronta = len(chave) >= 15 and not chave.upper().startswith(("COLE", "SUA", "INSIRA", "GERAR"))
    return jsonify({"configurada": pronta, "modelo": os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")})


@orientador_controller.post("/api/orientador/perguntar")
def perguntar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON válido."}), 400
    pergunta = dados.get("pergunta", "")
    if not isinstance(pergunta, str) or not 2 <= len(pergunta.strip()) <= 900:
        return jsonify({"erro": "Escreva uma pergunta de 2 a 900 caracteres."}), 400
    if dados.get("consentimento") is not True:
        return jsonify({"erro": "Confirme o envio da pergunta ao serviço externo de IA."}), 400
    historico = dados.get("historico", [])
    if not isinstance(historico, list) or len(historico) > 10:
        return jsonify({"erro": "Histórico inválido."}), 400

    def id_opcional(nome):
        valor = dados.get(nome)
        if valor in (None, ""):
            return None
        if type(valor) is not int or valor <= 0:
            raise FalhaOrientador(f"{nome} inválido.", 400)
        return valor

    try:
        propriedade_id = id_opcional("propriedade_id")
        safra_id = id_opcional("safra_id")
        # Validação do contexto ANTES de consumir a quota do provedor.
        servico = OrientadorIAService()
        # O método _contexto aplica isolamento por usuário no ORM.
        servico._contexto(g.usuario_id, propriedade_id, safra_id, False)
        if _limitado(g.usuario_id):
            return jsonify({"erro": "Limite de 8 perguntas em 10 minutos. Aguarde para perguntar novamente."}), 429
        resultado = servico.responder(
            g.usuario_id,
            pergunta.strip(),
            historico,
            propriedade_id=propriedade_id,
            safra_id=safra_id,
            incluir_clima=dados.get("incluir_clima") is True,
        )
        return jsonify(resultado), 200
    except FalhaOrientador as erro:
        return jsonify({"erro": str(erro)}), erro.status
