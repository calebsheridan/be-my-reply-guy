"""
Tweet Analyzer Agent

This file contains the TweetAnalyzerAgent class, which is responsible for analyzing
tweets using an AI model. It inherits from the base Agent class and implements
the process method to perform tweet analysis.

The agent uses the OpenAI API to generate an analysis of the given tweet and then
parses the analysis into a structured format.
"""

from .base_agent import Agent
import argparse
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class TweetAnalyzerAgent(Agent):
    DEFAULT_SYSTEM_PROMPT = """
    You are an expert tweet analyzer. Your task is to analyze the given tweet and provide insights on the following aspects:
    1. Sentiment: Determine if the overall sentiment is positive, negative, or neutral.
    2. Topics: Identify the main topics or themes discussed in the tweet.
    3. Entities: Recognize and list any notable entities (people, organizations, products, etc.) mentioned.
    4. Language: Detect the language used in the tweet.
    5. Tone: Describe the overall tone (e.g., formal, casual, humorous, sarcastic, etc.).
    """

    def __init__(self, model="gpt-4o", base_url="https://api.openai.com/v1", api_key=None, system_prompt=None):
        super().__init__(model, system_prompt or self.DEFAULT_SYSTEM_PROMPT, base_url, api_key)
        logger.info(f"TweetAnalyzerAgent initialized with model: {model}")

    def process(self, tweet):
        """
        Analyze the given tweet using the AI model.

        Args:
            tweet (str): The tweet text to be analyzed.

        Returns:
            str: An analysis of the tweet.
        """
        logger.info(f"Processing tweet: {tweet[:50]}...")  # Log first 50 characters of the tweet
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Analyze the following tweet:\n{tweet}"}
        ]
        
        try:
            logger.debug("Sending request to OpenAI API")
            analysis = self.get_chat_completion(messages)
            logger.info(f"Received response from OpenAI API: {analysis}")
            logger.info("Tweet analysis completed successfully")
            return analysis
        except Exception as e:
            logger.error(f"Error during tweet analysis: {str(e)}", exc_info=True)
            return None

def main():
    """Command line interface for TweetAnalyzerAgent."""
    parser = argparse.ArgumentParser(description='Analyze tweets using AI.')
    parser.add_argument('tweet', help='The tweet text to analyze')
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = TweetAnalyzerAgent()
    
    # Process the tweet
    result = agent.process(args.tweet)
    print("\nTweet Analysis Result:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    main()
