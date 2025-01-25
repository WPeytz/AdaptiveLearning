from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import re
import firebase_admin
from firebase_admin import credentials, auth, db

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
    # Log the request body for debugging
    print(f"Request data: {request.data}")
    print(f"JSON payload: {request.json}")
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

if __name__ == '__main__':
    app.run(debug=True)