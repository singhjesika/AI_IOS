import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Background3D from '../components/Background3D'
import ChatBackground from '../components/ChatBackground'
import Navbar from '../components/Navbar'
import Particles from '../components/Particles'

const agents = [
  { icon: '💰', name: 'Finance',  desc: 'Budget & investments',  color: '#00ff88', hint: 'Ask me about budgeting, investments, savings, or financial planning!' },
  { icon: '❤️', name: 'Health',   desc: 'Fitness & wellness',    color: '#ff4488', hint: 'Ask me about fitness, nutrition, mental wellness, or healthy habits!' },
  { icon: '📅', name: 'Planner',  desc: 'Tasks & schedule',      color: '#4488ff', hint: 'Ask me to plan your day, set reminders, or organize your schedule!' },
  { icon: '💻', name: 'Coding',   desc: 'Code assistant',        color: '#00ffcc', hint: 'Ask me to write code, debug errors, or review your code!' },
  { icon: '🎓', name: 'Study',    desc: 'Learning & research',   color: '#ffcc00', hint: 'Ask me to explain topics, make study plans, or quiz you!' },
  { icon: '✈️', name: 'Travel',   desc: 'Trip planning',         color: '#00ccff', hint: 'Ask me to plan trips, find destinations, or suggest itineraries!' },
  { icon: '🛒', name: 'Shopping', desc: 'Smart shopping',        color: '#ff8800', hint: 'Ask me for product recommendations, price comparisons, or shopping advice!' },
  { icon: '💼', name: 'Career',   desc: 'Job & growth',          color: '#aa88ff', hint: 'Ask me for resume tips, interview prep, or career advice!' },
]

const stats = [
  { icon: '🚀', label: 'API Status',    value: 'Online', color: '#00ff88' },
  { icon: '🧠', label: 'AI Tasks Today', value: '24',    color: '#00c8ff' },
  { icon: '⚡', label: 'Response Time', value: '142ms',  color: '#ffaa00' },
  { icon: '🔥', label: 'Streak Days',   value: '7',      color: '#ff6644' },
]

