
import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ProjectSidebar from '@/components/ProjectSidebar';
import EditorPanel from '@/components/EditorPanel';
import StoriesPanel from '@/components/StoriesPanel';
import { FileText, BookOpen, Settings } from "lucide-react";

const Index = () => {
  const [dyslexicMode, setDyslexicMode] = useState<boolean>(false);

  return (
    <div className="min-h-screen flex flex-col bg-black text-white">
      <header className="bg-black border-b border-scriptRed/20 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-scriptRed text-xl font-bold">Script</span>
            <span className="text-scriptGold text-xl font-bold">Voice</span>
          </div>
          <div className="text-sm text-gray-400">
            Story Intelligence Platform
          </div>
        </div>
      </header>
      
      <main className="flex-1 flex">
        <Tabs defaultValue="scripts" className="w-full flex">
          <div className="border-r border-scriptRed/20">
            <TabsList className="flex flex-col h-full w-16 bg-black border-r border-scriptRed/20 rounded-none">
              <TabsTrigger 
                value="scripts" 
                className="w-full data-[state=active]:bg-scriptRed/20 data-[state=active]:text-scriptRed flex flex-col p-3"
              >
                <FileText className="h-5 w-5 mb-1" />
                <span className="text-xs">Scripts</span>
              </TabsTrigger>
              <TabsTrigger 
                value="stories" 
                className="w-full data-[state=active]:bg-scriptRed/20 data-[state=active]:text-scriptRed flex flex-col p-3"
              >
                <BookOpen className="h-5 w-5 mb-1" />
                <span className="text-xs">Stories</span>
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 flex">
            <TabsContent value="scripts" className="flex-1 flex m-0 p-0">
              <ProjectSidebar 
                dyslexicMode={dyslexicMode} 
                setDyslexicMode={setDyslexicMode} 
              />
              <div className="flex-1 flex flex-col">
                <div className="flex-1 p-4">
                  <EditorPanel dyslexicMode={dyslexicMode} />
                </div>
              </div>
            </TabsContent>

            <TabsContent value="stories" className="flex-1 m-0 p-0">
              <StoriesPanel />
            </TabsContent>
          </div>
        </Tabs>
      </main>
    </div>
  );
};

export default Index;
