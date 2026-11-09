<div align="center">

# 🌱 AgroRisk

### Plataforma de gestão e monitoramento agrícola

**TCC • Técnico em Informática • 2026**

**Documentação atualizada em 07/11/2026:** esta versão reúne **Minhas Propriedades**, **Minha Safra unificada**, **Monitoramento**, **Relatórios em PDF**, **Assistente IA (Gemini)** e o **Dashboard original**. O cadastro, a edição e a exclusão continuam disponíveis nas telas de gestão. Recursos agrícolas avançados permanecem no código, mas foram retirados da navegação principal para simplificar a experiência.

> **Projeto acadêmico:** as janelas de colheita são referências preliminares. O sistema não garante produtividade, risco climático futuro ou resultado econômico.

![Python](https://img.shields.io/badge/Python-Backend-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-1B5E20?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Banco_de_Dados-4479A1?logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-Em_desenvolvimento-F5A623)

**Dashboard • Propriedades e mapas • Minha Safra • Clima • PDF • Assistente IA**

</div>

---

## Sobre o projeto

Pequenos e médios produtores rurais precisam reunir informações sobre propriedades, áreas, plantio, colheita e condições meteorológicas para tomar decisões mais bem informadas. O **AgroRisk** é uma aplicação web acadêmica que organiza esse acompanhamento em um único sistema.

A plataforma utiliza **Flask + SQLAlchemy + MySQL**, mapas **Leaflet/OpenStreetMap** com busca **Nominatim**, previsão de tempo pela **OpenWeather**, cálculo de **janelas preliminares de colheita**, geração de **PDF com jsPDF** e um **Assistente IA integrado ao Gemini** no servidor.

A interface foi reorganizada para evitar páginas duplicadas. **Minha Safra** concentra o cadastro, a seleção, o resumo, a edição e a exclusão. **Relatórios** apresenta informações complementares e a exportação de documentos. **Propriedades** leva à listagem de fazendas, e não diretamente ao cadastro.

> **Versão de referência:** pacote final do AgroRisk com as imagens do `index.html` atualizadas, em 07/11/2026. Os arquivos e endpoints descritos abaixo foram conferidos no código dessa versão. O funcionamento com MySQL, OpenWeather e Gemini reais ainda exige testes no ambiente do grupo; a documentação não comprova, sozinha, os critérios da rubrica.

### Navegação

- [Funcionalidades relevantes](#28-funcionalidades-relevantes)
- [Destaques do projeto](#destaques-do-projeto)
- [Navegação do sistema](#navegação-do-sistema)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Arquitetura utilizada](#arquitetura-utilizada)
- [Como executar](#como-executar-o-backend)
- [Rotas da API](#rotas-da-api)
- [Banco de dados e segurança](#banco-de-dados)
- [Testes e critérios da apresentação](#conferência-para-a-rubrica)
- [Status do projeto](#status-atual-do-projeto)

## 28 funcionalidades relevantes

A tabela mantém as **24 capacidades da documentação original**, com o comportamento atualizado, e acrescenta **4 recursos posteriores** efetivamente representados no código. Esta é uma **lista de capacidades**, não 28 fluxos independentes que garantem nota. O CRUD de cada domínio conta como uma área de gestão, não como quatro inovações.

### 1. Conta e acesso

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **01** | **Cadastro de usuários** | Criação de conta no MySQL, com senha tratada pelo backend. |
| **02** | **Login autenticado** | Validação de credenciais e token assinado e temporário para as rotas de dados. |
| **03** | **Gerenciamento do perfil** | Consulta e edição das informações da própria conta. |

### 2. Dashboard

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **04** | **Dashboard com indicadores gerais** | Totais de propriedades e safras, área registrada e resumos gerenciais. |

### 3. Gestão territorial e mapas

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **05** | **Gestão de propriedades rurais** | Cadastro, consulta, atualização, listagem e exclusão de propriedades da conta. |
| **06** | **Busca de cidade ou endereço no mapa** | Pesquisa Nominatim/OpenStreetMap para centralizar o mapa. |
| **07** | **Demarcação interativa de terrenos** | Desenho e edição de polígonos e retângulos no Leaflet. |
| **08** | **Cálculo de área e perímetro** | Valores aproximados em hectares e metros a partir do contorno. |
| **09** | **Armazenamento dos limites da propriedade** | Persistência de GeoJSON e coordenadas vinculadas à fazenda. |
| **10** | **Mapa da propriedade no monitoramento** | Visualização do contorno ou do ponto de referência da propriedade. |

### 4. Safras e planejamento agrícola

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **11** | **Gestão de safras na página Minha Safra** | Cadastro, consulta, edição e exclusão com confirmação, vinculados à propriedade. |
| **12** | **Validação da área plantada** | Confere limites do cadastro, inclusive a área disponível da propriedade. |
| **13** | **Seleção de safras por propriedade** | Lista apenas as safras relacionadas à propriedade escolhida. |
| **14** | **Estimativa de janela de colheita** | Intervalos preliminares para soja, milho e café a partir da data de plantio. |
| **15** | **Acompanhamento da situação da safra** | Separa calendário estimado e conclusão confirmada. |
| **16** | **Indicadores de acompanhamento** | Informações de área, cultura e status exibidas conforme os registros. |
| **17** | **Ver minhas safras** | Abre a lista das safras cadastradas, quando existe mais de uma. |
| **18** | **Confirmação de colheita concluída** | Atualiza a safra para **Finalizada**, após confirmação do produtor. |

### 5. Clima e alertas informativos

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **19** | **Clima atual da propriedade** | Consulta temperatura, umidade, vento e condições atuais pela OpenWeather. |
| **20** | **Previsão de curto prazo** | Exibe a previsão dos próximos dias em cartões de monitoramento. |
| **21** | **Indicador VPD** | Cálculo informativo do déficit de pressão de vapor. |
| **22** | **Avisos demonstrativos de calor e chuva** | Sinalizações por limiares ilustrativos, sem equivaler a laudo agronômico. |

### 6. Análises e documentos

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **23** | **Informações complementares da safra** | Clima consultado, custos/observações informados e etapas de referência. |
| **24** | **Geração e download de relatório em PDF** | Documento produzido no navegador com jsPDF, com dados e interpretação limitada ao que foi consultado. |

### 7. Assistência e ferramentas complementares

| Nº | Funcionalidade | O que entrega ao usuário |
|:--:|---|---|
| **25** | **Perguntas livres ao Assistente IA (Gemini)** | Conversa agrícola em linguagem natural, com chave mantida no Flask. |
| **26** | **Contexto de propriedade, safra e clima autorizado** | Envia dados selecionados ao Gemini somente após consentimento explícito. |
| **27** | **Calculadora de capacidade teórica de plantio** | Estima quantidade geométrica a partir de área útil e espaçamentos, sem prescrição técnica. |
| **28** | **Etapas da cultura e parâmetros agrícolas opcionais** | Referências de acompanhamento; o backend avançado pode armazenar observações e calcular cenários aritméticos se houver parâmetros informados. |

> **O que não foi contabilizado separadamente:** links, abas, cliques, botões, limpeza de formulários, animações e outras ações auxiliares. O serviço avançado é **opcional e não visível no menu principal**, para manter a interface simples.

> **Importante para o TCC:** a rubrica verifica **fluxos demonstrados e arquitetura**, não a quantidade desta lista. A equipe precisa comprovar os casos de uso reais percorrendo as camadas e o banco.

## Destaques do projeto

### Localize e demarque a fazenda no mapa

Em `cadastro_propriedade.html`, é possível pesquisar localizações, desenhar o terreno com Leaflet e estimar hectares e perímetro. O GeoJSON e as coordenadas passam pelo backend e ficam associados à propriedade.

**Arquivos principais:** `backend/static/js/cadastroPropriedade.js`, `backend/templates/cadastro_propriedade.html`.

### Gerencie tudo em Minha Safra

A antiga listagem **Safras** foi incorporada à página **Minha Safra** (`orientador.html`). O produtor pode criar uma safra, selecionar a propriedade, consultar sua **janela estimada de colheita**, editar ou excluir com confirmação. O botão **Ver minhas safras** exibe a lista quando há mais de um registro.

**Arquivos principais:** `backend/templates/orientador.html`, `backend/static/js/orientador-limpo.js`, `backend/static/js/analise-simples.js` e `backend/templates/cadastro_safras.html`.

### Monitore propriedades e o clima

A tela `monitoramento.html` mostra dados da propriedade, mapa e **cartões de previsão meteorológica**. O gráfico duplicado de temperatura/chuva e a antiga lista repetida de safras foram retirados da interface, mas a consulta ao serviço meteorológico foi preservada. **Não existe série histórica própria de clima gravada no MySQL.**

**Arquivos principais:** `backend/static/js/monitoramento.js`, `backend/services/clima_service.py`.

### Planeje a janela de colheita

O estimador calcula uma janela preliminar baseada em **cultura e data de plantio**, sem inferir maturação real ou prever clima de anos futuros.

| Cultura | Regra preliminar usada no protótipo |
|---|---|
| Soja | 100 a 140 dias após o plantio |
| Milho | 110 a 150 dias após o plantio |
| Café | 3 a 4 anos para a primeira colheita de uma lavoura nova |

**Arquivo principal:** `backend/services/estimar_colheita_service.py`.

### Gere o relatório em PDF

A página **Relatórios** seleciona propriedade e safra, apresenta informações complementares e permite **Baixar PDF**. O documento pode incluir identificação, plantio, janela de colheita, clima consultado, observações e interpretações informativas; parâmetros avançados só aparecem se disponíveis. A exportação é feita com **jsPDF** no navegador.

**Arquivos principais:** `backend/templates/relatorios.html`, `backend/static/js/relatorios.js`.

```javascript
// Trecho representativo da integração do botão de exportação.
function configurarBotaoPDF(safra) {
    const botao = document.getElementById("btnGerarPDF");
    if (!botao) return;
    botao.onclick = function () {
        gerarPDF(safra);
    };
}
```

> O PDF não garante produtividade nem retorno econômico. O clima exibido é atual ou previsto para curto prazo e não descreve automaticamente toda a safra.

### Converse com o Assistente IA

A página `assistente.html` permite perguntas abertas ao Gemini. O usuário pode selecionar a propriedade e a safra, habilitar previsão climática e **autorizar o envio**. O backend constrói o contexto autenticado e chama a API externa; a chave privada não é exposta em JavaScript. O histórico da conversa não é salvo em tabela do AgroRisk.

**Arquivos principais:** `backend/templates/assistente.html`, `backend/controllers/orientador_controller.py`, `backend/services/orientador_ia_service.py`.

### Calculadoras e análise técnica opcional

`ferramentas.html` oferece uma calculadora geométrica de plantio e outra consulta da janela de colheita. Existe ainda uma API de **análise avançada** com parâmetros da safra em tabela separada; sua interface antiga foi preservada apenas como backup, fora da navegação principal.

**Arquivos principais:** `backend/templates/ferramentas.html`, `backend/services/analise_avancada_service.py`, `backend/models/safra_parametros.py`.

### Navegação do sistema

O **mesmo menu lateral** é compartilhado pelas principais páginas internas, na seguinte ordem:

| Menu | Página / finalidade |
|---|---|
| **Dashboard** | `dashboard.html` — indicadores gerais e entrada após login |
| **Propriedades** | `propriedades.html` — lista de fazendas, com acesso a cadastro/edição e monitoramento |
| **Minha Safra** | `orientador.html` — resumo, estimativa, nova safra, edição e exclusão |
| **Relatórios** | `relatorios.html` — informações complementares e geração de PDF |
| **Assistente IA** | `assistente.html` — perguntas livres ao Gemini |
| **Perfil** | `perfil.html` — dados da conta, último item do menu |
| **Sair** | Volta à tela de autenticação; a saída deve encerrar o acesso local |

As telas `cadastro_propriedade.html`, `cadastro_safras.html`, `monitoramento.html` e `ferramentas.html` são acessadas pelos fluxos existentes, sem criar itens duplicados no menu. A URL legada `safras.html` **redireciona** para `orientador.html`.

### Imagens da página inicial

O `index.html` foi atualizado para utilizar imagens com tema agrícola e prévias coerentes com o AgroRisk. São **imagens de apresentação**, não comprovação de medições ou funcionalidades extras. O **Dashboard interno original** não foi substituído por uma tela fictícia.

**Arquivos de imagem:** `backend/static/img/dashboard-preview.png`, `backend/static/img/dashboard-real.png`, `backend/static/img/dashboard.png` e `backend/static/img/agricultura.jpg`.

## Estrutura do projeto

```text
AgroRisk/
├── README.md
├── .gitignore
├── LEIA-ME-*.md                  # Guias e histórico de alterações
├── docs/
│   ├── diagrama-classes.md
│   ├── REVISAO_RUBRICA_ETAPA_FINAL.md
│   └── backup_interface/       # Versões anteriores da interface
└── backend/
    ├── app.py                   # App factory, rotas e inicialização
    ├── config.py
    ├── requirements.txt
    ├── .env.example             # Modelo sem credenciais reais
    ├── controllers/
    │   ├── usuario_controller.py
    │   ├── propriedade_controller.py
    │   ├── safra_controller.py
    │   ├── clima_controller.py
    │   ├── orientador_controller.py
    │   └── analise_avancada_controller.py
    ├── models/
    │   ├── database.py
    │   ├── usuario.py
    │   ├── propriedade.py
    │   ├── safra.py
    │   └── safra_parametros.py
    ├── repositories/
    │   ├── usuario_repository.py
    │   ├── propriedade_repository.py
    │   ├── safra_repository.py
    │   └── analise_avancada_repository.py
    ├── services/
    │   ├── criar_*.py / atualizar_*.py / deletar_*.py
    │   ├── buscar_*.py / listar_*.py
    │   ├── estimar_colheita_service.py
    │   ├── clima_service.py
    │   ├── orientador_ia_service.py
    │   └── analise_avancada_service.py
    ├── security/
    │   └── auth.py
    ├── database/
    │   └── create_database.sql
    ├── templates/
    │   ├── _sidebar.html        # Menu lateral unificado
    │   ├── index.html           # Página inicial pública
    │   ├── login.html / cadastro.html
    │   ├── dashboard.html / perfil.html
    │   ├── propriedades.html / cadastro_propriedade.html
    │   ├── orientador.html      # Minha Safra unificada
    │   ├── cadastro_safras.html
    │   ├── monitoramento.html
    │   ├── relatorios.html
    │   ├── assistente.html      # Chat Gemini
    │   ├── ferramentas.html     # Calculadoras
    │   └── safras.html         # Rota legada redirecionada
    ├── static/
    │   ├── css/
    │   │   ├── style.css / index.css
    │   │   ├── sidebar-unificada.css
    │   │   ├── minha-safra-unificada.css
    │   │   └── outros CSS de páginas
    │   ├── js/
    │   │   ├── api.js
    │   │   ├── dashboard.js / propriedades.js
    │   │   ├── cadastroPropriedade.js / cadastroSafra.js
    │   │   ├── orientador-limpo.js / analise-simples.js
    │   │   ├── orientador.js / analiseAvancada.js
    │   │   ├── monitoramento.js / relatorios.js
    │   │   ├── indicadoresSafra.js / linhaTempoAgricola.js
    │   │   └── outros scripts de interface
    │   └── img/
    │       ├── dashboard-preview.png / dashboard-real.png
    │       ├── dashboard.png
    │       └── agricultura.jpg
    └── tests/
        ├── test_paginas_flask.py
        ├── test_protecao_contas.py
        ├── test_clima_service.py
        ├── test_orientador_ia.py
        └── test_analise_avancada.py
```

**Execução atual:** HTML e JavaScript são servidos pelo **Flask** a partir de `templates/` e `static/`. Não é necessário usar o Live Server. A aplicação web e a API compartilham a **mesma origem**; essa informação é relevante para a rubrica de cliente-servidor.

## Arquitetura utilizada

```text
Navegador
  HTML + CSS + JavaScript (templates/static)
                  |
                  | HTTP / JSON + Bearer token
                  v
              API Flask
                  |
             Controllers
                  |
               Services  ----------> OpenWeather / Gemini (APIs externas)
                  |
          Models / Repositories
                  |
                MySQL
```

Cada camada tem uma responsabilidade:

- **Frontend:** apresenta os formulários e resultados, guarda temporariamente o token do login e envia HTTP via `static/js/api.js`.
- **Controller:** recebe as rotas HTTP, interpreta parâmetros, obtém a identidade autenticada e devolve JSON.
- **Service:** valida regras de negócio, calcula janelas de colheita e coordena os fluxos.
- **Model:** representa tabelas e relacionamentos via SQLAlchemy.
- **Repository:** concentra consultas específicas e o acesso aos parâmetros opcionais da safra.
- **Banco:** persiste usuários, propriedades, safras e a tabela opcional `safra_parametros`.
- **Serviços externos:** o Flask consulta OpenWeather e Gemini; suas chaves não devem ir ao frontend.

> **Pendência arquitetural real:** as rotas de busca por localização e por cultura ainda executam SQLAlchemy diretamente em alguns **Controllers**, embora existam Services/Repositories alternativos. Para pontuar integralmente na rubrica é necessário demonstrar o caminho efetivo das requisições e refatorar onde exigido.

> **Cliente-servidor:** existem requisições HTTP entre JavaScript e API, mas as páginas e a API são hospedadas pelo **mesmo processo Flask** na versão atual. Caso a rubrica exija servidores independentes, isso ainda precisa ser implementado e validado.

## Integração do Frontend com a API

A comunicação com o backend é centralizada em `backend/static/js/api.js`. As páginas usam a mesma origem de onde foram servidas pelo Flask:

```javascript
const API_URL = window.location.origin;
```

Na execução local padrão:

```text
http://127.0.0.1:5000
```

O frontend utiliza **GET, POST, PUT e DELETE** para os cadastros e consultas. Nas rotas protegidas, envia `Authorization: Bearer <token>`; o backend verifica o token e o acesso à conta. O navegador **não substitui o MySQL** como repositório central de propriedades e safras.

### Funções de Safras no frontend

```javascript
listarSafras();
listarSafrasDaPropriedade(propriedadeId);
buscarSafra(id);
cadastrarSafra(dados);
atualizarSafra(id, dados);
excluirSafra(id);
estimarColheita(cultura, dataPlantio);
```

A tela Minha Safra reutiliza essas operações. A estimativa de colheita e a análise agrícola avançada são fluxos diferentes: **o calendário básico é preliminar**, enquanto parâmetros técnicos opcionais só podem alterar o cálculo quando informados.

## Tela Minha Safra unificada

A tela principal de acompanhamento de safras passou a ser:

```text
backend/templates/orientador.html
```

Ela permite escolher uma **propriedade** e uma **safra**, visualizar o resumo e a **janela estimada de colheita**, abrir o cadastro com **Nova Safra**, editar o registro e excluir com confirmação. Se houver mais de uma safra da propriedade, o produtor pode usar **Ver minhas safras** para abrir a listagem no mesmo ambiente.

A página antiga `safras.html` não é mais uma entrada do menu; o Flask **redireciona** a URL para `orientador.html` por compatibilidade. O resumo de Minha Safra é propositalmente curto, para não duplicar os documentos detalhados.

## JavaScript da página Minha Safra

Arquivos principais:

```text
backend/static/js/orientador-limpo.js
backend/static/js/analise-simples.js
backend/static/js/indicadoresSafra.js
backend/static/js/api.js
```

O frontend consulta propriedades e safras autenticadas, atualiza os seletores, apresenta a estimativa de colheita e controla a lista recolhida. A edição mantém o formulário existente em `cadastro_safras.html`. A exclusão solicita confirmação e somente atualiza a lista após a API confirmar a remoção; não é uma exclusão apenas em `localStorage`.

O script `safras.js` permanece no repositório para compatibilidade de versões anteriores, mas **não define mais a navegação principal**.

## Status das Safras

O AgroRisk separa **janela calculada** de **colheita efetivamente confirmada**:

- **Planejamento / em desenvolvimento:** o ciclo ainda está sendo acompanhado conforme o cadastro.
- **Na janela prevista:** a data atual está no período estimado, mas não comprova que houve colheita.
- **Janela encerrada:** a referência terminou sem confirmação.
- **Finalizada:** o produtor confirmou a conclusão; o status foi salvo no MySQL.

**Uma safra não se torna Finalizada automaticamente ao passar da data estimada.**

## Culturas das Safras

As culturas utilizadas pelo estimador atual são:

- **Soja:** janela preliminar de 100 a 140 dias após o plantio.
- **Milho:** janela preliminar de 110 a 150 dias após o plantio.
- **Café:** referência inicial de 3 a 4 anos após o plantio para uma lavoura nova.

Essas regras são **parâmetros do protótipo**, e não estimativas estatísticas validadas com dados históricos. As durações variam com a variedade, a região e as condições de manejo. Para um cafezal já produtivo, somente a data de plantio não permite prever a próxima colheita; eventos como florada e maturação precisam ser considerados.

**Exemplo para a mesma data de plantio, 22/10/2026:**

| Cultura | Início estimado | Fim estimado |
| --- | --- | --- |
| Soja | 30/01/2027 | 11/03/2027 |
| Milho | 09/02/2027 | 21/03/2027 |
| Café | 22/10/2029 | 22/10/2030 |

A API também retorna uma **data central de referência**, usada no cadastro, e apresenta a janela na interface.

## Cadastro de Safras

O botão **Nova Safra** abre o formulário já existente:

```text
backend/templates/cadastro_safras.html
```

Os dados incluem `propriedade_id`, `nome`, `cultura`, `data_plantio`, `area_plantada`, `custo_total` (opcional) e `observacoes`. A API valida a propriedade e a área cadastrada; o estimador fornece uma data de referência e uma janela de colheita. Após salvar, o fluxo retorna à página **Minha Safra**, com o registro selecionado sempre que possível.

## Monitoramento das propriedades e safras

O monitoramento (`monitoramento.html`) utiliza as coordenadas da propriedade como referência para a consulta à OpenWeather, além de apresentar mapa e indicadores do cadastro. A **lista de safras repetida** e o **gráfico de comparação climática** foram retirados dessa tela; a previsão de curto prazo permanece nos cartões. Não há medição automática de cada talhão nem histórico meteorológico próprio por safra.

## Edição das Safras

Em **Minha Safra**, o botão **Editar safra** abre o cadastro existente com o ID do registro:

```text
/cadastro_safras.html?id=ID_DA_SAFRA
```

O sistema consulta os dados do registro, permite alterá-los e salva as mudanças pela API, respeitando o vínculo com a propriedade e a conta autenticada.

## Exclusão das Safras

O botão **Excluir safra** solicita uma confirmação antes de disparar `DELETE /safras/<id>`. O backend verifica a identidade e a propriedade da conta. **A lista da Minha Safra só deve ser atualizada após confirmação de sucesso da API**. Faça testes de exclusão em dados de demonstração, nunca no banco real sem backup.

## Informações de Plantio e Colheita

O sistema armazena a data de plantio e uma data de colheita de referência. Para planejamento, o estimador apresenta também **uma janela de datas**, evitando afirmar que uma colheita acontecerá em um único dia exato.

A meteorologia atual e a previsão de curto prazo aparecem no monitoramento e na análise de safra, mas **não determinam automaticamente a janela de colheita para anos futuros**. A adaptação da estimativa ao clima exigiria dados históricos, cultivar, estágio fenológico e calibração agronômica.

## Integração com a API de Clima

A OpenWeather é consultada no backend com `OPENWEATHER_API_KEY` definida em `backend/.env`:

```text
GET /api/clima?lat=...&lon=...
GET /api/clima/previsao?lat=...&lon=...
```

O `backend/services/clima_service.py` encapsula essas requisições. A interface pode mostrar temperatura, umidade, vento, condições atuais e chuva prevista. Os dados são consultados em tempo real **quando a chave, o serviço e a internet estão disponíveis**.

> O sistema não tem uma série histórica meteorológica própria no MySQL. A previsão de curto prazo **não determina** a colheita para anos futuros.

## Minha Safra, Relatórios e Assistente IA

As responsabilidades agora são separadas:

- **Minha Safra (`orientador.html`):** resumo da safra escolhida, cultura, área, situação, datas e **janela estimada de colheita**; também serve para criar, editar, listar e excluir safras.
- **Relatórios (`relatorios.html`):** clima consultado, informações complementares, etapas de referência e **Baixar PDF**; não repete o painel de resumo como outra tela de gestão.
- **Assistente IA (`assistente.html`):** dúvidas livres sobre agricultura, com contexto opcional autorizado pelo usuário, e respostas geradas pelo Gemini.
- **Calculadoras (`ferramentas.html`):** simulação teórica de plantio e consulta de janela, fora do menu principal.

O PDF exportado por `relatorios.js` apresenta apenas informações disponíveis e conclusões limitadas aos dados informados. As regras demonstrativas de atenção climática não equivalem a diagnóstico agronômico.

### Funcionamento do Gemini

1. O usuário faz login, escreve sua pergunta e marca a autorização de envio.
2. Opcionalmente seleciona propriedade/safra e permite incluir previsão do tempo.
3. `POST /api/orientador/perguntar` valida identidade, contexto e consentimento.
4. `OrientadorIAService` monta a mensagem e consulta o Gemini por HTTP no servidor.
5. O assistente devolve o texto ao navegador. O conteúdo pode conter erros, e o histórico não é persistido em uma tabela.

A API aplica um limite simples de **8 perguntas por usuário a cada 10 minutos**, armazenado em memória do processo (não é um limitador distribuído de produção).

### Análise agrícola avançada opcional

O backend mantém uma tabela `safra_parametros` para registrar cultivar, idade da lavoura, altitude, irrigação, marcos observados e intervalos técnicos informados. Quando houver números preenchidos, pode calcular **cenários aritméticos** de produção e uma janela refinada; sem eles, preserva-se a janela preliminar. Esses cenários **não são previsões garantidas**.

Essa API permanece disponível para integração/testes, mas sua interface técnica antiga está arquivada em `docs/backup_interface/` e **não está exposta como opção principal em Minha Safra**.

## Repositories utilizados

Os Repositories existentes encapsulam consultas específicas ou persistência de parâmetros avançados. Nem todas as rotas de busca utilizam os Repositories no fluxo atual; essa é uma pendência que precisa ser demonstrada corretamente à banca.

### UsuarioRepository

Arquivo: `backend/repositories/usuario_repository.py`.

A busca por nome existe internamente, com referência à Procedure `sp_buscar_usuario_nome`, mas a busca global por usuários está bloqueada na API por privacidade; **não deve ser apresentada como consulta pública concluída**.

### PropriedadeRepository

Arquivo: `backend/repositories/propriedade_repository.py`.

Possui uma implementação de `buscar_por_localizacao`. A rota autenticada atual usa filtro SQLAlchemy diretamente no Controller e deve ser refatorada para seguir o fluxo de camadas exigido na disciplina.

### SafraRepository

Arquivo: `backend/repositories/safra_repository.py`.

Possui `buscar_por_cultura`, incluindo referência à Procedure `sp_buscar_safras_cultura`; a rota da API atualmente utiliza SQLAlchemy no Controller para aplicar o filtro da conta.

### AnaliseAvancadaRepository

Arquivo: `backend/repositories/analise_avancada_repository.py`.

Consulta a safra vinculada ao usuário e salva os parâmetros técnicos opcionais na tabela `safra_parametros`, sob a coordenação do Service.

> **Segurança:** mover buscas para Repositories não pode remover o isolamento entre contas; consultas globais ou Procedures que exponham informações de outros usuários não são aceitáveis.

## Stored Procedures referenciadas (não instaladas por padrão)

O projeto conserva referências às Procedures abaixo em alguns Repositories. O `backend/database/create_database.sql` **não instala essas Procedures**. É necessário verificar seu esquema antes de afirmar que uma chamada `CALL` foi realmente executada no MySQL.

### Usuários

```text
sp_buscar_usuario_nome
```

Pesquisa parcial por nome. O endpoint público de busca global de usuários está bloqueado por segurança.

### Propriedades

```text
sp_buscar_propriedades_localizacao
```

Consulta especial por localização, cuja integração arquitetural e autorização precisam ser conferidas.

### Safras

```text
sp_buscar_safras_cultura
```

Consulta especial por cultura, com a mesma necessidade de validar isolamento entre contas.

> **Ponto da rubrica:** não basta o Repository ou a Procedure existir em código; a equipe precisa demonstrar uma **consulta SQL real em Repository** quando essa evidência for exigida.

## Rotas da API

### Usuários

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/usuarios` | Cadastrar usuário |
| `POST` | `/login` | Autenticar e obter token |
| `GET` | `/usuarios` | Consultar informações permitidas da própria conta |
| `GET` | `/usuarios/<id>` | Consultar perfil autorizado |
| `PUT` | `/usuarios/<id>` | Atualizar perfil autorizado |
| `DELETE` | `/usuarios/<id>` | Excluir a própria conta (rota existente) |
| `GET` | `/usuarios/buscar?nome=...` | Pesquisa global bloqueada (`403`) |

### Propriedades

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/propriedades` | Listar propriedades da conta |
| `POST` | `/propriedades` | Cadastrar propriedade |
| `GET` | `/propriedades/<id>` | Consultar propriedade própria |
| `PUT` | `/propriedades/<id>` | Editar propriedade |
| `DELETE` | `/propriedades/<id>` | Excluir propriedade |
| `GET` | `/propriedades/buscar?localizacao=...` | Buscar propriedades da conta por localização |

### Safras

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/safras` | Listar safras da conta; admite filtro por propriedade |
| `POST` | `/safras` | Cadastrar safra |
| `GET` | `/safras/<id>` | Consultar safra própria |
| `PUT` | `/safras/<id>` | Atualizar safra ou registrar finalização |
| `DELETE` | `/safras/<id>` | Excluir safra |
| `GET` | `/safras/buscar?cultura=...` | Buscar safras da conta por cultura |
| `GET` | `/safras/estimar-colheita?cultura=...&data_plantio=AAAA-MM-DD` | Calcular estimativa preliminar |

### Clima

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/clima?lat=...&lon=...` | Condição meteorológica atual |
| `GET` | `/api/clima/previsao?lat=...&lon=...` | Previsão de curto prazo |

### Assistente IA e análise técnica

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/orientador/status` | Verificar configuração do Gemini (autenticado) |
| `POST` | `/api/orientador/perguntar` | Enviar pergunta com consentimento e contexto opcional |
| `GET` | `/api/analise-avancada/safras/<id>` | Consultar parâmetros e cálculos técnicos opcionais |
| `PUT` | `/api/analise-avancada/safras/<id>` | Validar e salvar parâmetros técnicos da safra |

### Páginas e diagnóstico

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api` | Informações básicas sobre a API |
| `GET` | `/` | Abrir a página inicial `index.html` |
| `GET` | `/dashboard.html` | Dashboard original do sistema |
| `GET` | `/propriedades.html` | Minhas Propriedades |
| `GET` | `/orientador.html` | Minha Safra unificada |
| `GET` | `/safras.html` | Redirecionar para Minha Safra |
| `GET` | `/relatorios.html` | Central de relatórios e PDF |
| `GET` | `/assistente.html` | Assistente IA |

As rotas de dados exigem token, com exceções explícitas para cadastro inicial e estimador público. A presença de uma rota não prova sua execução completa no banco de dados.

## Exemplo de JSON para cadastro de usuário

```json
{
  "nome": "Exemplo de Usuário",
  "email": "exemplo@dominio.com",
  "senha": "SENHA_DE_TESTE_FORTE"
}
```

A senha é processada no backend e armazenada como **hash**, não como texto simples.

## Exemplo de JSON para cadastro de propriedade

```json
{
  "nome": "Propriedade Demonstração",
  "cidade": "Vespasiano",
  "estado": "MG",
  "area": 10.5,
  "perimetro": 1200,
  "latitude": -19.6914,
  "longitude": -43.9264,
  "observacao": "Área de exemplo para o TCC"
}
```

O backend identifica o usuário autenticado pelo token; não basta enviar livremente um `usuario_id` no JSON.

## Exemplo de JSON para cadastro de safra

```json
{
  "propriedade_id": 1,
  "nome": "Safra Soja 2026/2027",
  "cultura": "Soja",
  "ano_safra": "2026",
  "data_plantio": "2026-10-22",
  "data_colheita": "2027-02-19",
  "area_plantada": 2.0,
  "observacoes": "Safra de demonstração"
}
```

A API valida a propriedade vinculada e os dados enviados. A data usada no exemplo é apenas a referência central da estimativa para essa cultura/data de plantio.

## Como executar o backend

**Requisitos:** Python com `pip`, MySQL/MariaDB (por exemplo, pelo XAMPP), internet para integrações externas e um navegador. Execute os comandos abaixo a partir da pasta do projeto.

No Windows, inicie primeiro o serviço **MySQL** no XAMPP. Não é necessário iniciar o Apache ou abrir o Live Server.

Entre no backend:

```powershell
cd backend
```

Crie e ative o ambiente virtual (recomendado):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Copie `backend/.env.example` para `backend/.env` e ajuste os dados localmente. **Nunca publique a chave real, a senha ou seu `.env` no GitHub.**

```dotenv
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@127.0.0.1:3306/agrorisk
OPENWEATHER_API_KEY=COLE_SUA_CHAVE_OPENWEATHER
SECRET_KEY=COLE_UMA_CHAVE_SECRETA_FORTE
FLASK_DEBUG=False

# Opcionais: necessários para o Assistente IA
GEMINI_API_KEY=COLE_SUA_CHAVE_GEMINI
GEMINI_MODEL=MODELO_DISPONIVEL_NA_SUA_CHAVE
```

**Atenção:** o nome `MODELO_DISPONIVEL_NA_SUA_CHAVE` é um **marcador de substituição**, não um modelo válido. Utilize um identificador de modelo Gemini realmente disponível à sua chave. A API pode retornar erro se o nome configurado não existir ou não estiver autorizado.

Para gerar uma `SECRET_KEY` forte:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Se estiver usando MySQL local do XAMPP com `root` sem senha **somente em desenvolvimento**, a URL poderá ser `mysql+pymysql://root:@127.0.0.1:3306/agrorisk`. Em ambiente público, configure um usuário exclusivo e senha forte.

Execute o Flask:

```powershell
python app.py
```

Abra o endereço:

```text
http://127.0.0.1:5000
```

Após autenticar, o Dashboard fica em `http://127.0.0.1:5000/dashboard.html` e a gestão de safras em `http://127.0.0.1:5000/orientador.html`.

**Linux/macOS:** a ativação do ambiente virtual geralmente usa `source venv/bin/activate`.

> Se o banco for antigo, faça **backup** antes de qualquer atualização de tabelas. O `db.create_all()` cria tabelas faltantes, mas não migra automaticamente colunas existentes.

## Banco de dados

O AgroRisk usa **MySQL** (ou MariaDB compatível), normalmente com a base local `agrorisk`.

Relacionamentos principais:

```text
Usuario (1) ─── (N) Propriedade (1) ─── (N) Safra
                                                    │
                                                    └── (0..1) SafraParametros
```

- `usuarios`: informações das contas e credenciais em hash.
- `propriedades`: fazendas, geolocalização, áreas e vínculo com usuários.
- `safras`: cultura, área plantada, datas, custos, observações, status e propriedade.
- `safra_parametros`: dados agrícolas **opcionais** de uma safra, em tabela separada.

O arquivo `backend/database/create_database.sql` serve como referência de instalação. **Não execute scripts antigos destrutivos em uma base com dados reais.**

O Flask executa `db.create_all()` durante a inicialização. Isso cria tabelas ausentes, mas **não altera automaticamente a estrutura das tabelas anteriores**. Faça migrações controladas quando necessário.

**Atenção ao uso em mais de um computador:** um MySQL local não sincroniza automaticamente com outro equipamento. Para acesso centralizado é preciso hospedar o servidor e o banco com autenticação, HTTPS e backups.

## Testes das funcionalidades avançadas

Dentro de `backend`, estão disponíveis scripts de testes:

```powershell
python tests/test_paginas_flask.py
python tests/test_protecao_contas.py
python tests/test_clima_service.py
python tests/test_orientador_ia.py
python tests/test_analise_avancada.py
```

Alguns testes utilizam **SQLite em memória, simulações de API e dados fictícios**. Eles ajudam a revisar o comportamento, mas **não substituem** testes manuais com MySQL, OpenWeather e Gemini reais.

### Busca de usuários por nome

```text
GET /usuarios/buscar?nome=Joao
```

**Status:** bloqueada por segurança (`403`); não demonstrar como funcionalidade concluída.

### Busca de propriedades por localização

```text
GET /propriedades/buscar?localizacao=Vespasiano
```

A rota atual restringe os resultados à conta, mas contém consulta SQLAlchemy no Controller e precisa de revisão arquitetural.

### Busca de safras por cultura

```text
GET /safras/buscar?cultura=Soja
```

A rota atual filtra os dados da conta, mas consulta SQLAlchemy diretamente no Controller.

### Testes do cadastro, edição e exclusão

Criar uma propriedade e uma safra de demonstração, editar os registros, atualizar o navegador, verificar a persistência e solicitar exclusão com confirmação. Testar ainda uma segunda conta para validar o isolamento dos dados.

### Testes das estimativas de colheita

Consultar Café, Soja e Milho com a mesma data de plantio e conferir os intervalos diferentes. Confirmar que uma safra **não é finalizada automaticamente**.

### Testes do Gemini

Usar a tela `assistente.html`, autorizar o envio e perguntar algo geral como "Quais cuidados básicos devo observar no plantio de café?". Testar também a resposta sem consentimento e com uma propriedade de outra conta: ambas devem ser recusadas.

### Testes do relatório PDF

Selecionar uma safra, consultar dados complementares, gerar o PDF e conferir identificação, área, datas, janela, clima disponível, metodologia e observações. Não incluir cenários inventados quando os parâmetros não foram informados.

## Tecnologias utilizadas

- **Python e Flask** — backend, rotas HTTP e servidor local da interface.
- **Flask-SQLAlchemy / SQLAlchemy / PyMySQL** — Models, transações e acesso ao banco.
- **MySQL / MariaDB** — persistência de usuários, propriedades, safras e parâmetros opcionais.
- **python-dotenv** — variáveis privadas de ambiente.
- **itsdangerous** — tokens assinados e temporários utilizados pela autenticação.
- **requests** — comunicação do servidor com APIs externas.
- **HTML, CSS e JavaScript** — frontend.
- **Bootstrap** e **Font Awesome** — componentes e ícones.
- **Leaflet, Leaflet Draw, OpenStreetMap e Nominatim** — mapas, polígonos e localização.
- **jsPDF** — geração e download de relatórios.
- **OpenWeather** — clima e previsão de curto prazo.
- **Google Gemini API** — perguntas livres e explicações com IA; chamada HTTP via backend, sem SDK específico obrigatório.

As bibliotecas e integrações externas exigem conexão e disponibilidade dos serviços; a versão acadêmica não deve ser anunciada como serviço de previsão agronômica validado.

## Diagrama de classes

O domínio principal possui `Usuario`, `Propriedade` e `Safra`, representados como Models SQLAlchemy. A versão atual inclui ainda `SafraParametros`, uma Model vinculada à safra para dados agrícolas opcionais.

```text
docs/diagrama-classes.md
```

Veja o [diagrama de classes](docs/diagrama-classes.md). **Atenção:** o desenho existente descreve principalmente as três entidades originais; é necessário revisá-lo para incluir `SafraParametros` e conferir os atributos/relacionamentos antes de apresentá-lo como diagrama completo da versão atual.

## Segurança do sistema

A implementação atual conta com:

- Senhas processadas com hash no backend, em vez de armazenamento em texto puro.
- Tokens assinados e temporários, configurados para **8 horas**.
- Rotas de dados protegidas e validação do acesso à conta nas operações principais.
- Chaves de banco, OpenWeather, Gemini e assinatura em `backend/.env` privado.
- Autorização explícita do envio das perguntas ao Gemini; verificação de acesso aos dados de contexto.
- Limite simples de requisições de IA no processo do Flask.
- Cabeçalhos HTTP básicos de proteção e `Cache-Control: no-store` para dados sensíveis.

**Ainda não é uma implantação pública pronta:** faltam HTTPS e servidor de produção, políticas de backup, proteção robusta contra abuso, revisão de permissões em todas as rotas, configuração segura do MySQL e testes completos de integração. O `.env` deve permanecer fora do GitHub. Se alguma chave foi exposta, **revogue-a e gere outra**.

## Conferência para a rubrica

A equipe deve demonstrar **funcionamento real**, além de apresentar o README. A revisão local identifica os seguintes pesos de referência na rubrica recebida:

| Critério | Pontos | O que conferir |
|---|---:|---|
| Quatro fluxos não CRUD | **4** | Demonstrar mapa, clima, janela de colheita e PDF/IA, conforme autorização da banca |
| Cliente-servidor | **4** | O frontend faz HTTP, mas ainda roda no **mesmo Flask da API** |
| Controller → Service → Model/Repository | **7** | Conferir a passagem real dos dados em cada fluxo |
| Persistência / ORM / consultas de Repository | **4** | SQLAlchemy, MySQL e consultas especiais executadas no Repository |
| Diagrama de classes | **3** | Atualizar conforme as quatro Models da versão atual |
| Fluxogramas de dados | **4** | Entrada e consulta percorrendo as camadas implementadas |
| Apresentação e README | **4** | Problema, público, casos de uso, arquitetura, tecnologias e evidências |

**Bônus possíveis:** IA como serviço, hospedagem e comprovação do consentimento, sujeitos aos requisitos específicos da atividade. Não se deve considerar bônus garantido apenas porque há uma tela ou integração escrita em código.

### Demonstração sugerida

| Etapa | Funcionalidade | O que mostrar |
|---|---|---|
| 1 | Login e Dashboard | Acesso autenticado e indicadores do painel original |
| 2 | Propriedades | Cadastro, desenho da área no mapa e persistência no MySQL |
| 3 | Minha Safra | Cadastro, resumo, estimativa de colheita, edição e exclusão com confirmação |
| 4 | Monitoramento | Localização da fazenda, dados meteorológicos atuais e previsão |
| 5 | Relatórios | Informações complementares e PDF gerado no navegador |
| 6 | Assistente IA | Pergunta ao Gemini com consentimento e dados opcionais |
| 7 | Arquitetura | Código de Controller, Service, Model/Repository e esquema do banco |

A rubrica mencionou **limite de 2 minutos para a demonstração em vídeo ou sistema hospedado**; confirme com o professor como esse limite se aplica à apresentação presencial. Prepare também um roteiro curto com **quatro fluxos não CRUD**, priorizando o que estiver realmente funcionando.

**Não exponha senhas, tokens, chaves de API, CPFs ou informações privadas reais.** Faça a demonstração com contas e registros de teste e com backup do banco.

## Status atual do projeto

O AgroRisk está em **fase de finalização acadêmica**, com interface e navegação reorganizadas. A versão atual inclui **Dashboard original**, cadastro de propriedades e áreas, **Minha Safra unificada**, consultas de clima e mapa, **Relatórios em PDF**, **Assistente Gemini** e calculadoras complementares.

Na última revisão de interface, o menu lateral foi padronizado e o `index.html` recebeu imagens agrícolas mais apropriadas. O monitoramento mantém a previsão meteorológica sem o gráfico duplicado; a antiga página de Safras foi unificada com Minha Safra.

### Pendências para a entrega final

- Validar os fluxos principais em **MySQL real**, com dados de teste e duas contas.
- Conferir a comunicação ao vivo com **OpenWeather** e **Gemini**, com chaves privadas válidas.
- Revisar a separação entre **frontend e API**, conforme a rubrica, caso sejam exigidos servidores distintos.
- Mover as consultas especiais ainda presentes nos Controllers para **Services/Repositories**, mantendo autorização.
- Atualizar o diagrama de classes e preparar os **fluxogramas** solicitados.
- Conferir a geração e abertura do PDF final, inclusive quando o clima estiver indisponível.
- Concluir os slides, a demonstração e a documentação do repositório.

**Projeto acadêmico:** estimativas e mensagens de IA são apoio informativo; não substituem assistência agronômica e não garantem colheita, rentabilidade ou condições meteorológicas futuras.

## Assistente AgroRisk com IA (Gemini)

O Assistente permite **perguntas livres**, com resposta gerada pelo Gemini por uma chamada HTTP feita no Flask. Pode utilizar contexto autenticado da propriedade e da safra, inclusive a análise técnica opcional e previsão de curto prazo, **somente quando o produtor autoriza o envio**.

Não há pesquisa web ao vivo integrada ao Gemini, e a IA pode cometer erros. Ela não deve ser utilizada para prescrever aplicações perigosas, prometer produtividade ou substituir um profissional habilitado.


