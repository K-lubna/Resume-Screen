# backend/app/scorer.py
from .model_utils import get_sentence_transformer, cosine_sim

def build_jd_profile(jd_text: str):
    model = get_sentence_transformer()
    from .extractor import BASE_SKILLS, extract_skills_experience
    skills, _ = extract_skills_experience(jd_text)
    jd_emb = model.encode(jd_text, convert_to_numpy=True)
    return {"skills": skills, "jd_emb": jd_emb, "raw": jd_text}

def score_resume_against_jd(resume_text: str, resume_skills: list, jd_profile: dict):
    model = get_sentence_transformer()
    res_emb = model.encode(resume_text, convert_to_numpy=True)
    sem_sim = cosine_sim(res_emb, jd_profile["jd_emb"])

    jd_skills = set(jd_profile.get("skills", []))
    matched = jd_skills.intersection(set(resume_skills))
    skill_ratio = len(matched) / max(1, len(jd_skills))

    jd_tokens = set(w for w in jd_profile["raw"].lower().split() if len(w) > 2)
    resume_tokens = set(w for w in resume_text.lower().split() if len(w) > 2)
    keyword_overlap = len(jd_tokens & resume_tokens) / max(1, len(jd_tokens))

    ats = 0.5 * skill_ratio + 0.35 * sem_sim + 0.15 * keyword_overlap

    top_matches = {
        "semantic_similarity": round(sem_sim, 3),
        "skill_ratio": round(skill_ratio, 3),
        "keyword_overlap": round(keyword_overlap, 3),
        "matched_skills": list(matched)
    }

    return ats, top_matches

def gap_analysis(resume_skills: list, jd_profile: dict):
    jd_skills = set(jd_profile.get("skills", []))
    resume_skills_set = set(resume_skills)
    missing = list(jd_skills - resume_skills_set)
    present = list(jd_skills & resume_skills_set)

    # Actionable suggestions
    suggestions = []
    for skill in missing:
        suggestions.append(f"Add projects or experience related to {skill}.")

    return {"missing_skills": missing, "present_skills": present, "suggestions": suggestions}
