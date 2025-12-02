# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from .parsers import extract_text_from_file
from .extractor import extract_skills_experience
from .scorer import build_jd_profile, score_resume_against_jd, gap_analysis

app = FastAPI(title="SmartResume AI - Screening API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeAnalysis(BaseModel):
    file_name: str
    ats_score: float
    top_matches: dict
    gaps: dict
    suggestions: List[str]
    resume_preview: str

class BatchResponse(BaseModel):
    results: List[ResumeAnalysis]

@app.post("/analyze_batch", response_model=BatchResponse)
async def analyze_batch(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    results = []
    jd_profile = build_jd_profile(job_description)

    for resume in resumes:
        text = await extract_text_from_file(resume)
        skills, _ = extract_skills_experience(text)
        ats_score, top_matches = score_resume_against_jd(text, skills, jd_profile)
        gaps = gap_analysis(skills, jd_profile)
        suggestions = [f"Consider improving: {s}" for s in gaps.get("missing_skills", [])]

        results.append({
            "file_name": resume.filename,
            "ats_score": round(ats_score,3),
            "top_matches": top_matches,
            "gaps": gaps,
            "suggestions": suggestions,
            "resume_preview": text[:500]
        })
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
