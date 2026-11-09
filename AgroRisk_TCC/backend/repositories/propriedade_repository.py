"""Consultas de Propriedade (ORM e SQL parametrizado) por conta logada."""
from sqlalchemy import text
from models.database import db
from models.propriedade import Propriedade


class PropriedadeRepository:
    @staticmethod
    def salvar(propriedade):
        db.session.add(propriedade)
        db.session.commit()
        return propriedade

    @staticmethod
    def excluir(propriedade):
        db.session.delete(propriedade)
        db.session.commit()

    @staticmethod
    def buscar_por_id_do_usuario(propriedade_id, usuario_id):
        return Propriedade.query.filter_by(id=propriedade_id, usuario_id=usuario_id).first()

    @staticmethod
    def listar_por_usuario(usuario_id):
        return (Propriedade.query
                .filter_by(usuario_id=usuario_id)
                .order_by(Propriedade.id.asc()).all())

    @staticmethod
    def buscar_por_localizacao(localizacao, usuario_id):
        # SQL permanece SOMENTE no Repository e filtra o dono no banco.
        # Bind parameters evitam concatenar entradas do usuario na consulta SQL.
        termo = "%" + localizacao.strip().lower() + "%"
        linhas = db.session.execute(text("""
            SELECT id FROM propriedades
            WHERE usuario_id = :usuario_id
              AND (LOWER(cidade) LIKE :termo
                   OR LOWER(estado) LIKE :termo
                   OR LOWER(nome) LIKE :termo)
            ORDER BY nome ASC LIMIT 100
        """), {"usuario_id": usuario_id, "termo": termo}).all()
        ids = [linha[0] for linha in linhas]
        if not ids:
            return []
        return (Propriedade.query.filter(Propriedade.id.in_(ids))
                .order_by(Propriedade.nome.asc()).all())
