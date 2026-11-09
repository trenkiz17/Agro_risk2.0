# AgroRisk: integração de clima para testes locais

Esta versão preserva as telas e a lógica de cadastro, propriedades, safras,
monitoramento e estimativa de colheita. Não instala nem migra o MySQL automaticamente.

## O que mudou

- `services/clima_service.py`: consulta as condições atuais do OpenWeather e a previsão
  gratuita de 5 dias/intervalos de 3 horas (agrupados em até 4 datas locais).
  Inclui VPD (kPa), índice instantâneo calculado pela temperatura e umidade.
- `controllers/clima_controller.py`: conserva `/api/clima` e acrescenta
  `/api/clima/previsao`.
- `frontend/js/api.js`: nova função `buscarPrevisaoClima`; correção do HTTP 204
  para que exclusão com sucesso não pareça falha.
- `frontend/monitoramento.html` e `js/monitoramento.js`: painel meteorológico ligado
  à propriedade selecionada por suas coordenadas; não interfere nas safras.
- `database/create_database.sql`: esquema alinhado aos modelos atuais para instalações
  novas, SEM dados de exemplo ou senhas padrões. Não migra tabelas existentes.
- `requirements.txt`: dependências de execução especificadas.

## Para testar

1. Crie backup do seu código e banco. Preserve seu `.env` atual (este ZIP NÃO contém `.env`).
2. No backend, rode `python -m pip install -r requirements.txt`.
3. No seu `.env` do backend, defina `OPENWEATHER_API_KEY=SUA_CHAVE_DE_VERDADE`.
   Não coloque essa chave no JavaScript, GitHub ou mensagens públicas.
4. Inicie o Flask normalmente.
5. No navegador, acesse
   `http://127.0.0.1:5000/api/clima?lat=-19.92&lon=-43.94`
   e `http://127.0.0.1:5000/api/clima/previsao?lat=-19.92&lon=-43.94`.
   São coordenadas APENAS PARA TESTE da região de Belo Horizonte, MG.
6. Na propriedade real, confira latitude e longitude no cadastro. Abra
   `monitoramento.html?id=ID_DA_PROPRIEDADE`. Os dados aparecerão no painel.
7. Se houver erro 400 sobre a chave, confirme configuração e ativação junto ao OpenWeather.
   Se a propriedade não tiver coordenadas, será exibido aviso na página.

## Testes locais sem chamar a internet

`cd backend`
`python -m unittest discover -s tests -v`

**Importante:** Os testes automatizados usam respostas simuladas da API. Não foi feita
uma chamada real à OpenWeather nem a um MySQL aqui. O VPD não determina irrigação,
risco de perda ou produtividade. A estimativa de colheita permanece baseada somente
em intervalos de ciclo, SEM integração com clima.

## Atenção com seu ZIP original

- Os ZIPs recebidos ainda possuem `login_usuario_service.py` e
  `criar_usuario_service.py` com senhas em texto puro. As alterações de hash
  discutidas antes não estão nesta cópia; precisa corrigir antes de publicar.
- A autenticação é baseada em `usuario_id` informado pelo navegador: insuficiente
  para internet pública, mesmo depois de implementar hash.
- `db.create_all()` não adiciona colunas a tabelas existentes. Se seu MySQL
  foi criado com o SQL antigo, `SHOW COLUMNS FROM safras;` ajuda a conferir
  `nome` e `observacoes`. Faça backup e migração específica se faltarem.
- O frontend mantém `http://127.0.0.1:5000` para testes no mesmo computador.
  Não sincroniza bancos diferentes nem funciona entre cidades dessa forma.
- Não envie `.env` nem `.git` em arquivos compartilhados. As pastas desses
  dois tipos foram deixadas de fora dos ZIPs de teste entregues.
