"""Smoke test: frontend servido pelo Flask e APIs protegidas, SEM tocar no MySQL."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "chave-exclusiva-para-testes-com-mais-de-32-caracteres"
os.environ["FLASK_DEBUG"] = "False"

from app import app

with app.test_client() as client:
    for pagina in [
        "/", "/index.html", "/login.html", "/cadastro.html",
        "/dashboard.html", "/perfil.html", "/propriedades.html",
        "/cadastro_propriedade.html", "/monitoramento.html",
        "/safras.html", "/cadastro_safras.html", "/relatorios.html"
    ]:
        resposta = client.get(pagina)
        assert resposta.status_code == 200, (pagina, resposta.status_code)
        assert b"<!DOCTYPE html>" in resposta.data
        assert b"/static/css/style.css" in resposta.data
        print("[OK] Pagina:", pagina)

    for asset in [
        "/static/css/style.css", "/static/js/api.js",
        "/static/img/dashboard.png", "/static/js/relatorios.js"
    ]:
        resposta = client.get(asset)
        assert resposta.status_code == 200, (asset, resposta.status_code)
        print("[OK] Recurso:", asset)

    js = client.get("/static/js/api.js").get_data(as_text=True)
    assert "window.location.origin" in js
    assert "http://127.0.0.1:5000" not in js
    assert client.get("/pagina_inexistente.html").status_code == 404
    assert client.get("/api").status_code == 200
    assert client.get("/propriedades").status_code == 401
    print("[OK] API responde e nao permite listar propriedades sem login")

print("TESTE DE PAGINAS FLASK PASSOU (SQLite temporario).")
