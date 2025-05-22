
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent } from "@/components/ui/card";
import { Folder, FolderOpen, FileText, Plus, Search, Edit, Save } from "lucide-react";

interface Project {
  id: string;
  name: string;
  lastEdited: string;
  notes?: string;
}

const ProjectSidebar: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([
    { 
      id: '1', 
      name: 'Welcome Script', 
      lastEdited: '2025-05-21',
      notes: 'Introduction script for new users.' 
    },
    { 
      id: '2', 
      name: 'Product Demo', 
      lastEdited: '2025-05-20',
      notes: 'Showcase of product features.' 
    },
    { 
      id: '3', 
      name: 'Podcast Intro', 
      lastEdited: '2025-05-19',
      notes: 'Opening for weekly podcast episode.' 
    },
  ]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProject, setSelectedProject] = useState('1');
  const [editingNotes, setEditingNotes] = useState(false);
  const [currentNotes, setCurrentNotes] = useState('');

  const filteredProjects = projects.filter(project => 
    project.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const addNewProject = () => {
    const newProject = {
      id: Date.now().toString(),
      name: 'New Script',
      lastEdited: new Date().toISOString().split('T')[0],
      notes: '',
    };
    setProjects([...projects, newProject]);
    setSelectedProject(newProject.id);
  };

  const handleNotesEdit = () => {
    const currentProject = projects.find(p => p.id === selectedProject);
    if (currentProject) {
      setCurrentNotes(currentProject.notes || '');
      setEditingNotes(true);
    }
  };

  const saveNotes = () => {
    setProjects(projects.map(project => 
      project.id === selectedProject ? { ...project, notes: currentNotes } : project
    ));
    setEditingNotes(false);
  };

  const selectedProjectData = projects.find(p => p.id === selectedProject);

  return (
    <div className="w-64 bg-black border-r border-scriptRed/20 h-full flex flex-col">
      <div className="p-4 border-b border-scriptRed/20">
        <h2 className="text-xl font-bold text-white mb-4">Projects</h2>
        <div className="relative">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-scriptRed" />
          <Input
            type="text"
            placeholder="Search scripts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-8 bg-gray-900 border-scriptRed/20 text-white"
          />
        </div>
      </div>
      
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-2">
          {filteredProjects.map((project) => (
            <div
              key={project.id}
              className={`p-2 rounded-md cursor-pointer flex items-center space-x-2 ${
                selectedProject === project.id ? 'bg-scriptRed/20' : 'hover:bg-gray-900'
              }`}
              onClick={() => setSelectedProject(project.id)}
            >
              {selectedProject === project.id ? (
                <FolderOpen className="h-4 w-4 text-scriptRed" />
              ) : (
                <Folder className="h-4 w-4 text-scriptRed" />
              )}
              <div className="flex-1 overflow-hidden">
                <p className="text-sm text-white truncate">{project.name}</p>
                <p className="text-xs text-gray-400">{project.lastEdited}</p>
              </div>
              <FileText className="h-3 w-3 text-gray-500" />
            </div>
          ))}
        </div>
      </ScrollArea>
      
      {/* Notes section */}
      <div className="p-4 border-t border-b border-scriptRed/20">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-sm font-semibold text-white">Notes</h3>
          {!editingNotes ? (
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={handleNotesEdit}
              className="h-6 w-6 text-scriptRed hover:bg-scriptRed/20"
            >
              <Edit className="h-3 w-3" />
            </Button>
          ) : (
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={saveNotes}
              className="h-6 w-6 text-scriptRed hover:bg-scriptRed/20"
            >
              <Save className="h-3 w-3" />
            </Button>
          )}
        </div>
        
        {editingNotes ? (
          <Textarea 
            value={currentNotes}
            onChange={(e) => setCurrentNotes(e.target.value)} 
            placeholder="Add notes about your script..."
            className="bg-gray-900 border-scriptRed/20 text-white text-xs h-24 resize-none"
          />
        ) : (
          <Card className="bg-gray-900 border-scriptRed/20 h-24 overflow-auto">
            <CardContent className="p-2 text-xs text-gray-300">
              {selectedProjectData?.notes || 'No notes for this script.'}
            </CardContent>
          </Card>
        )}
      </div>
      
      <div className="p-4">
        <Button 
          onClick={addNewProject}
          className="w-full bg-scriptRed hover:bg-scriptRed/80 text-white"
        >
          <Plus className="h-4 w-4 mr-1" /> New Script
        </Button>
      </div>
    </div>
  );
};

export default ProjectSidebar;

