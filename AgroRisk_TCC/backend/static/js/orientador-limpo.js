/* Navegação visual do Orientador AgroRisk — preserva cálculos e rotas existentes. */
(() => {
  'use strict';
  const secoes = {
    analise: ['agTabAnalise', 'agViewAnalise'],
    ia: ['agTabIA', 'agViewIA']
  };
  function mostrarSecao(nome, focar = false) {
    if (!Object.prototype.hasOwnProperty.call(secoes, nome)) return;
    for (const [chave, [idTab, idPainel]] of Object.entries(secoes)) {
      const aba = document.getElementById(idTab);
      const painel = document.getElementById(idPainel);
      if (!aba || !painel) return;
      const selecionada = chave === nome;
      aba.classList.toggle('is-active', selecionada);
      aba.setAttribute('aria-selected', String(selecionada));
      aba.tabIndex = selecionada ? 0 : -1;
      painel.hidden = !selecionada;
    }
    const contexto = document.getElementById('agContexto');
    if (contexto) contexto.hidden = false;
    const abaAtiva = document.getElementById(secoes[nome][0]);
    if (focar) abaAtiva?.focus();
  }
  // Ao pedir uma explicação de uma safra, mostrar o chat antes de focalizar a pergunta.
  document.addEventListener('agrorisk:preparar-pergunta-ia', () => mostrarSecao('ia'));
  document.addEventListener('DOMContentLoaded', () => {
    for (const [nome, [idTab]] of Object.entries(secoes)) {
      const aba = document.getElementById(idTab);
      aba?.addEventListener('click', () => mostrarSecao(nome));
      aba?.addEventListener('keydown', evento => {
        if (evento.key !== 'ArrowRight' && evento.key !== 'ArrowLeft') return;
        evento.preventDefault();
        const lista = Object.keys(secoes);
        const indice = lista.indexOf(nome);
        mostrarSecao(lista[(indice + (evento.key === 'ArrowRight' ? 1 : lista.length - 1)) % lista.length], true);
      });
    }
    mostrarSecao('analise');
  });
  window.AgroRiskOrientadorVisual = {mostrarSecao};
})();
