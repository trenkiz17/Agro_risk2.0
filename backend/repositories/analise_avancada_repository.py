"""Consultas SQL e persistência dos parâmetros avançados da safra.

SQL sempre parametrizado e limitado ao usuário autenticado.
"""
from sqlalchemy import text
from models.database import db
from models.safra import Safra
from models.safra_parametros import SafraParametros


class AnaliseAvancadaRepository:
    @staticmethod
    def buscar_safra_da_conta(safra_id, usuario_id):
        # Demonstração de consulta SQL segura na camada Repository.
        linha = db.session.execute(text("""
            SELECT s.id
            FROM safras AS s
            INNER JOIN propriedades AS p ON p.id = s.propriedade_id
            WHERE s.id = :safra_id AND p.usuario_id = :usuario_id
            LIMIT 1
        """), {"safra_id": safra_id, "usuario_id": usuario_id}).first()
        return db.session.get(Safra, safra_id) if linha else None

    @staticmethod
    def salvar_parametros(safra, validos):
        parametros = safra.parametros_avancados
        if parametros is None:
            parametros = SafraParametros(safra_id=safra.id)
            safra.parametros_avancados = parametros
        for chave, valor in validos.items():
            setattr(parametros, chave, valor)
        db.session.add(parametros)
        db.session.commit()
