import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Background3D from '../components/Background3D'
import Particles from '../components/Particles'

export default function Home() {
  const navigate = useNavigate()

  useEffect(() => {
    // Auto redirect to login after 3s or on click
  }, [])

  return (
    <div className="page-home">
      <Background3D />
      {/* Reduced from 40 → 12 particles on home page */}
      <Particles count={12} />
      <div className="home-content fade-in">
        <div style={{ fontSize: 80, marginBottom: 20, filter: 'drop-shadow(0 0 30px rgba(0,200,255,0.6))' }}>
          😊
        </div>
        <h1 className="home-title">AI_IOS</h1>
        <p className="home-sub">Your Personal Intelligent Operating System</p>
        <div className="home-features">
          <span>🧠 Finance</span>
          <span>❤️ Health</span>
          <span>📅 Planner</span>
          <span>💻 Coding</span>
          <span>✈️ Travel</span>
        </div>
        <button className="btn-login" style={{ width: 260, marginTop: 40 }} onClick={() => navigate('/login')}>
          ENTER YOUR AI UNIVERSE
        </button>
      </div>
    </div>
  )
}