# AgroRisk — conferência para a rubrica do TCC

Esta cópia é uma **versão de interface para testes**, não uma garantia de nota nem de implantação.

## Alterações desta versão

- `dashboard.html` continua como dashboard principal, mantendo seus indicadores originais.
- `orientador.html`: **apenas Análise Simples**, com propriedade, safra e janela estimada.
- `assistente.html`: **chat Gemini em página separada**, com contexto opcional e consentimento antes de enviar.
- `ferramentas.html`: cálculos de capacidade de plantio e consulta de janela de colheita, fora da tela principal.
- O formulário avançado deixou de aparecer no menu, mas seu backend (`/api/analise-avancada`), tabela e scripts foram preservados. Uma cópia da interface anterior está em `docs/backup_interface/`.
- Nenhum segredo `.env` foi incluído no pacote. Não publicar credenciais no GitHub.

## Conferência pela rubrica recebida

| Critério | Peso | Evidência / pendência |
| --- | ---: | --- |
| 4 fluxos não CRUD demonstrados ponta a ponta | 4 | Testar mapa/demarcação; clima real; estimativa de colheita; relatório PDF/IA, conforme validação do professor. |
| Cliente-servidor | 4 | API é consumida por HTTP, mas páginas e API estão no **mesmo Flask**. Faltam evidências de **servidores separados**, exigidas para parte dos pontos. |
| API em camadas | 7 | Existem Controllers, Services, Models e Repositories. Auditar cada rota e cada fluxo, pois a existência das pastas não prova organização completa. |
| CRUD/ORM e SQL em Repository | 4 | Há SQLAlchemy; verificar consultas SQL executadas nos Repositories e isolamento entre contas. |
| Diagrama de classes | 3 | Revisar `docs/diagrama-classes.md` conforme código atual, incluindo relacionamentos. |
| Fluxogramas | 4 | Criar/verificar fluxograma de entrada e de recuperação de dados, com as camadas reais. |
| Apresentação/README | 4 | Preparar slides: problema, público, 5 casos de uso + telas, arquitetura/diretórios, tecnologias e README. |
| Bônus | até 5 | IA Gemini (2) precisa ser testada ao vivo; hospedagem (2) exige frontend e API acessíveis; consentimento (1) precisa de evidência da decisão registrada no fluxo pertinente. |

**Demonstração:** a rubrica solicita até 2 minutos para a demonstração (vídeo ou sistema hospedado), com 4 fluxos não CRUD. Confirmar com o professor como esse tempo se aplica à apresentação ao vivo.

## Procedimento de testes antes da entrega

1. Preparar banco de teste/backup e `.env` privado.
2. Testar login, propriedades, mapa/demarcação, safras, clima e PDF.
3. Testar `Minha safra` e `Assistente IA` com dados de uma conta real de teste.
4. Testar uma segunda conta para confirmar que não consegue acessar a safra da primeira.
5. Documentar os resultados e corrigir as pendências de arquitetura/repositórios.
6. Somente depois enviar ao GitHub; inspecionar o `git status` antes de `git add`.
