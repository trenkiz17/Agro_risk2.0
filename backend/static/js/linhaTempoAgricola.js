/* Linha do tempo explicativa das culturas.
 * Usa a janela calculada pelo AgroRisk, sem inventar datas de floração ou crescimento.
 */
window.AgroRiskLinhaTempo = (() => {
  "use strict";
  const formatos = {
    cafe: [
      ["Implantação", "Plantio das mudas registrado no sistema."],
      ["1ª visita de acompanhamento", "Data sugerida para observar estabelecimento, raízes, folhas e manejo — não indica o início real do crescimento."],
      ["2ª visita de acompanhamento", "Data sugerida para acompanhar formação e, quando aplicável, estágios reprodutivos. O AgroRisk não prevê a data exata da floração."],
      ["Primeira colheita estimada", "Referência preliminar de 3 a 4 anos para uma lavoura nova de café; não se aplica diretamente a cafezal adulto."]
    ],
    milho: [
      ["Plantio", "Implantação das sementes na data informada."],
      ["1ª visita de acompanhamento", "Observe emergência, estande de plantas e crescimento. É uma data de vistoria sugerida, não uma previsão de estádio fenológico."],
      ["2ª visita de acompanhamento", "Observe desenvolvimento, formação de estruturas reprodutivas e condições da lavoura. Confirme as fases em campo."],
      ["Janela preliminar de colheita", "Faixa ilustrativa de 110 a 150 dias após o plantio, conforme o estimador atual."]
    ],
    soja: [
      ["Plantio", "Implantação das sementes na data informada."],
      ["1ª visita de acompanhamento", "Observe emergência e desenvolvimento vegetativo. A data é um lembrete, não uma previsão do crescimento."],
      ["2ª visita de acompanhamento", "Observe florescimento, vagens e grãos, conforme a fase real da cultura. A data não determina o florescimento."],
      ["Janela preliminar de colheita", "Faixa ilustrativa de 100 a 140 dias após o plantio, conforme o estimador atual."]
    ]
  };
  const normalizar = v => String(v||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").trim().toLowerCase();
  const dataBR = iso => {
    const data=String(iso||"").slice(0,10);
    return /^\d{4}-\d{2}-\d{2}$/.test(data)?`${data.slice(8,10)}/${data.slice(5,7)}/${data.slice(0,4)}`:"data não disponível";
  };
  const utc = value => {const x=String(value||"").slice(0,10);return /^\d{4}-\d{2}-\d{2}$/.test(x)?new Date(`${x}T12:00:00Z`):null;};
  const dataPonto = (plantio, inicio, frac) => {
    const inicioMs=utc(inicio)?.getTime(),plantioMs=utc(plantio)?.getTime();
    if(!Number.isFinite(inicioMs)||!Number.isFinite(plantioMs)||inicioMs<=plantioMs)return "Vistoria a programar";
    const dias=Math.round((inicioMs-plantioMs)/86400000*frac);
    return "Vistoria sugerida: "+dataBR(new Date(plantioMs+dias*86400000).toISOString().slice(0,10));
  };
  const ele=(nome,classe,conteudo)=>{const e=document.createElement(nome);e.className=classe;if(conteudo!=null)e.textContent=conteudo;return e;};
  function render(id,cultura,estimativa,dataPlantio){
    const root=document.getElementById(id);
    if(!root)return;
    root.replaceChildren();
    const itens=formatos[normalizar(cultura)];
    if(!estimativa?.inicio_janela || !estimativa?.fim_janela || !itens){
      root.append(ele("p","ag-tempo-vazio","Informe a cultura e a data de plantio para visualizar as etapas explicativas."));
      return;
    }
    const lista=ele("ol","ag-tempo-lista");
    itens.forEach((item,i)=>{
      const li=ele("li","ag-tempo-item");
      const numero=ele("span","ag-tempo-numero",String(i+1));
      const texto=ele("div","ag-tempo-texto");
      const quando=i===0?(dataPlantio?`Implantação: ${dataBR(dataPlantio)}`:"Início do cultivo"):
        i===itens.length-1?`Janela estimada: ${dataBR(estimativa.inicio_janela)} a ${dataBR(estimativa.fim_janela)}`:dataPonto(dataPlantio,estimativa.inicio_janela,i===1?0.3:0.7);
      texto.append(ele("strong","",item[0]),ele("span","ag-tempo-quando",quando),ele("p","",item[1]));
      li.append(numero,texto);lista.append(li);
    });
    root.append(lista,ele("p","ag-tempo-aviso","Plantio e janela de colheita vêm dos dados e do estimador do AgroRisk. As duas datas intermediárias são lembretes de vistoria distribuídos ao longo do calendário, NÃO previsões de crescimento, floração ou maturação. Para estimar fases biológicas, seriam necessários cultivar, local, clima e parâmetros validados."));
  }
  return {render};
})();
