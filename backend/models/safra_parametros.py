"""Parâmetros opcionais para análise agrícola avançada de uma safra.

Tabela própria: não adiciona colunas às tabelas legadas e não migra registros.
"""
from datetime import datetime
from models.database import db


class SafraParametros(db.Model):
    __tablename__ = "safra_parametros"

    safra_id = db.Column(db.Integer, db.ForeignKey("safras.id", ondelete="CASCADE"), primary_key=True)
    cultivar = db.Column(db.String(100))
    idade_lavoura_anos = db.Column(db.Float)
    altitude_m = db.Column(db.Float)
    irrigacao = db.Column(db.String(20))
    area_util_percentual = db.Column(db.Float)
    data_emergencia = db.Column(db.Date)
    data_florada = db.Column(db.Date)
    data_frutificacao = db.Column(db.Date)
    ciclo_min_dias = db.Column(db.Integer)
    ciclo_max_dias = db.Column(db.Integer)
    florada_colheita_min_dias = db.Column(db.Integer)
    florada_colheita_max_dias = db.Column(db.Integer)
    produtividade_baixa_sc_ha = db.Column(db.Float)
    produtividade_media_sc_ha = db.Column(db.Float)
    produtividade_alta_sc_ha = db.Column(db.Float)
    fonte_parametros = db.Column(db.String(350))
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        campos = (
            "cultivar", "idade_lavoura_anos", "altitude_m", "irrigacao", "area_util_percentual",
            "data_emergencia", "data_florada", "data_frutificacao", "ciclo_min_dias",
            "ciclo_max_dias", "florada_colheita_min_dias", "florada_colheita_max_dias",
            "produtividade_baixa_sc_ha", "produtividade_media_sc_ha", "produtividade_alta_sc_ha",
            "fonte_parametros",
        )
        result = {campo: getattr(self, campo) for campo in campos}
        for campo in ("data_emergencia", "data_florada", "data_frutificacao"):
            result[campo] = result[campo].isoformat() if result[campo] else None
        return result
