"""
Image Processor Agent

This file contains the ImageProcessorAgent class, which is responsible for processing
image files and analyzing them using an AI model. It inherits from the base Agent class
and implements the process method to perform image analysis.

The agent uses the OpenAI API to generate an analysis of the image.
"""

from .base_agent import Agent
import base64
import os
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
import argparse
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class ImageProcessorAgent(Agent):
    def __init__(self, model="gpt-4o", base_url="https://api.openai.com/v1", api_key=None):
        system_prompt = """
        You are an image analysis assistant. Analyze the provided image and
        describe its content in detail, noting important features, objects, and any text present.
        """
        
        super().__init__(
            model,
            system_prompt,
            base_url,
            api_key
        )
        self.client = OpenAI()
        logger.info(f"ImageProcessorAgent initialized with model: {self.model}")

    def process(self, image_path):
        """
        Process the given image file by analyzing it.

        Args:
            image_path (str): The path or URL to the image file to be processed.

        Returns:
            str: A description of the image content based on analysis.
        """
        logger.info(f"Processing image: {image_path}")
        
        try:
            img_data = self.load_image(image_path)
            if img_data is None:
                return "Error: Failed to load image."

            analysis = self.analyze_image(img_data)
            logger.info(f"Image processing completed successfully: {analysis[:100]}...")
            
            return analysis
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}", exc_info=True)
            return f"Error processing image: {str(e)}"

    def load_image(self, image_path):
        """Load image from file or URL."""
        try:
            if image_path.startswith(('http://', 'https://')):
                response = requests.get(image_path)
                if response.status_code != 200:
                    logger.error(f"Error: Failed to download image from {image_path}")
                    return None
                img = Image.open(BytesIO(response.content))
            else:
                if not os.path.exists(image_path):
                    logger.error(f"Error: Image file not found at {image_path}")
                    return None
                img = Image.open(image_path)

            img = img.convert('RGB')
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='JPEG')
            return img_byte_arr.getvalue()
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}", exc_info=True)
            return None

    def analyze_image(self, img_data):
        """Analyze the image using the OpenAI API."""
        logger.info("Analyzing image")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Analyze the following image:"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(img_data).decode('utf-8')}"}}
                    ]}
                ],
                max_tokens=300
            )
            logger.info("Image analysis completed successfully")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during image analysis: {str(e)}", exc_info=True)
            return None

def main():
    """Command line interface for ImageProcessorAgent."""
    parser = argparse.ArgumentParser(description='Process and analyze images using AI.')
    parser.add_argument('image_path', help='Path or URL to the image file')
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = ImageProcessorAgent()
    
    # Process the image
    result = agent.process(args.image_path)
    print("\nImage Analysis Result:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    main()
