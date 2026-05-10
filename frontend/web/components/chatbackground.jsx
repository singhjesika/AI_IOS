import React, { useEffect, useRef } from 'react'

export default function ChatBackground({ agentColor = '#00c8ff' }) {
  const mountRef = useRef(null)
  const canvasRef = useRef(null)
  const animRef = useRef(null)
  const mouseRef = useRef({ x: 0.5, y: 0.5 })

  // Particle canvas animation
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')

    let W = window.innerWidth
    let H = window.innerHeight
    canvas.width = W
    canvas.height = H

    // Parse agent color to rgba
    const hexToRgb = (hex) => {
      const r = parseInt(hex.slice(1,3),16)
      const g = parseInt(hex.slice(3,5),16)
      const b = parseInt(hex.slice(5,7),16)
      return `${r},${g},${b}`
    }
    const rgb = hexToRgb(agentColor)

    // Particle system
    const COUNT = 55
    const particles = Array.from({ length: COUNT }, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      r: 0.8 + Math.random() * 2.2,
      vx: (Math.random() - 0.5) * 0.35,
      vy: -0.18 - Math.random() * 0.45,
      opacity: 0.15 + Math.random() * 0.55,
      life: Math.random(),
      speed: 0.003 + Math.random() * 0.004,
      color: Math.random() > 0.45 ? rgb : '255,255,255',
    }))

    // Glowing orbs (large blobs)
    const orbs = [
      { x: 0.15, y: 0.25, r: 260, opacity: 0.055 },
      { x: 0.82, y: 0.65, r: 320, opacity: 0.04  },
      { x: 0.5,  y: 0.9,  r: 200, opacity: 0.035 },
    ]

    const onResize = () => {
      W = window.innerWidth; H = window.innerHeight
      canvas.width = W; canvas.height = H
    }
    window.addEventListener('resize', onResize)

    const onMouseMove = (e) => {
      mouseRef.current = { x: e.clientX / W, y: e.clientY / H }
    }
    window.addEventListener('mousemove', onMouseMove)

    let t = 0
    function draw() {
      animRef.current = requestAnimationFrame(draw)
      t += 0.008
      ctx.clearRect(0, 0, W, H)

      // === HEXAGON GRID ===
      const hexSize = 34
      const hexW = hexSize * Math.sqrt(3)
      const hexH = hexSize * 2
      const cols = Math.ceil(W / hexW) + 2
      const rows = Math.ceil(H / (hexH * 0.75)) + 2
      const offsetX = (mouseRef.current.x - 0.5) * 18
      const offsetY = (mouseRef.current.y - 0.5) * 12

      for (let row = -1; row < rows; row++) {
        for (let col = -1; col < cols; col++) {
          const cx = col * hexW + (row % 2 === 0 ? 0 : hexW / 2) + offsetX
          const cy = row * hexH * 0.75 + offsetY
          const dist = Math.hypot(cx - W * mouseRef.current.x, cy - H * mouseRef.current.y)
          const proximity = Math.max(0, 1 - dist / 380)
          const alpha = 0.03 + proximity * 0.09 + Math.sin(t + col * 0.4 + row * 0.3) * 0.012
          ctx.beginPath()
          for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i - Math.PI / 6
            const hx = cx + hexSize * Math.cos(angle)
            const hy = cy + hexSize * Math.sin(angle)
            i === 0 ? ctx.moveTo(hx, hy) : ctx.lineTo(hx, hy)
          }
          ctx.closePath()
          ctx.strokeStyle = `rgba(${rgb},${alpha})`
          ctx.lineWidth = 0.5
          ctx.stroke()
          // Occasional glow hex
          if (proximity > 0.55) {
            ctx.fillStyle = `rgba(${rgb},${proximity * 0.04})`
            ctx.fill()
          }
        }
      }

      // === GLOW ORBS (cursor-reactive) ===
      orbs.forEach((orb, i) => {
        const ox = orb.x * W + (mouseRef.current.x - 0.5) * 60 * (i % 2 === 0 ? 1 : -0.7)
        const oy = orb.y * H + (mouseRef.current.y - 0.5) * 40 * (i % 2 === 0 ? -0.5 : 1)
        const pulse = orb.opacity + Math.sin(t * 0.6 + i) * 0.015
        const grad = ctx.createRadialGradient(ox, oy, 0, ox, oy, orb.r)
        grad.addColorStop(0, `rgba(${rgb},${pulse})`)
        grad.addColorStop(0.5, `rgba(${rgb},${pulse * 0.4})`)
        grad.addColorStop(1, `rgba(${rgb},0)`)
        ctx.beginPath()
        ctx.arc(ox, oy, orb.r, 0, Math.PI * 2)
        ctx.fillStyle = grad
        ctx.fill()
      })

      // Mouse glow orb
      const mx = mouseRef.current.x * W
      const my = mouseRef.current.y * H
      const mGrad = ctx.createRadialGradient(mx, my, 0, mx, my, 180)
      mGrad.addColorStop(0, `rgba(${rgb},0.07)`)
      mGrad.addColorStop(1, `rgba(${rgb},0)`)
      ctx.beginPath()
      ctx.arc(mx, my, 180, 0, Math.PI * 2)
      ctx.fillStyle = mGrad
      ctx.fill()

      // === PARTICLES ===
      particles.forEach(p => {
        p.life += p.speed
        if (p.life > 1) {
          p.life = 0
          p.x = Math.random() * W
          p.y = H + 10
          p.vx = (Math.random() - 0.5) * 0.35
          p.vy = -0.18 - Math.random() * 0.45
        }
        p.x += p.vx
        p.y += p.vy
        const fade = p.life < 0.15 ? p.life / 0.15 : p.life > 0.75 ? (1 - p.life) / 0.25 : 1
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(${p.color},${p.opacity * fade})`
        ctx.fill()
        // Glow ring on bigger particles
        if (p.r > 1.8) {
          ctx.beginPath()
          ctx.arc(p.x, p.y, p.r * 2.5, 0, Math.PI * 2)
          ctx.fillStyle = `rgba(${p.color},${p.opacity * fade * 0.12})`
          ctx.fill()
        }
      })

      // === SCAN LINES (subtle horizontal) ===
      for (let i = 0; i < H; i += 4) {
        ctx.fillStyle = `rgba(0,0,0,${0.015 + (i % 8 === 0 ? 0.01 : 0)})`
        ctx.fillRect(0, i, W, 1)
      }
    }

    draw()

    return () => {
      cancelAnimationFrame(animRef.current)
      window.removeEventListener('resize', onResize)
      window.removeEventListener('mousemove', onMouseMove)
    }
  }, [agentColor])

  return (
    <>
      {/* Static CSS layers behind the canvas */}
      <div style={{
        position: 'fixed', inset: 0, zIndex: 0,
        background: 'radial-gradient(ellipse at 20% 30%, rgba(0,30,60,0.55) 0%, transparent 60%), radial-gradient(ellipse at 80% 70%, rgba(20,0,60,0.45) 0%, transparent 55%), #000',
        pointerEvents: 'none',
      }} />
      <canvas
        ref={canvasRef}
        style={{
          position: 'fixed', inset: 0, zIndex: 1,
          pointerEvents: 'none',
          mixBlendMode: 'screen',
        }}
      />
    </>
  )
}