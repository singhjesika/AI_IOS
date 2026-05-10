# AI_IOS – Architecture

## Overview

AI_IOS is a multi-agent AI personal assistant platform. Users interact through a chat interface; an **Orchestrator** classifies the intent and routes the query to the appropriate specialist agent.

---

## System Diagram

```
User ──► Frontend (Streamlit / React)
            │
            ▼
       FastAPI Backend
            │
     ┌──────┴──────────────────┐
     │       Orchestrator       │
     └──────┬──────────────────┘
            │ intent detection (keyword + ML)
            ▼
  ┌─────────────────────────────────────┐
  │  Finance  Health  Planner  Coding   │
  │  Study    Travel  Shopping Career   │
  │  Memory   (General fallback)        │
  └─────────────────────────────────────┘
            │
     Anthropic Claude API (LLM)
```

---

## Components

### Backend (`backend/`)
- **FastAPI** app with async SQLAlchemy (SQLite dev / PostgreSQL prod)
- **JWT** authentication via `python-jose` + `passlib`
- **Agents** – each agent has a specialist system prompt + optional service context
- **Services** – business logic layer between routes and models
- **ML** – TF-IDF + Logistic Regression for intent and sentiment classification

### Frontend (`frontend/streamlit_app/`)
- Full-page Streamlit application with multi-page navigation
- Communicates with backend via REST API

### ML Pipeline
| Model | Algorithm | Purpose |
|-------|-----------|---------|
| `intent_classifier.pkl` | TF-IDF + LR | Route query to correct agent |
| `sentiment_model.pkl`   | TF-IDF + LR | Detect user sentiment |
| `recommendation_model.pkl` | Markov chain | Suggest next agent |

---

## Data Flow

1. User sends a message via chat UI
2. FastAPI `/api/ai/chat` receives it (JWT-authenticated)
3. `Orchestrator.handle()` runs intent detection (ML → keyword fallback)
4. Matched agent builds a contextual system prompt + calls `AIService.complete()`
5. Response is stored in `Memory` table and returned to client

---

## Database Schema (simplified)

```
users         id, name, email, hashed_password, is_active
tasks         id, user_id, title, priority, is_completed, due_date
memories      id, user_id, role, content, created_at
subscriptions id, user_id, plan, is_active, expires_at
```