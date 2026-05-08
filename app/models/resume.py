from sqlalchemy import Column, Integer, String, Text, JSON
from app.db.session import Base

class ResumeAnalysisModel(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    extracted_text = Column(Text)
    skills = Column(JSON)  # Stores the list of skills
    analysis_summary = Column(Text)