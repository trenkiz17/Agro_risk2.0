from repositories.propriedade_repository import PropriedadeRepository


class BuscarPropriedadePorLocalizacaoService:
    def executar(self, localizacao, usuario_id):
        termo = str(localizacao or "").strip()
        if not termo or len(termo) > 100:
            raise ValueError("Informe uma localização válida com até 100 caracteres.")
        return [p.to_dict() for p in PropriedadeRepository.buscar_por_localizacao(termo, usuario_id)]
