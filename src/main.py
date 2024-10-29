"""
Main entry point for the Be My Reply Guy application.
This file orchestrates the overall flow of the application.
"""

from datetime import datetime
import os
from dotenv import load_dotenv
from agents.internet_search_agent import InternetSearchAgent
from agents.tweet_analyzer_with_tools_agent import TweetAnalyzerWithToolsAgent
from utils.config_handler import load_config
from agents.image_processor_agent import ImageProcessorAgent
from utils.tweet_fetcher import TweetFetcher
from agents.video_processor_agent import VideoProcessorAgent
from agents.tweet_analyzer_agent import TweetAnalyzerAgent
from agents.reply_generator_agent import ReplyGeneratorAgent
from utils.logger import Logger

# Set up logging
logger = Logger().get_logger(__name__)

def main():
    # Load environment variables
    load_dotenv()

    # Load configuration
    config = load_config()
    if config is None:
        print("Failed to load configuration. Exiting.")
        return

    tweet_url = "https://x.com/GroqInc/status/1851251889309986932"
    tweet_fetcher = TweetFetcher()
    tweet = tweet_fetcher.get_tweet_data(tweet_url)
    logger.info(f"Tweet: {tweet}")

    image_processor = ImageProcessorAgent()
    video_processor = VideoProcessorAgent()

    # avatar_description = image_processor.process(tweet['author']['avatar_url'])
    # banner_description = image_processor.process(tweet['author']['banner_url'])

    media_descriptions = []
    # Safely check if 'media' exists in tweet and has 'all' key
    if 'media' in tweet and 'all' in tweet['media']:
        for media in tweet['media']['all']:
            if media['type'] == 'photo':
                media_descriptions.append(image_processor.process(media['url']))
            elif media['type'] == 'video':
                media_descriptions.append(video_processor.process(media['url']))
    else:
        logger.info("No media found in tweet")
    
    quote_context = None
    if 'quote' in tweet:
        quote_context = f"""\n\n## Quoted Tweet\n\n### Quote Text\n\n{tweet['quote']['text']}\n\n### Quote Author\n\n{tweet['quote']['author']}"""

    tweet_context = f"""
## Tweet Text

{tweet['text']}

## Tweet Author

{tweet['author']}

## Tweet Media Descriptions

{media_descriptions}

{quote_context}
"""
    # tweet_analyzer = TweetAnalyzerAgent()
    # tweet_analysis = tweet_analyzer.process(tweet_context)
    tweet_analyzer_with_tools = TweetAnalyzerWithToolsAgent()
    tweet_analysis = tweet_analyzer_with_tools.process(tweet_context)
    # tweet_analysis = analyze_tweet(tweet_context)
    logger.info(f"Tweet analysis: {tweet_analysis}")

    reply_generator = ReplyGeneratorAgent()
    replies = reply_generator.process(tweet['text'], tweet_analysis)
    logger.info(f"Replies: {replies}")
    # return

    # Generate timestamp for the output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Format: YYYYMMDD_HHMMSS_mmm
    output_filename = f"generated_replies_{timestamp}.md"
    output_path = os.path.join(config['output_folder'], output_filename)

    # Ensure the output folder exists
    os.makedirs(config['output_folder'], exist_ok=True)

    # Write replies to file
    write_replies_to_file(tweet, tweet_context, tweet_analysis, replies, media_descriptions, output_path)

    print(f"Replies generated and saved to {output_path}")

def write_replies_to_file(tweet, tweet_context,tweet_analysis, replies, media_descriptions, output_file):
    with open(output_file, 'w') as f:
        f.write("# Generated Replies\n\n")
        f.write("## Original Tweet\n\n")
        f.write(f"{tweet['text']}\n\n")
        f.write(f"by @{tweet['author']['screen_name']}\n\n")
        f.write("## Generated Replies\n\n")
        for i, reply in enumerate(replies, 1):
            f.write(f"{i}. {reply}\n\n")
        f.write("## Tweet Analysis\n\n")
        f.write(f"{tweet_analysis}\n\n")
        f.write("## Tweet Context\n\n")
        f.write(f"{tweet_context}\n\n")
        f.write("## Media Descriptions\n\n")
        for desc in media_descriptions:
            f.write(f"- {desc}\n")

if __name__ == "__main__":
    main()
