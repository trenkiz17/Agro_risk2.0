# Orientador AgroRisk — IA Gemini e linha do tempo

## Como configurar e iniciar

1. Extraia o ZIP em **outra pasta**; ao abrir esta pasta verá `backend/` diretamente (não existe mais subpasta extra).
2. Dentro de `backend`, copie `.env.example` para `.env`. Mantenha `SECRET_KEY`, `DATABASE_URL` e `OPENWEATHER_API_KEY` conforme seu computador.
3. Gere sua chave **GEMINI_API_KEY** gratuitamente no [Google AI Studio](https://aistudio.google.com/apikey). Configure `GEMINI_MODEL=gemini-3.5-flash-lite` (modelo padrão; acesso depende da conta/região e dos limites do provedor).
4. Inicie o MySQL no XAMPP; no terminal da pasta raiz extraída execute:

   ```powershell
   cd backend
   python -m pip install -r requirements.txt
   python app.py
   ```

5. Abra `http://127.0.0.1:5000/login.html`, faça login e entre em `http://127.0.0.1:5000/orientador.html`.
6. **Marque o consentimento** antes de perguntar. Se quiser contexto da propriedade, selecione-a; os dados resumidos serão enviados ao Gemini.

> Não envie `.env` para o GitHub ou para colegas. O `.env.example` tem apenas exemplos. A chave Gemini é secreta e fica SOMENTE no Flask.

## O que foi implementado

- `POST /api/orientador/perguntar`: nova rota protegida por token, Controller e Service próprios, usa a API **Gemini**. Usuário precisa concordar com envio da pergunta/contexto. Contexto da propriedade e safra somente da conta autenticada. O servidor limita a 8 chamadas por 10 minutos por usuário (em memória, ideal apenas para protótipo).
- `GET /api/orientador/status`: checa se existe configuração da chave sem expô-la.
- Contexto opcional de propriedade, safra e previsão OpenWeather. Não envia dados pessoais, credenciais, geometrias nem observações livres. Se a previsão falhar, informa indisponibilidade.
- Chat com histórico curto em memória da aba (não é salvo no MySQL). Interface evita renderizar HTML da resposta (`textContent`), e mostra mensagens de erro sem comprometer as páginas antigas.
- Calculadora de mudas conservada. **Não é o modelo generativo** que calcula a fórmula: ela é executada no JavaScript local.
- Linha do tempo reformulada: agora apresenta datas sugeridas de vistoria calculadas a partir da data de plantio e do início da janela. **Essas datas não são previsões de crescimento/floração.** Uma previsão biológica precisaria de cultivar, clima e modelo agronômico validado.

## Limitações e privacidade

- O Gemini pode errar e **não fornece laudo agronômico**. Nenhuma previsão futura além dos dados do estimador é garantida. Não há pesquisa web ativa neste chat; previsões de 2029 não são fornecidas pelo OpenWeather.
- O plano gratuito do Gemini possui limites e disponibilidade variáveis; preços/uso de dados são definidos pelo Google. Verifique as condições antes de utilizar dados reais. Dados enviados ao serviço externo estão sujeitos às políticas do Google.
- O consentimento é recolhido por checkbox na sessão atual e não é persistido no banco; portanto, não declaramos automaticamente o bônus de "decisão registrada" da rubrica.
- Uso local/educacional. Antes de publicar, adicionar limites compartilhados de requisição, testes de carga, HTTPS e política de privacidade.
- Arquivos originais do dashboard, mapas, clima e PDF preservados, exceto a integração adicional no `backend/app.py` e os arquivos de orientador/linha do tempo.

## Teste de integração real

Sem uma chave válida não é possível executar uma chamada real ao Gemini. Testes automatizados utilizam simulação da resposta remota para validar parâmetros, rota, autenticação, autorização e erros. Configure sua chave e faça uma pergunta original para conferir a integração externa.
