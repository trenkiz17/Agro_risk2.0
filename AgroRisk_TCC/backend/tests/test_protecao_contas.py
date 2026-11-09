"""Teste isolado: usa SQLite EM MEMÓRIA, nunca toca o MySQL do AgroRisk.
Execute dentro de backend: python tests/test_protecao_contas.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "chave-exclusiva-para-testes-locais-e-nunca-producao"
os.environ["FRONTEND_ORIGINS"] = "http://127.0.0.1:5500"
os.environ["FLASK_DEBUG"] = "False"

from app import app  # noqa: E402


def verificar(resp, esperado, descricao):
    assert resp.status_code == esperado, (
        f"{descricao}: esperado HTTP {esperado}, "
        f"recebido {resp.status_code}: {resp.get_json(silent=True)}"
    )
    print(f"[OK] {descricao} (HTTP {esperado})")
    return resp.get_json(silent=True)


with app.test_client() as client:
    # Cadastro e login de duas contas distintas.
    a = verificar(client.post("/usuarios", json={
        "nome": "Conta A", "email": "teste.a@example.test", "senha": "Teste-12345-A"
    }), 201, "Cadastrar conta A")
    b = verificar(client.post("/usuarios", json={
        "nome": "Conta B", "email": "teste.b@example.test", "senha": "Teste-12345-B"
    }), 201, "Cadastrar conta B")

    login_a = verificar(client.post("/login", json={
        "email": "teste.a@example.test", "senha": "Teste-12345-A"
    }), 200, "Entrar na conta A")
    login_b = verificar(client.post("/login", json={
        "email": "teste.b@example.test", "senha": "Teste-12345-B"
    }), 200, "Entrar na conta B")
    auth_a = {"Authorization": "Bearer " + login_a["token"]}
    auth_b = {"Authorization": "Bearer " + login_b["token"]}

    verificar(client.get(f"/usuarios/{a['id']}"), 401, "Bloquear perfil sem token")
    verificar(client.get(f"/usuarios/{a['id']}", headers=auth_b), 404,
             "Impedir B de ler perfil A")
    verificar(client.put(f"/usuarios/{a['id']}", headers=auth_b, json={
        "nome": "Tentativa", "email": "teste.a@example.test"
    }), 404, "Impedir B de editar perfil A")

    # Forjar usuario_id no corpo não pode mudar o dono da propriedade.
    prop = verificar(client.post("/propriedades", headers=auth_a, json={
        "usuario_id": b["id"], "nome": "Propriedade da conta A",
        "cidade": "Belo Horizonte", "estado": "MG", "area": 10.0, "perimetro": 0
    }), 201, "Criar propriedade com ID do corpo falsificado")
    assert prop["usuario_id"] == a["id"]
    print("[OK] Proprietário determinado pelo token, não pelo JSON")

    lista_a = verificar(client.get(f"/propriedades?usuario_id={b['id']}",
                                 headers=auth_a), 200, "Listar propriedades por identidade do token")
    assert len(lista_a) == 1 and lista_a[0]["id"] == prop["id"]
    lista_b = verificar(client.get("/propriedades", headers=auth_b), 200,
                       "Conta B tem sua própria listagem")
    assert lista_b == []

    verificar(client.get(f"/propriedades/{prop['id']}", headers=auth_b), 404,
             "Bloquear leitura da propriedade alheia")
    verificar(client.put(f"/propriedades/{prop['id']}", headers=auth_b, json={
        "nome": "Invasao"
    }), 404, "Bloquear edição da propriedade alheia")
    verificar(client.delete(f"/propriedades/{prop['id']}", headers=auth_b), 404,
             "Bloquear exclusão da propriedade alheia")

    safra_payload = {
        "usuario_id": b["id"], "propriedade_id": prop["id"],
        "nome": "Café do teste", "cultura": "Café",
        "data_plantio": "2022-10-14", "area_plantada": 2.0
    }
    verificar(client.post("/safras", headers=auth_b, json=safra_payload), 400,
             "Bloquear safra criada por B na propriedade A")
    cadastro = verificar(client.post("/safras", headers=auth_a, json=safra_payload),
                        201, "Conta A cria safra mesmo com ID falsificado")
    safra = cadastro["safra"]
    verificar(client.get(f"/safras/{safra['id']}", headers=auth_b), 404,
             "Bloquear leitura de safra alheia")
    verificar(client.put(f"/safras/{safra['id']}", headers=auth_b, json={
        "status": "Finalizada"
    }), 404, "Bloquear finalização de safra alheia")
    verificar(client.delete(f"/safras/{safra['id']}", headers=auth_b), 404,
             "Bloquear exclusão de safra alheia")
    verificar(client.put(f"/safras/{safra['id']}", headers=auth_a, json={
        "status": "Finalizada"
    }), 200, "Permitir ao dono finalizar a safra")
    safra_salva = verificar(client.get(f"/safras/{safra['id']}", headers=auth_a),
                           200, "Consultar safra finalizada")
    assert safra_salva["status"] == "Finalizada"
    print("[OK] Status Finalizada persistiu no banco SQLite de teste")
    assert verificar(client.get("/safras", headers=auth_b), 200,
                    "Conta B não vê safras da conta A") == []

print("\nTODOS OS TESTES DE ISOLAMENTO PASSARAM (SQLite temporário).")
