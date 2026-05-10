import React, { useState } from 'react'

const navItems = [
  { icon: '🏠', label: 'Home', id: 'home' },
  { icon: '🧠', label: 'AI Chat', id: 'chat' },
  { icon: '📅', label: 'Planner', id: 'planner' },
  { icon: '💰', label: 'Finance', id: 'finance' },
  { icon: '❤️', label: 'Health', id: 'health' },
  { icon: '📊', label: 'Analytics', id: 'analytics' },
]

export default function Navbar({ user, onLogout, activePage, onNavigate }) {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <nav className={`navbar ${collapsed ? 'collapsed' : ''}`}>
      <div className="nav-logo" onClick={() => setCollapsed(!collapsed)}>
        {collapsed ? '⊕' : '⊕ AI_IOS'}
      </div>

      <div className="nav-items">
        {navItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${activePage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
            title={collapsed ? item.label : ''}
          >
            <span className="nav-icon">{item.icon}</span>
            {!collapsed && <span className="nav-label">{item.label}</span>}
          </button>
        ))}
      </div>

      <div className="nav-footer">
        <div className="nav-user">
          <span className="nav-icon">😊</span>
          {!collapsed && <span className="nav-label">{user?.name || 'Jesika'}</span>}
        </div>
        <button className="nav-logout" onClick={onLogout} title="Logout">
          {collapsed ? '🚪' : '🚪 Logout'}
        </button>
      </div>
    </nav>
  )
}