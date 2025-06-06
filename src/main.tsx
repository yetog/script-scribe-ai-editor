
import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

function App() {
  return (
    <div style={{ 
      padding: '40px', 
      fontFamily: 'system-ui, -apple-system, sans-serif', 
      textAlign: 'center',
      maxWidth: '800px',
      margin: '0 auto',
      lineHeight: '1.6'
    }}>
      <h1 style={{ 
        color: '#2563eb', 
        marginBottom: '20px',
        fontSize: '2.5rem'
      }}>
        🎬 ScriptVoice
      </h1>
      <h2 style={{ 
        color: '#64748b', 
        fontWeight: 'normal',
        marginBottom: '30px'
      }}>
        AI-Powered Story Intelligence Platform
      </h2>
      
      <div style={{
        background: '#f8fafc',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        padding: '30px',
        marginBottom: '30px'
      }}>
        <p style={{ fontSize: '1.1rem', marginBottom: '25px' }}>
          This is a <strong>Python Gradio application</strong>. The main interface runs on a separate server.
        </p>
        
        <div style={{ textAlign: 'left', marginBottom: '25px' }}>
          <h3 style={{ color: '#374151', marginBottom: '15px' }}>🚀 Quick Start:</h3>
          <ol style={{ paddingLeft: '20px', color: '#4b5563' }}>
            <li style={{ marginBottom: '8px' }}>
              Install dependencies: <code style={{ 
                background: '#e5e7eb', 
                padding: '2px 6px', 
                borderRadius: '4px',
                fontFamily: 'Monaco, monospace'
              }}>pip install -r requirements.txt</code>
            </li>
            <li style={{ marginBottom: '8px' }}>
              Run the app: <code style={{ 
                background: '#e5e7eb', 
                padding: '2px 6px', 
                borderRadius: '4px',
                fontFamily: 'Monaco, monospace'
              }}>python main.py</code>
            </li>
            <li>
              Access the full application at: <a 
                href="http://localhost:7860" 
                style={{ color: '#2563eb', textDecoration: 'none' }}
                target="_blank"
                rel="noopener noreferrer"
              >
                http://localhost:7860
              </a>
            </li>
          </ol>
        </div>
        
        <div style={{
          background: '#fef3c7',
          border: '1px solid #f59e0b',
          borderRadius: '8px',
          padding: '15px',
          fontSize: '0.9rem'
        }}>
          <strong>📝 Note:</strong> The actual ScriptVoice interface with AI tools, script editor, 
          TTS, OCR, and story intelligence features will be served by Gradio on port 7860.
        </div>
      </div>
      
      <div style={{ color: '#6b7280', fontSize: '0.9rem' }}>
        <p>✨ Features include: Script Editor, AI Enhancement, Text-to-Speech, OCR, Story Intelligence & more</p>
      </div>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
