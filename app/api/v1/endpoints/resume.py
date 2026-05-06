from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.ai_service import ai_service
from app.schemas.analysis import ResumeAnalysisResponse

router = APIRouter(prefix="/resume", tags=["Resume Processing"])

@router.post("/upload", response_model=ResumeAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Save file to disk
    file_path = await ai_service.save_upload_file(file)
    
    # 2. Extract text from PDF
    extracted_text = await ai_service.extract_text_from_file(file_path)
    
    # 3. Analyze text
    result = ai_service.analyze_resume_ai(extracted_text)
    
    return ResumeAnalysisResponse(
        filename=file.filename,
        file_type=file.content_type,
        extracted_text=extracted_text,
        skills=result["skills"],
        analysis_summary=result["analysis_summary"]
    )