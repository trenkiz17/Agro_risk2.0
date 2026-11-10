from sqlalchemy import text

from models.database import db
from models.usuario import Usuario


class UsuarioRepository:
    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def buscar_por_id(usuario_id):
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def salvar(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def confirmar():
        db.session.commit()

    @staticmethod
    def excluir(usuario):
        db.session.delete(usuario)
        db.session.commit()

    """
    Repository responsável pelas consultas
    que vão além do CRUD básico de usuários.
    """

    @staticmethod
    def buscar_por_nome(nome):

        banco = db.session.get_bind().dialect.name

        if banco == "mysql":

            sql = text(
                "CALL sp_buscar_usuario_nome(:nome)"
            )

            resultado = db.session.execute(
                sql,
                {
                    "nome": nome
                }
            )

            linhas = resultado.mappings().all()

            resultado.close()

            return [
                Usuario(**dict(linha))
                for linha in linhas
            ]

        # Fallback para testes locais
        return (
            Usuario.query
            .filter(
                Usuario.nome.like(
                    f"%{nome}%"
                )
            )
            .order_by(
                Usuario.nome.asc()
            )
            .all()
        )