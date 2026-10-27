# AgroRisk

Pequenos e médios produtores rurais enfrentam dificuldades para centralizar e organizar informações sobre suas propriedades, safras e atividades agrícolas. Essa falta de organização pode prejudicar o acompanhamento das lavouras, o planejamento de plantio e colheita e a tomada de decisões.

O **AgroRisk** foi desenvolvido como projeto acadêmico de TCC para auxiliar na gestão agrícola. A plataforma permite cadastrar usuários, propriedades e safras, visualizar áreas em mapas, consultar dados meteorológicos reais e acompanhar **janelas estimadas de colheita**. O sistema também apresenta análises de safras, permite confirmar a conclusão de uma colheita e exportar informações em PDF.

> **Versão documentada:** AgroRisk para demonstração acadêmica em 23/10/2026, executado pelo Flask com páginas em `backend/templates/` e CSS, JavaScript e imagens em `backend/static/`. Os itens apresentados foram identificados na versão atual do código. A gravação do vídeo e os testes no computador da equipe devem confirmar cada fluxo de ponta a ponta.

## Estrutura do projeto

```text
AgroRisk/
├── README.md
├── .gitignore
├── docs/
│   └── diagrama-classes.md
│
└── backend/
    ├── app.py
    ├── config.py
    ├── requirements.txt
    ├── .env.example
    │
    ├── controllers/
    │   ├── usuario_controller.py
    │   ├── propriedade_controller.py
    │   ├── safra_controller.py
    │   └── clima_controller.py
    │
    ├── models/
    │   ├── database.py
    │   ├── usuario.py
    │   ├── propriedade.py
    │   └── safra.py
    │
    ├── repositories/
    │   ├── usuario_repository.py
    │   ├── propriedade_repository.py
    │   └── safra_repository.py
    │
    ├── services/
    │   ├── login_usuario_service.py
    │   ├── criar_usuario_service.py
    │   ├── atualizar_usuario_service.py
    │   ├── criar_propriedade_service.py
    │   ├── listar_propriedade_service.py
    │   ├── criar_safra_service.py
    │   ├── atualizar_safra_service.py
    │   ├── estimar_colheita_service.py
    │   ├── clima_service.py
    │   └── ...
    │
    ├── security/
    │   └── auth.py
    ├── database/
    │   └── create_database.sql
    ├── templates/
    │   ├── index.html
    │   ├── login.html
    │   ├── cadastro.html
    │   ├── dashboard.html
    │   ├── perfil.html
    │   ├── propriedades.html
    │   ├── cadastro_propriedade.html
    │   ├── monitoramento.html
    │   ├── safras.html
    │   ├── cadastro_safras.html
    │   └── relatorios.html
    │
    ├── static/
    │   ├── css/style.css
    │   ├── js/
    │   │   ├── api.js
    │   │   ├── login.js
    │   │   ├── propriedades.js
    │   │   ├── safras.js
    │   │   ├── cadastroSafra.js
    │   │   ├── monitoramento.js
    │   │   ├── relatorios.js
    │   │   └── ...
    │   └── img/
    │
    └── tests/
        ├── test_paginas_flask.py
        ├── test_protecao_contas.py
        └── test_clima_service.py
```

**Mudança importante:** nas primeiras versões, o HTML ficava em `frontend/` e era aberto com Live Server. Na versão atual, **o próprio Flask entrega as páginas**, e não é necessário iniciar o Live Server. Os caminhos antigos do frontend foram preservados conceitualmente, mas os arquivos agora estão em `templates` e `static`.

## Arquitetura utilizada

```text
Interface HTML/CSS/JavaScript (Flask: templates + static)
                         ↓
                     API Flask
                         ↓
                 Controller (classe)
                         ↓
                 Service (caso de uso)
                         ↓
              Model / Repository
                         ↓
                      MySQL
```

Cada camada possui uma responsabilidade específica:

