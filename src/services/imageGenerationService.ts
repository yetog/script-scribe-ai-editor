export interface GeneratedImage {
  id: string;
  prompt: string;
  imageUrl: string;
  model: string;
  createdAt: string;
  metadata?: {
    contentType?: string;
    contentId?: string;
    title?: string;
  };
}

export interface MoodBoard {
  id: string;
  name: string;
  description: string;
  images: GeneratedImage[];
  createdAt: string;
  updatedAt: string;
}

class ImageGenerationService {
  private readonly API_BASE = 'https://openai.inference.de-txl.ionos.com/v1';
  private apiToken: string | null = null;

  setApiToken(token: string) {
    this.apiToken = token;
    localStorage.setItem('ionos_api_token', token);
  }

  getApiToken(): string | null {
    if (!this.apiToken) {
      this.apiToken = localStorage.getItem('ionos_api_token');
    }
    return this.apiToken;
  }

  async getAvailableModels() {
    const token = this.getApiToken();
    if (!token) throw new Error('IONOS API token not set');

    const response = await fetch(`${this.API_BASE}/models`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch models: ${response.statusText}`);
    }

    return response.json();
  }

  async generateImage(prompt: string, model: string = 'stable-diffusion-xl', size: string = '1024x1024'): Promise<GeneratedImage> {
    const token = this.getApiToken();
    if (!token) throw new Error('IONOS API token not set');

    const response = await fetch(`${this.API_BASE}/images/generations`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model,
        prompt,
        size
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to generate image: ${response.statusText}`);
    }

    const result = await response.json();
    const imageData = result.data[0];

    const generatedImage: GeneratedImage = {
      id: crypto.randomUUID(),
      prompt,
      imageUrl: `data:image/png;base64,${imageData.b64_json}`,
      model,
      createdAt: new Date().toISOString()
    };

    this.saveImageToHistory(generatedImage);
    return generatedImage;
  }

  async generateFromStoryElement(elementType: 'story' | 'character' | 'world_element', elementData: any): Promise<GeneratedImage> {
    let optimizedPrompt = '';
    
    switch (elementType) {
      case 'character':
        optimizedPrompt = `Character portrait: ${elementData.name}. ${elementData.description}. ${elementData.traits?.join(', ')}. Highly detailed, professional character design.`;
        break;
      case 'story':
        optimizedPrompt = `Scene from story: ${elementData.title}. ${elementData.description}. Cinematic, atmospheric, detailed environment.`;
        break;
      case 'world_element':
        optimizedPrompt = `${elementData.type}: ${elementData.name}. ${elementData.description}. Detailed concept art, fantasy/sci-fi style.`;
        break;
    }

    const image = await this.generateImage(optimizedPrompt);
    image.metadata = {
      contentType: elementType,
      contentId: elementData.id,
      title: elementData.name || elementData.title
    };

    return image;
  }

  saveImageToHistory(image: GeneratedImage) {
    const history = this.getImageHistory();
    history.unshift(image);
    // Keep only last 50 images
    const trimmedHistory = history.slice(0, 50);
    localStorage.setItem('image_generation_history', JSON.stringify(trimmedHistory));
  }

  getImageHistory(): GeneratedImage[] {
    const stored = localStorage.getItem('image_generation_history');
    return stored ? JSON.parse(stored) : [];
  }

  // Mood Board Management
  createMoodBoard(name: string, description: string = ''): MoodBoard {
    const moodBoard: MoodBoard = {
      id: crypto.randomUUID(),
      name,
      description,
      images: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.saveMoodBoard(moodBoard);
    return moodBoard;
  }

  getAllMoodBoards(): MoodBoard[] {
    const stored = localStorage.getItem('mood_boards');
    return stored ? JSON.parse(stored) : [];
  }

  getMoodBoard(id: string): MoodBoard | null {
    const boards = this.getAllMoodBoards();
    return boards.find(board => board.id === id) || null;
  }

  saveMoodBoard(moodBoard: MoodBoard) {
    const boards = this.getAllMoodBoards();
    const index = boards.findIndex(board => board.id === moodBoard.id);
    
    moodBoard.updatedAt = new Date().toISOString();
    
    if (index >= 0) {
      boards[index] = moodBoard;
    } else {
      boards.push(moodBoard);
    }

    localStorage.setItem('mood_boards', JSON.stringify(boards));
  }

  addImageToMoodBoard(boardId: string, image: GeneratedImage) {
    const board = this.getMoodBoard(boardId);
    if (board) {
      board.images.push(image);
      this.saveMoodBoard(board);
    }
  }

  removeImageFromMoodBoard(boardId: string, imageId: string) {
    const board = this.getMoodBoard(boardId);
    if (board) {
      board.images = board.images.filter(img => img.id !== imageId);
      this.saveMoodBoard(board);
    }
  }

  deleteMoodBoard(id: string) {
    const boards = this.getAllMoodBoards();
    const filtered = boards.filter(board => board.id !== id);
    localStorage.setItem('mood_boards', JSON.stringify(filtered));
  }
}

export const imageGenerationService = new ImageGenerationService();
