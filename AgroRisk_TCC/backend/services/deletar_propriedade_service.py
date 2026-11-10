from repositories.propriedade_repository import PropriedadeRepository


class DeletarPropriedadeService:

    def executar(
        self,
        propriedade_id,
        usuario_id=None
    ):

        propriedade = PropriedadeRepository.buscar_por_id_do_usuario(propriedade_id, usuario_id)

        if propriedade is None:

            return False

        if (
            usuario_id is not None
            and propriedade.usuario_id != usuario_id
        ):

            return False

        PropriedadeRepository.excluir(propriedade)

        return True