# 🧠 AI-IOS — AI Life Optimization System

> Full-stack AI platform for intelligent daily decision-making — built with FastAPI + Python 3.12

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── agents/
│   │   ├── __init__.py          ← AgentOrchestrator (auto-router)
│   │   ├── finance_agent.py     ← Budget, savings, investments
│   │   ├── health_agent.py      ← Sleep, exercise, nutrition
│   │   └── planner_agent.py     ← Tasks, focus, scheduling
│   ├── api/routes/
│   │   ├── user.py              ← Auth, profile endpoints
│   │   ├── task.py              ← Task CRUD + AI suggest
│   │   └── ai.py                ← Agent chat + voice
│   ├── models/
│   │   ├── user_model.py        ← SQLAlchemy User ORM
│   │   └── task_model.py        ← SQLAlchemy Task ORM
│   ├── schemas/
│   │   ├── user_schemas.py      ← Pydantic request/response
│   │   └── task_model.py        ← Pydantic request/response
│   ├── services/
│   │   ├── user_service.py      ← User business logic
│   │   ├── task_service.py      ← Task business logic
│   │   └── ai_service.py        ← OpenAI / Anthropic wrapper
│   ├── utils/
│   │   └── helper.py            ← JWT, hashing, pagination
│   ├── config.py                ← Pydantic Settings
│   ├── database.py              ← SQLAlchemy engine + session
│   └── main.py                  ← FastAPI app entry point
├── requirements.txt
└── .env.example
```

---

## 🚀 Quick Start

### 1. Clone & enter the backend folder
```bash
git clone <repo-url>
cd backend
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY and ANTHROPIC_API_KEY
```

### 5. Run the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open API docs
- Swagger UI → http://localhost:8000/docs
- ReDoc      → http://localhost:8000/redoc

---

## 🔑 Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/register` | Register new user |
| POST | `/api/v1/users/login` | Login & get JWT token |
| GET | `/api/v1/users/me` | Get current user profile |
| PUT | `/api/v1/users/me` | Update profile |
| POST | `/api/v1/tasks/` | Create a task |
| GET | `/api/v1/tasks/` | List tasks (filterable) |
| PUT | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete task |
| POST | `/api/v1/tasks/ai/suggest` | AI task breakdown from a goal |
| GET | `/api/v1/tasks/ai/insight` | Daily productivity insight |
| POST | `/api/v1/ai/chat` | Chat with AI agent |
| POST | `/api/v1/ai/voice` | Voice query (text transcript) |
| GET | `/api/v1/ai/agents` | List available agents |

---

## 🤖 AI Agents

| Agent | Triggers | Powered By |
|-------|----------|------------|
| **Health** | sleep, exercise, diet, stress… | GPT-4o |
| **Finance** | money, budget, invest, save… | GPT-4o |
| **Planner** | task, focus, schedule, goal… | GPT-4o (default) |

---

## 🧪 Run Tests
```bash
pytest tests/ -v --asyncio-mode=auto
```

---

## 🏗 Tech Stack

- **FastAPI** + **Uvicorn** — async REST API
- **SQLAlchemy 2** (async) + **SQLite** (dev) / **PostgreSQL** (prod)
- **Pydantic v2** — validation & settings
- **OpenAI GPT-4o** + **Anthropic Claude** — AI agents
- **python-jose** — JWT authentication
- **passlib / bcrypt** — password hashing
- **Loguru** — structured logging
