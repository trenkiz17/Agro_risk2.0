from repositories.safra_repository import SafraRepository


class ListarSafrasService:
    def executar(self, usuario_id, propriedade_id=None):
        return [safra.to_dict() for safra in SafraRepository.listar_por_usuario(usuario_id, propriedade_id)]
