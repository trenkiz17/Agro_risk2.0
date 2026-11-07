/* Orientador AgroRisk: calculadora local e assistente Gemini via API Flask. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const norm = s => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const numeroBR = valor => Number(valor).toLocaleString("pt-BR", {maximumFractionDigits: 0});
  const dataBR = valor => {
    const d=String(valor || "").slice(0,10);
    return /^\d{4}-\d{2}-\d{2}$/.test(d) ? `${d.slice(8,10)}/${d.slice(5,7)}/${d.slice(0,4)}` : "indisponível";
  };
  function capacidadeMudas(area, percentual, linhas, plantas) {
    if (![area, percentual, linhas, plantas].every(Number.isFinite) ||
        area <= 0 || area > 100000 || percentual <= 0 || percentual > 100 ||
        linhas < 0.1 || linhas > 100 || plantas < 0.1 || plantas > 100) {
      throw new Error("Confira a área (até 100 mil ha), percentual de uso e espaçamentos positivos.");
    }
    const areaUtilM2 = area * 10000 * percentual / 100;
    const estimativa = Math.floor(areaUtilM2 / (linhas * plantas));
    return {areaUtilM2, estimativa};
  }
  // Histórico curto para manter o contexto. Não é gravado no banco nem em localStorage.
  const mensagens = [];
  let emEnvio = false;
  let propriedades = [];
  let safras = [];

  function textoOpcao(texto) {return String(texto||"").slice(0,110);}
  function preencherSelect(id, itens, label) {
    const seletor=$(id);
    seletor.replaceChildren();
    const inicial=document.createElement("option");inicial.value="";inicial.textContent=label;seletor.append(inicial);
    itens.forEach(item=>{const opt=document.createElement("option");opt.value=item.id;opt.textContent=textoOpcao(item.nome);seletor.append(opt);});
  }
  function status(texto,erro=false){
    $("statusOrientador").textContent=texto;
    $("statusOrientador").classList.toggle("ag-ai-erro",erro);
  }
  async function carregarDadosContexto(){
    // Usa as rotas já autenticadas do AgroRisk; nenhum registro de outra conta é oferecido.
    const props=await listarPropriedades();
    propriedades=Array.isArray(props)?props:[];
    preencherSelect("propriedadeContexto",propriedades,"Sem propriedade selecionada");
    const saf=await listarSafras();
    safras=Array.isArray(saf)?saf:[];
    atualizarSafrasContexto();
    // Links vindos do relatório podem abrir diretamente a safra escolhida.
    const idUrl = Number(new URLSearchParams(window.location.search).get("safra_id"));
    const daUrl = safras.find(s => Number(s.id)===idUrl);
    if (daUrl && propriedades.some(p => Number(p.id)===Number(daUrl.propriedade_id))) {
      $("propriedadeContexto").value=String(daUrl.propriedade_id);
      atualizarSafrasContexto();
      $("safraContexto").value=String(daUrl.id);
      document.dispatchEvent(new Event("agrorisk:safra-selecionada"));
    }
    document.dispatchEvent(new Event("agrorisk:safras-carregadas"));
  }
  function atualizarSafrasContexto(){
    const id=Number($("propriedadeContexto").value);
    const itens=id?safras.filter(s=>Number(s.propriedade_id)===id):[];
    preencherSelect("safraContexto",itens,"Sem safra selecionada");
    $("safraContexto").disabled=!id;
    document.dispatchEvent(new Event("agrorisk:safra-selecionada"));
  }
  async function checarIA(){
    const token=sessionStorage.getItem("agrorisk_token");
    if(!token){status("Faça login para usar a IA e consultar seus dados.",true);return;}
    try{
      const r=await fetch("/api/orientador/status",{headers:{Authorization:`Bearer ${token}`},cache:"no-store"});
      if(!r.ok)throw new Error("Faça login novamente para usar a IA.");
      const dados=await r.json();
      status(dados.configurada?"IA conectada ao backend • Modelo: "+dados.modelo:"IA não configurada: adicione GEMINI_API_KEY ao backend/.env.",!dados.configurada);
    }catch(e){status(e.message||"Não foi possível verificar o serviço de IA.",true);}
  }
  async function enviar(texto){
    const pergunta=String(texto||"").trim();
    if(!pergunta||emEnvio)return;
    if(!$("consentimentoIA").checked){status("Autorize o envio ao Gemini antes de perguntar.",true);return;}
    const token=sessionStorage.getItem("agrorisk_token");
    if(!token){status("Faça login novamente antes de perguntar.",true);return;}
    emEnvio=true;$("botaoEnviarIA").disabled=true;$("textoPergunta").disabled=true;
    mostrarMensagem(pergunta,true);
    mostrarMensagem("Consultando IA...");
    const carregando=$("conversaOrientador").lastElementChild;
    try {
      const propriedade_id=Number($("propriedadeContexto").value)||null;
      const safra_id=Number($("safraContexto").value)||null;
      const resposta=await fetch("/api/orientador/perguntar",{
        method:"POST",cache:"no-store",
        headers:{"Authorization":`Bearer ${token}`,"Content-Type":"application/json"},
        body:JSON.stringify({pergunta,consentimento:true,historico:mensagens.slice(-6),propriedade_id,safra_id,
          incluir_clima:$("incluirClimaContexto").checked && !!propriedade_id})
      });
      let dados={};try{dados=await resposta.json()}catch{}
      if(!resposta.ok)throw new Error(dados.erro||`Erro ${resposta.status} ao consultar a IA.`);
      const textoResposta=String(dados.resposta||"A IA não retornou uma resposta.");
      carregando.textContent=textoResposta;
      mensagens.push({role:"user",text:pergunta},{role:"model",text:textoResposta});
      while(mensagens.length>6)mensagens.shift();
      $("textoPergunta").value="";
      status("Resposta recebida do Gemini • Verifique informações técnicas antes de decidir.");
    }catch(e){
      carregando.textContent=e.message||"Não foi possível consultar a IA.";
      carregando.classList.add("ag-chat-erro");
      status("Falha ao consultar a IA. Os demais recursos do AgroRisk continuam disponíveis.",true);
    }finally{emEnvio=false;$("botaoEnviarIA").disabled=false;$("textoPergunta").disabled=false;$("textoPergunta").focus();}
  }
  function mostrarMensagem(texto,usuario=false) {
    const log=$("conversaOrientador");
    const item=document.createElement("div");
    item.className=`ag-chat-bolha ${usuario?"ag-chat-usuario":"ag-chat-sistema"}`;
    item.textContent=texto;
    log.append(item);
    log.scrollTop=log.scrollHeight;
  }
  async function consultarEstimativa(evento){
    evento.preventDefault();
    const resultado=$("resultadoEstimativaOrientador");
    resultado.hidden=false;
    resultado.textContent="Consultando estimativa do AgroRisk...";
    const cultura=$("culturaOrientador").value;
    const plantio=$("dataOrientador").value;
    window.AgroRiskLinhaTempo?.render("linhaTempoOrientador", "", null);
    if (!plantio) {resultado.textContent="Informe a data de plantio.";return;}
    try {
      // Usa a função existente de api.js, conectada ao estimador Flask do AgroRisk.
      const dados=await estimarColheita(cultura,plantio);
      if(!dados || !dados.inicio_janela || !dados.fim_janela){
        resultado.textContent="Não foi possível consultar a estimativa. Verifique se o Flask está ativo.";
        return;
      }
      resultado.textContent=`Janela preliminar: ${dataBR(dados.inicio_janela)} a ${dataBR(dados.fim_janela)}.\n\n${dados.aviso || "Estimativa de calendário não garantida."}`;
      window.AgroRiskLinhaTempo?.render("linhaTempoOrientador",cultura,dados,plantio);
    } catch(e){
      resultado.textContent="A consulta à API falhou. Confira o servidor Flask.";
      console.error(e);
    }
  }
  document.addEventListener("DOMContentLoaded",()=>{
    $("formMudas")?.addEventListener("submit",evento=>{
      evento.preventDefault();
      const out=$("resultadoMudas");out.hidden=false;
      try {
        const area=Number($("areaHa").value),percentual=Number($("areaUtil").value);
        const linhas=Number($("espLinhas").value),plantas=Number($("espPlantas").value);
        const {areaUtilM2,estimativa}=capacidadeMudas(area,percentual,linhas,plantas);
        out.textContent=`Capacidade geométrica estimada: ${numeroBR(estimativa)} posições de plantio.\nÁrea plantável usada: ${areaUtilM2.toLocaleString("pt-BR",{maximumFractionDigits:2})} m².\nFórmula: área plantável (m²) ÷ [espaçamento linhas (m) × espaçamento plantas (m)].\n\nEsse número não é recomendação de mudas nem considera perdas e particularidades da fazenda.`;
      } catch(e){out.textContent=e.message;}
    });
    $("formEstimativaOrientador")?.addEventListener("submit",consultarEstimativa);
    if (!$("formPerguntaOrientador")) return; // As calculadoras são uma página independente.
    mostrarMensagem("Olá! Como posso ajudar no planejamento da sua lavoura?");
    $("formPerguntaOrientador").addEventListener("submit",evento=>{evento.preventDefault();enviar($("textoPergunta").value);});
    // Sugestões apenas preenchem o campo; envio é sempre uma ação explícita do usuário.
    $("sugestoesOrientador").querySelectorAll("[data-pergunta]").forEach(botao=>botao.addEventListener("click",()=>{ $("textoPergunta").value=botao.dataset.pergunta;$("textoPergunta").focus(); }));
    $("propriedadeContexto").addEventListener("change",atualizarSafrasContexto);
    $("safraContexto").addEventListener("change",()=>document.dispatchEvent(new Event("agrorisk:safra-selecionada")));
    // Os botões dos dois modos apenas preenchem a caixa. O usuário precisa conferir
    // e enviar a mensagem, respeitando o consentimento já exigido pelo chat.
    document.addEventListener("agrorisk:preparar-pergunta-ia", evento => {
      const texto = String(evento.detail?.texto || "").trim();
      if (!texto) return;
      $("textoPergunta").value = texto;
      $("textoPergunta").scrollIntoView({behavior:"smooth", block:"center"});
      $("textoPergunta").focus({preventScroll:true});
      status("Pergunta preparada. Leia, marque o consentimento e clique em Perguntar à IA.");
    });
    $("limparConversaIA").addEventListener("click",()=>{mensagens.length=0;$("conversaOrientador").replaceChildren();mostrarMensagem("Nova conversa iniciada. Como posso ajudar?");});
    checarIA();
    if(sessionStorage.getItem("agrorisk_token"))carregarDadosContexto().catch(e=>status("Não foi possível carregar as propriedades da conta.",true));
  });
  // Funções expostas apenas para teste automatizado dos cálculos.
  window.AgroRiskCalculos={capacidadeMudas};
})();
