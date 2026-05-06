from pydantic import BaseModel
from typing import Optional

class ResumeAnalysisResponse(BaseModel):
    filename: str
    file_type: str
    extracted_text: str
    skills: list[str]
    analysis_summary: Optional[str] = None

    class Config:
        from_attributes = True