"""Estudos de cenários e janelas de colheita, sem alegar previsão agronômica precisa.

Os intervalos técnicos são introduzidos pelo produtor (idealmente de laudo, cultivar
ou assistência técnica). Sem eles, mantém-se a estimativa ampla existente.
"""
from datetime import date, timedelta
from math import isfinite

from repositories.analise_avancada_repository import AnaliseAvancadaRepository
from services.estimar_colheita_service import EstimarColheitaService


CAMPOS = (
    "cultivar", "idade_lavoura_anos", "altitude_m", "irrigacao", "area_util_percentual",
    "data_emergencia", "data_florada", "data_frutificacao", "ciclo_min_dias", "ciclo_max_dias",
    "florada_colheita_min_dias", "florada_colheita_max_dias", "produtividade_baixa_sc_ha",
    "produtividade_media_sc_ha", "produtividade_alta_sc_ha", "fonte_parametros",
)
DATAS = {"data_emergencia", "data_florada", "data_frutificacao"}
INTERVALOS = (("ciclo_min_dias", "ciclo_max_dias"), ("florada_colheita_min_dias", "florada_colheita_max_dias"))


def _numero(valor, campo, minimo, maximo, inteiro=False):
    if valor is None or valor == "":
        return None
    if isinstance(valor, bool):
        raise ValueError(f"{campo}: número inválido.")
    try:
        n = float(valor)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{campo}: informe um número válido.") from exc
    if not isfinite(n) or not minimo <= n <= maximo or (inteiro and not n.is_integer()):
        raise ValueError(f"{campo}: valor fora do intervalo permitido ({minimo} a {maximo}).")
    return int(n) if inteiro else n


def validar_parametros(dados):
    if not isinstance(dados, dict):
        raise ValueError("Envie os parâmetros em um objeto JSON.")
    campos_indevidos = set(dados) - set(CAMPOS)
    if campos_indevidos:
        raise ValueError("O formulário contém campos não reconhecidos.")
    valor = {}
    for campo in CAMPOS:
        entrada = dados.get(campo)
        if campo in DATAS:
            try:
                valor[campo] = date.fromisoformat(entrada) if entrada else None
            except (ValueError, TypeError) as exc:
                raise ValueError(f"{campo}: data inválida (AAAA-MM-DD).") from exc
        elif campo in ("cultivar", "fonte_parametros"):
            limite = 100 if campo == "cultivar" else 350
            entrada = str(entrada or "").strip()
            if len(entrada) > limite:
                raise ValueError(f"{campo}: máximo de {limite} caracteres.")
            valor[campo] = entrada or None
        elif campo == "irrigacao":
            if entrada not in (None, "", "sim", "nao", "nao_informado"):
                raise ValueError("Irrigação inválida.")
            valor[campo] = entrada or None
        else:
            limites = {
                "idade_lavoura_anos": (0, 100), "altitude_m": (-100, 5500),
                "area_util_percentual": (0.01, 100),
                "ciclo_min_dias": (40, 2500), "ciclo_max_dias": (40, 2500),
                "florada_colheita_min_dias": (60, 500), "florada_colheita_max_dias": (60, 500),
                "produtividade_baixa_sc_ha": (0, 1000),
                "produtividade_media_sc_ha": (0, 1000), "produtividade_alta_sc_ha": (0, 1000),
            }
            lo, hi = limites[campo]
            valor[campo] = _numero(entrada, campo, lo, hi, inteiro=campo.endswith("_dias"))
    for minimo, maximo in INTERVALOS:
        a, b = valor[minimo], valor[maximo]
        if (a is None) != (b is None):
            raise ValueError(f"Informe {minimo} e {maximo} juntos.")
        if a is not None and a > b:
            raise ValueError("O intervalo mínimo não pode ultrapassar o máximo.")
    produtividades = [valor[c] for c in ("produtividade_baixa_sc_ha", "produtividade_media_sc_ha", "produtividade_alta_sc_ha")]
    if any(v is not None for v in produtividades):
        if not all(v is not None for v in produtividades):
            raise ValueError("Para comparar cenários, informe as três produtividades em sacas de 60 kg/ha.")
        if produtividades != sorted(produtividades):
            raise ValueError("Produtividades devem estar na ordem: baixa ≤ média ≤ alta.")
    if valor["data_frutificacao"] and valor["data_florada"] and valor["data_frutificacao"] < valor["data_florada"]:
        raise ValueError("A frutificação observada não pode ocorrer antes da florada observada.")
    return valor


