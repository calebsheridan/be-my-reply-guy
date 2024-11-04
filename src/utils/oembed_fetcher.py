import requests
from typing import Dict, Optional

class OEmbedFetcher:
    def __init__(self):
        self.oembed_url = "https://publish.twitter.com/oembed"

    def get_embed_html(self, tweet_url: str) -> Optional[str]:
        """Fetch the oEmbed HTML for a tweet."""
        try:
            params = {
                'url': tweet_url,
                'omit_script': False,  # Include the Twitter widgets.js
                'align': 'center',
                'theme': 'light'  # or 'dark' if you prefer
            }
            response = requests.get(self.oembed_url, params=params)
            response.raise_for_status()
            return response.json()['html']
        except Exception as e:
            print(f"Error fetching oEmbed: {e}")
            return None 