- **Frontend:** recebe as ações dos usuários, valida os campos básicos, envia requisições e apresenta os resultados.
- **Controller:** interpreta requisições HTTP, identifica o usuário autenticado, aciona os Services e devolve respostas JSON.
- **Service:** aplica as validações e regras de negócio e coordena cada caso de uso.
- **Model:** representa as entidades e executa operações básicas de persistência com SQLAlchemy.
- **Repository:** deve concentrar consultas especiais e, quando utilizadas, chamadas a *Stored Procedures*.
- **Banco de dados:** armazena usuários, propriedades e safras no MySQL.

A integração com a **OpenWeather** está encapsulada no `ClimaService`, em vez de expor a chave da API no navegador.

> **Ponto de melhoria arquitetural:** na versão inspecionada, as rotas de busca de propriedades por localização e de safras por cultura ainda montam consultas SQLAlchemy diretamente nos Controllers. Os Repositories existem, mas essas rotas precisam ser refatoradas para atender integralmente às exigências da disciplina.

## Funcionalidades Implementadas

Esta seção mantém a organização do README original por **Usuários, Propriedades e Safras**, incluindo a enumeração dos casos de uso identificados para a entrega. A atividade da disciplina exige que uma funcionalidade esteja implementada de **ponta a ponta: Tela → API → Controller → Service → Model/Repository → Banco de Dados**. Por isso, a relação abaixo separa os **14 fluxos principais identificados** de outros recursos disponíveis que ainda precisam de adequação ou comprovação específica para entrarem na contagem de 20.

| Nº | Funcionalidade principal | Interface / operação |
| ---: | --- | --- |
| 1 | Cadastrar usuário | Cadastro → `POST /usuarios` |
| 2 | Realizar login | Login → `POST /login` |
| 3 | Consultar o próprio perfil | Perfil → `GET /usuarios/<id>` |
| 4 | Atualizar o próprio perfil | Perfil → `PUT /usuarios/<id>` |
| 5 | Cadastrar propriedade | Cadastro de propriedade → `POST /propriedades` |
| 6 | Listar propriedades da conta | Propriedades → `GET /propriedades` |
| 7 | Consultar propriedade por ID | Propriedade/monitoramento → `GET /propriedades/<id>` |
| 8 | Atualizar propriedade | Edição → `PUT /propriedades/<id>` |
| 9 | Excluir propriedade | Propriedades → `DELETE /propriedades/<id>` |
| 10 | Cadastrar safra | Cadastro de safra → `POST /safras` |
| 11 | Listar safras da conta | Safras → `GET /safras` |
| 12 | Consultar safra por ID | Edição/análise → `GET /safras/<id>` |
| 13 | Atualizar safra | Edição → `PUT /safras/<id>` |
| 14 | Excluir safra | Safras → `DELETE /safras/<id>` |

**Observação para a avaliação:** a presença de um fluxo no código não substitui a demonstração e os testes reais. **Não declaramos 20 funcionalidades completas sem validar os seis fluxos adicionais exigidos pelo professor.**

### Usuários

**CRUD de Usuários:**

- Cadastrar usuário pela tela de cadastro;
- Consultar os dados do próprio usuário na tela de perfil;
- Atualizar os dados da própria conta;
- Excluir usuário por meio da rota autenticada do backend (a existência de uma tela de exclusão deve ser conferida antes de incluí-la na contagem oficial);
- Listar informações da própria conta pela API, sem expor a lista de todas as contas existentes.

**Funcionalidades além do CRUD:**

- Realizar login com e-mail e senha;
- Armazenar senhas com hash;
- Receber token de autenticação temporário;
- Impedir acesso ao perfil de outra conta;
- Converter para hash senhas antigas após login válido, quando aplicável.

O sistema possui cadastro, login, consulta e atualização dos dados da própria conta. O backend também contém uma rota para exclusão de usuário e Services relacionados, mas essa operação só deve ser contada na atividade após conferir uma interface utilizável e demonstrar o fluxo completo.

O login utiliza senhas com **hash**, e contas antigas podem ter suas senhas convertidas para hash após autenticação bem-sucedida. As consultas protegidas exigem um **token de autenticação assinado**, associado à conta.

