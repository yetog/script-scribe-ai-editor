
import { Story, Character, WorldElement, KnowledgeBase, Chapter, Scene } from '@/types/story';

const KNOWLEDGE_BASE_KEY = 'scriptvoice_knowledge_base';

export class StoryService {
  private static instance: StoryService;
  private knowledgeBase: KnowledgeBase;

  private constructor() {
    this.knowledgeBase = this.loadKnowledgeBase();
  }

  public static getInstance(): StoryService {
    if (!StoryService.instance) {
      StoryService.instance = new StoryService();
    }
    return StoryService.instance;
  }

  private loadKnowledgeBase(): KnowledgeBase {
    const stored = localStorage.getItem(KNOWLEDGE_BASE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
    return {
      stories: {},
      characters: {},
      worldElements: {}
    };
  }

  private saveKnowledgeBase(): void {
    localStorage.setItem(KNOWLEDGE_BASE_KEY, JSON.stringify(this.knowledgeBase));
  }

  // Story operations
  createStory(title: string, description: string = ''): Story {
    const id = Date.now().toString();
    const story: Story = {
      id,
      title,
      description,
      content: '',
      tags: [],
      characters: [],
      worldElements: [],
      chapters: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    this.knowledgeBase.stories[id] = story;
    this.saveKnowledgeBase();
    return story;
  }

  updateStory(id: string, updates: Partial<Story>): Story | null {
    if (!this.knowledgeBase.stories[id]) return null;
    
    this.knowledgeBase.stories[id] = {
      ...this.knowledgeBase.stories[id],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    
    this.saveKnowledgeBase();
    return this.knowledgeBase.stories[id];
  }

  deleteStory(id: string): boolean {
    if (!this.knowledgeBase.stories[id]) return false;
    delete this.knowledgeBase.stories[id];
    this.saveKnowledgeBase();
    return true;
  }

  getStory(id: string): Story | null {
    return this.knowledgeBase.stories[id] || null;
  }

  getAllStories(): Story[] {
    return Object.values(this.knowledgeBase.stories);
  }

  // Character operations
  createCharacter(name: string, description: string = ''): Character {
    const id = Date.now().toString();
    const character: Character = {
      id,
      name,
      description,
      traits: [],
      relationships: {},
      notes: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    this.knowledgeBase.characters[id] = character;
    this.saveKnowledgeBase();
    return character;
  }

  updateCharacter(id: string, updates: Partial<Character>): Character | null {
    if (!this.knowledgeBase.characters[id]) return null;
    
    this.knowledgeBase.characters[id] = {
      ...this.knowledgeBase.characters[id],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    
    this.saveKnowledgeBase();
    return this.knowledgeBase.characters[id];
  }

  deleteCharacter(id: string): boolean {
    if (!this.knowledgeBase.characters[id]) return false;
    delete this.knowledgeBase.characters[id];
    this.saveKnowledgeBase();
    return true;
  }

  getCharacter(id: string): Character | null {
    return this.knowledgeBase.characters[id] || null;
  }

  getAllCharacters(): Character[] {
    return Object.values(this.knowledgeBase.characters);
  }

  // World Element operations
  createWorldElement(name: string, type: WorldElement['type'], description: string = ''): WorldElement {
    const id = Date.now().toString();
    const worldElement: WorldElement = {
      id,
      name,
      type,
      description,
      tags: [],
      notes: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    this.knowledgeBase.worldElements[id] = worldElement;
    this.saveKnowledgeBase();
    return worldElement;
  }

  updateWorldElement(id: string, updates: Partial<WorldElement>): WorldElement | null {
    if (!this.knowledgeBase.worldElements[id]) return null;
    
    this.knowledgeBase.worldElements[id] = {
      ...this.knowledgeBase.worldElements[id],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    
    this.saveKnowledgeBase();
    return this.knowledgeBase.worldElements[id];
  }

  deleteWorldElement(id: string): boolean {
    if (!this.knowledgeBase.worldElements[id]) return false;
    delete this.knowledgeBase.worldElements[id];
    this.saveKnowledgeBase();
    return true;
  }

  getWorldElement(id: string): WorldElement | null {
    return this.knowledgeBase.worldElements[id] || null;
  }

  getAllWorldElements(): WorldElement[] {
    return Object.values(this.knowledgeBase.worldElements);
  }

  // Search and filtering
  searchContent(query: string): {
    stories: Story[];
    characters: Character[];
    worldElements: WorldElement[];
  } {
    const lowerQuery = query.toLowerCase();
    
    const stories = this.getAllStories().filter(story =>
      story.title.toLowerCase().includes(lowerQuery) ||
      story.description.toLowerCase().includes(lowerQuery) ||
      story.content.toLowerCase().includes(lowerQuery) ||
      story.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
    );

    const characters = this.getAllCharacters().filter(character =>
      character.name.toLowerCase().includes(lowerQuery) ||
      character.description.toLowerCase().includes(lowerQuery) ||
      character.notes.toLowerCase().includes(lowerQuery) ||
      character.traits.some(trait => trait.toLowerCase().includes(lowerQuery))
    );

    const worldElements = this.getAllWorldElements().filter(element =>
      element.name.toLowerCase().includes(lowerQuery) ||
      element.description.toLowerCase().includes(lowerQuery) ||
      element.notes.toLowerCase().includes(lowerQuery) ||
      element.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
    );

    return { stories, characters, worldElements };
  }
}

export const storyService = StoryService.getInstance();
