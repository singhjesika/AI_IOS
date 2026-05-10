import React, { useEffect, useRef, useState } from 'react'

export default function FloatingAvatar({ greet = true, message = "Welcome, Jesika! I'm your AI assistant. Let's explore together!" }) {
  const [bubbleVisible, setBubbleVisible] = useState(false)
  const [isTalking, setIsTalking] = useState(false)
  const [glowSize, setGlowSize] = useState(30)
  const glowRef = useRef(null)

  useEffect(() => {
    if (!greet) return
    const timer = setTimeout(() => {
      setBubbleVisible(true)
      speakWelcome()
    }, 800)
    return () => {
      clearTimeout(timer)
      window.speechSynthesis?.cancel()
    }
  }, [greet])

  function speakWelcome() {
    if (!window.speechSynthesis) return
    const speak = () => {
      const msg = new SpeechSynthesisUtterance(message)
      msg.pitch = 1.4
      msg.rate = 0.95
      msg.volume = 1
      const voices = window.speechSynthesis.getVoices()
      const female = voices.find(v =>
        /female|zira|samantha|victoria|karen|moira/i.test(v.name)
      )
      if (female) msg.voice = female

      let glowInterval
      msg.onstart = () => {
        setIsTalking(true)
        glowInterval = setInterval(() => {
          setGlowSize(20 + Math.random() * 25)
        }, 150)
      }
      msg.onend = () => {
        setIsTalking(false)
        setGlowSize(30)
        clearInterval(glowInterval)
      }
      window.speechSynthesis.cancel()
      window.speechSynthesis.speak(msg)
    }

    if (window.speechSynthesis.getVoices().length > 0) {
      speak()
    } else {
      window.speechSynthesis.onvoiceschanged = speak
    }
  }

  return (
    <div className="avatar-section">
      {bubbleVisible && (
        <div className="speech-bubble visible">
          Welcome, Jesika! 👋
        </div>
      )}
      <div className="avatar-wrapper">
        <div
          className="avatar-glow"
          style={{ boxShadow: `0 0 ${glowSize}px rgba(0,200,255,0.4)` }}
        />
        <div
          className="avatar-body"
          style={{
            filter: `drop-shadow(0 0 ${glowSize}px rgba(0,200,255,0.6))`,
            transform: isTalking ? 'scale(1.05)' : 'scale(1)',
            transition: 'transform 0.1s'
          }}
        >
          😊
        </div>
        <div className="book">📚</div>
      </div>
      <p className="avatar-label">AI ASSISTANT</p>
    </div>
  )
}