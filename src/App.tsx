
import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BookOpen, Edit, Palette, Settings } from "lucide-react";
import StoriesPanel from '@/components/StoriesPanel';
import { Toaster } from "@/components/ui/toaster";

function App() {
  const [activeTab, setActiveTab] = useState('stories');

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-6">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-red-500 to-yellow-500 bg-clip-text text-transparent">
            🎬 ScriptVoice
          </h1>
          <p className="text-xl text-gray-300">AI-Powered Story Intelligence Platform</p>
          <p className="text-sm text-gray-400 mt-2">
            Transform your stories with intelligent script writing, voice synthesis, and creative knowledge management
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-2 w-full max-w-md mx-auto bg-gray-900 mb-8">
            <TabsTrigger 
              value="stories" 
              className="data-[state=active]:bg-red-600 data-[state=active]:text-white"
            >
              <BookOpen className="h-4 w-4 mr-2" />
              Stories
            </TabsTrigger>
            <TabsTrigger 
              value="app" 
              className="data-[state=active]:bg-red-600 data-[state=active]:text-white"
            >
              <Edit className="h-4 w-4 mr-2" />
              Launch App
            </TabsTrigger>
          </TabsList>

          <TabsContent value="stories" className="mt-0">
            <StoriesPanel />
          </TabsContent>

          <TabsContent value="app" className="mt-0">
            <div className="text-center py-20">
              <div className="bg-gray-900 rounded-lg p-8 max-w-2xl mx-auto">
                <Edit className="h-16 w-16 mx-auto mb-4 text-red-500" />
                <h3 className="text-2xl font-semibold mb-4 text-gray-300">Full ScriptVoice Application</h3>
                <p className="text-gray-400 mb-6">
                  Access the complete Python/Gradio application with advanced script editing, 
                  AI mood board generation, and story intelligence features.
                </p>
                <a 
                  href="http://localhost:7860" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                >
                  🚀 Launch ScriptVoice App
                </a>
                <p className="text-sm text-gray-500 mt-4">
                  Make sure to run: <code className="bg-gray-800 px-2 py-1 rounded">python main.py</code>
                </p>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>
      
      <Toaster />
    </div>
  );
}

export default App;
