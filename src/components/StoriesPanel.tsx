
import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BookOpen, Users, Globe, Plus, Search, Edit, Trash2, Tag } from "lucide-react";
import { storyService } from '@/services/storyService';
import { Story, Character, WorldElement } from '@/types/story';

const StoriesPanel = () => {
  const [stories, setStories] = useState<Story[]>([]);
  const [characters, setCharacters] = useState<Character[]>([]);
  const [worldElements, setWorldElements] = useState<WorldElement[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);
  const [isCreateStoryOpen, setIsCreateStoryOpen] = useState(false);
  const [isCreateCharacterOpen, setIsCreateCharacterOpen] = useState(false);
  const [isCreateWorldElementOpen, setIsCreateWorldElementOpen] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    setStories(storyService.getAllStories());
    setCharacters(storyService.getAllCharacters());
    setWorldElements(storyService.getAllWorldElements());
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      const results = storyService.searchContent(searchQuery);
      setStories(results.stories);
      setCharacters(results.characters);
      setWorldElements(results.worldElements);
    } else {
      loadData();
    }
  };

  const CreateStoryDialog = () => (
    <Dialog open={isCreateStoryOpen} onOpenChange={setIsCreateStoryOpen}>
      <DialogTrigger asChild>
        <Button className="bg-scriptRed hover:bg-scriptRed/80">
          <Plus className="h-4 w-4 mr-2" /> New Story
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-black border-scriptRed/20">
        <DialogHeader>
          <DialogTitle className="text-white">Create New Story</DialogTitle>
        </DialogHeader>
        <form onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.currentTarget);
          const title = formData.get('title') as string;
          const description = formData.get('description') as string;
          storyService.createStory(title, description);
          loadData();
          setIsCreateStoryOpen(false);
        }}>
          <div className="space-y-4">
            <div>
              <Label htmlFor="title" className="text-white">Title</Label>
              <Input name="title" required className="bg-gray-900 border-scriptRed/20 text-white" />
            </div>
            <div>
              <Label htmlFor="description" className="text-white">Description</Label>
              <Textarea name="description" className="bg-gray-900 border-scriptRed/20 text-white" />
            </div>
            <Button type="submit" className="bg-scriptRed hover:bg-scriptRed/80">
              Create Story
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );

  const CreateCharacterDialog = () => (
    <Dialog open={isCreateCharacterOpen} onOpenChange={setIsCreateCharacterOpen}>
      <DialogTrigger asChild>
        <Button className="bg-scriptRed hover:bg-scriptRed/80">
          <Plus className="h-4 w-4 mr-2" /> New Character
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-black border-scriptRed/20">
        <DialogHeader>
          <DialogTitle className="text-white">Create New Character</DialogTitle>
        </DialogHeader>
        <form onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.currentTarget);
          const name = formData.get('name') as string;
          const description = formData.get('description') as string;
          storyService.createCharacter(name, description);
          loadData();
          setIsCreateCharacterOpen(false);
        }}>
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="text-white">Name</Label>
              <Input name="name" required className="bg-gray-900 border-scriptRed/20 text-white" />
            </div>
            <div>
              <Label htmlFor="description" className="text-white">Description</Label>
              <Textarea name="description" className="bg-gray-900 border-scriptRed/20 text-white" />
            </div>
            <Button type="submit" className="bg-scriptRed hover:bg-scriptRed/80">
              Create Character
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );

  const CreateWorldElementDialog = () => (
    <Dialog open={isCreateWorldElementOpen} onOpenChange={setIsCreateWorldElementOpen}>
      <DialogTrigger asChild>
        <Button className="bg-scriptRed hover:bg-scriptRed/80">
          <Plus className="h-4 w-4 mr-2" /> New World Element
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-black border-scriptRed/20">
        <DialogHeader>
          <DialogTitle className="text-white">Create New World Element</DialogTitle>
        </DialogHeader>
        <form onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.currentTarget);
          const name = formData.get('name') as string;
          const type = formData.get('type') as WorldElement['type'];
          const description = formData.get('description') as string;
          storyService.createWorldElement(name, type, description);
          loadData();
          setIsCreateWorldElementOpen(false);
        }}>
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="text-white">Name</Label>
              <Input name="name" required className="bg-gray-900 border-scriptRed/20 text-white" />
            </div>
            <div>
              <Label htmlFor="type" className="text-white">Type</Label>
              <Select name="type" required>
                <SelectTrigger className="bg-gray-900 border-scriptRed/20 text-white">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent className="bg-black border-scriptRed/20">
                  <SelectItem value="location">Location</SelectItem>
                  <SelectItem value="organization">Organization</SelectItem>
                  <SelectItem value="concept">Concept</SelectItem>
                  <SelectItem value="item">Item</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="description" className="text-white">Description</Label>
              <Textarea name="description" className="bg-gray-900 border-scriptRed/20 text-white" />
            </div>
            <Button type="submit" className="bg-scriptRed hover:bg-scriptRed/80">
              Create World Element
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );

  return (
    <div className="w-full h-full bg-black text-white p-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-4 flex items-center">
          <BookOpen className="h-6 w-6 mr-2 text-scriptRed" />
          Story Intelligence
        </h1>
        
        <div className="flex gap-2 mb-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search stories, characters, world..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="pl-10 bg-gray-900 border-scriptRed/20 text-white"
            />
          </div>
          <Button onClick={handleSearch} className="bg-scriptRed hover:bg-scriptRed/80">
            Search
          </Button>
        </div>

        <div className="flex gap-2">
          <CreateStoryDialog />
          <CreateCharacterDialog />
          <CreateWorldElementDialog />
        </div>
      </div>

      <Tabs defaultValue="stories" className="w-full">
        <TabsList className="bg-gray-900 mb-4">
          <TabsTrigger value="stories" className="data-[state=active]:bg-scriptRed">
            <BookOpen className="h-4 w-4 mr-2" />
            Stories ({stories.length})
          </TabsTrigger>
          <TabsTrigger value="characters" className="data-[state=active]:bg-scriptRed">
            <Users className="h-4 w-4 mr-2" />
            Characters ({characters.length})
          </TabsTrigger>
          <TabsTrigger value="world" className="data-[state=active]:bg-scriptRed">
            <Globe className="h-4 w-4 mr-2" />
            World ({worldElements.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="stories">
          <ScrollArea className="h-[600px]">
            <div className="grid gap-4">
              {stories.map((story) => (
                <Card key={story.id} className="bg-gray-900 border-scriptRed/20 hover:border-scriptRed/40 cursor-pointer">
                  <CardHeader>
                    <CardTitle className="text-white flex justify-between items-start">
                      <span>{story.title}</span>
                      <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="text-scriptRed hover:bg-scriptRed/20">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="text-red-400 hover:bg-red-400/20">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-300 mb-2">{story.description}</p>
                    <div className="flex flex-wrap gap-1 mb-2">
                      {story.tags.map((tag) => (
                        <Badge key={tag} variant="outline" className="border-scriptRed/50 text-scriptRed">
                          <Tag className="h-3 w-3 mr-1" />
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-xs text-gray-400">
                      Created: {new Date(story.createdAt).toLocaleDateString()}
                      {story.chapters.length > 0 && ` • ${story.chapters.length} chapters`}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="characters">
          <ScrollArea className="h-[600px]">
            <div className="grid gap-4">
              {characters.map((character) => (
                <Card key={character.id} className="bg-gray-900 border-scriptRed/20 hover:border-scriptRed/40 cursor-pointer">
                  <CardHeader>
                    <CardTitle className="text-white flex justify-between items-start">
                      <span>{character.name}</span>
                      <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="text-scriptRed hover:bg-scriptRed/20">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="text-red-400 hover:bg-red-400/20">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-300 mb-2">{character.description}</p>
                    <div className="flex flex-wrap gap-1 mb-2">
                      {character.traits.map((trait) => (
                        <Badge key={trait} variant="outline" className="border-scriptGold/50 text-scriptGold">
                          {trait}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-xs text-gray-400">
                      Created: {new Date(character.createdAt).toLocaleDateString()}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="world">
          <ScrollArea className="h-[600px]">
            <div className="grid gap-4">
              {worldElements.map((element) => (
                <Card key={element.id} className="bg-gray-900 border-scriptRed/20 hover:border-scriptRed/40 cursor-pointer">
                  <CardHeader>
                    <CardTitle className="text-white flex justify-between items-start">
                      <span>{element.name}</span>
                      <div className="flex gap-2">
                        <Badge variant="outline" className="border-scriptGold/50 text-scriptGold">
                          {element.type}
                        </Badge>
                        <Button variant="ghost" size="icon" className="text-scriptRed hover:bg-scriptRed/20">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="text-red-400 hover:bg-red-400/20">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-300 mb-2">{element.description}</p>
                    <div className="flex flex-wrap gap-1 mb-2">
                      {element.tags.map((tag) => (
                        <Badge key={tag} variant="outline" className="border-scriptRed/50 text-scriptRed">
                          <Tag className="h-3 w-3 mr-1" />
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-xs text-gray-400">
                      Created: {new Date(element.createdAt).toLocaleDateString()}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default StoriesPanel;
