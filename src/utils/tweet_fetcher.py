"""
Tweet Fetcher Utility

This file contains the TweetFetcher class, which is responsible for fetching
and parsing metadata from Twitter/X posts using the FxTwitter service.
"""

import json
import re
import requests
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlparse
from utils.logger import Logger

logger = Logger().get_logger(__name__)

class TweetFetcher:
    """Utility class to fetch data from Twitter/X posts using FxTwitter service"""
    
    FXTWITTER_BASE = "https://api.fxtwitter.com"
    
    def __init__(self):
        logger.info("Initializing TweetMetadata utility")
    
    @staticmethod
    def _extract_tweet_info(url: str) -> Optional[Tuple[str, str]]:
        """Extract the tweet author and ID from a Twitter or X.com URL"""
        pattern = r'(?:twitter\.com|x\.com)/(\w+)/status/(\d+)'
        match = re.search(pattern, url)
        if match:
            author, tweet_id = match.group(1), match.group(2)
            logger.debug(f"Extracted author: {author}, tweet ID: {tweet_id}")
            return author, tweet_id
        logger.warning(f"Could not extract tweet info from URL: {url}")
        return None

    @staticmethod
    def _is_valid_tweet_url(url: str) -> bool:
        """Validate if the given URL is a Twitter/X post URL"""
        parsed = urlparse(url)
        is_valid = parsed.netloc in ['twitter.com', 'x.com'] and '/status/' in url
        if not is_valid:
            logger.warning(f"Invalid tweet URL format: {url}")
        return is_valid

    def get_tweet_data(self, url: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch data for a given tweet URL
        Returns None if URL is invalid or request fails
        """
        logger.info(f"Fetching data for URL: {url}")

        if not self._is_valid_tweet_url(url):
            logger.error("Invalid tweet URL provided")
            return None

        tweet_info = self._extract_tweet_info(url)
        if not tweet_info:
            logger.error("Failed to extract tweet information")
            return None

        author, tweet_id = tweet_info
        try:
            api_url = f"{self.FXTWITTER_BASE}/status/{tweet_id}"
            logger.debug(f"Making request to: {api_url}")
            
            response = requests.get(api_url)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 200:
                metadata = response.json()
                tweet = metadata['tweet']
                if tweet:
                    logger.debug(f"Response content:\n{json.dumps(tweet, indent=2, ensure_ascii=False)}")
                return tweet
            
            logger.error(f"Failed to fetch metadata. Status code: {response.status_code}")
            logger.debug(f"Response content: {metadata}")
            return None
            
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}", exc_info=True)
            return None

def main():
    """Command line interface for TweetMetadata utility."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch data from Twitter/X posts.')
    parser.add_argument('url', help='The tweet URL')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    fetcher = TweetFetcher()
    tweet = fetcher.get_tweet_data(args.url)
    
    if tweet:
        logger.info("\nTweet Data:")
        logger.info("-" * 50)
        logger.info(f"Text: {tweet.get('text', 'N/A')}")
        logger.info(f"Author: {tweet.get('author', {}).get('name', 'N/A')}")
        logger.info(f"Screen name: {tweet.get('author', {}).get('screen_name', 'N/A')}")
        logger.info(f"Media count: {len(tweet.get('media', {}).get('all', []))}")
    else:
        logger.error("Failed to fetch tweet data")

if __name__ == "__main__":
    main()
