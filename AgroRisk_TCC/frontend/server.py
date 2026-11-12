"""Servidor web do AgroRisk separado da API.

- Frontend: 127.0.0.1:5500 (paginas HTML e arquivos estaticos).
- Backend:  127.0.0.1:5000 (rotas da API; banco MySQL).

O proxy HTTP de rotas de dados mantém o navegador na mesma origem, portanto
os JavaScripts, o token Bearer e as telas originais continuam funcionando
inclusive pelo Cloudflare Tunnel, sem CORS aberto e sem mudar a API_URL.
"""
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, Response, abort, jsonify, redirect, render_template, request, url_for

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

PAGINAS = {
    "index", "login", "cadastro", "dashboard", "perfil", "propriedades",
    "cadastro_propriedade", "monitoramento", "safras", "cadastro_safras",
    "relatorios", "orientador", "assistente", "ferramentas",
}
PREFIXOS_API = ("api", "usuarios", "propriedades", "safras")
ROTAS_API_EXATAS = ("login",)


def create_frontend_app():
    app = Flask(
        __name__,
        template_folder=str(BACKEND / "templates"),
        static_folder=str(BACKEND / "static"),
        static_url_path="/static",
    )

    # Nunca transformar a URL do backend em um destino arbitrario vindo da web.
    backend_url = os.environ.get("AGRORISK_BACKEND_URL", "http://127.0.0.1:5000").rstrip("/")
    if backend_url not in ("http://127.0.0.1:5000", "http://localhost:5000", "http://127.0.0.1:5001"):
        raise RuntimeError("AGRORISK_BACKEND_URL deve apontar para a API local na porta 5000.")

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.route("/<path:recurso>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    def pagina_ou_proxy(recurso):
        # Acoes e consultas de dados sao encaminhadas por HTTP para o servidor API.
        primeiro = recurso.split("/", 1)[0]
        if primeiro in PREFIXOS_API or recurso in ROTAS_API_EXATAS:
            if len(request.get_data(cache=True)) > 2 * 1024 * 1024:
                return jsonify({"erro": "Requisicao muito grande."}), 413

            path = request.full_path
            if path.endswith("?"):
                path = path[:-1]
            headers = {}
            for nome in ("Authorization", "Content-Type", "Accept"):
                valor = request.headers.get(nome)
                if valor:
                    headers[nome] = valor

            chamada = Request(
                url=f"{backend_url}{path}",
                data=request.get_data() if request.method in ("POST", "PUT", "PATCH", "DELETE") else None,
                headers=headers,
                method=request.method,
            )
            try:
                resposta = urlopen(chamada, timeout=60)
            except HTTPError as erro:
                resposta = erro  # Inclui 401, 404 e 422 do backend, sem mascarar.
            except (URLError, TimeoutError):
                app.logger.warning("API local inacessivel pela porta 5000")
                return jsonify({"erro": "API indisponivel. Inicie o backend na porta 5000."}), 502

            with resposta:
                corpo = resposta.read()
                codigo = resposta.status
                tipo = resposta.headers.get("Content-Type", "application/json")
                retorno = Response(corpo, status=codigo, content_type=tipo)
                # Nao guardar dados de contas no cache do navegador ou do proxy.
                retorno.headers["Cache-Control"] = "no-store"
                retorno.headers["X-Content-Type-Options"] = "nosniff"
                return retorno

        # Somente as paginas HTML previstas podem ser servidas pelo frontend.
        if request.method != "GET" or not recurso.endswith(".html"):
            abort(404)
        pagina = recurso[:-5]
        if pagina not in PAGINAS:
            abort(404)
        if pagina == "safras":
            return redirect(url_for("pagina_ou_proxy", recurso="orientador.html", **request.args.to_dict(flat=True)))
        return render_template(f"{pagina}.html")

    @app.after_request
    def cabecalhos(resposta):
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return resposta

    return app


app = create_frontend_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=False)
