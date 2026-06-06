from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
from models import Evaluation
from google.genai import types

# 1. Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Load evaluation prompt from evaluation.md
evaluation_prompt = Path('prompts/student_performance.md').read_text()
# 3. Initialize Gemini client
client = genai.Client(api_key=API_KEY)
# 4. Upload PDF notes and audio via File API
audio = client.files.upload(file='data/test_audio.m4a')
notes = client.files.upload(file='data/expressions.pdf')

# 6. Send file references + topic text to Gemini
response = client.models.generate_content(
    model="gemini-3-flash-preview", 
    contents=[evaluation_prompt, audio],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        temperature=0,
        response_schema=Evaluation
    )
)
# 7. Parse response against Evaluation Pydantic model
res = Evaluation.model_validate_json(response.text)
# 8. Print result
print(res.model_dump_json())