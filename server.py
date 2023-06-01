from flask import Flask

from dotenv import load_dotenv
import os
import openai

# Set up OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from routes.courseCreationRoutes import bp as courseCreation_bp
from routes.courseDefinitionRoutes import bp as courseDef_bp
from routes.assignmentCreationRoutes import bp as assignmentCreation_bp

app = Flask(__name__)

app.register_blueprint(courseCreation_bp)
app.register_blueprint(courseDef_bp)
app.register_blueprint(assignmentCreation_bp)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
