# Innova Content Agent

MVP para criação, revisão e aprovação de conteúdo para LinkedIn, Instagram e
YouTube.

## Stack

- Next.js 16, React 19, TypeScript e Tailwind CSS
- FastAPI, SQLAlchemy, Alembic e PostgreSQL
- LangGraph com nós separados
- OpenAI Responses API ou provider mock local

## Docker

1. Copie `.env.example` para `.env`.
2. Defina um `JWT_SECRET` forte.
3. Para usar OpenAI, defina `LLM_PROVIDER=openai` e `OPENAI_API_KEY`.
4. Execute:

```powershell
docker compose up --build
```

- Frontend: `http://100.108.2.19:3002`
- API: `http://100.108.2.19:8000`
- Swagger: `http://100.108.2.19:8000/docs`

O ambiente Docker de homologação/produção está configurado para a máquina
`innovaapps` na rede Tailscale. Consulte
[DEPLOY-INNOVAAPPS.md](DEPLOY-INNOVAAPPS.md).

## Desenvolvimento local

Backend:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\pip install -e ".[dev]"
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\uvicorn app.main:app --reload
```

Frontend:

```powershell
cd apps/web
npm install
npm run dev
```

Sem uma chave OpenAI, mantenha `LLM_PROVIDER=mock`. O fluxo completo funciona
com conteúdo determinístico para desenvolvimento.

## Verificação

```powershell
cd apps/api
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m ruff check app tests

cd ..\web
npm run lint
npm run build
```
