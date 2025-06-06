
"""Image generation service using IONOS AI Model Hub."""

import requests
import json
import os
from typing import Dict, List, Optional
from config import IONOS_API_TOKEN, IONOS_IMAGE_URL

class IONOSImageGenerator:
    """Image generation service using IONOS AI Model Hub."""
    
    def __init__(self):
        self.api_token = IONOS_API_TOKEN
        self.base_url = IONOS_IMAGE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def generate_image(self, prompt: str, style: str = "photorealistic", size: str = "1024x1024") -> Optional[str]:
        """Generate an image using IONOS AI Model Hub."""
        if not self.api_token:
            return None
        
        # Style-specific prompt enhancements
        style_prompts = {
            "photorealistic": f"{prompt}, photorealistic, high quality, detailed",
            "artistic": f"{prompt}, artistic style, painted, creative",
            "cinematic": f"{prompt}, cinematic lighting, dramatic, film-like",
            "fantasy": f"{prompt}, fantasy art, magical, ethereal",
            "noir": f"{prompt}, film noir style, black and white, dramatic shadows"
        }
        
        enhanced_prompt = style_prompts.get(style, f"{prompt}, high quality")
        
        payload = {
            "model": "dall-e-3",
            "prompt": enhanced_prompt,
            "n": 1,
            "size": size,
            "quality": "standard"
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                return result['data'][0]['url']
            
        except requests.exceptions.RequestException as e:
            print(f"Error generating image: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        
        return None
    
    def generate_mood_board_images(self, story_context: str, character_context: str = "", world_context: str = "") -> List[str]:
        """Generate multiple images for a mood board based on story elements."""
        images = []
        
        # Generate different types of images
        prompts = []
        
        if story_context:
            prompts.append(f"Scene from story: {story_context}")
        
        if character_context:
            prompts.append(f"Character portrait: {character_context}")
        
        if world_context:
            prompts.append(f"Environment and setting: {world_context}")
        
        # Add some general mood images if we don't have enough context
        if len(prompts) < 3:
            prompts.append(f"Atmospheric mood for: {story_context or 'creative story'}")
        
        for prompt in prompts[:4]:  # Limit to 4 images
            image_url = self.generate_image(prompt, style="cinematic")
            if image_url:
                images.append(image_url)
        
        return images

# Global instance
image_generator = IONOSImageGenerator()
