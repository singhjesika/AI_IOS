import React, { useState } from 'react'

export default function GlassLogin({ onLogin }) {
  const [tab, setTab] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit() {
    setError('')
    if (!email || !password) { setError('Please fill in all fields.'); return }
    setLoading(true)

    try {
      const endpoint = tab === 'login' ? '/api/auth/login' : '/api/auth/register'
      const body = tab === 'login' ? { email, password } : { email, password, full_name: name }
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      const data = await res.json().catch(() => ({}))
      if (res.ok) {
        onLogin({ email, name: name || 'Jesika', token: data.access_token })
      } else {
        setError(data.detail || 'Something went wrong.')
      }
    } catch {
      // Demo fallback
      if (email === 'jesika@ai.com' && password === '1234') {
        onLogin({ email, name: 'Jesika', token: 'demo' })
      } else {
        setError('Demo mode: use jesika@ai.com / 1234')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-glass fade-in">
      <div className="logo">⊕ AI_IOS</div>
      <div className="tagline">Your Personal AI Assistant</div>
      <div className="scan-line" />

      <div className="tabs">
        <button className={`tab ${tab === 'login' ? 'active' : ''}`} onClick={() => setTab('login')}>Login</button>
        <button className={`tab ${tab === 'signup' ? 'active' : ''}`} onClick={() => setTab('signup')}>Sign Up</button>
      </div>

      {tab === 'signup' && (
        <div className="field">
          <label>Full Name</label>
          <input value={name} onChange={e => setName(e.target.value)} placeholder="Jesika" />
        </div>
      )}
      <div className="field">
        <label>Email</label>
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="jesika@ai.com" />
      </div>
      <div className="field">
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="••••••••"
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        />
      </div>

      <button className="btn-login" onClick={handleSubmit} disabled={loading}>
        {loading ? 'CONNECTING...' : tab === 'login' ? 'LOGIN' : 'CREATE ACCOUNT'}
      </button>
      <div className="error-msg">{error}</div>
    </div>
  )
}