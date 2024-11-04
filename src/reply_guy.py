from typing import Dict, List

from src.agents.image_processor_agent import ImageProcessorAgent
from src.agents.reply_generator_agent import ReplyGeneratorAgent
from src.agents.tweet_analyzer_with_tools_agent import TweetAnalyzerWithToolsAgent
from src.agents.video_processor_agent import VideoProcessorAgent
from src.utils.tweet_fetcher import TweetFetcher
from src.utils.config_handler import load_config

class ReplyGuy:
    def __init__(self):
        self.config = load_config()
        self.tweet_fetcher = TweetFetcher()
        self.image_processor = ImageProcessorAgent()
        self.video_processor = VideoProcessorAgent()
        self.tweet_analyzer = TweetAnalyzerWithToolsAgent()
        self.reply_generator = ReplyGeneratorAgent()
    
    def process_tweet(self, tweet_url: str) -> Dict:
        try:
            tweet = self.tweet_fetcher.get_tweet_data(tweet_url)
            media_descriptions = self._process_media(tweet)
            tweet_context = self._build_tweet_context(tweet, media_descriptions)
            analysis = self.tweet_analyzer.process(tweet_context)
            replies = self.reply_generator.process(tweet['text'], analysis)
            output_path = "output_path"
            
            return {
                "status": "success",
                "tweet": tweet,
                "analysis": analysis,
                "replies": replies,
                "output_path": output_path
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            } 
    
    def _process_media(self, tweet: Dict) -> List[str]:
        """Process any media (images/videos) attached to the tweet."""
        media_descriptions = []
        
        if 'media' in tweet and 'all' in tweet['media']:
            for media in tweet['media']['all']:
                if media['type'] == 'photo':
                    media_descriptions.append(self.image_processor.process(media['url']))
                elif media['type'] == 'video':
                    media_descriptions.append(self.video_processor.process(media['url']))
        
        return media_descriptions
    
    def _build_tweet_context(self, tweet: Dict, media_descriptions: List[str]) -> str:
        """Build a context dictionary containing tweet information and media descriptions."""

        quote_context = None
        if 'quote' in tweet:
            quote_context = f"""\n\n## Quoted Tweet\n\n### Quote Text\n\n{tweet['quote']['text']}\n\n### Quote Author\n\n{tweet['quote']['author']}"""

        tweet_context = f"""
        ## Tweet Text\n\n{tweet['text']}

        ## Tweet Author\n\n{tweet['author']}

        ## Tweet Media Descriptions\n\n{media_descriptions}

        {quote_context}
        """
        return tweet_context
