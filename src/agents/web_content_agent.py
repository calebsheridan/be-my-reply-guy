"""
Web Content Agent

This file contains the WebContentAgent class, which is responsible for processing
web URLs and generating summaries of their content. It inherits from the base Agent class
and implements the process method to perform web content analysis.

The agent uses Firecrawl for web scraping and can be extended to use OpenAI for better summarization.
"""

from .base_agent import Agent
from firecrawl.firecrawl import FirecrawlApp
import os
import argparse
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class WebContentAgent(Agent):
    def __init__(self, model="gpt-4", base_url="https://api.openai.com/v1", api_key=None):
        system_prompt = """
        You are a web content analysis assistant. Process web pages and provide
        clear, concise summaries of their content while preserving key information.
        """
        
        super().__init__(
            model,
            system_prompt,
            base_url,
            api_key
        )
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        self.firecrawl_app = FirecrawlApp(api_key=self.firecrawl_api_key) if self.firecrawl_api_key else None
        logger.info(f"WebContentAgent initialized with model: {self.model}")

    def process(self, url: str) -> str:
        """
        Process the given URL and generate a summary of its content.

        Args:
            url (str): The URL to process

        Returns:
            str: A summary of the web content or error message
        """
        logger.info(f"Processing URL: {url}")
        
        # Check if URL is an image
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            return "Error: URL is an image"
            
        if not self.firecrawl_app:
            logger.error("Firecrawl not initialized. Cannot process URL.")
            return "Error: Firecrawl not initialized"

        try:
            content = self.scrape_content(url)
            if not content:
                return "Error: Failed to scrape content"
                
            summary = self.summarize_content(content)
            logger.info(f"URL processing completed successfully: {summary[:100]}...")
            
            return f"URL content summary: {summary}"
        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}", exc_info=True)
            return f"Error processing URL: {str(e)}"

    def scrape_content(self, url: str) -> str:
        """Scrape content from the URL using Firecrawl."""
        try:
            scraped_data = self.firecrawl_app.scrape_url(url, params={'formats': ['markdown']})
            return scraped_data.get('markdown', '')
        except Exception as e:
            logger.error(f"Error in scrape_content: {str(e)}", exc_info=True)
            return None

    def summarize_content(self, content: str) -> str:
        """Summarize the content using the OpenAI API."""
        logger.info("Summarizing content using LLM")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Please provide a comprehensive summary of the following web content:\n\n{content}"}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content
            logger.info("Content summarization completed successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error during content summarization: {str(e)}", exc_info=True)
            # Fallback to simple truncation if LLM summarization fails
            max_length = 20000
            return content[:max_length] + "..." if len(content) > max_length else content

def main():
    """Command line interface for WebContentAgent."""
    parser = argparse.ArgumentParser(description='Process and summarize web content.')
    parser.add_argument('url', help='URL to process')
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = WebContentAgent()
    
    # Process the URL
    result = agent.process(args.url)
    print("\nWeb Content Analysis Result:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    main()

