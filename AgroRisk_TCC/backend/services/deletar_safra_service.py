from repositories.safra_repository import SafraRepository


class DeletarSafraService:

    def executar(
        self,
        safra_id,
        usuario_id=None
    ):

        safra = SafraRepository.buscar_por_id_com_usuario(safra_id, usuario_id)

        if safra is None:
            return False

        SafraRepository.excluir(safra)

        return True