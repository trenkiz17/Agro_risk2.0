# AgroRisk – versão Flask com templates, static e autenticação

**Esta pasta é uma CÓPIA DE TESTE.** Seu projeto anterior com Live Server e seu backup do GitHub continuam intactos.

## O que foi alterado

- As 11 páginas HTML foram para `backend/templates/` (renderizadas pelo Flask).
- CSS, todos os JavaScripts e imagens foram para `backend/static/css/`, `backend/static/js/`, `backend/static/img/`.
- Referências de CSS/JS/imagens nos HTML usam `{{ url_for('static', filename='...') }}`.
- Links das páginas `login.html`, `safras.html` etc. continuam válidos por uma rota Flask que só aceita os 11 nomes esperados.
- `static/js/api.js` usa `window.location.origin` e não depende mais da porta 5500 do Live Server.
- Corrigidos os imports `from security.auth ...` em `app.py` e no `usuario_controller.py`.
- Mantidas as proteções existentes: hashes de senha, token temporário de 8 horas, cabeçalho Authorization e autorização por usuário nos controllers.
- Como páginas e API têm a mesma origem, a configuração CORS para a porta 5500 foi retirada da **cópia de teste**.
- Incluídos cabeçalhos HTTP básicos (`nosniff`, `Referrer-Policy`, `Cache-Control: no-store` para endpoints de dados).
- Flask local configurado para `127.0.0.1` em vez de expor o servidor de desenvolvimento na rede.
- **Não alteramos** Models, regras de colheita, serviços climáticos, SQL nem dados MySQL.

## Instalação no Windows – passo a passo

1. **Não substitua nem apague sua versão atual.** Extraia este ZIP para uma pasta NOVA.
2. Faça um backup do MySQL antes dos testes que gravarem, editarem ou excluírem dados. Esta cópia usa o MESMO banco indicado na DATABASE_URL; pasta separada não isola o banco.
3. Crie `backend/.env` na nova pasta. Se o `.env` anterior já funciona, você pode **copiar localmente** dele as variáveis `DATABASE_URL`, `OPENWEATHER_API_KEY` e `SECRET_KEY`. Não compartilhe nem envie o `.env` ao Git. O ZIP só contém `.env.example` sem credenciais.
4. Se não tiver `SECRET_KEY`, gere com `python -c "import secrets; print(secrets.token_urlsafe(48))"` e coloque o resultado em `backend/.env`. Os valores de exemplo NÃO são válidos.
5. Abra o terminal do VS Code dentro de `backend/` e execute:

   ```powershell
   python -m pip install -r requirements.txt
   python app.py
   ```

6. Abra **http://127.0.0.1:5000/**. Não execute o Live Server. Login: **http://127.0.0.1:5000/login.html**.
7. Por causa da mudança da porta 5500 para 5000, o navegador terá outro `localStorage` e `sessionStorage`. **Entre novamente na conta**. Os dados que já estiverem no MySQL continuam lá, desde que a `DATABASE_URL` seja a mesma. A **foto de perfil**, que ainda é local ao navegador, não será sincronizada; isso exige upload futuro.
8. Para interromper, use `Ctrl+C` no terminal do Flask.

## Testes sem mexer no MySQL

Dentro da pasta `backend/`:

```powershell
python tests/test_paginas_flask.py
python tests/test_protecao_contas.py
```

Ambos configuram um SQLite em memória para testes. Não use seus dados reais no teste de cadastro/exclusão até fazer backup.

## Checklist manual na nova versão

- Abra index, login e cadastro e confirme CSS e imagens.
- Faça login e atualize perfil.
- Consulte propriedade e mapa; o mapa e a busca por localização dependem de internet e serviços externos (Leaflet/OpenStreetMap).
- Consulte safras, filtre, veja estimativas e **Analisar Safra**.
- Confira clima e previsão (OpenWeather precisa de chave válida no `.env`).
- Gere um PDF e confirme status `Finalizada` com uma **safra de teste**.
- Faça logout e valide que `/propriedades` via API sem token retorna `401`.

## O que ainda NÃO está concluído

- Implantação pública com HTTPS e servidor WSGI (não publique `python app.py` na internet).
- Migração para MySQL central e backups gerenciados. `db.create_all()` não faz migração de esquema.
- Upload e sincronização da foto de perfil (ela ainda usa `localStorage`).
- Bloqueio/rate limiting de tentativas repetidas de login, revogação de tokens e revisão de segurança em produção.
- Foram corrigidas duas referências já quebradas no ZIP original: o fundo do hero usa `img/agricultura.jpg` (imagem já existente) no lugar de `img/fazenda.jpg` ausente, e o avatar da lista de propriedades só define `src` quando há foto local.
- CDN Bootstrap/Font Awesome/Leaflet e a consulta ao OpenWeather exigem internet.

## Voltar para o Live Server

1. Feche o Flask desta cópia (`Ctrl+C`).
2. Abra sua pasta **original intacta** no VS Code.
3. Inicie o backend e o Live Server originais com suas configurações anteriores.

O banco não foi migrado nem apagado por esta conversão. Se gravou dados no banco durante os testes, esses dados permanecerão: um backup de pasta não reverte operações do MySQL.