A busca global de usuários por nome, embora esteja representada em arquivos antigos de Repository e SQL, **não está disponível na API atual**: a rota foi bloqueada para evitar exposição indevida de dados pessoais. A listagem global de todas as contas também não é oferecida ao usuário comum.

### Propriedades

**CRUD de Propriedades:**

- Cadastrar uma propriedade;
- Listar as propriedades vinculadas à conta autenticada;
- Consultar uma propriedade pelo ID;
- Atualizar as informações de uma propriedade;
- Excluir uma propriedade, observando as regras de dependência com safras.

**Funcionalidades além do CRUD:**

- Delimitar áreas no mapa e armazenar localização, coordenadas e GeoJSON;
- Buscar propriedades por cidade, estado ou nome dentro da própria conta;
- Abrir o monitoramento de uma propriedade específica;
- Visualizar as safras vinculadas à propriedade.

As principais ações são:

- Cadastrar, listar, consultar, editar e excluir propriedades vinculadas à conta.
- Informar nome, cidade, estado, observações, área e perímetro.
- Marcar ou delimitar propriedades no mapa e guardar coordenadas e GeoJSON quando disponíveis.
- Abrir o monitoramento de uma propriedade específica.
- Consultar as safras relacionadas à propriedade.

O backend possui busca por localização. Na versão atual, a consulta filtra propriedades pertencentes ao usuário autenticado, mas a implementação dessa busca ainda precisa ser concentrada no Service/Repository para cumprir estritamente a arquitetura solicitada na atividade.

### Safras

**CRUD de Safras:**

- Cadastrar uma safra vinculada a uma propriedade;
- Listar safras da conta autenticada;
- Consultar uma safra por ID;
- Atualizar uma safra;
- Excluir uma safra.

**Funcionalidades além do CRUD:**

- Filtrar safras por propriedade e cultura;
- Estimar a janela de colheita conforme a cultura;
- Abrir a análise de uma safra específica;
- Consultar clima atual e previsão da propriedade;
- Confirmar a conclusão da colheita e persistir o status no MySQL;
- Gerar relatório PDF de uma safra.

As principais ações são:

- Cadastrar, listar, consultar, atualizar e excluir safras associadas a propriedades.
- Identificar cultura, data de plantio, área cultivada e informações complementares.
- Selecionar propriedade e visualizar somente suas safras.
- Consultar uma janela preliminar de colheita para **café, milho ou soja**.
- Abrir **Analisar Safra**, com calendário estimado, clima atual e previsão de curto prazo.
- Registrar o status **Finalizada** após confirmação explícita do usuário e salvar no MySQL.
- Exportar as informações da análise em PDF.

A análise deixou de exibir **lucro estimado** e **produtividade estimada**, pois não existe no protótipo um modelo suficientemente fundamentado para apresentar esses resultados. Campos legados podem continuar na Model/banco por compatibilidade, sem compor o relatório.

### Recursos adicionais que já existem

Estes recursos agregam valor ao projeto, mas **não são somados automaticamente aos 14 fluxos principais** para a atividade de 20 funcionalidades:

1. Consultar o clima atual pela OpenWeather.
2. Consultar previsão meteorológica de curto prazo.
3. Calcular janelas estimadas de colheita para café, milho e soja.
4. Filtrar safras por propriedade.
5. Buscar safras por cultura.
6. Buscar propriedades por localização.
7. Apresentar a análise climática e temporal da safra.
8. Confirmar o encerramento de uma safra (na versão atual reutiliza `AtualizarSafraService`).
9. Gerar relatório PDF no navegador.
10. Consultar indicadores de acompanhamento no dashboard.

Para incluir novos itens na contagem oficial, cada fluxo deve cumprir **a arquitetura e a persistência exigidas na atividade**, e ser apresentado em funcionamento.

**Situação da meta de 20 funcionalidades:** há 14 fluxos principais identificados e 6 ou mais possibilidades de ampliação. A equipe **não deve apresentar os itens ainda em adequação como se já estivessem comprovados**. Para o prazo da atividade, priorizar a demonstração objetiva das funções existentes e a implementação/validação dos casos de uso restantes, com Service próprio quando exigido. A disponibilidade de uma rota ou de um botão, isoladamente, não atende ao requisito do professor.

