from repositories.safra_repository import SafraRepository


class BuscarSafraPorCulturaService:
    def executar(self, cultura, usuario_id):
        nome = str(cultura or "").strip()
        if not nome or len(nome) > 100:
            raise ValueError("Informe uma cultura válida com até 100 caracteres.")
        return [s.to_dict() for s in SafraRepository.buscar_por_cultura(nome, usuario_id)]
