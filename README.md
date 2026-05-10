<<<<<<< HEAD
# 🤖 AI_IOS – Your Personal AI Assistant Platform

A full-stack, multi-agent AI assistant with a FastAPI backend, Streamlit frontend, and ML-powered intent routing.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Multi-agent Chat** | Finance, Health, Planner, Coding, Study, Travel, Shopping, Career, Memory |
| 🧠 **ML Intent Routing** | TF-IDF + Logistic Regression classifier routes queries to the right agent |
| 🔐 **JWT Auth** | Secure signup / login with bcrypt password hashing |
| ✅ **Task Manager** | Full CRUD task management with priorities and due dates |
| 💰 **Finance Tracker** | Expense logging, budget overview, AI-generated insights |
| 🏃 **Health Tracker** | Log steps, calories, sleep, weight; AI recommendations |
| 📅 **Smart Planner** | Calendar events, daily overview, AI schedule suggestions |
| 🎙️ **Voice Support** | Speech-to-text transcription and text-to-speech synthesis |
| 📊 **Analytics** | Usage dashboard, agent breakdown, activity streaks |
| 🌐 **Streamlit UI** | Ready-to-use web frontend with full API integration |

---

## 🗂️ Project Structure

```
AI_IOS/
├── backend/          # FastAPI application
│   ├── main.py       # Entry point
│   ├── database.py   # Async SQLAlchemy setup
│   └── app/
│       ├── agents/   # 9 specialist AI agents + orchestrator
│       ├── api/      # REST routes
│       ├── config/   # Settings + JWT security
│       ├── ml/       # Intent & sentiment ML models
│       ├── models/   # SQLAlchemy ORM models
│       ├── schemas/  # Pydantic request/response models
│       ├── services/ # Business logic layer
│       ├── tests/    # Pytest test suite
│       └── utils/    # Logger, helpers, prompts, validators
├── frontend/
│   └── streamlit_app/  # Full Streamlit web UI
├── scripts/            # DB init, seed, deploy
├── data/               # Sample data files
└── docs/               # Architecture & API docs
=======
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
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd
```

---

## 🚀 Quick Start

<<<<<<< HEAD
### 1. Clone & Setup

```bash
git clone https://github.com/yourname/AI_IOS.git
cd AI_IOS
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env .env.local
# Edit .env.local and add your ANTHROPIC_API_KEY
```

### 3. Initialise Database

```bash
cd backend
python ../scripts/init_db.py
python ../scripts/seed.py    # optional: load sample data
```

### 4. Train ML Models

```bash
cd backend
python app/ml/train_intent.py
python app/ml/train_sentiment.py
python app/ml/recommend.py
```

### 5. Start Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

### 6. Start Streamlit Frontend

```bash
cd frontend/streamlit_app
streamlit run app.py
```
App: http://localhost:8501

### 7. One-command Deploy

```bash
bash scripts/deploy.sh dev     # development
bash scripts/deploy.sh prod    # production
```

---

## 🧪 Running Tests

```bash
cd backend
pytest app/tests/ -v
```

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) |
| `SECRET_KEY` | JWT signing secret |
| `DATABASE_URL` | SQLite (default) or PostgreSQL |
| `DEFAULT_MODEL` | Claude model to use |

---

## 🤖 Agents

| Agent | Triggers | Speciality |
|-------|----------|------------|
| Finance | money, budget, expense | Financial planning |
| Health | health, workout, sleep | Wellness coaching |
| Planner | schedule, reminder, event | Time management |
| Coding | code, debug, function | Programming help |
| Study | learn, exam, quiz | Tutoring |
| Travel | trip, flight, visa | Travel planning |
| Shopping | buy, product, price | Product recommendations |
| Career | resume, job, interview | Career coaching |
| Memory | remember, recall | History lookup |

---

## 📄 License

MIT License – feel free to use and modify.
=======
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
>>>>>>> 7c6fe786d0ebce90909c90ce7f1ac9867d4e86fd
