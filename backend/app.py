import os

from dotenv import load_dotenv

from flask import Flask, jsonify, render_template, abort, request
from security.auth import exigir_autenticacao

from models.database import db

from controllers.usuario_controller import usuario_controller
from controllers.propriedade_controller import propriedade_controller
from controllers.safra_controller import safra_controller
from controllers.clima_controller import clima_controller


def create_app():

    # Carrega backend/.env independentemente da pasta aberta no terminal.
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Frontend e API agora compartilham a mesma origem: CORS não é necessário.
    # Não ativar CORS aberto em uma instalação pública.

    chave_secreta = os.getenv("SECRET_KEY", "")
    if len(chave_secreta) < 32 or chave_secreta.startswith(("GERAR_", "GERE_", "SUA_", "COLE_", "INSIRA_")):
        raise RuntimeError(
            "Defina SECRET_KEY com pelo menos 32 caracteres no backend/.env."
        )
    app.config["SECRET_KEY"] = chave_secreta
    app.config["AGRORISK_TOKEN_TTL"] = 8 * 60 * 60  # 8 horas

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/agrorisk"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ==========================================
    # CONTROLLERS
    # ==========================================

    app.register_blueprint(
        usuario_controller.blueprint
    )

    app.register_blueprint(
        propriedade_controller.blueprint
    )

    app.register_blueprint(
        safra_controller.blueprint
    )

    app.register_blueprint(
        clima_controller.blueprint
    )

    # Requisições de dados exigem identidade verificada pelo Flask.
    # Login, cadastro inicial, saúde da API e estimador público ficam livres.
    @app.before_request
    def proteger_dados():
        from flask import request
        if request.method == "OPTIONS":
            return None

        rota = request.path.rstrip("/") or "/"
        if (rota == "/usuarios" and request.method == "POST") or (
            rota == "/safras/estimar-colheita" and request.method == "GET"
        ):
            return None

        protegido = any(
            rota == prefixo or rota.startswith(prefixo + "/")
            for prefixo in ("/usuarios", "/propriedades", "/safras", "/api/clima")
        )
        return exigir_autenticacao() if protegido else None

    # ==========================================
    # FRONTEND / ROTA INICIAL
    # ==========================================

    @app.get("/")
    def home():
        return render_template("index.html")

    # Permite manter os mesmos links *.html já usados nos JS e templates,
    # sem reescrever os fluxos de navegação do projeto.
    paginas = {
        "index", "login", "cadastro", "dashboard", "perfil",
        "propriedades", "cadastro_propriedade", "monitoramento",
        "safras", "cadastro_safras", "relatorios"
    }

    @app.get("/<pagina>.html")
    def abrir_pagina(pagina):
        if pagina not in paginas:
            abort(404)
        return render_template(f"{pagina}.html")

    @app.after_request
    def cabecalhos_seguranca(resposta):
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Evita cache de respostas que podem conter dados da conta.
        if request.path.startswith(("/usuarios", "/propriedades", "/safras", "/login")):
            resposta.headers["Cache-Control"] = "no-store"
        return resposta

    # ==========================================
    # INFORMAÇÕES DA API
    # ==========================================

    @app.get("/api")
    def api_info():

        return jsonify({
            "nome": "AgroRisk API",
            "status": "online",
            "versao": "1.0"
        })

    # ==========================================
    # BANCO DE DADOS
    # ==========================================

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":

    debug = os.getenv(
        "FLASK_DEBUG",
        "False"
    ).strip().lower() == "true"

    app.run(
        debug=debug,
        host="127.0.0.1",
        port=5000
    )