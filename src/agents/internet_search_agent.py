"""
Internet search tool for the Be My Reply Guy application.
This file contains the InternetSearchAgent class for searching the internet using the Perplexity API.
"""

from .base_agent import Agent
import os
import argparse
from openai import OpenAI
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class InternetSearchAgent(Agent):
    def __init__(self, model="llama-3.1-sonar-small-128k-online", base_url="https://api.perplexity.ai", api_key=None):
        system_prompt = """
        You are a helpful assistant that searches the internet for information.
        """
        
        super().__init__(
            model,
            system_prompt,
            base_url,
            api_key
        )
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        logger.info(f"InternetSearchAgent initialized with model: {self.model}")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def process(self, query: str) -> str:
        """
        Search the internet using the Perplexity API.
        
        Args:
            query (str): The search query
            
        Returns:
            str: The search results or error message
        """
        logger.info(f"Processing search query: {query}")
        
        try:
            result = self.search_internet(query)
            logger.info(f"Search completed successfully: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"Error processing search: {str(e)}", exc_info=True)
            return f"Error processing search: {str(e)}"

    def search_internet(self, query: str) -> str:
        """Execute the internet search using Perplexity API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Search the internet for: {query}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in search_internet: {str(e)}", exc_info=True)
            raise

def main():
    """Command line interface for InternetSearchAgent."""
    parser = argparse.ArgumentParser(description='Search the internet using AI.')
    parser.add_argument('query', help='The search query')
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = InternetSearchAgent()
    
    # Process the search
    result = agent.process(args.query)
    print("\nSearch Result:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    main()
