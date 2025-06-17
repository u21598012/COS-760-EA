import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Emotion from './components/Emotion'

function App() {
  const [count, setCount] = useState(0)
    const colours_text = Array.from({ length: 500 }, () =>
        `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`
        );

        localStorage.setItem('colours_text', JSON.stringify(colours_text));
  return (
    <>
      <Emotion/>
    </>
  )
}

export default App