## Integração do Frontend com a API

A comunicação entre páginas e backend é centralizada em:

```text
backend/static/js/api.js
```

O endereço é obtido automaticamente da origem em que o site foi aberto:

```javascript
const API_URL = window.location.origin;
```

Ao executar o Flask localmente, essa origem normalmente será:

```text
http://127.0.0.1:5000
```

O arquivo fornece funções auxiliares para os métodos **GET, POST, PUT e DELETE**, além de funções específicas para usuários, propriedades, safras, estimativa de colheita e clima.

Nas rotas protegidas, o frontend envia o token recebido no login pelo cabeçalho `Authorization: Bearer ...`. O backend verifica a assinatura, a validade e a identificação da conta; não deve confiar apenas no `usuario_id` enviado pelo JavaScript.

### Funções de Safras no frontend

Algumas funções utilizadas em `backend/static/js/api.js`:

```javascript
listarSafras();
listarSafrasDaPropriedade(propriedadeId);
buscarSafra(id);
cadastrarSafra(dados);
atualizarSafra(id, dados);
excluirSafra(id);
estimarColheita(cultura, dataPlantio);
```

A API é responsável pela persistência no MySQL; o navegador não é o armazenamento central das safras.

## Tela de Safras

Foi desenvolvida a tela de acompanhamento das safras com cartões gerados automaticamente pelo JavaScript, indicadores de quantidade, área cultivada, situação no calendário e acesso às operações principais.

Arquivo da versão atual:

```text
backend/templates/safras.html
```

A tela apresenta as safras da conta e permite acessar o cadastro, a edição, a exclusão e a análise. Os cartões são preenchidos dinamicamente pelo JavaScript, considerando a propriedade, a cultura, as datas e o status registrados. Os indicadores da listagem ajudam a visualizar a situação das safras e a área cultivada.

## JavaScript da tela de Safras

O script da listagem organiza dados reais consultados na API, constrói os cartões, atualiza a visualização após alterações e disponibiliza os botões das operações da safra.

Arquivo:

```text
backend/static/js/safras.js
```

É responsável por consultar a API, montar os cartões, aplicar filtros e atualizar a interface. Os dados persistentes vêm do backend/MySQL. Qualquer compatibilidade residual com `localStorage` não deve ser considerada uma sincronização entre dispositivos.

## Status das Safras

O AgroRisk distingue a **situação calculada pelo calendário** do **status confirmado pelo produtor**:

- **Planejamento / em desenvolvimento:** acompanhamento conforme os registros e a janela estimada.
- **Na janela prevista:** a data atual está dentro do intervalo estimado, mas isso não comprova que houve colheita.
- **Janela encerrada:** a previsão terminou sem uma confirmação de conclusão.
- **Finalizada:** o usuário confirmou a conclusão, e o status foi atualizado no MySQL.

**Uma safra não é finalizada automaticamente porque sua data prevista passou.** Essa distinção evita apresentar uma previsão como se fosse um resultado efetivamente ocorrido.

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

Arquivo:

```text
backend/templates/cadastro_safras.html
```

O formulário envia dados como `propriedade_id`, `nome`, `cultura`, `data_plantio`, `area_plantada`, `custo_total` (opcional) e `observacoes` para a API. A data de colheita de referência é calculada com o apoio do estimador do backend. O sistema verifica campos obrigatórios, cultura e a relação entre a área informada e a propriedade.

O cadastro consulta o **EstimarColheitaService**, que devolve a janela estimada de acordo com a cultura selecionada.

## Monitoramento das Safras

O sistema permite acompanhar a safra no contexto de sua propriedade. O monitoramento usa as coordenadas da propriedade como referência para consultar o clima. Quando uma área foi demarcada no mapa, a API utiliza um ponto de referência da área, não uma medição individual de cada hectare.

As consultas meteorológicas são realizadas pelo backend e dependem de uma chave válida da OpenWeather no `.env`.

