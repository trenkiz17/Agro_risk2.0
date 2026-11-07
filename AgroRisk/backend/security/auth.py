"""Identidade autenticada pelo token assinado e temporário do Flask."""

from flask import current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from models.database import db
from models.usuario import Usuario


def _serializador():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt="agrorisk-token-v1"
    )


def criar_token(usuario_id):
    return _serializador().dumps({"uid": int(usuario_id)})


def exigir_autenticacao():
    cabecalho = request.headers.get("Authorization", "")
    partes = cabecalho.split()
    if len(partes) != 2 or partes[0].lower() != "bearer":
        return jsonify({"erro": "Faça login para continuar."}), 401

    try:
        payload = _serializador().loads(
            partes[1],
            max_age=current_app.config["AGRORISK_TOKEN_TTL"]
        )
        usuario_id = int(payload["uid"])
        if usuario_id < 1:
            raise ValueError("ID inválido")
    except (BadSignature, SignatureExpired, ValueError, KeyError, TypeError):
        return jsonify({"erro": "Sessão inválida ou expirada. Entre novamente."}), 401

    if db.session.get(Usuario, usuario_id) is None:
        return jsonify({"erro": "Conta indisponível. Faça login novamente."}), 401

    g.usuario_id = usuario_id
    return None
