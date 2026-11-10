from repositories.usuario_repository import UsuarioRepository


class DeletarUsuarioService:
    def executar(self, usuario_id):

        usuario = UsuarioRepository.buscar_por_id(usuario_id)

        if usuario is None:
            return False

        UsuarioRepository.excluir(usuario)

        return True