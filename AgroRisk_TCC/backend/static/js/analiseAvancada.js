/* AgroRisk: dois modos de análise (simples e avançado).
 * Reaproveita o endpoint de análise já autenticado; não executa cálculos
 * de colheita no navegador, nem envia dados automaticamente à IA.
 */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const campos = {
    cultivar:'refCultivar', idade_lavoura_anos:'refIdade', altitude_m:'refAltitude',
    irrigacao:'refIrrigacao', area_util_percentual:'refAreaUtil',
    data_emergencia:'refEmergencia', data_florada:'refFlorada', data_frutificacao:'refFrutificacao',
    ciclo_min_dias:'refCicloMin', ciclo_max_dias:'refCicloMax',
    florada_colheita_min_dias:'refFloradaMin', florada_colheita_max_dias:'refFloradaMax',
    produtividade_baixa_sc_ha:'refProdBaixa', produtividade_media_sc_ha:'refProdMedia',
    produtividade_alta_sc_ha:'refProdAlta', fonte_parametros:'refFonte'
  };
  const token = () => sessionStorage.getItem('agrorisk_token');
  const idSafra = () => Number($('safraContexto')?.value) || null;
  const br = n => Number(n).toLocaleString('pt-BR', {maximumFractionDigits: 2});
  const dataBR = x => /^\d{4}-\d{2}-\d{2}$/.test(String(x||''))
    ? `${x.slice(8,10)}/${x.slice(5,7)}/${x.slice(0,4)}` : '—';
  const novo = (tag, classe='', texto) => {
    const el = document.createElement(tag);
    if (classe) el.className = classe;
    if (texto !== undefined) el.textContent = texto;
    return el;
  };
  let solicitacao = 0;
  let ultimaAnalise = null;

  function status(msg, erro=false) {
    const el = $('mensagemAnalise');
    el.textContent = msg;
    el.hidden = !msg;
    el.classList.toggle('ag-ai-erro', erro);
  }
  function selecionarModo(modo, focar=false) {
    const simples = modo === 'simples';
    $('painelAnaliseSimples').hidden = !simples;
    $('painelAnaliseAvancada').hidden = simples;
    for (const [id, ativo] of [['abaModoSimples', simples], ['abaModoAvancado', !simples]]) {
      const tab = $(id);
      tab.classList.toggle('is-active', ativo);
      tab.setAttribute('aria-selected', String(ativo));
      tab.tabIndex = ativo ? 0 : -1;
      if (ativo && focar) tab.focus();
    }
  }
  function limpar() {
    ultimaAnalise = null;
    for (const id of Object.values(campos)) $(id).value = '';
    $('resultadoAnaliseAvancada').hidden = true;
    $('resultadoAnaliseAvancada').replaceChildren();
    $('ajudaIASimples').disabled = true;
    $('resumoAnaliseSimples').replaceChildren();
    $('resumoAnaliseSimples').append(novo('p', '', 'Selecione uma safra para carregar a análise automaticamente.'));
  }
  function preencher(params) {
    for (const [key, id] of Object.entries(campos)) $(id).value = params?.[key] ?? '';
  }
  async function requisitar(metodo, id, corpo) {
    const r = await fetch(`/api/analise-avancada/safras/${encodeURIComponent(id)}`, {
      method: metodo, cache: 'no-store',
      headers: {Authorization: `Bearer ${token()}`, 'Content-Type': 'application/json'},
      ...(corpo ? {body: JSON.stringify(corpo)} : {})
    });
    let obj = {};
    try { obj = await r.json(); } catch {}
    if (!r.ok) throw Error(obj.erro || `Erro HTTP ${r.status}`);
    return obj;
  }
  function linha(dest, titulo, valor) {
    const p = novo('p');
    p.append(novo('strong', '', titulo + ' '), document.createTextNode(valor));
    dest.append(p);
  }
  function aviso(root, msg) {
    root.append(novo('p', 'ag-analise-aviso', msg));
  }
  function renderSimples(res) {
    const root = $('resumoAnaliseSimples');
    root.replaceChildren();
    root.append(novo('h3', '', `${res.safra} · ${res.cultura}`));
    const dados = novo('div', 'ag-resumo-metricas');
    const itens = [
      ['Data de plantio', dataBR(res.data_plantio)],
      ['Área cadastrada', res.area_plantada_ha == null ? 'Não informada' : `${br(res.area_plantada_ha)} ha`],
    ];
    for (const [titulo, valor] of itens) {
      const item = novo('div', 'ag-resumo-metrica');
      item.append(novo('span', '', titulo), novo('strong', '', valor));
      dados.append(item);
    }
    root.append(dados);
    if (res.janela_preliminar) {
      const ref = novo('div', 'ag-resumo-janela');
      ref.append(novo('span', '', 'Janela preliminar do AgroRisk'));
      ref.append(novo('strong', '', `${dataBR(res.janela_preliminar.inicio_janela)} a ${dataBR(res.janela_preliminar.fim_janela)}`));
      ref.append(novo('p', '', 'Referência geral de calendário da cultura. Não é uma previsão precisa para a sua fazenda.'));
      root.append(ref);
    } else aviso(root, 'A safra ainda não possui dados suficientes para calcular a janela preliminar.');

    if (res.janela_refinada) {
      const ref = novo('div', 'ag-resumo-janela ag-resumo-refinada');
      ref.append(novo('span', '', 'Janela calculada com parâmetros informados'));
      ref.append(novo('strong', '', `${dataBR(res.janela_refinada.inicio_janela)} a ${dataBR(res.janela_refinada.fim_janela)}`));
      ref.append(novo('p', '', `Método: ${res.janela_refinada.metodo}. Resultado ainda não validado agronomicamente.`));
      root.append(ref);
    }
    if (res.cenarios_producao) {
      const c = res.cenarios_producao;
      const bloco = novo('div', 'ag-resumo-producao');
      bloco.append(novo('h4', '', 'Cenários de produção informados (não previsão)'));
      const grade = novo('div', 'ag-refina-cenario');
      for (const [label, k] of [['Baixo', 'baixa'], ['Intermediário', 'media'], ['Alto', 'alta']]) {
        const item = novo('div');
        item.append(novo('span', '', label), novo('strong', '', `${br(c[k])} sc`));
        grade.append(item);
      }
      bloco.append(grade);
      bloco.append(novo('p', 'ag-etiqueta', `Área produtiva considerada: ${br(c.area_considerada_ha)} ha. Valores calculados a partir das produtividades inseridas pelo produtor.`));
      root.append(bloco);
    }
    const info = novo('details', 'ag-resumo-proximos');
    info.append(novo('summary', '', 'Como melhorar a precisão?'));
    const ul = novo('ul');
    const avisos = res.avisos?.length ? res.avisos.slice(0, 4) : ['Acompanhe as etapas da lavoura em campo e mantenha os dados atualizados.'];
    for (const texto of avisos) ul.append(novo('li', '', texto));
    info.append(ul);
    root.append(info);
    $('ajudaIASimples').disabled = false;
  }
  function renderAvancado(res) {
    const root = $('resultadoAnaliseAvancada');
    root.replaceChildren();
    root.hidden = false;
    root.append(novo('h3', '', `Análise de ${res.safra} (${res.cultura})`));
    if (res.janela_preliminar) {
      linha(root, 'Janela inicial:', `${dataBR(res.janela_preliminar.inicio_janela)} a ${dataBR(res.janela_preliminar.fim_janela)}`);
    }
    if (res.janela_refinada) {
      root.append(novo('h3', '', 'Janela calculada com seus parâmetros'));
      linha(root, 'Intervalo:', `${dataBR(res.janela_refinada.inicio_janela)} a ${dataBR(res.janela_refinada.fim_janela)}`);
      linha(root, 'Método:', res.janela_refinada.metodo);
      linha(root, 'Origem:', res.janela_refinada.fonte);
      root.append(novo('p', '', 'Resultado condicionado aos parâmetros; não é uma previsão validada.'));
    } else {
      root.append(novo('p', '', 'Sem intervalo técnico suficiente para refinar. A janela geral permanece como referência.'));
    }
    if (res.pontos_de_acompanhamento?.length) {
      root.append(novo('h3', '', 'Datas registradas e intervalos calculados'));
      for (const item of res.pontos_de_acompanhamento) {
        const txt = item.data ? dataBR(item.data) : `${dataBR(item.inicio)} a ${dataBR(item.fim)}`;
        root.append(novo('div', 'ag-refina-etapa', `${item.fase} (${item.tipo}): ${txt}`));
      }
    }
    if (res.cenarios_producao) {
      const c = res.cenarios_producao;
      root.append(novo('h3', '', 'Cenários hipotéticos de produção'));
      const grade = novo('div', 'ag-refina-cenario');
      for (const [label, k] of [['Baixo', 'baixa'], ['Intermediário', 'media'], ['Alto', 'alta']]) {
        const tile = novo('div');
        tile.append(novo('span', '', label), novo('strong', '', br(c[k]) + ' sc de 60 kg'));
        grade.append(tile);
      }
      root.append(grade);
      linha(root, 'Área considerada:', br(c.area_considerada_ha) + ' ha');
      root.append(novo('p', '', 'Cálculo = área produtiva × produtividade (sacas/ha) informada. Não é previsão real.'));
    }
    if (res.avisos?.length) {
      root.append(novo('h3', '', 'O que falta para melhorar a análise?'));
      const ul = novo('ul');
      for (const aviso of res.avisos) ul.append(novo('li', '', aviso));
      root.append(ul);
    }
  }
  function render(res) {
    ultimaAnalise = res;
    renderSimples(res);
    renderAvancado(res);
  }
  async function trocarSafra() {
    const numero = ++solicitacao;
    const id = idSafra();
    limpar();
    $('botaoSalvarAnalise').disabled = !id;
    if (!id) {
      status('Selecione uma propriedade e uma safra para visualizar a estimativa.');
      return;
    }
    status('Buscando a estimativa da safra no AgroRisk...');
    try {
      const obj = await requisitar('GET', id);
      if (numero !== solicitacao || id !== idSafra()) return;
      preencher(obj.parametros);
      render(obj);
      status('');
    } catch (e) {
      if (numero === solicitacao) status(e.message, true);
    }
  }
  function dados() {
    const payload = {};
    for (const [key, id] of Object.entries(campos)) {
      const value = $(id).value.trim();
      payload[key] = value === '' ? null : ($(id).type === 'number' ? Number(value) : value);
    }
    return payload;
  }
  // Monta a pergunta na área de chat, mas não envia nada antes de uma ação
  // explícita do usuário e do aceite do checkbox de consentimento.
  function prepararPergunta(tipo) {
    if (!idSafra()) {
      status('Escolha uma safra antes de pedir uma explicação personalizada à IA.', true);
      return;
    }
    let texto;
    if (tipo === 'avancada') {
      texto = 'Estou preenchendo a Estimativa Agrícola Avançada da safra selecionada. Explique de forma simples o que são cultivar, datas observadas, intervalo técnico entre florada e colheita e cenários em sacas/ha. Quais dados devo obter e de que fontes confiáveis? Não invente valores, datas ou produtividade.';
    } else {
      texto = `Explique de forma simples a estimativa de colheita da safra selecionada (${ultimaAnalise?.cultura || 'cultura cadastrada'}). Qual a diferença entre janela preliminar e cálculo refinado? Quais informações verificáveis faltam para melhorar a análise sem inventar precisão?`;
    }
    document.dispatchEvent(new CustomEvent('agrorisk:preparar-pergunta-ia', {detail: {texto}}));
  }
  document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('agrorisk:safra-selecionada', trocarSafra);
    document.addEventListener('agrorisk:safras-carregadas', trocarSafra);
    $('abaModoSimples').addEventListener('click', () => selecionarModo('simples'));
    $('abaModoAvancado').addEventListener('click', () => selecionarModo('avancado'));
    for (const tabId of ['abaModoSimples', 'abaModoAvancado']) {
      $(tabId).addEventListener('keydown', e => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          e.preventDefault();
          selecionarModo(tabId === 'abaModoSimples' ? 'avancado' : 'simples', true);
        }
      });
    }
    $('ajudaIASimples').addEventListener('click', () => prepararPergunta('simples'));
    $('ajudaIAAvancada').addEventListener('click', () => prepararPergunta('avancada'));
    $('formAnaliseAvancada').addEventListener('submit', async e => {
      e.preventDefault();
      const id = idSafra();
      if (!id) return;
      const btn = $('botaoSalvarAnalise');
      btn.disabled = true;
      const versao = ++solicitacao;
      status('Salvando os parâmetros no MySQL...');
      try {
        const obj = await requisitar('PUT', id, dados());
        if (versao === solicitacao && id === idSafra()) {
          render(obj);
          preencher(obj.parametros);
          status('Parâmetros salvos. A estimativa foi atualizada e também está disponível no modo simples.');
        }
      } catch (err) {
        if (versao === solicitacao) status(err.message, true);
      } finally {
        btn.disabled = !idSafra();
      }
    });
    selecionarModo('simples');
  });
})();
