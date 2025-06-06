
"""Image generation service using IONOS AI Model Hub."""

import requests
import json
import os
import base64
from typing import Dict, List, Optional
from datetime import datetime
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
        
        # Ensure directories exist
        os.makedirs("generated_images", exist_ok=True)
        os.makedirs("mood_boards", exist_ok=True)
    
    def generate_image(self, prompt: str, style: str = "photorealistic", size: str = "1024x1024") -> Optional[str]:
        """Generate an image using IONOS AI Model Hub."""
        if not self.api_token:
            print("❌ IONOS API token not configured")
            return None
        
        # Style-specific prompt enhancements
        style_prompts = {
            "photorealistic": f"{prompt}, photorealistic, high quality, detailed, 8k resolution",
            "artistic": f"{prompt}, artistic style, painted, creative, masterpiece",
            "cinematic": f"{prompt}, cinematic lighting, dramatic, film-like, professional photography",
            "fantasy": f"{prompt}, fantasy art, magical, ethereal, concept art",
            "noir": f"{prompt}, film noir style, black and white, dramatic shadows, vintage"
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
            print(f"🎨 Generating image with prompt: {enhanced_prompt[:100]}...")
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 401:
                print("❌ Authentication failed - check IONOS API token")
                return None
            elif response.status_code == 429:
                print("❌ Rate limit exceeded - please wait before trying again")
                return None
            
            response.raise_for_status()
            
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                image_data = result['data'][0]
                
                # Handle both URL and base64 responses
                if 'url' in image_data:
                    image_url = image_data['url']
                    print("✅ Image generated successfully (URL)")
                    return image_url
                elif 'b64_json' in image_data:
                    # Save base64 image locally
                    image_filename = f"generated_images/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    with open(image_filename, 'wb') as f:
                        f.write(base64.b64decode(image_data['b64_json']))
                    print(f"✅ Image generated and saved as {image_filename}")
                    return image_filename
            
        except requests.exceptions.Timeout:
            print("❌ Request timeout - image generation took too long")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - please check your internet connection")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
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
            prompts.append(f"Atmospheric mood for: {story_context or character_context or world_context or 'creative story'}")
        
        print(f"🎨 Generating {len(prompts)} mood board images...")
        
        for i, prompt in enumerate(prompts[:4]):  # Limit to 4 images
            print(f"Generating image {i+1}/{len(prompts[:4])}")
            image_url = self.generate_image(prompt, style="cinematic")
            if image_url:
                images.append(image_url)
            else:
                print(f"❌ Failed to generate image {i+1}")
        
        print(f"✅ Generated {len(images)} out of {len(prompts[:4])} requested images")
        return images

# Global instance
image_generator = IONOSImageGenerator()
