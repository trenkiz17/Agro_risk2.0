# AgroRisk — patch “Analisar Safra” com OpenWeather e status de colheita

## O que este patch altera

Substitui APENAS os quatro arquivos nas pastas relativas ao seu frontend:

- `frontend/relatorios.html`
- `frontend/js/relatorios.js`
- `frontend/safras.html`
- `frontend/js/safras.js`

E ADICIONA:

- `frontend/js/indicadoresSafra.js`

Não altera `backend/`, credenciais, conexão MySQL, modelos, cadastro de propriedades/safras nem os cálculos já implementados no Flask. Faz uso de funções já existentes em `frontend/js/api.js`: `listarPropriedades()`, `listarSafras()`, `buscarClima()`, `buscarPrevisaoClima()` e `atualizarSafra()`.

### Antes de aplicar

1. Faça backup dos arquivos existentes e do banco MySQL.
2. Confira se o seu projeto já possui as rotas `/api/clima`, `/api/clima/previsao`, `/safras/estimar-colheita` e `PUT /safras/<id>`.
3. Copie esses arquivos mantendo as pastas e os nomes. O `indicadoresSafra.js` PRECISA estar presente e carregado ANTES do `safras.js` e do `relatorios.js` — os HTMLs inclusos já fazem isso.
4. Inicie o Flask e o frontend normalmente. Recarregue a página com Ctrl+F5 para evitar scripts antigos em cache.

## O que aparece no botão Analisar Safra

- Nome, propriedade, cultura, área, data de plantio, data central estimada, **janela preliminar de colheita em meses/anos**.
- **Status de calendário**: Planejamento, Em andamento, Na janela prevista, Janela encerrada.
- **Status confirmado**: Finalizada SOMENTE se o produtor clicar em **Confirmar colheita concluída** e a atualização no MySQL retornar sucesso.
- **Clima atual do OpenWeather** no ponto de referência da propriedade (temperatura e condição), chuva prevista acumulada no horizonte consultado e triagem experimental de atenção baseada em 35 °C / 50 mm; os critérios demonstrativos NÃO são recomendações agronômicas.
- Relatório PDF atualizado com os indicadores carregados e uma segunda página com metodologia e limitações.
- Custos exibidos quando `custo_total` existir; receitas e lucros continuam não calculados quando faltam preço de venda e produção física. Dados NÃO são inventados.

## Teste para o TCC em 14/10/2026

Cadastre uma safra de Café, com propriedade válida e data de plantio:

- **14/10/2026**: em andamento após plantio; primeira colheita preliminar de 2029 a 2030.
- **14/10/2023**: início da janela estimada HOJE (14/10/2026); ainda não está finalizada.
- **14/10/2022**: último dia da janela preliminar (14/10/2025 a 14/10/2026); ainda não está finalizada.
- **14/10/2021**: janela estimada encerrada; ainda não significa safra concluída.

Para testar a conclusão, clique em **Confirmar colheita concluída**, confirme no diálogo, recarregue a página e veja se **Finalizada** persistiu no MySQL.

### Limitações reais (importantes na defesa do TCC)

- A estimativa de café já existente no Flask usa **3 a 4 anos após o plantio** como referência à **primeira colheita de lavoura nova**; não há previsão confiável do clima de 2029/2030 no OpenWeather atual.
- Para milho e soja, seguem os intervalos demonstrativos do backend: 110–150 e 100–140 dias, respectivamente.
- O script `indicadoresSafra.js` repete os valores do serviço do Flask somente para mostrar os status na listagem sem requisitar cada safra separadamente. Se você alterar os parâmetros do backend, atualize também esse script.
- Clima atual e previsão **NÃO são histórico climático de quatro anos**; este patch NÃO grava leituras no MySQL.
- O botão de finalizar usa o endpoint PUT existente e sua autenticação ATUAL. Antes de publicar o site online, o backend precisa autenticar e validar a propriedade de cada safra com segurança. Não exponha esse backend publicamente.
- Os limiares de calor/chuva são **sinalizadores ilustrativos**, não cálculo validado de risco agronômico.

## Verificações realizadas

- Sintaxe dos 3 JavaScripts validada com `node --check`.
- 9 casos de calendário/status (incluindo 29/02, janela vencida e status explicitamente Finalizada).
- 11 verificações simuladas de renderização, consulta climática e confirmação (sem API externa / MySQL real).
- Dois HTMLs verificados sem IDs duplicados.

O teste real do PUT, da API OpenWeather e do MySQL deve ser feito no seu ambiente.
