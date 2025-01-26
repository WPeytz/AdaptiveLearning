from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, db
import os
from dotenv import load_dotenv
import random

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
    import json

    openai.api_key = os.getenv("OPENAI_API_KEY")

    data = request.json
    topic = data.get("topic", random.choice(MATH_TOPICS))
    difficulty = data.get("difficulty", "Easy")

    try:
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

        Requirements:
        1. The question field is a single string.
        2. Provide exactly four unique answer choices in "options", labeled A), B), C), D).
        3. Provide exactly one correct answer in the "answer" field.
        4. Use random or varied numbers so the same question doesn't repeat each time.
        5. Ensure the 'answer' is always correct for the question.
        6. No extra commentary or keys—only these three fields: question, options, answer.
        7. Use the metric system for units (e.g., meters, grams, liters).
        8. No questions about fractions
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use a valid model name like "gpt-4" or "gpt-3.5-turbo"
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful math tutor. Return ONLY valid JSON with no extra text."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,  # Increase temperature for more varied responses
        )

        raw_content = response.choices[0].message["content"].strip()
        print("Raw API Response:", raw_content)  # Debugging
        question_obj = json.loads(raw_content)

        return jsonify(question_obj), 200

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)