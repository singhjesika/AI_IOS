/**
 * chatParticles.js
 * ─────────────────────────────────────────────
 * Drop this script into your HTML agent/chat page.
 * It creates a full-screen canvas with:
 *   • Animated hexagon grid (mouse-reactive)
 *   • Glowing orb blobs (cursor-reactive)
 *   • Rising particles
 *   • Subtle scan lines
 *
 * Usage:
 *   <canvas id="chat-bg-canvas"></canvas>
 *   <script src="chatParticles.js"></script>
 *   <script>initChatBg({ color: '#00c8ff' })</script>
 *
 * Or call  updateChatBgColor('#ffcc00')  when agent changes.
 * ─────────────────────────────────────────────
 */

;(function (global) {
  let _canvas, _ctx, _raf, _W, _H
  let _rgb = '0,200,255'
  let _mouse = { x: 0.5, y: 0.5 }
  let _particles = []
  let _t = 0
  let _orbs = []
  let _running = false

  function hexToRgb(hex) {
    hex = hex.replace('#', '')
    if (hex.length === 3) hex = hex.split('').map(c => c+c).join('')
    return [
      parseInt(hex.slice(0,2),16),
      parseInt(hex.slice(2,4),16),
      parseInt(hex.slice(4,6),16),
    ].join(',')
  }

  function makeParticles() {
    _particles = Array.from({ length: 60 }, () => resetParticle({}))
  }

  function resetParticle(p) {
    p.x    = Math.random() * _W
    p.y    = _H + 5 + Math.random() * 100
    p.r    = 0.7 + Math.random() * 2.2
    p.vx   = (Math.random() - 0.5) * 0.38
    p.vy   = -(0.2 + Math.random() * 0.5)
    p.life = 0
    p.speed= 0.003 + Math.random() * 0.004
    p.opacity = 0.18 + Math.random() * 0.55
    p.useAccent = Math.random() > 0.45
    return p
  }

  function makeOrbs() {
    _orbs = [
      { rx: 0.15, ry: 0.25, r: 260, o: 0.055, dx: 1,    dy: -0.5 },
      { rx: 0.82, ry: 0.65, r: 320, o: 0.04,  dx: -0.7, dy:  1   },
      { rx: 0.5,  ry: 0.9,  r: 200, o: 0.035, dx: 0.6,  dy: -0.8 },
    ]
  }

  function drawFrame() {
    _raf = requestAnimationFrame(drawFrame)
    _t += 0.008
    _ctx.clearRect(0, 0, _W, _H)

    const mx = _mouse.x, my = _mouse.y
    const hexSize = 34
    const hexW = hexSize * Math.sqrt(3)
    const hexH = hexSize * 2
    const cols = Math.ceil(_W / hexW) + 2
    const rows = Math.ceil(_H / (hexH * 0.75)) + 2
    const offX  = (mx - 0.5) * 18
    const offY  = (my - 0.5) * 12

    // ─── Hexagon grid ───────────────────────────────────────────
    for (let row = -1; row < rows; row++) {
      for (let col = -1; col < cols; col++) {
        const cx = col * hexW + (row % 2 === 0 ? 0 : hexW / 2) + offX
        const cy = row * hexH * 0.75 + offY
        const dist = Math.hypot(cx - mx * _W, cy - my * _H)
        const prox = Math.max(0, 1 - dist / 380)
        const alpha = 0.028 + prox * 0.09 + Math.sin(_t + col * 0.4 + row * 0.3) * 0.012
        _ctx.beginPath()
        for (let i = 0; i < 6; i++) {
          const angle = (Math.PI / 3) * i - Math.PI / 6
          const hx = cx + hexSize * Math.cos(angle)
          const hy = cy + hexSize * Math.sin(angle)
          i === 0 ? _ctx.moveTo(hx, hy) : _ctx.lineTo(hx, hy)
        }
        _ctx.closePath()
        _ctx.strokeStyle = `rgba(${_rgb},${alpha})`
        _ctx.lineWidth = 0.5
        _ctx.stroke()
        if (prox > 0.55) {
          _ctx.fillStyle = `rgba(${_rgb},${prox * 0.045})`
          _ctx.fill()
        }
      }
    }

    // ─── Glow orbs ──────────────────────────────────────────────
    _orbs.forEach((orb, i) => {
      const ox = orb.rx * _W + (mx - 0.5) * 60 * orb.dx
      const oy = orb.ry * _H + (my - 0.5) * 40 * orb.dy
      const pulse = orb.o + Math.sin(_t * 0.6 + i) * 0.015
      const g = _ctx.createRadialGradient(ox, oy, 0, ox, oy, orb.r)
      g.addColorStop(0,   `rgba(${_rgb},${pulse})`)
      g.addColorStop(0.5, `rgba(${_rgb},${pulse * 0.38})`)
      g.addColorStop(1,   `rgba(${_rgb},0)`)
      _ctx.beginPath()
      _ctx.arc(ox, oy, orb.r, 0, Math.PI * 2)
      _ctx.fillStyle = g
      _ctx.fill()
    })

    // Mouse glow
    const mxPx = mx * _W, myPx = my * _H
    const mg = _ctx.createRadialGradient(mxPx, myPx, 0, mxPx, myPx, 175)
    mg.addColorStop(0, `rgba(${_rgb},0.08)`)
    mg.addColorStop(1, `rgba(${_rgb},0)`)
    _ctx.beginPath()
    _ctx.arc(mxPx, myPx, 175, 0, Math.PI * 2)
    _ctx.fillStyle = mg
    _ctx.fill()

    // ─── Particles ──────────────────────────────────────────────
    _particles.forEach(p => {
      p.life += p.speed
      if (p.life > 1) resetParticle(p)
      p.x += p.vx
      p.y += p.vy
      const fade = p.life < 0.15
        ? p.life / 0.15
        : p.life > 0.75
          ? (1 - p.life) / 0.25
          : 1
      const col = p.useAccent ? _rgb : '255,255,255'
      _ctx.beginPath()
      _ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      _ctx.fillStyle = `rgba(${col},${p.opacity * fade})`
      _ctx.fill()
      if (p.r > 1.8) {
        _ctx.beginPath()
        _ctx.arc(p.x, p.y, p.r * 2.8, 0, Math.PI * 2)
        _ctx.fillStyle = `rgba(${col},${p.opacity * fade * 0.1})`
        _ctx.fill()
      }
    })

    // ─── Scan lines ─────────────────────────────────────────────
    for (let y = 0; y < _H; y += 4) {
      _ctx.fillStyle = `rgba(0,0,0,${0.012 + (y % 8 === 0 ? 0.01 : 0)})`
      _ctx.fillRect(0, y, _W, 1)
    }
  }

  function onResize() {
    _W = window.innerWidth
    _H = window.innerHeight
    _canvas.width  = _W
    _canvas.height = _H
    makeParticles()
  }

  function onMouseMove(e) {
    _mouse.x = e.clientX / _W
    _mouse.y = e.clientY / _H
  }

  // Public API
  global.initChatBg = function ({ canvasId = 'chat-bg-canvas', color = '#00c8ff' } = {}) {
    _canvas = document.getElementById(canvasId)
    if (!_canvas) {
      console.warn('[chatParticles] Canvas not found:', canvasId)
      return
    }
    _ctx = _canvas.getContext('2d')
    _W = window.innerWidth
    _H = window.innerHeight
    _canvas.width  = _W
    _canvas.height = _H
    _canvas.style.cssText = 'position:fixed;inset:0;z-index:1;pointer-events:none;mix-blend-mode:screen;'

    _rgb = hexToRgb(color)
    makeParticles()
    makeOrbs()

    window.addEventListener('resize',    onResize)
    window.addEventListener('mousemove', onMouseMove)

    if (_running) cancelAnimationFrame(_raf)
    _running = true
    drawFrame()
  }

  global.updateChatBgColor = function (color) {
    _rgb = hexToRgb(color)
  }

  global.destroyChatBg = function () {
    cancelAnimationFrame(_raf)
    _running = false
    window.removeEventListener('resize',    onResize)
    window.removeEventListener('mousemove', onMouseMove)
    if (_canvas) _ctx.clearRect(0, 0, _W, _H)
  }

})(window)