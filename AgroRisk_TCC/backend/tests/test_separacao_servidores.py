"""Testes simples de duas portas, sem rede externa ou MySQL real.

Executar com: python -m pytest backend/tests/test_separacao_servidores.py -q
Requer instalacao dos requirements do projeto.
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(BACKEND))

os.environ["SECRET_KEY"] = "chave-teste-para-separacao-servidores-mais-de-32-caracteres"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from frontend.server import app as frontend_app


def test_frontend_entrega_paginas_e_recursos():
    with frontend_app.test_client() as cliente:
        assert cliente.get("/").status_code == 200
        assert cliente.get("/dashboard.html").status_code == 200
        assert cliente.get("/assistente.html").status_code == 200
        assert cliente.get("/static/css/style.css").status_code == 200
        assert cliente.get("/site-nao-existe.html").status_code == 404


def test_frontend_encaminha_api_e_token():
    class Resposta:
        status = 200
        headers = {"Content-Type": "application/json"}
        def read(self):
            return b'{"status":"online"}'
        def __enter__(self):
            return self
        def __exit__(self, *_):
            return False

    chamadas = []
    def simular_api(req, timeout=20):
        chamadas.append(req)
        return Resposta()

    with patch("frontend.server.urlopen", side_effect=simular_api):
        with frontend_app.test_client() as cliente:
            resultado = cliente.get("/propriedades?pagina=1", headers={"Authorization": "Bearer token-exemplo"})
            assert resultado.status_code == 200
            assert resultado.json["status"] == "online"
            assert resultado.headers["Cache-Control"] == "no-store"

    assert len(chamadas) == 1
    assert chamadas[0].full_url == "http://127.0.0.1:5000/propriedades?pagina=1"
    assert chamadas[0].get_header("Authorization") == "Bearer token-exemplo"


def test_backend_modo_api_nao_entrega_paginas(monkeypatch):
    monkeypatch.setenv("AGRORISK_API_ONLY", "1")
    from app import create_app
    api = create_app()
    with api.test_client() as cliente:
        assert cliente.get("/api").status_code == 200
        assert cliente.get("/dashboard.html").status_code == 404
        assert cliente.get("/propriedades").status_code == 401
