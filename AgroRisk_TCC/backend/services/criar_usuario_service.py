from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from werkzeug.security import generate_password_hash


class CriarUsuarioService:
    def executar(self, dados):
        campos_obrigatorios = ["nome", "email", "senha"]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        usuario_existente = UsuarioRepository.buscar_por_email(dados["email"])

        if usuario_existente:
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        usuario = Usuario(
            nome=dados["nome"],
            email=dados["email"],
            senha=generate_password_hash(dados["senha"]),
        )

        UsuarioRepository.salvar(usuario)

        return usuario.to_dict()