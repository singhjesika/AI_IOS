import React, { useMemo } from 'react'

// Usage:
//   Login page:  <Particles count={8} />
//   Home page:   <Particles count={12} />
//   Chat page:   handled by ChatBackground instead (richer effect)

export default function Particles({ count = 12 }) {
  const particles = useMemo(() => (
    Array.from({ length: count }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      size: 1 + Math.random() * 2.5,
      duration: 6 + Math.random() * 10,
      delay: Math.random() * 8,
      color: ['#00c8ff', '#00ffcc', '#ffffff'][Math.floor(Math.random() * 3)],
      opacity: 0.18 + Math.random() * 0.3,
    }))
  ), [count])

  return (
    <div className="particles-container">
      {particles.map(p => (
        <div
          key={p.id}
          className="particle"
          style={{
            left: `${p.left}%`,
            top: `${p.top}%`,
            width: `${p.size}px`,
            height: `${p.size}px`,
            background: p.color,
            opacity: p.opacity,
            animationDuration: `${p.duration}s`,
            animationDelay: `${p.delay}s`,
            boxShadow: `0 0 ${p.size * 2}px ${p.color}`,
          }}
        />
      ))}
    </div>
  )
}