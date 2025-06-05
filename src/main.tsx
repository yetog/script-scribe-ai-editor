
import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', textAlign: 'center' }}>
      <h1>ScriptVoice - AI-Powered Story Intelligence Platform</h1>
      <p>This is a Python Gradio application. To run it:</p>
      <ol style={{ textAlign: 'left', maxWidth: '400px', margin: '0 auto' }}>
        <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
        <li>Run the app: <code>python main.py</code></li>
        <li>Access at: <a href="http://localhost:7860">http://localhost:7860</a></li>
      </ol>
      <p style={{ marginTop: '20px', color: '#666' }}>
        The actual application interface will be served by Gradio on port 7860.
      </p>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
