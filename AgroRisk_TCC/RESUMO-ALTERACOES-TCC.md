# AgroRisk — mudanças desta versão para a rubrica

**Mantenha seu `backend/.env` atual no PC e não o inclua no GitHub.**

## O que foi implementado

1. Dois servidores: frontend Flask separado em `frontend/server.py` (porta 5500) e backend em `backend/app.py` com `AGRORISK_API_ONLY=1` (porta 5000).
2. Proxy HTTP no frontend para requisições da API. Mantido JS original e autenticação Bearer, sem liberar CORS a qualquer origem.
3. Reorganização dos fluxos de login, usuários, propriedades e safras para consultar e persistir por Repositories, incluindo buscas SQL parametrizadas e filtros de segurança por usuário.
4. Fluxogramas Mermaid de entrada e recuperação de dados, diagrama de classes atualizado com `SafraParametros` e guia para slides e demonstração de 2 minutos.
5. Novos testes automáticos propostos para o frontend, backend API-only e isolamentos de consulta no SQLite.
6. Todos os arquivos visuais/mobile já ajustados foram preservados.

## O que não foi comprovado automaticamente

- Início efetivo dos servidores Python, MySQL do seu XAMPP, login, edição, PDF, IA Gemini e consulta climática em sua máquina.
- Os novos testes Python dependem de Flask/Flask-SQLAlchemy e devem ser executados no seu Windows.
- A pontuação da rubrica não é garantida: apresente evidências, fluxogramas, slides e demonstração.

## Para iniciar

Leia `LEIA-ME-ARQUITETURA-2-SERVIDORES.md`, que contém os três comandos por terminal.

**ATENÇÃO:** O Cloudflare Tunnel deve apontar para `127.0.0.1:5500`, não mais `5000`, no modo separado.
