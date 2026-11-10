"""Os filtros SQL no Repository nunca podem retornar registros de outra conta.

Executar com: python -m pytest backend/tests/test_consultas_repository.py -q
"""
import sys
from datetime import date
from pathlib import Path

import pytest
from flask import Flask

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from models.database import db
from models.usuario import Usuario
from models.propriedade import Propriedade
from models.safra import Safra
from models.safra_parametros import SafraParametros
from repositories.propriedade_repository import PropriedadeRepository
from repositories.safra_repository import SafraRepository


@pytest.fixture()
def dados():
    app = Flask(__name__)
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///:memory:", SQLALCHEMY_TRACK_MODIFICATIONS=False)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        u1 = Usuario(nome="Pessoa 1", email="p1@teste.local", senha="x")
        u2 = Usuario(nome="Pessoa 2", email="p2@teste.local", senha="x")
        db.session.add_all([u1, u2]); db.session.commit()
        p1 = Propriedade(usuario_id=u1.id, nome="Sítio Verde", cidade="Vespasiano", estado="MG", area=10, perimetro=100)
        p2 = Propriedade(usuario_id=u2.id, nome="Sítio Secreto", cidade="Vespasiano", estado="MG", area=15, perimetro=120)
        db.session.add_all([p1, p2]); db.session.commit()
        s1 = Safra(propriedade_id=p1.id, nome="Soja A", cultura="Soja", ano_safra="2026", area_plantada=2, data_plantio=date(2026,1,1))
        s2 = Safra(propriedade_id=p2.id, nome="Soja B", cultura="Soja", ano_safra="2026", area_plantada=3, data_plantio=date(2026,1,2))
        db.session.add_all([s1, s2]); db.session.commit()
        yield (u1.id, u2.id, p1.id, p2.id)
        db.session.remove(); db.drop_all()


def test_filtro_de_localizacao_respeita_usuario(dados):
    u1, u2, p1, p2 = dados
    encontrados = PropriedadeRepository.buscar_por_localizacao("Vespasiano", u1)
    assert [p.id for p in encontrados] == [p1]
    assert PropriedadeRepository.buscar_por_localizacao("Secreto", u1) == []
    assert len(PropriedadeRepository.listar_por_usuario(u2)) == 1


def test_busca_de_safra_respeita_usuario(dados):
    u1, u2, p1, p2 = dados
    encontrados = SafraRepository.buscar_por_cultura("soja", u1)
    assert len(encontrados) == 1
    assert encontrados[0].propriedade_id == p1
    assert len(SafraRepository.listar_por_usuario(u2)) == 1
    assert SafraRepository.listar_por_usuario(u1, p2) == []
