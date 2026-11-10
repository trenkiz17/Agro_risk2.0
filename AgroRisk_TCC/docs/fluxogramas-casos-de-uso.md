# Fluxogramas reais dos casos de uso — AgroRisk

Esses fluxos correspondem às rotas e às classes do projeto desta versão. As setas mostram **requisições HTTP** e chamadas entre **Controller → Service → Repository → Model/SQL**. Use-os na apresentação da rubrica.

## Fluxo 1 — Entrada de dados (cadastro de propriedade)

**Caso de uso:** usuário autenticado cadastra uma propriedade com nome, cidade, estado, área e localização. A interface envia `POST /propriedades`.

```mermaid
flowchart TD
    A[Usuário preenche o formulário no frontend 5500] --> B[JavaScript api.js envia POST /propriedades]
    B --> C[Frontend encaminha HTTP à API 5000]
    C --> D{Token válido em before_request?}
    D -- Não --> E[Resposta HTTP 401]
    D -- Sim --> F[PropriedadeController.criar_propriedade]
    F --> G[CriarPropriedadeService.executar]
    G --> H{Campos e valores válidos?}
    H -- Não --> I[Resposta HTTP 400]
    H -- Sim --> J[Cria a Model Propriedade]
    J --> K[PropriedadeRepository.salvar]
    K --> L[(MySQL: tabela propriedades)]
    L --> M[Service converte Model para JSON]
    M --> N[Controller responde HTTP 201]
    N --> O[Frontend atualiza a interface]
```

**Evidências:** `backend/controllers/propriedade_controller.py`, `backend/services/criar_propriedade_service.py`, `backend/repositories/propriedade_repository.py`, `backend/models/propriedade.py`, `backend/static/js/api.js`.

## Fluxo 2 — Recuperação de dados (consulta de propriedades por localização)

**Caso de uso:** usuário autenticado busca propriedades da própria conta por cidade, estado ou nome. A interface pode chamar `GET /propriedades/buscar?localizacao=...`.

```mermaid
flowchart TD
    A[Usuário solicita consulta no frontend 5500] --> B[JavaScript realiza GET /propriedades/buscar]
    B --> C[Frontend encaminha HTTP à API 5000]
    C --> D{Token válido em before_request?}
    D -- Não --> E[Resposta HTTP 401]
    D -- Sim --> F[PropriedadeController.buscar_propriedade_por_localizacao]
    F --> G[BuscarPropriedadePorLocalizacaoService.executar]
    G --> H{Filtro válido?}
    H -- Não --> I[Resposta HTTP 400]
    H -- Sim --> J[PropriedadeRepository.buscar_por_localizacao]
    J --> K[SQL parametrizado com usuario_id]
    K --> L[(MySQL: propriedades)]
    L --> M[Repository carrega Models autorizadas]
    M --> N[Service converte Models em JSON]
    N --> O[Controller retorna HTTP 200]
    O --> P[Frontend exibe os resultados]
```

**Evidências:** `backend/controllers/propriedade_controller.py`, `backend/services/buscar_propriedade_por_localizacao_service.py`, `backend/repositories/propriedade_repository.py`.

**Observação:** o endpoint de busca existe e pode ser testado com a API; verifique se a interface específica apresenta esse filtro antes de afirmar que está exposto como pesquisa de localização na tela. Para demonstração visual, a listagem por usuário é outro fluxo de recuperação implementado em `ListarPropriedadesService` e `PropriedadeRepository.listar_por_usuario`.

## Fluxo 3 — Recuperação de dados (listagem de safras)

```mermaid
flowchart TD
    A[Usuário abre Minha Safra] --> B[JS GET /safras]
    B --> C[Frontend 5500 envia HTTP para API 5000]
    C --> D{Token válido?}
    D -- Não --> E[HTTP 401]
    D -- Sim --> F[SafraController.listar_safras]
    F --> G[ListarSafrasService.executar]
    G --> H[SafraRepository.listar_por_usuario]
    H --> I[SQLAlchemy filtra propriedade do usuário]
    I --> J[(MySQL: safras e propriedades)]
    J --> K[JSON com safras autorizadas]
    K --> L[Frontend exibe safra cadastrada]
```

## Cuidados ao apresentar

- As telas são entregues pelo servidor frontend, mas quem valida tokens e acessa o banco é a API.
- Repositories são responsáveis pelas consultas SQL/ORM; Models representam o domínio.
- Mostre os dois terminais executando em portas **5500 e 5000**, a chamada via navegador (Network) e a estrutura de diretórios.
- Não mostre senhas, tokens ou chaves reais.
