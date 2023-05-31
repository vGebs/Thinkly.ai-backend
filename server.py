from flask import Flask

from dotenv import load_dotenv
import os
import openai

# Set up OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from courseCreationRoutes import bp as courseCreation_bp

app = Flask(__name__)

app.register_blueprint(courseCreation_bp)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
