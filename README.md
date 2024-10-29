# Be My Reply Guy

Generate replies to people on Twitter using AI. This tool helps you generate contextually relevant replies by analyzing tweets, their media content, and generating appropriate responses.

## How It Works

- Fetch tweet data from a twitter.com/x.com URL
- Process tweet media, including images, videos, urls and quotes
- Search the internet and visit web sites
- Analyze the tweet with the right context
- Generate replies, including custom configuration

## Project Structure

```
be-my-reply-guy/
├── config/
│ └── config.yaml
├── src/
│ ├── agents/
│ │ ├── base_agent.py
│ │ ├── tweet_analyzer_agent.py
│ │ ├── tweet_analyzer_with_tools_agent.py
│ │ ├── reply_generator_agent.py
│ │ ├── internet_search_agent.py
│ │ ├── image_processor_agent.py
│ │ ├── video_processor_agent.py
│ │ └── web_content_agent.py
│ ├── utils/
│ │ ├── config_handler.py
│ │ ├── tools_manager.py
│ │ └── tools_registry.py
│ ├── main.py
├── .env
├── INSTRUCTIONS.md
├── README.md
├── requirements.txt
└── SPECS.md
```

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/calebsheridan/be-my-reply-guy.git
   cd be-my-reply-guy
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with the required API keys:
   ```
   PERPLEXITY_API_KEY=
   CLAUDE_API_KEY=
   GROQ_API_KEY=
   OPENAI_API_KEY=
   FIRECRAWL_API_KEY=
   ```

5. Configure your `config/config.yaml` file with the desired settings.

6. Run the application:
   ```
   python src/main.py
   ```

