from flask import Flask

from dotenv import load_dotenv
import json
import os
import openai
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials, initialize_app

# Set up OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load your service account key JSON string from the environment variable
firebase_service_key = os.getenv("FIREBASE_SERVICE_KEY")
service_account_key = json.loads(firebase_service_key)

# Initialize the Firebase Admin SDK with the service account key
cred = credentials.Certificate(service_account_key)
initialize_app(cred)

# Now you can use Firestore and other Firebase services
db = firestore.client()

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
