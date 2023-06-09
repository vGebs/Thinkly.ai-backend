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
from routes.quizCreationRoutes import bp as quizCreation_bp
from routes.gradingRoutes import bp as grades_bp
from routes.noteQuestionRoutes import bp as notesQs_bp

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    return {"response": "ok"}, 200


app.register_blueprint(courseCreation_bp)
app.register_blueprint(courseDef_bp)
app.register_blueprint(assignmentCreation_bp)
app.register_blueprint(quizCreation_bp)
app.register_blueprint(grades_bp)
app.register_blueprint(notesQs_bp)

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
