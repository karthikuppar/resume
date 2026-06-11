import time
from google import genai
from google.genai import types
from app.services.memory_service import search_resume_memory

client = genai.Client()

def ask_career_copilot(user_message: str) -> str:
    """
    The Agentic Engine with Production Retry Logic.
    """
    system_instruction = """
    You are the 'AI Career Copilot', a brilliant Career Coach and Technical Recruiter.
    You help users analyze their uploaded resumes, find skill gaps, and match with jobs.
    
    CRITICAL RULES: 
    1. You MUST use your 'search_resume_memory' tool to answer questions.
    2. If the user asks about "my skills", "my name", or "what I am lacking", assume they are the candidate whose resume was uploaded. 
    3. Search the memory for terms like "missing skills", "name", or "weaknesses" to find the answer.
    4. Never guess. Always rely on the data returned by the tool.
    """

    print("Waking up Agent...")

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2, 
            tools=[search_resume_memory], 
        )
    )

    print(f"Agent thinking about: '{user_message}'")
    
    # --- PRODUCTION RESILIENCE: Retry Logic ---
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # We try to send the message...
            response = chat.send_message(user_message)
            return response.text
            
        except Exception as e:
            # If it fails, we check if it is a 503 Busy error
            if "503" in str(e) and attempt < max_retries - 1:
                print(f"Google servers are busy. Retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(5) # Wait 5 seconds before trying again
            else:
                # If it's a different error, or we ran out of retries, we finally crash.
                raise e