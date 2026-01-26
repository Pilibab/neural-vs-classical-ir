import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import ResultProvider from './provider/ResultProvider.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ResultProvider>
      <App />
    </ResultProvider>
  </StrictMode>,
)
