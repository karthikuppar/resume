from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import analyze_resume_text
from app.services.memory_service import add_text_to_memory
from app.services.agent_service import ask_career_copilot 
from app.schemas.analysis import ResumeAnalysisResult

router = APIRouter()

# --- PHASE 1 & 3: The Extraction & Memory Route ---
@router.post("/analyze", response_model=ResumeAnalysisResult)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Endpoint to upload a resume PDF, get structured AI analysis, and save to memory.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    try:
        file_bytes = await file.read()
        print(f"Extracting text from {file.filename}...")
        raw_text = extract_text_from_pdf(file_bytes)
        
        print("Sending text to Gemini for extraction...")
        analysis_result = analyze_resume_text(raw_text)
        
        # --- PHASE 3: UPGRADED MEMORY INTEGRATION ---
        print("Saving full profile to Long-Term Memory (Qdrant)...")
        
        # 1. Save the Candidate's Name as a distinct memory
        add_text_to_memory(
            text_chunk=f"The candidate's name is {analysis_result.candidate_name}", 
            metadata={"candidate_name": analysis_result.candidate_name, "type": "general_info"}
        )

        # 2. Save their Skills
        for skill in analysis_result.skills_found:
            add_text_to_memory(
                text_chunk=f"Skill: {skill}", 
                metadata={"candidate_name": analysis_result.candidate_name, "type": "skill"}
            )
            
        # 3. Save their Missing Skills / Areas for Improvement
        for missing in analysis_result.areas_for_improvement:
            add_text_to_memory(
                text_chunk=f"Missing Skill / Weakness: {missing}", 
                metadata={"candidate_name": analysis_result.candidate_name, "type": "missing_skill"}
            )
            
        print("Memory storage complete!")
        # ---------------------------------------
        
        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- PHASE 4: The Agent Chat Route ---

# We create a simple schema so FastAPI knows the user will send {"message": "Hello"}
class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """
    Endpoint to talk to the AI Career Copilot. It will use tools to search memory.
    """
    try:
        print(f"User asked: {request.message}")
        
        # Pass the user's message to our Agent service
        agent_reply = ask_career_copilot(request.message)
        
        # Return the Agent's answer as JSON
        return {"reply": agent_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))