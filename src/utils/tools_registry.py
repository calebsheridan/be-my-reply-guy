"""
Central registry for all available tools.
Register new tools here to make them available throughout the application.
"""

from utils.tools_manager import Tool, ToolsManager
from agents.internet_search_agent import InternetSearchAgent
from agents.image_processor_agent import ImageProcessorAgent
from agents.web_content_agent import WebContentAgent
from agents.video_processor_agent import VideoProcessorAgent

def search_internet(params):
    """Implementation function for internet search tool."""
    agent = InternetSearchAgent()
    return agent.process(params["query"])

def analyze_image(params):
    """Implementation function for image analysis tool."""
    agent = ImageProcessorAgent()
    return agent.process(params["image_url"])

def summarize_webpage(params):
    """Implementation function for web content summarization tool."""
    agent = WebContentAgent()
    return agent.process(params["url"])

def analyze_video(params):
    """Implementation function for video analysis tool."""
    agent = VideoProcessorAgent()
    return agent.process(params["video_url"])

def register_all_tools(tools_manager: ToolsManager):
    """Register all available tools with the provided manager."""
    tools_manager.register_tool(Tool(
        name="search_internet",
        description="Search the internet for information",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        },
        implementation=search_internet
    ))

    tools_manager.register_tool(Tool(
        name="analyze_image",
        description="Analyze an image from a given URL",
        parameters={
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "URL of the image to analyze"
                }
            },
            "required": ["image_url"]
        },
        implementation=analyze_image
    ))

    tools_manager.register_tool(Tool(
        name="summarize_webpage",
        description="Generate a summary of a webpage's content",
        parameters={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL of the webpage to summarize"
                }
            },
            "required": ["url"]
        },
        implementation=summarize_webpage
    ))

    tools_manager.register_tool(Tool(
        name="analyze_video",
        description="Analyze a video by extracting and analyzing key frames",
        parameters={
            "type": "object",
            "properties": {
                "video_url": {
                    "type": "string",
                    "description": "URL or path to the video file to analyze"
                }
            },
            "required": ["video_url"]
        },
        implementation=analyze_video
    ))
