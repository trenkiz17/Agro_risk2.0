/* AgroRisk — Guia de navegação opcional.
 * Não altera dados, não chama APIs nem interfere nos formulários existentes.
 */
(() => {
  "use strict";
  const roteiros = {
    dashboard: {
      titulo: "Por onde começar?",
      descricao: "Um caminho simples para explorar o AgroRisk sem perder as funcionalidades existentes.",
      etapas: [
        ["Cadastre sua propriedade", "Informe o nome e localize a área no mapa.", "cadastro_propriedade.html"],
        ["Cadastre uma safra", "Vincule uma cultura à propriedade, informe o plantio e a área.", "cadastro_safras.html"],
        ["Acompanhe as condições", "Abra o monitoramento para consultar o clima e a previsão.", "propriedades.html"],
        ["Consulte a análise", "Na área de Safras, abra uma análise e exporte o PDF.", "orientador.html"]
      ]
    },
    propriedade: {
      titulo: "Passo a passo do cadastro",
      descricao: "Siga as etapas; você continua usando o mesmo formulário e mapa.",
      etapas: [
        ["Pesquise a região", "Use Pesquisar Local para encontrar a cidade ou o endereço desejado.", "#btnPesquisar"],
        ["Desenhe os limites", "Use a ferramenta de polígono no mapa. Área e perímetro serão calculados.", "#map"],
        ["Preencha os dados", "Identifique a fazenda, a cidade e o estado.", "#nome"],
        ["Confira e salve", "Veja os valores calculados antes de salvar a propriedade.", "#salvar"]
      ]
    },
    safra: {
      titulo: "Passo a passo da safra",
      descricao: "A colheita exibida é uma faixa estimada; não representa previsão garantida.",
      etapas: [
        ["Selecione a propriedade", "A safra precisa estar associada a uma propriedade cadastrada.", "#propriedade"],
        ["Escolha a cultura e a área", "Informe café, milho ou soja e quantos hectares serão cultivados.", "#cultura"],
        ["Informe o plantio", "O backend calcula a janela inicial a partir dessa data.", "#plantio"],
        ["Confira antes de salvar", "Leia a linha do tempo, revise os dados e confirme.", "#btnSalvarSafra"]
      ]
    },
    propriedades: {
      titulo: "O que fazer com uma propriedade?",
      descricao: "Depois do cadastro, cada fazenda pode ser acompanhada individualmente.",
      etapas: [
        ["Abra o monitoramento", "Selecione uma propriedade na listagem para consultar os dados dela.", null],
        ["Consulte a localização", "Confira a área e o perímetro cadastrados.", null],
        ["Associe uma safra", "Acesse o cadastro de safra e selecione esta propriedade.", "cadastro_safras.html"]
      ]
    },
    safras: {
      titulo: "Como acompanhar uma safra?",
      descricao: "Use os dados cadastrados para consultar a janela e a análise.",
      etapas: [
        ["Filtre por propriedade", "Selecione a fazenda para localizar mais rapidamente as safras.", "#filtroPropriedadeSafras"],
        ["Observe o status", "A situação no calendário não confirma uma colheita efetivamente realizada.", null],
        ["Analise e gere PDF", "Abra uma safra em Analisar Safra e use Gerar PDF.", "relatorios.html"]
      ]
    },
    monitoramento: {
      titulo: "Entenda o monitoramento",
      descricao: "Os dados de clima são atuais ou de curto prazo e não preveem o tempo de anos futuros.",
      etapas: [
        ["Localize sua propriedade", "Confira o mapa e as informações cadastradas.", ".monitor-map"],
        ["Veja o clima atual", "Temperatura e umidade dependem da consulta à OpenWeather.", "#temperatura"],
        ["Veja os próximos dias", "Acompanhe o gráfico de temperatura e chuva previstas.", ".grafico-box"],
        ["Acompanhe as safras", "Veja as safras associadas à mesma propriedade.", "#secaoSafras"]
      ]
    },
    relatorios: {
      titulo: "Como gerar um relatório?",
      descricao: "O arquivo em PDF reúne os dados que você cadastrou e a análise disponível.",
      etapas: [
        ["Selecione a propriedade", "Encontre a fazenda no filtro do relatório.", "#filtroPropriedadeRelatorio"],
        ["Selecione uma safra", "Escolha a safra que deseja analisar.", "#filtroSafraRelatorio"],
        ["Confira a janela", "Veja a estimativa de colheita e sua explicação.", "#janelaColheitaRelatorio"],
        ["Gere o PDF", "Após carregar a análise, clique em Gerar PDF.", "#btnGerarPDF"]
      ]
    }
  };
  function elemento(tag, classe, texto) {
    const el = document.createElement(tag);
    if (classe) el.className = classe;
    if (texto != null) el.textContent = texto;
    return el;
  }
  function iniciar(container) {
    const roteiro = roteiros[container.dataset.agroriskGuia];
    if (!roteiro) return;
    const detalhes = elemento("details", "ag-guia-detalhes");
    const resumo = elemento("summary", "ag-guia-resumo");
    resumo.append(elemento("span", "ag-guia-icone", "?"), elemento("span", "", roteiro.titulo));
    resumo.append(elemento("span", "ag-guia-abrir", "Ver guia"));
    const corpo = elemento("div", "ag-guia-conteudo");
    const descricao = elemento("p", "ag-guia-descricao", roteiro.descricao);
    const etapa = elemento("div", "ag-guia-etapa");
    const progresso = elemento("div", "ag-guia-progresso");
    progresso.setAttribute("role", "progressbar");
    progresso.setAttribute("aria-valuemin", "1");
    progresso.setAttribute("aria-valuemax", String(roteiro.etapas.length));
    const barra = elemento("div", "ag-guia-barra");
    progresso.append(barra);
    const rodape = elemento("div", "ag-guia-acoes");
    const voltar = elemento("button", "ag-botao ag-botao-auxiliar", "Anterior");
    const proximo = elemento("button", "ag-botao ag-botao-principal", "Próximo passo");
    voltar.type = proximo.type = "button";
    const contador = elemento("span", "ag-guia-contador");
    rodape.append(voltar, contador, proximo);
    corpo.append(descricao, progresso, etapa, rodape);
    detalhes.append(resumo, corpo);
    container.append(detalhes);
    let atual=0;
    const render = () => {
      const dados=roteiro.etapas[atual];
      etapa.replaceChildren();
      etapa.append(elemento("strong", "ag-guia-titulo-etapa", dados[0]), elemento("p", "ag-guia-texto-etapa", dados[1]));
      if(dados[2]) {
        const link=elemento("a", "ag-guia-link", dados[2].startsWith("#")||dados[2].startsWith(".") ? "Ir para este campo" : "Abrir esta página");
        link.href=dados[2];
        if(dados[2].startsWith("#") || dados[2].startsWith(".")){
          link.href="#";
          link.addEventListener("click", evento=>{
            evento.preventDefault();
            const alvo=document.querySelector(dados[2]);
            if(!alvo) return;
            alvo.scrollIntoView({behavior:"smooth",block:"center"});
            alvo.classList.add("ag-guia-destaque");
            if(["INPUT","SELECT","TEXTAREA","BUTTON"].includes(alvo.tagName)) alvo.focus({preventScroll:true});
            window.setTimeout(()=>alvo.classList.remove("ag-guia-destaque"),2200);
          });
        }
        etapa.append(link);
      }
      barra.style.width=`${(atual+1)/roteiro.etapas.length*100}%`;
      progresso.setAttribute("aria-valuenow",String(atual+1));
      contador.textContent=`${atual+1} / ${roteiro.etapas.length}`;
      voltar.disabled=atual===0;
      proximo.textContent=atual===roteiro.etapas.length-1?"Recomeçar":"Próximo passo";
    };
    voltar.addEventListener("click",()=>{atual=Math.max(0,atual-1);render();});
    proximo.addEventListener("click",()=>{atual=(atual+1)%roteiro.etapas.length;render();});
    render();
  }
  document.addEventListener("DOMContentLoaded",()=>document.querySelectorAll("[data-agrorisk-guia]").forEach(iniciar));
})();
