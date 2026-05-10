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
```

---

## 🚀 Quick Start

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