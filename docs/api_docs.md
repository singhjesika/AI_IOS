# AI_IOS – API Documentation

Base URL: `http://localhost:8000/api`

---

## Auth

### POST `/auth/signup`
Register a new user.
```json
{ "name": "Alice", "email": "alice@example.com", "password": "Alice123" }
```

### POST `/auth/login`
Returns a JWT access token (form-data: `username`, `password`).

---

## User

### GET `/user/me`
Returns the authenticated user's profile.

### PUT `/user/me`
Update name or avatar URL.

### DELETE `/user/me`
Delete the account.

---

## AI Chat

### POST `/ai/chat`
```json
{ "message": "Help me plan my budget", "context": {} }
```
Returns:
```json
{ "reply": "...", "agent": "finance" }
```

### GET `/ai/history?limit=20`
Recent chat messages.

### DELETE `/ai/history`
Clear all chat history.

---

## Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/tasks/` | List all tasks |
| POST   | `/tasks/` | Create task |
| GET    | `/tasks/{id}` | Get single task |
| PUT    | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

---

## Finance

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/finance/summary` | Monthly summary |
| POST   | `/finance/expense` | Log expense |
| GET    | `/finance/expenses` | List expenses |
| GET    | `/finance/budget` | Budget overview |
| GET    | `/finance/insights` | AI insights |

---

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/health/summary` | Health metrics summary |
| POST   | `/health/log` | Log a metric |
| GET    | `/health/logs` | View logs |
| GET    | `/health/recommendations` | AI recommendations |

---

## Planner

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/planner/events` | List events |
| POST   | `/planner/events` | Create event |
| GET    | `/planner/today` | Today's plan |
| GET    | `/planner/suggest` | AI schedule suggestion |

---

## Voice

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/voice/transcribe` | Audio → text (file upload) |
| POST   | `/voice/synthesize` | Text → audio (base64) |

---

## Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/analytics/dashboard` | Dashboard stats |
| GET    | `/analytics/usage?days=7` | Usage over time |
| GET    | `/analytics/agents` | Agent usage breakdown |

---

## Errors

| Code | Meaning |
|------|---------|
| 400  | Bad request / validation error |
| 401  | Unauthorized – missing or invalid JWT |
| 404  | Resource not found |
| 500  | Internal server error |