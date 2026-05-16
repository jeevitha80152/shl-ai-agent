import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_hiring_intent(user_message):
    prompt = f"""
You are an AI hiring assistant.

Analyze this hiring query:
"{user_message}"

Return ONLY valid JSON:

{{
  "role_type": "technical OR behavioral OR unknown",
  "role": "job title",
  "skills": ["skill1", "skill2", "skill3"]
}}

Examples:
Technical:
software developer, data analyst, backend engineer

Behavioral:
sales manager, HR recruiter, customer support manager

Unknown:
if query is vague
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print("Gemini error:", e)

        return {
            "role_type": "unknown",
            "role": "",
            "skills": []
        }