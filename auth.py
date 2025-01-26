from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app/'
})

app = Flask(__name__)
CORS(app)  # Allow all origins by default

# Default route for the root URL
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Adaptive Learning API!"}), 200

# Handle requests for favicon.ico
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response for favicon.ico requests

# Endpoint for user signup/login
@app.route('/login', methods=['POST'])
def login():
    token = request.json.get('idToken')
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return jsonify({"message": "Login successful", "uid": uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Example function to write data to the database
def save_user_progress(user_id, progress):
    ref = db.reference(f'users/{user_id}/progress')
    ref.set(progress)

# Example function to read data from the database
def get_user_progress(user_id):
    ref = db.reference(f'users/{user_id}/progress')
    return ref.get()

# Test endpoint to save user progress
@app.route('/test/save_progress', methods=['POST'])
def test_save_progress():
    user_id = request.json.get('user_id')
    progress = request.json.get('progress')
    try:
        save_user_progress(user_id, progress)
        return jsonify({"message": "Progress saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test endpoint to get user progress
@app.route('/test/get_progress/<user_id>', methods=['GET'])
def test_get_progress(user_id):
    try:
        progress = get_user_progress(user_id)
        if progress:
            return jsonify(progress), 200
        return jsonify({"message": "No progress found for this user."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch questions by topic and difficulty
@app.route('/questions', methods=['GET'])
def get_questions():
    topic = request.args.get('topic')  # e.g., "Fractions"
    difficulty = request.args.get('difficulty')  # e.g., "Easy"
    try:
        # Query the questions from Firebase
        ref = db.reference('questions')
        questions = ref.order_by_child('topic').equal_to(topic).get()
        filtered = [q for q in questions.values() if q['difficulty'] == difficulty]
        return jsonify(filtered), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch a specific question by its ID
@app.route('/questions/<question_id>', methods=['GET'])
def get_question_by_id(question_id):
    try:
        # Fetch the question from Firebase using the question_id
        ref = db.reference(f'questions/{question_id}')
        question = ref.get()
        if question:
            return jsonify(question), 200
        return jsonify({"message": "Question not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to generate a question using AI
@app.route('/generate_question', methods=['POST'])
def generate_question():
    print("Endpoint /generate_question has been called.")
    import openai

    # Use the API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Add this print statement to confirm the API key being used
    print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))

    data = request.json
    topic = data.get("topic", "Math")
    difficulty = data.get("difficulty", "Easy")

    try:
        # Updated prompt for the new API
        prompt = f"Create a {difficulty} level multiple-choice question about {topic}. Include four options and specify the correct answer."

        # Use the new ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating quiz questions."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the content of the response
        question_text = response.choices[0].message["content"].strip()

        # Parse the response into a question structure
        lines = question_text.split("\n")
        question = {
            "question": lines[0],  # First line as the question
            "options": lines[1:5],  # Next 4 lines as options
            "answer": lines[5] if len(lines) > 5 else "Option 1"  # Optional: parse the correct answer
        }
        return jsonify(question), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)