from repositories.propriedade_repository import PropriedadeRepository
from models.propriedade import Propriedade


class BuscarPropriedadePorIdService:
    def executar(self, propriedade_id, usuario_id=None):
        if usuario_id is None:
            # Compatibilidade para outros servicos antigos, sem expor dado pela rota.
            propriedade = Propriedade.buscar_por_id(propriedade_id)
        else:
            propriedade = PropriedadeRepository.buscar_por_id_do_usuario(propriedade_id, usuario_id)
        return propriedade.to_dict() if propriedade else None