export default function Dashboard({ user, onLogout }) {
  const [activePage, setActivePage] = useState('home')
  const [activeAgent, setActiveAgent] = useState(agents[0])
  const [chat, setChat] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    if (window.speechSynthesis) {
      const msg = new SpeechSynthesisUtterance(`Welcome back, ${user?.name || 'there'}! Your AI dashboard is ready.`)
      msg.pitch = 1.4
      msg.rate = 0.95
      const voices = window.speechSynthesis.getVoices()
      const female = voices.find(v => /female|zira|samantha|victoria|karen/i.test(v.name))
      if (female) msg.voice = female
      setTimeout(() => window.speechSynthesis.speak(msg), 400)
    }
    return () => window.speechSynthesis?.cancel()
  }, [])

  function handleLogout() {
    window.speechSynthesis?.cancel()
    onLogout()
    navigate('/login')
  }

  function openAgent(agent) {
    setActiveAgent(agent)
    setChat([{
      role: 'ai',
      text: `${agent.icon} Hi ${user?.name || 'there'}! I'm your ${agent.name} AI assistant. ${agent.hint}`,
    }])
    setActivePage('chat')
    window.speechSynthesis?.cancel()
    if (window.speechSynthesis) {
      const msg = new SpeechSynthesisUtterance(`Hi! I'm your ${agent.name} assistant. How can I help you today?`)
      msg.pitch = 1.4; msg.rate = 0.95
      const v = window.speechSynthesis.getVoices()
      const f = v.find(x => /female|zira|samantha|victoria|karen/i.test(x.name))
      if (f) msg.voice = f
      window.speechSynthesis.speak(msg)
    }
  }

  async function sendMessage() {
    if (!input.trim()) return
    const userMsg = { role: 'user', text: input }
    setChat(prev => [...prev, userMsg])
    const sent = input
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('http://127.0.0.1:8000/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: sent,
          agent: activeAgent.name,
          history: chat.map(m => ({ role: m.role === 'ai' ? 'assistant' : 'user', content: m.text }))
        })
      })
      const data = await res.json()
      const reply = data.response || data.message || 'Got it!'
      setChat(prev => [...prev, { role: 'ai', text: reply }])
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel()
        const m = new SpeechSynthesisUtterance(reply.substring(0, 150))
        m.pitch = 1.4; m.rate = 0.95
        window.speechSynthesis.speak(m)
      }
    } catch {
      setChat(prev => [...prev, { role: 'ai', text: "⚠️ I need a connection to answer. Please check your backend!" }])
    } finally {
      setLoading(false)
    }
  }

  const isChatPage = activePage === 'chat'

  return (
    <div className="page-dashboard">
      {/* Background: rich chat bg on chat page, simple 3D elsewhere */}
      {isChatPage
        ? <ChatBackground agentColor={activeAgent.color} />
        : (
          <>
            <Background3D />
            {/* Subtle particles on dashboard home — not chat */}
            <Particles count={10} />
          </>
        )
      }

      <Navbar user={user} onLogout={handleLogout} activePage={activePage} onNavigate={setActivePage} />

      <main className="dash-main" style={{ position: 'relative', zIndex: 10 }}>
        {activePage === 'home' && (
          <>
            <div className="welcome-banner fade-in">
              <div className="welcome-avatar">😊📚</div>
              <div className="welcome-text">
                <h2>Welcome back, {user?.name || 'there'}!</h2>
                <p>Your AI universe is ready. What would you like to explore today?</p>
              </div>
            </div>

            <div className="section-title">System Status</div>
            <div className="stats-grid">
              {stats.map(s => (
                <div className="stat-card" key={s.label}>
                  <div className="stat-icon">{s.icon}</div>
                  <div className="stat-label">{s.label}</div>
                  <div className="stat-value" style={{ color: s.color }}>{s.value}</div>
                </div>
              ))}
            </div>

            <div className="section-title" style={{ marginTop: 30 }}>AI Agents</div>
            <div className="agents-grid">
              {agents.map(a => (
                <div className="agent-card" key={a.name} onClick={() => openAgent(a)}>
                  <div className="agent-icon">{a.icon}</div>
                  <div className="agent-name">{a.name}</div>
                  <div className="agent-desc">{a.desc}</div>
                </div>
              ))}
            </div>
          </>
        )}

        {isChatPage && (
          <div className="chat-panel fade-in">
            {/* Agent header bar */}
            <div style={{
              display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20,
              padding: '16px 24px',
              background: 'rgba(0,0,0,0.45)',
              border: `1px solid ${activeAgent.color}33`,
              borderRadius: 16,
              backdropFilter: 'blur(16px)',
            }}>
              <span style={{ fontSize: 36 }}>{activeAgent.icon}</span>
              <div>
                <div style={{ fontFamily: 'Orbitron, monospace', fontSize: 18, color: activeAgent.color, letterSpacing: 2 }}>
                  {activeAgent.name} Agent
                </div>
                <div style={{ fontSize: 13, color: 'rgba(255,255,255,0.4)', marginTop: 2 }}>
                  {activeAgent.hint}
                </div>
              </div>
              <button
                onClick={() => setActivePage('home')}
                style={{
                  marginLeft: 'auto', padding: '8px 18px', borderRadius: 10,
                  background: 'rgba(255,70,70,0.12)', border: '1px solid rgba(255,70,70,0.35)',
                  color: '#ff5555', cursor: 'pointer', fontFamily: 'Rajdhani, sans-serif',
                  fontSize: 13, letterSpacing: 1,
                }}
              >
                ✕ Close
              </button>
            </div>

            <div className="chat-messages">
              {chat.map((m, i) => (
                <div key={i} className={`chat-msg ${m.role}`}>
                  <span className="chat-icon">{m.role === 'user' ? '👤' : '🤖'}</span>
                  <div
                    className="chat-text"
                    style={m.role === 'ai' ? {
                      background: 'rgba(0,0,0,0.55)',
                      border: `1px solid ${activeAgent.color}22`,
                      backdropFilter: 'blur(12px)',
                    } : undefined}
                  >
                    {m.text}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="chat-msg ai">
                  <span className="chat-icon">🤖</span>
                  <div className="chat-text typing" style={{ background: 'rgba(0,0,0,0.45)', backdropFilter: 'blur(12px)' }}>
                    Thinking...
                  </div>
                </div>
              )}
            </div>

            <div className="chat-input-row">
              <input
                className="chat-input"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && sendMessage()}
                placeholder={`Ask ${activeAgent.name} anything...`}
                style={{
                  background: 'rgba(0,0,0,0.5)',
                  border: `1px solid ${activeAgent.color}33`,
                  backdropFilter: 'blur(12px)',
                }}
              />
              <button
                className="chat-send"
                onClick={sendMessage}
                style={{
                  background: `rgba(${parseInt(activeAgent.color.slice(1,3),16)},${parseInt(activeAgent.color.slice(3,5),16)},${parseInt(activeAgent.color.slice(5,7),16)},0.18)`,
                  border: `1px solid ${activeAgent.color}55`,
                  color: activeAgent.color,
                }}
              >
                Send ➤
              </button>
            </div>
          </div>
        )}

        {!['home', 'chat'].includes(activePage) && (
          <div className="coming-soon fade-in">
            <div style={{ fontSize: 64, marginBottom: 20 }}>🚀</div>
            <h2 style={{ fontFamily: 'Orbitron', color: '#00c8ff', marginBottom: 10 }}>
              {activePage.toUpperCase()}
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.4)' }}>
              Coming soon — connect your backend to activate this agent.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}