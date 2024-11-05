from flask import Blueprint, render_template, request, jsonify
from src.reply_guy import ReplyGuy
from web.forms import TweetForm

web = Blueprint('web', __name__)
tweet_processor = ReplyGuy()  # config would be loaded from your config handler

@web.route('/', methods=['GET', 'POST'])
def index():
    form = TweetForm()
    if form.validate_on_submit():
        tweet_url = form.tweet_url.data
        result = tweet_processor.process_tweet(tweet_url)
        return render_template('result.html', result=result)
    return render_template('index.html', form=form)

@web.route('/api/analyze', methods=['POST'])
def analyze_tweet():
    data = request.get_json()
    tweet_url = data.get('tweet_url')
    if not tweet_url:
        return jsonify({"error": "No tweet URL provided"}), 400
    
    result = tweet_processor.process_tweet(tweet_url)
    return jsonify(result)
