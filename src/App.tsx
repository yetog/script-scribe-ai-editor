
import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BookOpen, Edit, Palette, Settings } from "lucide-react";
import StoriesPanel from '@/components/StoriesPanel';
import MoodBoardPanel from '@/components/MoodBoardPanel';
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
          <TabsList className="grid grid-cols-4 w-full max-w-2xl mx-auto bg-gray-900 mb-8">
            <TabsTrigger 
              value="stories" 
              className="data-[state=active]:bg-red-600 data-[state=active]:text-white"
            >
              <BookOpen className="h-4 w-4 mr-2" />
              Stories
            </TabsTrigger>
            <TabsTrigger 
              value="moodboard" 
              className="data-[state=active]:bg-red-600 data-[state=active]:text-white"
            >
              <Palette className="h-4 w-4 mr-2" />
              Mood Board
            </TabsTrigger>
            <TabsTrigger 
              value="editor" 
              className="data-[state=active]:bg-red-600 data-[state=active]:text-white"
            >
              <Edit className="h-4 w-4 mr-2" />
              Editor
            </TabsTrigger>
            <TabsTrigger 
              value="settings" 
              className="data-[state=active]:bg-red-600 data-[state=active]:text-white"
            >
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </TabsTrigger>
          </TabsList>

          <TabsContent value="stories" className="mt-0">
            <StoriesPanel />
          </TabsContent>

          <TabsContent value="moodboard" className="mt-0">
            <MoodBoardPanel />
          </TabsContent>

          <TabsContent value="editor" className="mt-0">
            <div className="text-center py-20">
              <Edit className="h-16 w-16 mx-auto mb-4 text-gray-600" />
              <h3 className="text-2xl font-semibold mb-2 text-gray-300">Script Editor</h3>
              <p className="text-gray-400">Coming soon - Advanced script editing with AI assistance</p>
            </div>
          </TabsContent>

          <TabsContent value="settings" className="mt-0">
            <div className="text-center py-20">
              <Settings className="h-16 w-16 mx-auto mb-4 text-gray-600" />
              <h3 className="text-2xl font-semibold mb-2 text-gray-300">Settings</h3>
              <p className="text-gray-400">Configuration and preferences panel</p>
            </div>
          </TabsContent>
        </Tabs>
      </div>
      
      <Toaster />
    </div>
  );
}

export default App;
