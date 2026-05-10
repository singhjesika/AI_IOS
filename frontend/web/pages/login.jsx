import React from 'react'
import { useNavigate } from 'react-router-dom'
import Background3D from '../components/Background3D'
import FloatingAvatar from '../components/FloatingAvatar'
import GlassLogin from '../components/GlassLogin'
import Particles from '../components/Particles'

export default function LoginPage({ onLogin }) {
  const navigate = useNavigate()

  function handleLogin(user) {
    onLogin(user)
    navigate('/dashboard')
  }

  return (
    <div className="page-login">
      <Background3D />
      {/* Reduced from 30 → 8 particles on login page */}
      <Particles count={8} />
      <div className="login-content">
        <FloatingAvatar greet={true} />
        <GlassLogin onLogin={handleLogin} />
      </div>
    </div>
  )
}