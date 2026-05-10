
"""
AI_IOS - Streamlit Web App with Beautiful Login UI
"""
import streamlit as st
import requests

# ─── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="AI_IOS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000/api"

# ─── Session State ─────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def api_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def login(email: str, password: str) -> bool:
    try:
        resp = requests.post(
            f"{API_BASE}/auth/login",
            data={"username": email, "password": password},
        )
        if resp.status_code == 200:
            st.session_state.token = resp.json()["access_token"]
            profile = requests.get(f"{API_BASE}/user/me", headers=api_headers())
            st.session_state.user = profile.json()
            return True
    except Exception:
        pass
    return False


def signup(name: str, email: str, password: str) -> bool:
    try:
        resp = requests.post(
            f"{API_BASE}/auth/signup",
            json={"name": name, "email": email, "password": password},
        )
        return resp.status_code == 201
    except Exception:
        return False


def send_message(message: str) -> dict:
    try:
        resp = requests.post(
            f"{API_BASE}/ai/chat",
            json={"message": message},
            headers=api_headers(),
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return {"reply": "Error reaching AI service.", "agent": "error"}


# ─── Auth Page ─────────────────────────────────────────
def auth_page():
    st.title("🤖 AI_IOS")
    st.subheader("Your Personal AI Assistant")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        email    = st.text_input("Email",    key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            if login(email, password):
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab_signup:
        name     = st.text_input("Full Name", key="signup_name")
        email_s  = st.text_input("Email",     key="signup_email")
        pass_s   = st.text_input("Password",  type="password", key="signup_pass")
        if st.button("Create Account", use_container_width=True):
            if signup(name, email_s, pass_s):
                st.success("Account created! Please login.")
            else:
                st.error("Signup failed. Email may already exist.")


# ─── Main App ──────────────────────────────────────────
def main_app():
    user = st.session_state.user

    # Sidebar
    with st.sidebar:
        st.title("🤖 AI_IOS")
        st.write(f"👤 {user.get('name', 'User')}")
        st.divider()
        page = st.radio(
            "Navigate",
            ["💬 Chat", "✅ Tasks", "💰 Finance", "🏃 Health", "📅 Planner", "📊 Analytics"],
        )
        st.divider()
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user  = None
            st.session_state.messages = []
            st.rerun()

    # Pages
    if page == "💬 Chat":
        chat_page()
    elif page == "✅ Tasks":
        tasks_page()
    elif page == "💰 Finance":
        finance_page()
    elif page == "🏃 Health":
        health_page()
    elif page == "📅 Planner":
        planner_page()
    elif page == "📊 Analytics":
        analytics_page()


# ─── Chat Page ─────────────────────────────────────────
def chat_page():
    st.header("💬 Chat with AI_IOS")

    # Show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and "agent" in msg:
                st.caption(f"🤖 Handled by: {msg['agent']} agent")

    # Input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = send_message(prompt)
            reply = result.get("reply", "No response.")
            agent = result.get("agent", "general")
            st.write(reply)
            st.caption(f"🤖 Handled by: {agent} agent")

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply,
            "agent": agent,
        })

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            requests.delete(f"{API_BASE}/ai/history", headers=api_headers())
            st.rerun()


# ─── Tasks Page ────────────────────────────────────────
def tasks_page():
    st.header("✅ Tasks")

    try:
        tasks = requests.get(f"{API_BASE}/tasks/", headers=api_headers()).json()
    except Exception:
        tasks = []

    with st.expander("➕ New Task"):
        title    = st.text_input("Title")
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        if st.button("Add Task"):
            requests.post(
                f"{API_BASE}/tasks/",
                json={"title": title, "priority": priority},
                headers=api_headers(),
            )
            st.rerun()

    if not tasks:
        st.info("No tasks yet. Create one above!")
    else:
        for task in tasks:
            col1, col2, col3 = st.columns([6, 2, 1])
            with col1:
                done = "✅" if task["is_completed"] else "⬜"
                st.write(f"{done} **{task['title']}**")
            with col2:
                priority_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                st.write(priority_colors.get(task["priority"], "⚪") + " " + task["priority"])
            with col3:
                if st.button("🗑️", key=f"del_{task['id']}"):
                    requests.delete(f"{API_BASE}/tasks/{task['id']}", headers=api_headers())
                    st.rerun()


