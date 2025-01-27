from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
import random
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app/'
})

app = Flask(__name__)
CORS(app)  # Allow all origins by default

# List of common math topics
MATH_TOPICS = ["Fractions", "Decimals and Percentages", "Ratios and Proportions", "Geometry", "Basic Algebra"]

@app.route('/generate_question', methods=['POST'])
def generate_question():
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")
    data = request.json
    user_id = data.get("user_id", "test_user")
    topic = data.get("topic", random.choice(MATH_TOPICS))
    difficulty = data.get("difficulty", "Easy")

    try:
        # Load user performance from Firebase
        user_ref = db.reference(f'performance/{user_id}')
        performance_data = user_ref.get() or {"correct_streak": 0, "incorrect_streak": 0}
        correct_streak = performance_data.get("correct_streak", 0)

        # Add randomization for variation
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

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful math tutor. Return ONLY valid JSON with no extra text."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
        )

        raw_content = response.choices[0].message["content"].strip()
        question_obj = json.loads(raw_content)

        # Include the correct streak in the response
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
    app.run(debug=True, host='0.0.0.0', port=5003)