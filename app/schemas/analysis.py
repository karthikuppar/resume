from pydantic import BaseModel, Field
from typing import List

class ResumeAnalysisResult(BaseModel):
    candidate_name: str = Field(default="Unknown", description="The name of the candidate found in the resume")
    skills_found: List[str] = Field(description="List of technical skills extracted from the resume")
    years_of_experience: int = Field(default=0, description="Total years of professional experience. Use 0 if student or fresher")
    strengths: List[str] = Field(description="2-3 key strengths identified in the resume")
    areas_for_improvement: List[str] = Field(description="2-3 weak points or missing industry-standard skills")
    readability_score: int = Field(description="A score from 1 to 100 judging formatting and grammar")