class AnaliseAvancadaService:
    @staticmethod
    def _safra_da_conta(safra_id, usuario_id):
        safra = AnaliseAvancadaRepository.buscar_safra_da_conta(safra_id, usuario_id)
        if not safra:
            raise LookupError("Safra não encontrada na sua conta.")
        return safra

    def salvar(self, safra_id, usuario_id, dados):
        safra = self._safra_da_conta(safra_id, usuario_id)
        validos = validar_parametros(dados)
        # Datas chamadas "observadas" não podem ser futuras nem anteriores ao plantio.
        for campo in DATAS:
            dia = validos[campo]
            if dia and dia > date.today():
                raise ValueError(f"{campo}: informe apenas uma observação que já ocorreu.")
            if dia and safra.data_plantio and dia < safra.data_plantio:
                raise ValueError(f"{campo}: observação anterior ao plantio registrado.")
        # Validação antes do commit impede persistência parcial de parâmetros incorretos.
        AnaliseAvancadaRepository.salvar_parametros(safra, validos)
        return self.consultar(safra_id, usuario_id)

    def consultar(self, safra_id, usuario_id):
        safra = self._safra_da_conta(safra_id, usuario_id)
        p = safra.parametros_avancados
        params = p.to_dict() if p else {campo: None for campo in CAMPOS}
        resultado = {
            "safra_id": safra.id, "safra": safra.nome, "cultura": safra.cultura,
            "data_plantio": safra.data_plantio.isoformat() if safra.data_plantio else None,
            "area_plantada_ha": float(safra.area_plantada), "parametros": params,
            "janela_preliminar": None, "janela_refinada": None,
            "qualidade_dados": "Referência preliminar", "cenarios_producao": None,
            "pontos_de_acompanhamento": [], "avisos": [],
        }
        if safra.data_plantio:
            inicial = EstimarColheitaService().executar(safra.cultura, safra.data_plantio)
            resultado["janela_preliminar"] = {k: inicial[k] for k in ("inicio_janela", "fim_janela", "aviso")}
            resultado["pontos_de_acompanhamento"].append({"fase": "Plantio registrado", "data": safra.data_plantio.isoformat(), "tipo": "registrada"})
        else:
            resultado["avisos"].append("Informe uma data de plantio para obter a referência inicial.")
        for campo, titulo in (("data_emergencia", "Emergência observada"), ("data_florada", "Florada observada"), ("data_frutificacao", "Formação dos frutos observada")):
            if params[campo]:
                resultado["pontos_de_acompanhamento"].append({"fase": titulo, "data": params[campo], "tipo": "observada"})
        fonte = params["fonte_parametros"]
        if p:
            min_d = params["ciclo_min_dias"]
            max_d = params["ciclo_max_dias"]
            fl_min = params["florada_colheita_min_dias"]
            fl_max = params["florada_colheita_max_dias"]
            if params["data_florada"] and fl_min is not None:
                data = date.fromisoformat(params["data_florada"])
                janela = (data + timedelta(days=fl_min), data + timedelta(days=fl_max))
                metodo = "florada observada + ciclo informado entre florada e colheita"
            elif safra.data_plantio and min_d is not None:
                janela = (safra.data_plantio + timedelta(days=min_d), safra.data_plantio + timedelta(days=max_d))
                metodo = "plantio registrado + duração técnica informada da cultura"
            else:
                janela = None
            if janela:
                resultado["janela_refinada"] = {
                    "inicio_janela": janela[0].isoformat(), "fim_janela": janela[1].isoformat(),
                    "metodo": metodo,
                    "fonte": fonte or "Parâmetros informados pelo produtor sem fonte técnica identificada",
                    "validada": False,
                }
                resultado["qualidade_dados"] = "Intervalo calculado com parâmetros informados"
                resultado["pontos_de_acompanhamento"].append({"fase": "Janela calculada para revisão", "inicio": janela[0].isoformat(), "fim": janela[1].isoformat(), "tipo": "estimada"})
                if not fonte:
                    resultado["avisos"].append("Registre a origem dos dias técnicos para dar rastreabilidade à estimativa.")
            if params["data_florada"] and fl_min is None:
                resultado["avisos"].append("Florada observada, mas falta informar o intervalo técnico entre florada e colheita para refinar a janela.")
            prod = [params[c] for c in ("produtividade_baixa_sc_ha", "produtividade_media_sc_ha", "produtividade_alta_sc_ha")]
            if all(v is not None for v in prod):
                area = float(safra.area_plantada) * (params["area_util_percentual"] or 100) / 100
                resultado["cenarios_producao"] = {
                    "area_considerada_ha": round(area, 3), "unidade": "sacas de 60 kg",
                    "produtividade_unidade": "sacas de 60 kg/ha", "fonte": fonte or "Valores hipotéticos informados pelo produtor",
                    "baixa": round(area * prod[0], 2), "media": round(area * prod[1], 2), "alta": round(area * prod[2], 2),
                    "observacao": "Cenários matemáticos, não previsão de rendimento real. Dados devem vir de histórico ou referência técnica.",
                }
            if params["cultivar"] is None:
                resultado["avisos"].append("Informar a cultivar e seu ciclo regional pode melhorar a referência temporal.")
        if not resultado["janela_refinada"]:
            resultado["avisos"].append("Sem parâmetros de ciclo validados/informados, mantém-se a janela preliminar; não é possível estreitá-la com segurança.")
        if not resultado["cenarios_producao"]:
            resultado["avisos"].append("Para calcular cenários de produção, informe as produtividades baixa, média e alta em sacas/ha; não serão inventadas.")
        if safra.cultura.strip().lower() in ("café", "cafe"):
            resultado["avisos"].append("Café é perene: o intervalo de 3–4 anos do protótipo não significa colheitas a cada quatro anos e não estima a safra anual de um cafezal adulto.")
        return resultado
