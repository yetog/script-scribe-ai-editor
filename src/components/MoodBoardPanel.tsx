
import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { 
  Image as ImageIcon, 
  Plus, 
  Settings, 
  Download, 
  Trash2, 
  Sparkles,
  Grid2X2,
  Palette,
  Camera
} from "lucide-react";
import { imageGenerationService, GeneratedImage, MoodBoard } from '@/services/imageGenerationService';
import { storyService } from '@/services/storyService';

const MoodBoardPanel = () => {
  const [moodBoards, setMoodBoards] = useState<MoodBoard[]>([]);
  const [selectedBoard, setSelectedBoard] = useState<MoodBoard | null>(null);
  const [imageHistory, setImageHistory] = useState<GeneratedImage[]>([]);
  const [apiToken, setApiToken] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isCreateBoardOpen, setIsCreateBoardOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    loadData();
    setApiToken(imageGenerationService.getApiToken() || '');
  }, []);

  const loadData = () => {
    setMoodBoards(imageGenerationService.getAllMoodBoards());
    setImageHistory(imageGenerationService.getImageHistory());
  };

  const handleSaveApiToken = () => {
    if (apiToken.trim()) {
      imageGenerationService.setApiToken(apiToken.trim());
      toast({
        title: "API Token Saved",
        description: "IONOS API token has been saved successfully.",
      });
      setIsSettingsOpen(false);
    }
  };

  const handleGenerateImage = async (prompt: string, model: string = 'stable-diffusion-xl') => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    try {
      const image = await imageGenerationService.generateImage(prompt, model);
      setImageHistory(prev => [image, ...prev.slice(0, 49)]);
      
      if (selectedBoard) {
        imageGenerationService.addImageToMoodBoard(selectedBoard.id, image);
        setSelectedBoard({...selectedBoard, images: [...selectedBoard.images, image]});
      }
      
      toast({
        title: "Image Generated",
        description: "Your image has been generated successfully!",
      });
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: error instanceof Error ? error.message : "Failed to generate image",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCreateBoard = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const name = formData.get('name') as string;
    const description = formData.get('description') as string;
    
    const newBoard = imageGenerationService.createMoodBoard(name, description);
    setMoodBoards(prev => [newBoard, ...prev]);
    setIsCreateBoardOpen(false);
  };

  const handleGenerateFromStoryElement = async (elementType: 'story' | 'character' | 'world_element', elementId: string) => {
    setIsGenerating(true);
    try {
      let elementData;
      switch (elementType) {
        case 'story':
          elementData = storyService.getAllStories().find(s => s.id === elementId);
          break;
        case 'character':
          elementData = storyService.getAllCharacters().find(c => c.id === elementId);
          break;
        case 'world_element':
          elementData = storyService.getAllWorldElements().find(w => w.id === elementId);
          break;
      }

      if (elementData) {
        const image = await imageGenerationService.generateFromStoryElement(elementType, elementData);
        setImageHistory(prev => [image, ...prev.slice(0, 49)]);
        
        if (selectedBoard) {
          imageGenerationService.addImageToMoodBoard(selectedBoard.id, image);
          setSelectedBoard({...selectedBoard, images: [...selectedBoard.images, image]});
        }
        
        toast({
          title: "Image Generated",
          description: `Generated image for ${elementData.name || elementData.title}`,
        });
      }
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: error instanceof Error ? error.message : "Failed to generate image",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const ImageGenerationDialog = () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button className="bg-scriptRed hover:bg-scriptRed/80">
          <Sparkles className="h-4 w-4 mr-2" />
          Generate Image
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-black border-scriptRed/20 max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-white">Generate AI Image</DialogTitle>
        </DialogHeader>
        <form onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.currentTarget);
          const prompt = formData.get('prompt') as string;
          const model = formData.get('model') as string;
          handleGenerateImage(prompt, model);
        }}>
          <div className="space-y-4">
            <div>
              <Label htmlFor="prompt" className="text-white">Prompt</Label>
              <Textarea 
                name="prompt" 
                placeholder="Describe the image you want to generate..."
                required 
                className="bg-gray-900 border-scriptRed/20 text-white min-h-20" 
              />
            </div>
            <div>
              <Label htmlFor="model" className="text-white">Model</Label>
              <Select name="model" defaultValue="stable-diffusion-xl">
                <SelectTrigger className="bg-gray-900 border-scriptRed/20 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-black border-scriptRed/20">
                  <SelectItem value="stable-diffusion-xl">Stable Diffusion XL (Photorealistic)</SelectItem>
                  <SelectItem value="flux-1-schnell">FLUX.1-schnell (Artistic)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" disabled={isGenerating} className="bg-scriptRed hover:bg-scriptRed/80 w-full">
              {isGenerating ? "Generating..." : "Generate Image"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );

  const SettingsDialog = () => (
    <Dialog open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="border-scriptGold text-scriptGold hover:bg-scriptGold hover:text-black">
          <Settings className="h-4 w-4 mr-2" />
          Settings
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-black border-scriptRed/20">
        <DialogHeader>
          <DialogTitle className="text-white">Image Generation Settings</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <Label htmlFor="apiToken" className="text-white">IONOS API Token</Label>
            <Input
              id="apiToken"
              type="password"
              value={apiToken}
              onChange={(e) => setApiToken(e.target.value)}
              placeholder="Enter your IONOS API token..."
              className="bg-gray-900 border-scriptRed/20 text-white"
            />
            <p className="text-sm text-gray-400 mt-1">
              Get your free API token from IONOS AI Model Hub
            </p>
          </div>
          <Button onClick={handleSaveApiToken} className="bg-scriptRed hover:bg-scriptRed/80">
            Save Token
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );

  return (
    <div className="w-full h-full bg-black text-white p-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-4 flex items-center">
          <Palette className="h-6 w-6 mr-2 text-scriptRed" />
          Mood Boarding
        </h1>
        
        <div className="flex gap-2 mb-4">
          <Dialog open={isCreateBoardOpen} onOpenChange={setIsCreateBoardOpen}>
            <DialogTrigger asChild>
              <Button className="bg-scriptRed hover:bg-scriptRed/80">
                <Plus className="h-4 w-4 mr-2" />
                New Board
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-black border-scriptRed/20">
              <DialogHeader>
                <DialogTitle className="text-white">Create Mood Board</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleCreateBoard}>
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
                    Create Board
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
          
          <ImageGenerationDialog />
          <SettingsDialog />
        </div>
      </div>

      <Tabs defaultValue="boards" className="w-full">
        <TabsList className="bg-gray-900 mb-4">
          <TabsTrigger value="boards" className="data-[state=active]:bg-scriptRed">
            <Grid2X2 className="h-4 w-4 mr-2" />
            Mood Boards ({moodBoards.length})
          </TabsTrigger>
          <TabsTrigger value="history" className="data-[state=active]:bg-scriptRed">
            <Camera className="h-4 w-4 mr-2" />
            History ({imageHistory.length})
          </TabsTrigger>
          <TabsTrigger value="story-gen" className="data-[state=active]:bg-scriptRed">
            <Sparkles className="h-4 w-4 mr-2" />
            Story Generation
          </TabsTrigger>
        </TabsList>

        <TabsContent value="boards">
          <ScrollArea className="h-[600px]">
            <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
              {moodBoards.map((board) => (
                <Card 
                  key={board.id} 
                  className="bg-gray-900 border-scriptRed/20 hover:border-scriptRed/40 cursor-pointer"
                  onClick={() => setSelectedBoard(board)}
                >
                  <CardHeader>
                    <CardTitle className="text-white text-lg">{board.name}</CardTitle>
                    <p className="text-gray-300 text-sm">{board.description}</p>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-3 gap-2 mb-3">
                      {board.images.slice(0, 6).map((image, idx) => (
                        <div key={idx} className="aspect-square bg-gray-800 rounded overflow-hidden">
                          <img 
                            src={image.imageUrl} 
                            alt={image.prompt}
                            className="w-full h-full object-cover"
                          />
                        </div>
                      ))}
                      {board.images.length === 0 && (
                        <div className="col-span-3 h-20 bg-gray-800 rounded flex items-center justify-center">
                          <ImageIcon className="h-8 w-8 text-gray-600" />
                        </div>
                      )}
                    </div>
                    <div className="flex justify-between items-center text-xs text-gray-400">
                      <span>{board.images.length} images</span>
                      <span>{new Date(board.createdAt).toLocaleDateString()}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="history">
          <ScrollArea className="h-[600px]">
            <div className="grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
              {imageHistory.map((image) => (
                <Card key={image.id} className="bg-gray-900 border-scriptRed/20">
                  <CardContent className="p-2">
                    <div className="aspect-square bg-gray-800 rounded overflow-hidden mb-2">
                      <img 
                        src={image.imageUrl} 
                        alt={image.prompt}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <p className="text-xs text-gray-300 line-clamp-2">{image.prompt}</p>
                    <div className="flex items-center justify-between mt-2">
                      <Badge variant="outline" className="border-scriptGold/50 text-scriptGold text-xs">
                        {image.model}
                      </Badge>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => selectedBoard && imageGenerationService.addImageToMoodBoard(selectedBoard.id, image)}
                        className="text-scriptRed hover:bg-scriptRed/20 p-1 h-6"
                      >
                        <Plus className="h-3 w-3" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="story-gen">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card className="bg-gray-900 border-scriptRed/20">
              <CardHeader>
                <CardTitle className="text-white">Characters</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-48">
                  {storyService.getAllCharacters().map((character) => (
                    <div key={character.id} className="flex items-center justify-between p-2 hover:bg-gray-800 rounded">
                      <span className="text-gray-300">{character.name}</span>
                      <Button
                        size="sm"
                        onClick={() => handleGenerateFromStoryElement('character', character.id)}
                        disabled={isGenerating}
                        className="bg-scriptRed hover:bg-scriptRed/80 h-6 px-2"
                      >
                        <Sparkles className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </ScrollArea>
              </CardContent>
            </Card>

            <Card className="bg-gray-900 border-scriptRed/20">
              <CardHeader>
                <CardTitle className="text-white">Stories</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-48">
                  {storyService.getAllStories().map((story) => (
                    <div key={story.id} className="flex items-center justify-between p-2 hover:bg-gray-800 rounded">
                      <span className="text-gray-300">{story.title}</span>
                      <Button
                        size="sm"
                        onClick={() => handleGenerateFromStoryElement('story', story.id)}
                        disabled={isGenerating}
                        className="bg-scriptRed hover:bg-scriptRed/80 h-6 px-2"
                      >
                        <Sparkles className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </ScrollArea>
              </CardContent>
            </Card>

            <Card className="bg-gray-900 border-scriptRed/20">
              <CardHeader>
                <CardTitle className="text-white">World Elements</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-48">
                  {storyService.getAllWorldElements().map((element) => (
                    <div key={element.id} className="flex items-center justify-between p-2 hover:bg-gray-800 rounded">
                      <div>
                        <span className="text-gray-300">{element.name}</span>
                        <Badge variant="outline" className="border-scriptGold/50 text-scriptGold text-xs ml-2">
                          {element.type}
                        </Badge>
                      </div>
                      <Button
                        size="sm"
                        onClick={() => handleGenerateFromStoryElement('world_element', element.id)}
                        disabled={isGenerating}
                        className="bg-scriptRed hover:bg-scriptRed/80 h-6 px-2"
                      >
                        <Sparkles className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MoodBoardPanel;
