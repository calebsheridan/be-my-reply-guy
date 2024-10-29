"""
Video Processor Agent

This file contains the VideoProcessorAgent class, which is responsible for processing
video files by extracting key frames and analyzing them using an AI model. It inherits
from the base Agent class and implements the process method to perform video analysis.

The agent uses OpenCV for frame extraction and the OpenAI API to generate an analysis
of the extracted frames.
"""

from .base_agent import Agent
import cv2
import base64
import os
from openai import OpenAI
import requests
from urllib.parse import urlparse
import argparse
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class VideoProcessorAgent(Agent):
    def __init__(self, model="gpt-4o", base_url="https://api.openai.com/v1", api_key=None):
        
        system_prompt = """
        You are a media processing assistant. Analyze the provided video frames and
        describe the content, noting any changes or progression across the frames.
        """
        
        super().__init__(
            model,
            system_prompt,
            base_url,
            api_key
        )
        self.client = OpenAI()
        logger.info(f"VideoProcessorAgent initialized with model: {self.model}")

    def extract_frames(self, video_path):
        """Extract specified frames from the video."""
        logger.info(f"Extracting frames from video: {video_path}")
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []
        if total_frames < 1:
            logger.warning("Video contains no frames")
            return frames
            
        # Calculate frame positions based on video length
        if total_frames == 1:
            positions = [0]
        elif total_frames == 2:
            positions = [0, 1]
        else:
            positions = [
                0,                    # First frame
                total_frames // 2,    # Middle frame
                total_frames - 1      # Last frame
            ]

        for position in positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
                logger.debug(f"Frame extracted at position {position}")
            else:
                logger.warning(f"Failed to extract frame at position {position}")

        cap.release()
        logger.info(f"Extracted {len(frames)} frames")
        return frames

    def encode_frame(self, frame):
        """Encode a frame to base64 string."""
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')

    def analyze_frames(self, frames):
        """Analyze the extracted frames using the OpenAI API."""
        logger.info("Analyzing frames")
        encoded_frames = [self.encode_frame(frame) for frame in frames]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Analyze the following frames from a video:"},
                        *[{"type": "text", "text": f"Frame {i+1}:"} for i in range(len(encoded_frames))],
                        *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}} for frame in encoded_frames]
                    ]}
                ],
                max_tokens=300
            )
            logger.info("Frame analysis completed successfully")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during frame analysis: {str(e)}", exc_info=True)
            return None

    def process(self, video_path):
        """
        Process the given video file by extracting frames and analyzing them.

        Args:
            video_path (str): The path or URL to the video file to be processed.

        Returns:
            str: A description of the video content based on frame analysis.
        """
        logger.info(f"Processing video: {video_path}")
        
        try:
            if video_path.startswith(('http://', 'https://')):
                # Handle URL
                response = requests.get(video_path)
                if response.status_code != 200:
                    logger.error(f"Error: Failed to download video from {video_path}")
                    return f"Error: Failed to download video. Status code: {response.status_code}"
                
                # Save the video to a temporary file
                temp_file = f"temp_{os.path.basename(urlparse(video_path).path)}"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                video_path = temp_file
            elif not os.path.exists(video_path):
                logger.error(f"Error: Video file not found at {video_path}")
                return "Error: Video file not found."

            frames = self.extract_frames(video_path)
            if not frames:
                logger.error("Error: Failed to extract frames from the video.")
                return "Error: Failed to extract frames from the video."

            analysis = self.analyze_frames(frames)
            logger.info(f"Video processing completed successfully: {analysis}")
            
            # Clean up temporary file if it was created
            if video_path.startswith('temp_'):
                os.remove(video_path)
            
            return analysis
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}", exc_info=True)
            return f"Error processing video: {str(e)}"

def main():
    """Command line interface for VideoProcessorAgent."""
    parser = argparse.ArgumentParser(description='Process and analyze videos using AI.')
    parser.add_argument('video_path', help='Path or URL to the video file')
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = VideoProcessorAgent()
    
    # Process the video
    result = agent.process(args.video_path)
    print("\nVideo Analysis Result:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    main()
