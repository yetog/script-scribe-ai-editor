
import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

const App = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
      <div className="max-w-2xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          🎬 ScriptVoice - AI-Powered Story Intelligence
        </h1>
        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            This is now a Python Gradio Application!
          </h2>
          <p className="text-gray-600 mb-6">
            To run the full ScriptVoice application with all AI features, please use the Python version:
          </p>
          <div className="bg-gray-100 rounded-lg p-4 mb-4">
            <code className="text-sm">
              pip install -r requirements.txt<br/>
              python main.py
            </code>
          </div>
          <p className="text-sm text-gray-500">
            The app will be available at: <strong>http://localhost:7860</strong>
          </p>
        </div>
        <div className="text-left bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Features Available in Python Version:</h3>
          <ul className="text-blue-800 space-y-2">
            <li>• 📝 Advanced Script Editor with TTS</li>
            <li>• 🤖 AI Knowledge Assistant</li>
            <li>• 📚 Story & Character Management</li>
            <li>• 🌍 World Building Tools</li>
            <li>• 🔍 RAG-Powered Search</li>
            <li>• 📷 OCR Text Extraction</li>
            <li>• ✨ Context-Aware AI Enhancement</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