## Edição das Safras

O acesso à edição identifica o registro selecionado, por exemplo:

```text
/cadastro_safras.html?id=ID_DA_SAFRA
```

O sistema busca os dados da safra e permite atualizar as informações por meio da API, respeitando a propriedade e a conta autenticada.

## Exclusão das Safras

A listagem permite solicitar a exclusão de uma safra, mediante confirmação do usuário. A operação utiliza `DELETE /safras/<id>`, e o backend confere se o registro pertence à conta autenticada.

Após uma exclusão válida, a listagem pode ser recarregada para refletir os dados persistidos no MySQL.

## Informações de Plantio e Colheita

O sistema armazena a data de plantio e uma data de colheita de referência. Para planejamento, o estimador apresenta também **uma janela de datas**, evitando afirmar que uma colheita acontecerá em um único dia exato.

A meteorologia atual e a previsão de curto prazo aparecem no monitoramento e na análise de safra, mas **não determinam automaticamente a janela de colheita para anos futuros**. A adaptação da estimativa ao clima exigiria dados históricos, cultivar, estágio fenológico e calibração agronômica.

## Integração com a API de Clima

A integração utiliza o **OpenWeather**, com a chave configurada em `OPENWEATHER_API_KEY` no `.env` do backend.

O arquivo `backend/services/clima_service.py` encapsula as chamadas externas e o tratamento de erros. A rota `/api/clima` fornece condições atuais; a rota `/api/clima/previsao` fornece previsão de curto prazo, quando disponível.

Os dados exibidos podem incluir temperatura, umidade, vento, condição do tempo e precipitação prevista. São informações meteorológicas consultadas em tempo de execução: **o projeto ainda não mantém uma série histórica própria de clima no MySQL**.

## Analisar Safra e Relatórios

Ao selecionar **Analisar Safra**, o AgroRisk apresenta os dados da safra, a propriedade vinculada, o status confirmado, a janela estimada de colheita e as condições meteorológicas disponíveis.

A análise pode destacar atenção a calor ou chuva segundo regras demonstrativas. Essas indicações **não representam diagnóstico agronômico ou previsão garantida de perda de produção**.

O relatório pode ser exportado em **PDF**, gerado pelo JavaScript no navegador com jsPDF. Na versão atual, não são exibidas estimativas de lucro nem produtividade; o custo informado pelo usuário pode ser apresentado como dado cadastrado.

## Repositories utilizados

Os Repositories foram criados para encapsular **consultas especiais**, como pesquisas por nome, localização ou cultura e possíveis chamadas a Stored Procedures. O CRUD principal utiliza as operações das Models, não um Repository para cada operação simples.

### UsuarioRepository

Arquivo:

```text
backend/repositories/usuario_repository.py
```

Método existente: `buscar_por_nome(nome)`. A implementação contém uma opção de chamada à Stored Procedure `sp_buscar_usuario_nome`, mas a **rota pública de busca global de usuários está bloqueada por segurança**. Portanto, não é uma funcionalidade demonstrável atualmente na interface.

### PropriedadeRepository

Arquivo:

```text
backend/repositories/propriedade_repository.py
```

Método existente: `buscar_por_localizacao(localizacao)`. O Repository tem integração para a Procedure `sp_buscar_propriedades_localizacao`, porém a rota atual realiza uma consulta autenticada diretamente no Controller. **É preciso mover a busca para Service/Repository**, preservando o isolamento de contas, para cumprir integralmente o padrão exigido.

### SafraRepository

Arquivo:

```text
backend/repositories/safra_repository.py
```

Método existente: `buscar_por_cultura(cultura)`. O Repository tem integração para a Procedure `sp_buscar_safras_cultura`, mas a rota atual consulta SQLAlchemy no Controller. Deve ser refatorada para utilizar um Service específico e o Repository, sempre limitando resultados à conta logada.

## Procedures criadas