# ─── Finance Page ──────────────────────────────────────
def finance_page():
    st.header("💰 Finance")
    try:
        summary  = requests.get(f"{API_BASE}/finance/summary",  headers=api_headers()).json()
        insights = requests.get(f"{API_BASE}/finance/insights", headers=api_headers()).json()
    except Exception:
        summary = {}
        insights = {}

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expenses", f"${summary.get('total_expenses_this_month', 0):,.2f}")
    col2.metric("Budget Remaining", f"${summary.get('budget_remaining', 0):,.2f}")
    col3.metric("Top Category", summary.get("top_categories", ["-"])[0] if summary.get("top_categories") else "-")

    st.divider()
    st.subheader("💡 AI Insights")
    st.info(insights.get("insights", "No insights yet."))

    with st.expander("➕ Log Expense"):
        amount   = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Health", "Entertainment", "Other"])
        desc     = st.text_input("Description")
        if st.button("Add Expense"):
            requests.post(
                f"{API_BASE}/finance/expense",
                params={"amount": amount, "category": category, "description": desc},
                headers=api_headers(),
            )
            st.success("Expense logged!")


# ─── Health Page ───────────────────────────────────────
def health_page():
    st.header("🏃 Health")
    try:
        summary = requests.get(f"{API_BASE}/health/summary", headers=api_headers()).json()
        recs    = requests.get(f"{API_BASE}/health/recommendations", headers=api_headers()).json()
    except Exception:
        summary = {}
        recs    = {}

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Steps",       summary.get("steps", 0))
    col2.metric("Calories",    summary.get("calories", 0))
    col3.metric("Sleep (hrs)", summary.get("sleep_hours", 0))
    col4.metric("Water (ml)",  summary.get("water_ml", 0))

    st.divider()
    st.subheader("💡 Health Recommendations")
    st.info(recs.get("recommendations", "No recommendations yet."))

    with st.expander("📝 Log Metric"):
        metric = st.selectbox("Metric", ["steps", "calories", "sleep_hours", "water_ml", "weight"])
        value  = st.number_input("Value", min_value=0.0, step=1.0)
        unit   = st.text_input("Unit (optional)")
        if st.button("Log"):
            requests.post(
                f"{API_BASE}/health/log",
                params={"metric": metric, "value": value, "unit": unit},
                headers=api_headers(),
            )
            st.success("Metric logged!")


# ─── Planner Page ──────────────────────────────────────
def planner_page():
    st.header("📅 Planner")
    try:
        today  = requests.get(f"{API_BASE}/planner/today",  headers=api_headers()).json()
        events = requests.get(f"{API_BASE}/planner/events", headers=api_headers()).json()
    except Exception:
        today  = {}
        events = []

    st.subheader("Today's Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Events",    len(today.get("events", [])))
    col2.metric("Tasks",     len(today.get("tasks", [])))
    col3.metric("Reminders", len(today.get("reminders", [])))

    with st.expander("➕ Add Event"):
        title = st.text_input("Event Title")
        date  = st.date_input("Date")
        time  = st.time_input("Time")
        notes = st.text_area("Notes")
        if st.button("Save Event"):
            requests.post(
                f"{API_BASE}/planner/events",
                params={"title": title, "date": str(date), "time": str(time), "notes": notes},
                headers=api_headers(),
            )
            st.success("Event saved!")


# ─── Analytics Page ────────────────────────────────────
def analytics_page():
    st.header("📊 Analytics")
    try:
        dashboard = requests.get(f"{API_BASE}/analytics/dashboard", headers=api_headers()).json()
        agents    = requests.get(f"{API_BASE}/analytics/agents",    headers=api_headers()).json()
    except Exception:
        dashboard = {}
        agents    = {}

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Messages", dashboard.get("total_messages", 0))
    col2.metric("Streak Days",    dashboard.get("streak_days", 0))
    col3.metric("Agents Used",    len(dashboard.get("agents_used", [])))

    st.divider()
    st.subheader("Agent Usage Breakdown")
    agent_counts = agents.get("agent_counts", {})
    if agent_counts:
        import pandas as pd
        df = pd.DataFrame(agent_counts.items(), columns=["Agent", "Count"])
        st.bar_chart(df.set_index("Agent"))
    else:
        st.info("No agent usage data yet.")


# ─── Entry ─────────────────────────────────────────────
if st.session_state.token:
    main_app()
else:
    auth_page()