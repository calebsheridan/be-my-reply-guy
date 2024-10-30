"""
Base Agent

This file contains the abstract base class for all agent implementations in the project.
It provides a common interface and shared functionality for different types of agents.

The Agent class is designed to be flexible, allowing for different AI models and
configurations to be injected, making it easier to swap out or update components.
"""

from abc import ABC, abstractmethod
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.logger import Logger

logger = Logger().get_logger(__name__)

# Load environment variables from .env file
load_dotenv()

class Agent(ABC):
    def __init__(self, 
                 model="gpt-4o-mini", 
                 system_prompt="You are a helpful AI assistant.", 
                 base_url="https://api.openai.com/v1", 
                 api_key=None):
        self.model = model
        self.system_prompt = system_prompt
        self.base_url = base_url
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as OPENAI_API_KEY environment variable.")
        self.client = self._setup_openai_client()

    def _setup_openai_client(self):
        """
        Set up and return the OpenAI client with the provided base URL and API key.
        """
        return OpenAI(api_key=self.api_key, base_url=self.base_url)

    @abstractmethod
    def process(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses for processing specific tasks.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The processed result, which will vary depending on the specific agent implementation.
        """
        pass

    def get_chat_completion(self, messages):
        """
        Get a chat completion from the OpenAI API using the set up client.

        Args:
            messages (list): A list of message dictionaries to send to the API.

        Returns:
            str: The content of the API's response message.

        Raises:
            Exception: If there's an error in the API call.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during API call: {str(e)}")
            raise

    def get_chat_completions(self, messages, n=1):
        """
        Get a chat completion from the OpenAI API using the set up client.

        Args:
            messages (list): A list of message dictionaries to send to the API.

        Returns:
            str: The content of the API's response message.

        Raises:
            Exception: If there's an error in the API call.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                n=n
            )
            return [choice.message.content for choice in response.choices]
        except Exception as e:
            logger.error(f"Error during API call: {str(e)}")
            raise