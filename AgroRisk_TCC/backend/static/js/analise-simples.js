/* Minha Safra unificada: cadastro, seleção, resumo, edição e exclusão via API Flask/MySQL. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const texto = (valor, vazio='Não informado') => valor == null || String(valor).trim()==='' ? vazio : String(valor);
  const numBR = valor => Number(valor).toLocaleString('pt-BR',{maximumFractionDigits:2});
  const dataBR = valor => /^\d{4}-\d{2}-\d{2}$/.test(String(valor||'')) ? `${valor.slice(8,10)}/${valor.slice(5,7)}/${valor.slice(0,4)}` : '—';
  const no = (tag,classe,conteudo) => { const el=document.createElement(tag); if(classe)el.className=classe; if(conteudo!=null)el.textContent=conteudo; return el; };
  const mensagem = (valor,erro=false)=>{const el=$('mensagemAnalise');el.hidden=!valor;el.textContent=valor;el.classList.toggle('ag-ai-erro',erro);};
  let propriedades=[];
  let safras=[];
  let rodada=0;
  let excluindo=false;

  function idSelecionado(){return Number($('safraContexto').value)||0;}
  function safraAtual(){return safras.find(s=>Number(s.id)===idSelecionado())||null;}
  function setLinks(safra){
    const id=safra?.id;
    $('acoesSafraSelecionada').hidden=!id;
    $('linkEditarSafra').href=id?`cadastro_safras.html?id=${encodeURIComponent(id)}`:'cadastro_safras.html';
    $('linkRelatorioSafra').href=id?`relatorios.html?id=${encodeURIComponent(id)}`:'relatorios.html';
    $('linkIAContextual').href=id?`assistente.html?safra_id=${encodeURIComponent(id)}`:'assistente.html';
    const propriedadeId=Number($('propriedadeContexto').value)||0;
    $('linkNovaSafra').href=propriedadeId?`cadastro_safras.html?propriedade_id=${encodeURIComponent(propriedadeId)}`:'cadastro_safras.html';
  }
  function atualizarUrl(safra){
    const url=new URL(window.location.href);
    if(safra) url.searchParams.set('safra_id',String(safra.id));
    else url.searchParams.delete('safra_id');
    const prop=Number($('propriedadeContexto').value)||0;
    if(prop)url.searchParams.set('propriedade_id',String(prop));
    else url.searchParams.delete('propriedade_id');
    history.replaceState(null,'',url.pathname+url.search);
  }
  function opciones(el,items,placeholder){
    el.replaceChildren(new Option(placeholder,''));
    for(const item of items)el.add(new Option(String(item.nome||'Safra sem nome').slice(0,120),String(item.id)));
  }
  function daPropriedade(){
    const id=Number($('propriedadeContexto').value)||0;
    return safras.filter(s=>Number(s.propriedade_id)===id).sort((a,b)=>String(b.data_plantio||'').localeCompare(String(a.data_plantio||'')));
  }
  function painelLista(abrir=false){
    const painel=$('painelMinhasSafras'),botao=$('btnVerMinhasSafras');
    painel.hidden=!abrir;
    botao.setAttribute('aria-expanded',String(abrir));
    $('iconeListaSafras').textContent=abrir?'⌃':'⌄';
  }
  function atualizarLista(){
    const items=daPropriedade(), lista=$('listaMinhasSafras');
    $('totalSafrasLabel').textContent=items.length===1?'1 safra na propriedade':`${items.length} safras na propriedade`;
    $('contadorListaSafras').textContent=`(${items.length})`;
    $('btnVerMinhasSafras').hidden=items.length<=1;
    if(items.length<=1)painelLista(false);
    lista.replaceChildren();
    for(const safra of items){
      const linha=no('button','ag-item-safra'+(Number(safra.id)===idSelecionado()?' ag-item-ativo':''));
      linha.type='button';linha.setAttribute('aria-pressed',String(Number(safra.id)===idSelecionado()));
      const dados=no('span','ag-item-info');
      dados.append(no('strong','',texto(safra.nome,'Safra sem nome')),
        no('small','',`${texto(safra.cultura)} · ${texto(safra.area_plantada,'—')} ha`));
      linha.append(dados,no('span','ag-item-acao','Ver resumo ›'));
      linha.addEventListener('click',()=>{
        $('safraContexto').value=String(safra.id);
        selecionarSafra();
        painelLista(false);
      });
      lista.append(linha);
    }
  }
  function resumoLocal(safra){
    const raiz=$('resumoAnaliseSimples');raiz.replaceChildren();
    if(!safra){
      raiz.append(no('p','ag-analise-vazio','Você ainda não selecionou uma safra. Use Nova Safra para começar.'));
      return;
    }
    raiz.append(no('h3','ag-simples-safra',`${texto(safra.nome,'Safra')} · ${texto(safra.cultura)}`));
    const indicadores=(typeof AgroRiskIndicadores !== 'undefined')?AgroRiskIndicadores.situacao(safra):null;
    const grid=no('div','ag-resumo-metricas');
    const status=indicadores?.status||texto(safra.status,'Planejamento');
    for(const [rotulo,valor] of [
      ['Situação',status],
      ['Área plantada',safra.area_plantada!=null?`${numBR(safra.area_plantada)} ha`:'—'],
      ['Plantio',dataBR(safra.data_plantio)]
    ]){
      const item=no('div','ag-resumo-metrica');item.append(no('span','',rotulo),no('strong','',valor));grid.append(item);
    }
    raiz.append(grid);
    const janela=(typeof AgroRiskIndicadores !== 'undefined')?AgroRiskIndicadores.janela(safra):null;
    const bloco=no('div','ag-resumo-janela ag-janela-colheita');
    bloco.append(no('span','','Previsão de colheita'),
      no('strong','',janela?`${dataBR(janela.inicio)} a ${dataBR(janela.fim)}`:'Ainda não disponível'));
    bloco.append(no('p','','Janela preliminar de referência; a colheita real depende da variedade, do clima e do manejo.'));
    raiz.append(bloco);
  }
  function aplicarJanelaRefinada(obj){
    if(!obj||!obj.janela_refinada)return;
    const janela=obj.janela_refinada;
    const bloco=$('resumoAnaliseSimples').querySelector('.ag-janela-colheita');
    if(!bloco||!janela.inicio_janela||!janela.fim_janela)return;
    bloco.querySelector('span').textContent='Janela com parâmetros técnicos cadastrados';
    bloco.querySelector('strong').textContent=`${dataBR(janela.inicio_janela)} a ${dataBR(janela.fim_janela)}`;
    bloco.querySelector('p').textContent='Intervalo calculado com os parâmetros registrados. É uma estimativa, não uma data garantida.';
  }
  async function carregarAnaliseAvancada(safra){
    if(!safra)return;
    const id=Number(safra.id), versao=++rodada;
    try{
      const token=sessionStorage.getItem('agrorisk_token');
      const resp=await fetch(`/api/analise-avancada/safras/${encodeURIComponent(id)}`,{headers:{Authorization:`Bearer ${token}`},cache:'no-store'});
      if(!resp.ok)return; // a estimativa inicial permanece disponível
      const obj=await resp.json();
      if(versao!==rodada||id!==idSelecionado())return;
      aplicarJanelaRefinada(obj);
    }catch(err){console.warn('Refinamento indisponível. Mantida a janela preliminar.',err);}
  }
  function selecionarSafra(){
    const safra=safraAtual();
    rodada++;
    setLinks(safra);resumoLocal(safra);atualizarLista();atualizarUrl(safra);
    mensagem(safra?'':safras.length?'Escolha uma safra.':'Cadastre uma safra para começar.');
    if(safra)carregarAnaliseAvancada(safra);
  }
  function atualizarPropriedade({preferida=0}={}){
    const id=Number($('propriedadeContexto').value)||0;
    const items=daPropriedade();
    opciones($('safraContexto'),items,id?'Escolha uma safra':'Escolha uma propriedade');
    $('safraContexto').disabled=!id||items.length===0;
    let selecionada=items.find(s=>Number(s.id)===Number(preferida));
    if(!selecionada&&items.length)selecionada=items[0];
    if(selecionada)$('safraContexto').value=String(selecionada.id);
    painelLista(false);selecionarSafra();
  }
  async function excluirSelecionada(){
    const safra=safraAtual();
    if(!safra||excluindo)return;
    if(!window.confirm(`Excluir permanentemente a safra "${texto(safra.nome)}"? Esta ação remove o registro do banco de dados e não pode ser desfeita.`))return;
    const botao=$('btnExcluirSafra');excluindo=true;botao.disabled=true;
    mensagem('Excluindo safra...');
    try{
      const resultado=await excluirSafra(safra.id);
      if(!resultado)throw new Error('A API não confirmou a exclusão.');
      safras=safras.filter(item=>Number(item.id)!==Number(safra.id));
      atualizarPropriedade();
      mensagem('Safra excluída com sucesso do MySQL.');
    }catch(err){mensagem(err.message||'Não foi possível excluir a safra.',true);}
    finally{excluindo=false;botao.disabled=false;}
  }
  async function iniciar(){
    if(!sessionStorage.getItem('agrorisk_token')){location.replace('login.html');return;}
    try{
      const [p,s]=await Promise.all([listarPropriedades(),listarSafras()]);
      const props=Array.isArray(p)?p:p?.data;
      const regs=Array.isArray(s)?s:s?.data;
      if(!Array.isArray(props)||!Array.isArray(regs))throw new Error('Não foi possível carregar os dados da conta.');
      propriedades=props;
      safras=regs.filter(item=>props.some(propriedade=>Number(propriedade.id)===Number(item.propriedade_id)));
      opciones($('propriedadeContexto'),propriedades,'Escolha uma propriedade');
      const params=new URLSearchParams(location.search);
      const safraID=Number(params.get('safra_id')||params.get('id'))||0;
      const registro=safras.find(item=>Number(item.id)===safraID);
      const propID=registro?.propriedade_id || Number(params.get('propriedade_id')) || propriedades[0]?.id;
      if(propID&&propriedades.some(item=>Number(item.id)===Number(propID)))$('propriedadeContexto').value=String(propID);
      atualizarPropriedade({preferida:safraID});
      if(!propriedades.length)mensagem('Primeiro cadastre uma propriedade em Minhas Propriedades.');
    }catch(err){
      console.error(err);mensagem(err.message||'Falha ao carregar as safras.',true);
      $('resumoAnaliseSimples').replaceChildren(no('p','ag-analise-vazio','Dados temporariamente indisponíveis.'));
    }
  }
  document.addEventListener('DOMContentLoaded',()=>{
    $('propriedadeContexto').addEventListener('change',()=>atualizarPropriedade());
    $('safraContexto').addEventListener('change',selecionarSafra);
    $('btnExcluirSafra').addEventListener('click',excluirSelecionada);
    $('btnVerMinhasSafras').addEventListener('click',()=>painelLista($('painelMinhasSafras').hidden));
    iniciar();
  });
})();
