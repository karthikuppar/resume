from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.services.ai_service import ai_service
from app.schemas.analysis import ResumeAnalysisResponse
from app.models.resume import ResumeAnalysisModel

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
    
    # 3. Analyze text with AI
    result = ai_service.analyze_resume_ai(extracted_text)
    
    # 4. Save the results to the PostgreSQL database
    new_analysis = ResumeAnalysisModel(
        filename=file.filename,
        extracted_text=extracted_text,
        skills=result["skills"],
        analysis_summary=result["analysis_summary"]
    )
    db.add(new_analysis)
    await db.commit()
    
    # 5. Return the response to the user
    return ResumeAnalysisResponse(
        filename=file.filename,
        file_type=file.content_type,
        extracted_text=extracted_text,
        skills=result["skills"],
        analysis_summary=result["analysis_summary"]
    )

# Notice how this is now correctly aligned to the far left edge!
@router.get("/history")
async def get_history(db: AsyncSession = Depends(get_db)):
    # 1. Ask the database for all records, sorted by newest first
    query = select(ResumeAnalysisModel).order_by(ResumeAnalysisModel.id.desc())
    result = await db.execute(query)
    
    # 2. Extract the list of records
    records = result.scalars().all()
    
    # 3. Return them to the frontend
    return records