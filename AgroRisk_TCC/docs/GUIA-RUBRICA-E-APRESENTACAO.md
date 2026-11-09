# Preparação final para a rubrica do TCC — AgroRisk

Documento de trabalho para revisão; **não representa nota garantida**.

## Requisitos oficiais

A rubrica possui 30 pontos principais. Os critérios de **arquitetura cliente-servidor (4)** e **API em camadas (7)** são obrigatórios; bônus não substituem esses itens. A demonstração obrigatória dura até **2 minutos** e deve mostrar **4 funcionalidades não CRUD** de ponta a ponta. Slides devem incluir problema/público, 5 casos de uso com suas telas, arquitetura e diretórios, tecnologias e README.

| Critério | Máximo | Evidência nesta versão | Falta validar |
| --- | ---: | --- | --- |
| Fluxo de 4 funcionalidades não CRUD | 4 | Fluxos candidatos: mapa, clima, estimativa agrícola, relatório PDF, IA | Testar na máquina e gravar 2 min; CRUD isolado não conta |
| Frontend e API em servidores separados | 4 | `frontend/server.py` (5500) e `backend/app.py` API-only (5000). Requisições por HTTP via proxy | Executar os dois processos, mostrar `Network` e acesso pelo Cloudflare na 5500 |
| API em camadas | 7 | Controllers, Services, Repositories e Models; filtros de propriedades e safras agora passam por Repository | Auditar os demais casos de uso; existência das pastas sozinha não garante os 7 pontos |
| Persistência / ORM / SQL | 4 | SQLAlchemy e SQL parametrizado em `PropriedadeRepository` e `SafraRepository` | Testar com MySQL e mostrar CRUD + buscas com resultados corretos |
| Diagrama de classes | 3 | `docs/diagrama-classes.md` atualizado com `SafraParametros` | Conferir que o Mermaid renderiza e combina com o banco real |
| Fluxogramas | 4 | `docs/fluxogramas-casos-de-uso.md`: entrada e recuperação com todas as camadas | Incluir imagens/links na apresentação |
| Apresentação e README | 4 | README preservado; este guia de slides e mapa de telas | Produzir slides e capturar telas reais com dados de teste |
| Bônus IA, hospedagem, consentimento | até 5 | Gemini e consentimento no fluxo de IA; túnel acessa o frontend | Testar IA, mostrar decisão do usuário, garantir frontend/API funcionando na hora |

## Cinco casos de uso para os slides

1. **Autenticar usuário** — `backend/templates/login.html` + rota `POST /login`.
2. **Cadastrar e delimitar propriedade** — `backend/templates/cadastro_propriedade.html` + mapa + `POST /propriedades`.
3. **Cadastrar / analisar safra** — `backend/templates/orientador.html` e `backend/templates/cadastro_safras.html` + `POST /safras`.
4. **Consultar clima e previsão** — `backend/templates/monitoramento.html` + `/api/clima` e `/api/clima/previsao`.
5. **Gerar relatório agrícola ou consultar IA** — `backend/templates/relatorios.html` e `assistente.html` + rotas de API relacionadas.

## Roteiro sugerido de demonstração (até 2 minutos)

| Duração | O que mostrar | Não CRUD? |
| --- | --- | --- |
| 0:00–0:25 | Selecionar propriedade e mostrar **mapa e área delimitada** | Sim, se cálculo e mapa funcionarem |
| 0:25–0:50 | **Clima atual e previsão** baseados na localização | Sim |
| 0:50–1:15 | **Estimativa de colheita** ao escolher cultura e data | Sim |
| 1:15–1:45 | **Relatório em PDF** de safra existente, com informações calculadas | Sim, se gerar documento efetivamente |
| 1:45–2:00 | Mostrar os dois servidores e os diretórios da arquitetura | Evidência complementar |

As quatro funções precisam ser vistas de ponta a ponta, não apenas clicadas. Caso uma delas falhe, use o **Assistente IA** como alternativa **somente se a integração estiver funcionando**. Grave com dados fictícios e sem exibir tokens e credenciais.

## Organização dos slides

1. Capa — AgroRisk, equipe, disciplina e objetivo.
2. Problema, público-alvo e solução proposta.
3. Cinco casos de uso, com cinco capturas reais do site.
4. Figura da arquitetura: celular/navegador → frontend 5500 → API 5000 → MySQL; API → serviços de clima e IA.
5. Pastas `controllers/`, `services/`, `repositories/`, `models/` e principais tecnologias.
6. Diagrama de classes e os dois fluxogramas.
7. Demonstração e README (link do repositório).

## Pontos que ainda precisam da sua máquina

- Sem acesso ao seu XAMPP, `.env`, chaves e túnel, não é possível garantir persistência, clima, Gemini, PDF ou 4 fluxos funcionais reais.
- Atualize o GitHub **depois** de testar os dois servidores.
- Para o bônus de hospedagem, o servidor frontend e o backend devem estar ativos durante a avaliação; Tunnel gratuito exige seu PC ligado.
- Para o bônus de consentimento, confirme em tela se os termos e a decisão estão claros no fluxo da IA.

## Verificações feitas antes da entrega desta edição

- Compilação estática dos arquivos Python (sem erro sintático).
- Verificação de sintaxe de 20 arquivos JavaScript pelo Node.js.
- Interpretação Jinja de 15 templates e renderização de 14 páginas com contexto simulado.
- Consulta SQL com dois usuários fictícios executada em SQLite para testar o filtro por conta.
- **Não foi possível executar a suíte Flask/SQLAlchemy completa neste ambiente**, pois as dependências Flask não estavam disponíveis e não foi possível instalá-las sem acesso à rede. No seu computador, instale os requirements e execute:

  ```powershell
  cd backend
  python -m pip install -r requirements-dev.txt
  python -m pytest tests/test_separacao_servidores.py tests/test_consultas_repository.py -q
  ```

  Para os demais testes existentes, consulte os comandos nos arquivos `backend/tests/*.py`.
