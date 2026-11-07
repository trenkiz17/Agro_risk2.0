"""Execute: python tests/test_orientador_ia.py (usa SQLite em memória e Gemini simulado)."""
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'chave-para-teste-com-mais-de-trinta-e-dois-caracteres'
os.environ['GEMINI_API_KEY'] = 'CHAVE_DE_TESTE_FICTICIA_NAO_ENVIAR_12345'
os.environ['FLASK_DEBUG'] = 'False'

from app import app  # noqa E402

class RespostaGemini:
    status_code = 200
    ok = True
    def json(self):
        return {'candidates': [{'content': {'parts': [{'text': 'Resposta simulada do Gemini.'}]}}]}

with app.test_client() as client:
    assert client.get('/api/orientador/status').status_code == 401
    assert client.post('/api/orientador/perguntar', json={'pergunta': 'Bom dia!', 'consentimento': True}).status_code == 401

    assert client.post('/usuarios', json={'nome': 'Agricultor A', 'email': 'agro-a@example.test', 'senha': 'Senha-local-forte-A'}).status_code == 201
    assert client.post('/usuarios', json={'nome': 'Agricultor B', 'email': 'agro-b@example.test', 'senha': 'Senha-local-forte-B'}).status_code == 201
    a = client.post('/login', json={'email': 'agro-a@example.test', 'senha': 'Senha-local-forte-A'}).get_json()
    b = client.post('/login', json={'email': 'agro-b@example.test', 'senha': 'Senha-local-forte-B'}).get_json()
    ha = {'Authorization': 'Bearer ' + a['token']}
    hb = {'Authorization': 'Bearer ' + b['token']}
    prop = client.post('/propriedades', headers=ha, json={'nome': 'Fazenda Teste', 'cidade': 'Vespasiano', 'estado': 'MG', 'area': 2.0, 'perimetro': 500}).get_json()
    assert prop['id']

    assert client.post('/api/orientador/perguntar', headers=ha, json={'pergunta': 'Qual o melhor plano?'}).status_code == 400
    assert client.post('/api/orientador/perguntar', headers=hb, json={'pergunta': 'Como plantar café?', 'consentimento': True, 'propriedade_id': prop['id']}).status_code == 404
    captured = []
    def fake_post(url, **kwargs):
        captured.append(kwargs['json'])
        return RespostaGemini()
    with patch('services.orientador_ia_service.requests.post', side_effect=fake_post):
        ok = client.post('/api/orientador/perguntar', headers=ha, json={'pergunta': 'Como planejo o plantio?', 'consentimento': True, 'propriedade_id': prop['id']})
        assert ok.status_code == 200, ok.get_json()
        assert ok.get_json()['resposta'] == 'Resposta simulada do Gemini.'
        assert 'Vespasiano' in str(captured[0]['contents'])
        assert 'senha' not in str(captured[0]['contents']).lower()
    assert client.get('/orientador.html').status_code == 200
    print('OK: login, privacidade, consentimento, contexto e IA simulada (SQLite).')
