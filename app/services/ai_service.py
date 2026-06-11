import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.schemas.analysis import ResumeAnalysisResult

# 1. Load the .env file so Python can find your key
load_dotenv()

# 2. Initialize the modern Client
# It automatically looks for os.environ.get("GEMINI_API_KEY")
client = genai.Client()

def analyze_resume_text(resume_text: str) -> ResumeAnalysisResult:
    """
    Takes raw resume text, sends it to Gemini using the modern SDK, 
    and forces a structured JSON response.
    """
    system_prompt = """
    You are an elite Technical Recruiter and AI Resume Analyzer. 
    Your job is to read the provided resume text and extract the information perfectly.
    You must NOT invent any information. If a detail is missing, leave it empty or default to 0.
    """

    print("Calling modern Gemini API...")
    
    # 3. Make the API call using the new structure
    response = client.models.generate_content(
        model='gemini-2.5-flash', # We upgraded you to the newest fast model
        contents=resume_text,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=ResumeAnalysisResult, # Our Pydantic Blueprint!
            temperature=0.1
        )
    )

    # 4. Validate the JSON string returned by Gemini
    validated_data = ResumeAnalysisResult.model_validate_json(response.text)
    
    return validated_data