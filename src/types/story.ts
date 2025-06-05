
export interface Character {
  id: string;
  name: string;
  description: string;
  traits: string[];
  relationships: { [characterId: string]: string };
  notes: string;
  createdAt: string;
  updatedAt: string;
}

export interface WorldElement {
  id: string;
  name: string;
  type: 'location' | 'organization' | 'concept' | 'item';
  description: string;
  tags: string[];
  notes: string;
  createdAt: string;
  updatedAt: string;
}

export interface Story {
  id: string;
  title: string;
  description: string;
  content: string;
  tags: string[];
  characters: string[]; // Character IDs
  worldElements: string[]; // WorldElement IDs
  chapters: Chapter[];
  createdAt: string;
  updatedAt: string;
}

export interface Chapter {
  id: string;
  title: string;
  content: string;
  scenes: Scene[];
  order: number;
}

export interface Scene {
  id: string;
  title: string;
  content: string;
  characters: string[]; // Character IDs present in scene
  order: number;
}

export interface KnowledgeBase {
  stories: { [id: string]: Story };
  characters: { [id: string]: Character };
  worldElements: { [id: string]: WorldElement };
}
