# backend/app/extractor.py
import re

# Base skill list (you can expand this)
BASE_SKILLS = [
    "python", "java", "c", "c++", "react", "sql", "javascript",
    "docker", "flask", "django", "html", "css", "tensorflow", "pytorch"
]

def extract_skills_experience(resume_text: str):
    """
    Extract skills and experience from resume text
    """
    resume_text_lower = resume_text.lower()
    found_skills = [skill for skill in BASE_SKILLS if skill in resume_text_lower]

    # Simple experience extraction using regex for years (1-10 years)
    exp_matches = re.findall(r"(\d+)\s*[-+]?\s*(year|yr)s?", resume_text_lower)
    experience_years = [int(m[0]) for m in exp_matches] if exp_matches else []

    return found_skills, experience_years
