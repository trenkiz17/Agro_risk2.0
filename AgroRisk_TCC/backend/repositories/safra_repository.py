"""Consultas de Safra, com isolamento pela propriedade de cada conta."""
from sqlalchemy import text
from models.database import db
from models.safra import Safra
from models.propriedade import Propriedade


class SafraRepository:
    @staticmethod
    def buscar_por_id_com_usuario(safra_id, usuario_id):
        return (Safra.query
                .join(Propriedade, Safra.propriedade_id == Propriedade.id)
                .filter(Safra.id == safra_id, Propriedade.usuario_id == usuario_id)
                .first())

    @staticmethod
    def salvar(safra):
        db.session.add(safra)
        db.session.commit()
        return safra

    @staticmethod
    def excluir(safra):
        db.session.delete(safra)
        db.session.commit()

    @staticmethod
    def listar_por_usuario(usuario_id, propriedade_id=None):
        query = (Safra.query
                 .join(Propriedade, Safra.propriedade_id == Propriedade.id)
                 .filter(Propriedade.usuario_id == usuario_id))
        if propriedade_id is not None:
            query = query.filter(Safra.propriedade_id == propriedade_id)
        return query.order_by(Safra.id.asc()).all()

    @staticmethod
    def buscar_por_cultura(cultura, usuario_id):
        # SQL real e parametrizado: evidencia o requisito de consultas no Repository.
        linhas = db.session.execute(text("""
            SELECT s.id FROM safras AS s
            INNER JOIN propriedades AS p ON p.id = s.propriedade_id
            WHERE p.usuario_id = :usuario_id AND LOWER(s.cultura) = :cultura
            ORDER BY s.id DESC LIMIT 100
        """), {"usuario_id": usuario_id, "cultura": cultura.strip().lower()}).all()
        ids = [linha[0] for linha in linhas]
        if not ids:
            return []
        return (Safra.query.filter(Safra.id.in_(ids))
                .order_by(Safra.id.desc()).all())
