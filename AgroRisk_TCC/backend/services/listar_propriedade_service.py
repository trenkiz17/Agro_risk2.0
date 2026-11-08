from repositories.propriedade_repository import PropriedadeRepository


class ListarPropriedadesService:
    def executar(self, usuario_id):
        return [p.to_dict() for p in PropriedadeRepository.listar_por_usuario(usuario_id)]
