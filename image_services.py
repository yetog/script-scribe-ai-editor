
"""Image processing and OCR services for ScriptVoice."""

import pytesseract
from PIL import Image
from typing import Tuple
import os


def extract_text_from_image(image_path) -> Tuple[str, str]:
    """Extract text from uploaded image using OCR with improved error handling."""
    if image_path is None:
        return "", '<div class="status-error">❌ Please upload an image</div>'
    
    if not os.path.exists(image_path):
        return "", '<div class="status-error">❌ Image file not found</div>'
    
    try:
        # Open and process the image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for better OCR results)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(img, config='--psm 6')
            
            if text.strip():
                # Clean up the text a bit
                cleaned_text = text.strip().replace('\n\n\n', '\n\n')
                return cleaned_text, '<div class="status-success">✅ Text extracted successfully! Content added to editor.</div>'
            else:
                return "", '<div class="status-error">❌ No readable text found in the image. Try with a clearer image.</div>'
    
    except Exception as e:
        return "", f'<div class="status-error">❌ Error extracting text: {str(e)}</div>'


def preprocess_image_for_ocr(image_path: str) -> str:
    """Preprocess image to improve OCR accuracy (utility function)."""
    try:
        with Image.open(image_path) as img:
            # Convert to grayscale for better OCR
            img = img.convert('L')
            
            # Enhance contrast
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            
            # Save preprocessed image
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            img.save(preprocessed_path)
            return preprocessed_path
            
    except Exception:
        return image_path  # Return original if preprocessing fails