A versão antiga do README documentava três Stored Procedures. Os Repositories da versão atual ainda contêm referências a seus nomes; **o `backend/database/create_database.sql` da versão atual cria apenas as tabelas e não instala essas Procedures**. Assim, a equipe não deve declarar sua execução comprovada nesta versão sem verificar a instalação real do banco.

### Usuários

```text
sp_buscar_usuario_nome
```

Consulta especial de busca parcial por nome. Atualmente a pesquisa global está indisponível na API para impedir exposição dos dados de outras contas.

### Propriedades

```text
sp_buscar_propriedades_localizacao
```

Consulta especial de propriedades por localização. A implementação atual da rota usa um filtro de propriedade do usuário autenticado, mas ainda precisa respeitar a separação Controller → Service → Repository para a atividade.

### Safras

```text
sp_buscar_safras_cultura
```

Consulta especial de safras por cultura. O endpoint atual filtra safras do usuário autenticado diretamente com SQLAlchemy no Controller, em vez de fazer a chamada ao Repository.

> **Segurança:** não é apropriado documentar procedures que retornem senhas ou que permitam buscar informações de contas sem autorização. As chamadas `CALL`, quando utilizadas, devem ficar nos Repositories, e não nas Controllers.

## Rotas da API

### Usuários

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/usuarios` | Cadastrar usuário |
| `POST` | `/login` | Autenticar e obter token |
| `GET` | `/usuarios` | Consultar informações permitidas da própria conta |
| `GET` | `/usuarios/<id>` | Consultar o próprio perfil |
| `PUT` | `/usuarios/<id>` | Atualizar o próprio perfil |
| `DELETE` | `/usuarios/<id>` | Excluir a própria conta (rota presente) |
| `GET` | `/usuarios/buscar?nome=...` | Bloqueada para pesquisa global de usuários (`403`) |

### Propriedades

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/propriedades` | Listar propriedades da conta |
| `POST` | `/propriedades` | Cadastrar propriedade |
| `GET` | `/propriedades/<id>` | Consultar propriedade própria |
| `PUT` | `/propriedades/<id>` | Atualizar propriedade |
| `DELETE` | `/propriedades/<id>` | Excluir propriedade |
| `GET` | `/propriedades/buscar?localizacao=...` | Buscar propriedades da conta por localização |

### Safras

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/safras` | Listar safras da conta (admite filtro por propriedade) |
| `POST` | `/safras` | Cadastrar safra |
| `GET` | `/safras/<id>` | Consultar safra própria |
| `PUT` | `/safras/<id>` | Atualizar safra, inclusive status confirmado |
| `DELETE` | `/safras/<id>` | Excluir safra |
| `GET` | `/safras/buscar?cultura=...` | Buscar safras da conta por cultura |
| `GET` | `/safras/estimar-colheita?cultura=...&data_plantio=AAAA-MM-DD` | Calcular janela de colheita |

### Clima e sistema

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/clima?lat=...&lon=...` | Clima atual |
| `GET` | `/api/clima/previsao?lat=...&lon=...` | Previsão de curto prazo |
| `GET` | `/api` | Verificar informações básicas da API |
| `GET` | `/` | Abrir página inicial do AgroRisk |

Os endpoints de dados pessoais, propriedades, safras e clima exigem token na versão atual; o cadastro inicial e o login são públicos. As buscas devem manter o isolamento entre contas.

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

**Requisitos:** Python e dependências do `requirements.txt`, MySQL/MariaDB disponível, navegador e, para clima real, uma chave OpenWeather.

No Windows, com XAMPP, inicie primeiro o módulo **MySQL** no painel. Não é necessário ligar o Apache para servir as páginas do AgroRisk.

Entre na pasta do backend:

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

Crie o arquivo `backend/.env` a partir de `.env.example` (preencha os valores **somente em sua máquina**):

```dotenv
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@127.0.0.1:3306/agrorisk
OPENWEATHER_API_KEY=COLE_SUA_CHAVE_AQUI
SECRET_KEY=COLE_UMA_CHAVE_FORTE_AQUI
FLASK_DEBUG=False
```

