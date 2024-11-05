from flask import Flask
from web.routes import web
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__, 
        template_folder='web/templates'
    )
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    
    # Register the blueprint
    app.register_blueprint(web)
    
    return app

# Create the app instance outside of __main__
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='127.0.0.1')
