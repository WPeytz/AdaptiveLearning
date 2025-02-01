from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
from google.cloud import secretmanager
import random
import json
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# # Verify if the key is loaded
# print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
# print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Fetch service account JSON from Secret Manager
def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    project_id = "adaptivelearning-449114"
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

# Load Firebase credentials from Secret Manager
service_account_json = get_secret("serviceAccountKey")

# Convert string to dictionary and load credentials
cred = credentials.Certificate(json.loads(service_account_json))  # Directly load from JSON string
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app/'
})

app = Flask(__name__, static_folder='static')
CORS(app)  # Allow all origins by default

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# List of common math topics
MATH_TOPICS = ["Fractions", "Decimals and Percentages", "Ratios and Proportions", "Geometry", "Basic Algebra"]

@app.route('/generate_question', methods=['POST'])
def generate_question():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "Missing OpenAI API key"}), 500  # Handle missing key
    client = OpenAI(api_key=api_key)
    
    data = request.json
    user_id = data.get("user_id", "test_user")
    topic = data.get("topic", random.choice(MATH_TOPICS))
    difficulty = data.get("difficulty", "Easy")

    try:
        user_ref = db.reference(f'performance/{user_id}')
        performance_data = user_ref.get() or {"correct_streak": 0, "incorrect_streak": 0}
        correct_streak = performance_data.get("correct_streak", 0)

        random_contexts = [
            "in a real-world shopping scenario",
            "while planning a school event",
            "in a geometry problem involving shapes",
            "to solve an everyday math problem",
            "for understanding ratios in a recipe"
        ]
        random_context = random.choice(random_contexts)

        prompt = f"""
        Create a unique {difficulty}-level multiple-choice question about {topic} {random_context}.
        Use random numbers and vary the math operations involved to ensure the questions are not repetitive.

        Return ONLY valid JSON with the following structure (and nothing more):
        {{
          "question": "<Your question text>",
          "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "answer": "<One correct option from the above>"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        raw_content = response.choices[0].message.content.strip()
        question_obj = json.loads(raw_content)

        question_obj["correct_streak"] = correct_streak
        return jsonify(question_obj), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    user_id = data.get("user_id", "test_user")
    is_correct = data.get("is_correct", False)

    try:
        user_ref = db.reference(f'performance/{user_id}')
        performance_data = user_ref.get() or {"correct_streak": 0, "incorrect_streak": 0}

        if is_correct:
            performance_data["correct_streak"] += 1
            performance_data["incorrect_streak"] = 0
        else:
            performance_data["correct_streak"] = 0
            performance_data["incorrect_streak"] += 1

        # Save back to Firebase
        user_ref.update(performance_data)

        return jsonify({"message": "Answer recorded successfully", "correct_streak": performance_data["correct_streak"]}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Save the user's feedback about a question's difficulty to the database.
    """
    data = request.json
    user_id = data.get("user_id", "test_user")
    question = data.get("question", "")
    difficulty_feedback = data.get("difficulty", "No Feedback")

    try:
        # Save feedback in Firebase
        feedback_ref = db.reference(f'feedback/{user_id}')
        feedback_data = {
            "question": question,
            "difficulty_feedback": difficulty_feedback
        }
        feedback_ref.push(feedback_data)

        return jsonify({"message": "Feedback submitted successfully"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use PORT env variable
    app.run(debug=True, host='0.0.0.0', port=port)