**Não use os valores de exemplo literalmente.** Se você utiliza XAMPP com `root` sem senha somente em desenvolvimento local, uma conexão possível é `mysql+pymysql://root:@127.0.0.1:3306/agrorisk`. Em produção, utilize credenciais exclusivas e senha forte.

Para gerar uma `SECRET_KEY` aleatória, execute:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Inicie o servidor:

```powershell
python app.py
```

Abra:

```text
http://127.0.0.1:5000
```

**Não é necessário abrir o Live Server.** Para executar em Linux/macOS, a ativação do ambiente virtual geralmente é `source venv/bin/activate`.

## Banco de dados

O AgroRisk utiliza **MySQL** (ou MariaDB compatível) e um banco chamado `agrorisk` na configuração local padrão.

O arquivo `backend/database/create_database.sql` define as tabelas de instalações novas. **Não execute scripts antigos com `DROP DATABASE` em bancos que contenham dados reais.** Faça backup antes de mudanças. O `db.create_all()` cria tabelas ausentes, mas **não atualiza automaticamente colunas de tabelas antigas**; alterações de estrutura devem ser feitas por migrações controladas.

Relacionamentos principais:

```text
Usuario (1) ─── (N) Propriedade (1) ─── (N) Safra
```

Os dados de safras e propriedades ficam vinculados às contas por chaves e regras de acesso no backend. Um banco local não se sincroniza automaticamente entre computadores; para acesso na escola e em casa é necessário hospedar o Flask e conectar todos os usuários a um banco central.

## Testes das funcionalidades avançadas

Os testes automatizados e a demonstração no navegador são complementares. Dentro da pasta `backend`, podem ser executados:

```powershell
python tests/test_paginas_flask.py
python tests/test_protecao_contas.py
python tests/test_clima_service.py
```

Alguns testes utilizam bancos temporários ou simulações; eles não substituem o teste real com MySQL e as telas do AgroRisk.

### Busca de usuários por nome

```text
GET /usuarios/buscar?nome=Joao
```

**Status:** bloqueada na API atual (`403`), para não expor dados de outras pessoas. Não demonstrar como funcionalidade concluída.

### Busca de propriedades por localização

```text
GET /propriedades/buscar?localizacao=Vespasiano
```

O código da rota restringe os resultados à conta autenticada. A consulta ainda precisa passar por Service/Repository próprio para aderir integralmente à arquitetura obrigatória.

### Busca de safras por cultura

```text
GET /safras/buscar?cultura=Soja
```

O código da rota restringe resultados às propriedades da conta autenticada. A consulta ainda precisa passar por Service/Repository próprio para aderir integralmente à arquitetura obrigatória.

### Testes do cadastro, acompanhamento e finalização

Na demonstração, conferir se o cadastro retorna sucesso, se a safra aparece na listagem, se pode ser editada e se o status **Finalizada** continua registrado após atualizar a página.

### Testes das estimativas de colheita

Usar a mesma data de plantio para Café, Soja e Milho e comprovar que os intervalos mudam conforme os parâmetros do `EstimarColheitaService`. As estimativas são preliminares, sem modelagem histórica do clima.

## Tecnologias utilizadas

- **Python** e **Flask** — backend e servidor local das páginas.
- **Flask-SQLAlchemy / SQLAlchemy / PyMySQL** — modelos e acesso ao banco.
- **MySQL / MariaDB** — persistência de usuários, propriedades e safras.
- **python-dotenv** — configuração por variáveis de ambiente.
- **itsdangerous** — tokens assinados e temporários (biblioteca utilizada pela autenticação).
- **requests** — consulta à API meteorológica.
- **HTML, CSS e JavaScript** — interface.
- **Bootstrap** e **Font Awesome** — componentes visuais e ícones.
- **Leaflet** — mapas e delimitação de áreas.
- **jsPDF** — exportação do relatório para PDF.
- **OpenWeather** — clima atual e previsão de curto prazo.

## Diagrama de classes

O domínio principal envolve `Usuario`, `Propriedade` e `Safra`, cada uma representada por uma Model SQLAlchemy. O arquivo a ser incluído no repositório é:

```text
docs/diagrama-classes.md
```

