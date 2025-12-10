import os
import sys
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(json.dumps({"error": "GEMINI_API_KEY not found in .env"}))
    sys.exit(1)

genai.configure(api_key=API_KEY)

def parse_workout(text):
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    You are a fitness data extraction assistant.
    Extract the workout routine from the following text and return it strictly as valid JSON.
    Do not include markdown formatting (like ```json), just the raw JSON string.
    
    Structure your JSON like this:
    {{
        "routineName": "Inferred Name or General Workout",
        "exercises": [
            {{
                "name": "Exercise Name",
                "sets": 3,
                "reps": "10-12",
                "weight": "100lbs",
                "notes": "Any extra info"
            }}
        ]
    }}

    Text to parse:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        # Clean potential markdown
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return clean_text
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Please provide the workout text as an argument."}))
        sys.exit(1)
        
    input_text = sys.argv[1]
    # If input is a file path
    if os.path.isfile(input_text):
        with open(input_text, 'r') as f:
            input_text = f.read()
            
    result = parse_workout(input_text)
    print(result)
