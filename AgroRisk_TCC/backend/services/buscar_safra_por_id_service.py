from models.safra import Safra
from models.propriedade import Propriedade
from repositories.safra_repository import SafraRepository


class BuscarSafraPorIdService:

    def executar(
        self,
        safra_id,
        usuario_id=None
    ):

        if usuario_id is not None:
            safra = SafraRepository.buscar_por_id_com_usuario(safra_id, usuario_id)
        else:
            safra = Safra.buscar_por_id(safra_id)
        if safra is None:
            return None

        return safra.to_dict()