Consulte o [diagrama de classes](docs/diagrama-classes.md). A relação usuário–propriedade–safra deve ser coerente com as chaves estrangeiras do MySQL. O arquivo do diagrama deve ser adicionado ao GitHub junto ao README, pois o link não funcionará se ele não estiver no repositório.

## Segurança do sistema

A versão atual possui:

- Armazenamento de senhas com hash.
- Autenticação por token assinado e temporário, com duração configurada de oito horas.
- Exigência de token em rotas de dados e verificação de acesso às informações da conta.
- Variáveis `SECRET_KEY`, `DATABASE_URL` e `OPENWEATHER_API_KEY` no `.env` local.
- Alguns cabeçalhos HTTP de proteção e configurações voltadas ao uso local.

**Ainda não está pronta para publicação pública:** é necessário implantar HTTPS, proteção contra tentativas repetidas de login, backups, configuração segura de conexão MySQL, revisão de autorização em todos os endpoints e um servidor de produção para Flask. O `.env` deve permanecer fora do Git; credenciais expostas anteriormente precisam ser substituídas.

## Vídeo de demonstração da atividade

A entrega exige **vídeo obrigatório de no máximo 5 minutos**, além do commit/push no repositório oficial. Para demonstrar o AgroRisk de hoje, o grupo pode seguir este roteiro, ajustando o tempo às telas efetivamente testadas:

| Tempo sugerido | Demonstração | O que comprovar |
| --- | --- | --- |
| 0:00–0:35 | Apresentação do sistema e arquitetura | HTML/JS no Flask, Controller, Service e MySQL |
| 0:35–1:15 | Cadastro e login | Usuário cadastrado, autenticação e perfil carregado |
| 1:15–2:10 | Propriedades | Cadastro, listagem, consulta, edição, localização e exclusão em dados de teste |
| 2:10–3:20 | Safras | Cadastro, listagem, edição e exclusão; vínculo com uma propriedade |
| 3:20–4:10 | Estimativa e análise | Café, Milho e Soja com janelas diferentes; análise com clima real |
| 4:10–4:45 | Conclusão e PDF | Confirmar finalização, recarregar e gerar relatório |
| 4:45–5:00 | Encerramento | Mostrar README, diagrama e persistência dos registros |

Gravar apenas operações que estiverem funcionando, sem expor CPF, senhas, chaves de API, tokens ou dados privados reais. A equipe deve usar **contas, propriedades e safras de demonstração**. Não apagar os próprios dados durante a gravação.

**Antes do envio:** conferir a lista oficial de funcionalidades, o diagrama em `docs/diagrama-classes.md`, o vídeo e o repositório atualizado. A exigência de **20 funcionalidades completas** precisa ser verificada conforme a rubrica do professor, não apenas pela quantidade de telas ou rotas.

## Status atual do projeto

O AgroRisk evoluiu de páginas separadas abertas com Live Server para uma aplicação em que **o Flask entrega tanto o frontend quanto a API**. O projeto já integra usuários, propriedades, safras, mapas, clima real, estimativas preliminares de colheita, análise de safra, confirmação de finalização e relatório PDF.

O sistema funciona localmente com MySQL iniciado pelo XAMPP e Flask disponível em `http://127.0.0.1:5000`, conforme as configurações do ambiente.

### Melhorias planejadas

- Adequar e validar os fluxos adicionais para comprovar **20 funcionalidades completas** segundo os critérios da disciplina.
- Refatorar buscas avançadas para utilizar Services/Repositories sem regras de consulta diretamente nos Controllers.
- Concluir os testes de segurança e de integração.
- Preparar hospedagem central com Flask, MySQL, HTTPS e backups.
- Implementar armazenamento persistente e autenticado da foto de perfil, hoje guardada no navegador.
- Avaliar séries históricas climáticas e aprimorar as estimativas com dados agronômicos fundamentados.

**Projeto acadêmico:** os dados climáticos e as datas estimadas apoiam a demonstração do TCC, mas não substituem orientação técnica nem garantem uma data de colheita.
