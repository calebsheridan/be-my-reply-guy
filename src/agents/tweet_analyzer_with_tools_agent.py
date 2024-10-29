"""
Tweet Analyzer With Tools Agent

This file contains the TweetAnalyzerWithToolsAgent class, which extends the base Agent
to analyze tweets using AI models and additional tools like internet search and image analysis.
"""

from .base_agent import Agent
from utils.tools_manager import ToolsManager
from utils.tools_registry import register_all_tools
import argparse
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class TweetAnalyzerWithToolsAgent(Agent):
    BASE_SYSTEM_PROMPT = """
    Role: You are an expert at analyzing social media content, especially tweets.

    Instructions: Analyze the given tweet and provide insights on:
    1. Sentiment: Determine if the overall sentiment is positive, negative, or neutral.
    2. Topics: Identify the main topics or themes discussed.
    3. Entities: Recognize notable entities (people, organizations, products, etc.).
    4. Context: Provide relevant background information using the available tools.
    5. Tone: Describe the overall tone (formal, casual, humorous, sarcastic, etc.).

    Function calling: Use the supplied tools to help analyze the tweet.
    Available tools:
    {tool_descriptions}
    """

    def __init__(self, model="gpt-4o", base_url="https://api.openai.com/v1", api_key=None):
        self.tools_manager = ToolsManager()
        register_all_tools(self.tools_manager)
        
        # Generate tool descriptions from registered tools
        tool_descriptions = []
        for tool_name, tool in self.tools_manager.tools.items():  # Access the tools dictionary correctly
            tool_descriptions.append(f"   - `{tool_name}`: {tool.description}")
        
        system_prompt = self.BASE_SYSTEM_PROMPT.format(
            tool_descriptions="\n".join(tool_descriptions)
        )
        
        super().__init__(model, system_prompt, base_url, api_key)
        logger.info(f"TweetAnalyzerWithToolsAgent initialized with model: {model}")

    def process(self, tweet_context: str) -> str:
        """
        Analyze the given tweet using the AI model and additional tools.

        Args:
            tweet_context (str): A string containing the tweet context including
                                  id, author, content, and media_descriptions.

        Returns:
            str: An analysis of the tweet.
        """
        logger.info(f"Processing tweet: {tweet_context[:50]}...")
        
        tools = self.tools_manager.get_tool_definitions()
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Analyze this tweet:\n\n{tweet_context}"}
        ]
        
        try:
            while True:
                logger.debug("Sending request to OpenAI API")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )

                response_message = response.choices[0].message
                
                if not response_message.tool_calls:
                    logger.info("Analysis complete - no more tool calls")
                    return response_message.content

                messages.append(response_message)
                for tool_call in response_message.tool_calls:
                    logger.info(f"Processing tool call: {tool_call.function.name}")
                    try:
                        result = self.tools_manager.execute_tool(
                            tool_call.function.name,
                            tool_call.function.arguments
                        )
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": result
                        })
                    except ValueError as e:
                        logger.warning(f"Tool execution failed: {e}")
                        
        except Exception as e:
            logger.error(f"Error during tweet analysis: {str(e)}", exc_info=True)
            return None

def main():
    """Command line interface for TweetAnalyzerWithToolsAgent."""
    parser = argparse.ArgumentParser(description='Analyze tweets using AI and additional tools.')
    parser.add_argument('tweet', help='The tweet text to analyze')
    
    args = parser.parse_args()
    
    # Create a mock processed tweet for demonstration
    processed_tweet = {
        'id': '123',
        'author': 'user',
        'content': args.tweet,
        'media_descriptions': []
    }
    
    # Initialize the agent
    agent = TweetAnalyzerWithToolsAgent()
    
    # Process the tweet
    result = agent.process(processed_tweet)
    print("\nTweet Analysis Result:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    main()
