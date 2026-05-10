import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function Background3D() {
  const mountRef = useRef(null)

  useEffect(() => {
    const mount = mountRef.current
    const w = window.innerWidth, h = window.innerHeight

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(w, h)
    renderer.domElement.style.position = 'fixed'
    renderer.domElement.style.top = '0'
    renderer.domElement.style.left = '0'
    renderer.domElement.style.zIndex = '0'
    mount.appendChild(renderer.domElement)

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, w / h, 0.1, 2000)
    camera.position.z = 400

    // Stars
    const starGeo = new THREE.BufferGeometry()
    const starPos = new Float32Array(8000 * 3)
    for (let i = 0; i < 8000 * 3; i++) starPos[i] = (Math.random() - 0.5) * 2000
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3))
    scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, transparent: true, opacity: 0.8 })))

    // Nebula layers
    const nebulas = [
      { count: 2000, color: 0x0088ff, spread: 800, size: 2 },
      { count: 1500, color: 0x00ffcc, spread: 600, size: 1.5 },
      { count: 1000, color: 0xff00ff, spread: 500, size: 2.5 },
      { count: 800,  color: 0xffaa00, spread: 400, size: 2 },
    ]
    nebulas.forEach(({ count, color, spread, size }) => {
      const geo = new THREE.BufferGeometry()
      const pos = new Float32Array(count * 3)
      for (let i = 0; i < count * 3; i++) pos[i] = (Math.random() - 0.5) * spread
      geo.setAttribute('position', new THREE.BufferAttribute(pos, 3))
      scene.add(new THREE.Points(geo, new THREE.PointsMaterial({ color, size, transparent: true, opacity: 0.4 })))
    })

    // Rings
    const ring1 = new THREE.Mesh(
      new THREE.TorusGeometry(200, 1, 2, 100),
      new THREE.MeshBasicMaterial({ color: 0x00c8ff, transparent: true, opacity: 0.15, wireframe: true })
    )
    ring1.rotation.x = Math.PI / 3
    scene.add(ring1)

    const ring2 = new THREE.Mesh(
      new THREE.TorusGeometry(300, 0.8, 2, 100),
      new THREE.MeshBasicMaterial({ color: 0x0044ff, transparent: true, opacity: 0.08, wireframe: true })
    )
    ring2.rotation.x = -Math.PI / 4
    ring2.rotation.y = Math.PI / 6
    scene.add(ring2)

    // Mouse parallax
    let mouse = { x: 0, y: 0 }
    const onMouseMove = (e) => {
      mouse.x = (e.clientX / window.innerWidth - 0.5) * 0.5
      mouse.y = (e.clientY / window.innerHeight - 0.5) * 0.5
    }
    window.addEventListener('mousemove', onMouseMove)

    // Resize
    const onResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight
      camera.updateProjectionMatrix()
      renderer.setSize(window.innerWidth, window.innerHeight)
    }
    window.addEventListener('resize', onResize)

    // Animation loop
    let animId
    const animate = () => {
      animId = requestAnimationFrame(animate)
      ring1.rotation.z += 0.001
      ring2.rotation.z -= 0.0008
      camera.position.x += (mouse.x * 50 - camera.position.x) * 0.02
      camera.position.y += (-mouse.y * 50 - camera.position.y) * 0.02
      camera.lookAt(scene.position)
      renderer.render(scene, camera)
    }
    animate()

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('mousemove', onMouseMove)
      window.removeEventListener('resize', onResize)
      mount.removeChild(renderer.domElement)
      renderer.dispose()
    }
  }, [])

  return <div ref={mountRef} />
}