from repositories.propriedade_repository import PropriedadeRepository
from models.propriedade import Propriedade


class AtualizarPropriedadeService:
    def executar(self, propriedade_id, dados, usuario_id=None):
        propriedade = (PropriedadeRepository.buscar_por_id_do_usuario(propriedade_id, usuario_id)
                       if usuario_id is not None else Propriedade.buscar_por_id(propriedade_id))
        if propriedade is None:
            return None
        propriedade.atualizar(
            nome=dados.get("nome"), cidade=dados.get("cidade"),
            estado=dados.get("estado"), observacao=dados.get("observacao"),
            area=dados.get("area"), perimetro=dados.get("perimetro"),
            latitude=dados.get("latitude"), longitude=dados.get("longitude"),
            geojson=dados.get("geojson"),
        )
        return propriedade.to_dict()
