"""
Reply Generator Agent

This file contains the ReplyGeneratorAgent class, which is responsible for generating
replies to tweets using AI models. It inherits from the base Agent class and implements
the process method to generate appropriate responses.
"""

from .base_agent import Agent
from utils.config_handler import load_config
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class ReplyGeneratorAgent(Agent):
    def __init__(self, model="gpt-4o", base_url="https://api.openai.com/v1", api_key=None):
        system_prompt = """
        You are an expert at generating contextually appropriate replies to tweets.
        Generate engaging and relevant responses while maintaining the specified personality
        and adhering to given criteria.
        """
        super().__init__(model, system_prompt, base_url, api_key)
        self.config = load_config()
        logger.info(f"ReplyGeneratorAgent initialized with model: {model}")

    def process(self, tweet, tweet_analysis):
        """
        Generate replies for the given tweet using the AI model.

        Args:
            tweet (str): The original tweet text
            tweet_analysis (str): Analysis of the tweet from TweetAnalyzerAgent
            media_descriptions (list, optional): List of media descriptions from ImageProcessorAgent

        Returns:
            list: Generated reply options
        """
        logger.info(f"Generating replies for tweet: {tweet[:50]}...")

        try:
            prompt = self._create_personality_aware_prompt(tweet, tweet_analysis)
            replies = self._generate_replies(prompt)
            logger.info(f"Successfully generated {len(replies)} replies")
            return replies
        except Exception as e:
            logger.error(f"Error generating replies: {str(e)}", exc_info=True)
            return []

    def _create_personality_aware_prompt(self, tweet_context, tweet_analysis):
        """Create a detailed prompt incorporating all available context."""
        reply_guy_config = self.config['reply_guy_account']
        reply_criteria = self.config['reply_criteria']

        prompt = f"""
        Generate a reply to the following tweet:
        "{tweet_context}"

        Tweet Analysis:
        {tweet_analysis}
        """

        prompt += "\nConsider the following criteria for the reply:\n"
        for criterion in reply_criteria:
            for key, value in criterion.items():
                prompt += f"- {key.capitalize()}: {value}\n"

        prompt += f"\nAvoid discussing: {', '.join(reply_guy_config['avoid_topics'])}"
        return prompt

    def _generate_replies(self, prompt):
        """Generate replies using the AI model."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.get_chat_completions(messages, self.config['number_of_replies'])
            return response
        except Exception as e:
            logger.error(f"Error in reply generation: {str(e)}", exc_info=True)
            return []
