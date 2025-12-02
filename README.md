📄 Resume Screener — AI-Powered Multi-Resume ATS Analyzer
An AI-driven Resume Screening System that analyzes multiple resumes at once, matches them against a Job Description, calculates ATS scores, highlights missing skills, and visualizes skill heatmaps — powered by FastAPI + Streamlit + Sentence Transformers.
🚀 Features
✅ AI-Powered Resume Analysis
Extracts text from PDF/DOCX resumes
Extracts skills & experience
Computes ATS Score using:
Skill Match Ratio
Semantic Similarity
Keyword Overlap
🔍 Multi-Resume Comparison
Upload 10+ resumes at once and compare:
ATS Scores
Matching Skills
Missing Skills
Skill Heatmaps
Automatic improvement suggestions
📊 Interactive Dashboard
Built using Streamlit, includes:
Resume comparison tables
Skill heatmap
Detailed suggestions
Resume preview
📁 Project Structure
resume-screener/
├─ backend/
│  ├─ app/
│  │  ├─ main.py          # FastAPI endpoints
│  │  ├─ parsers.py       # Extract text from PDF/DOCX
│  │  ├─ extractor.py     # Extract skills & experience
│  │  ├─ scorer.py        # ATS score, matching, gaps
│  │  ├─ model_utils.py   # Sentence transformer helpers
│  │  └─ config.py
│  ├─ requirements.txt
│  └─ Dockerfile
│
├─ frontend/
│  ├─ streamlit_app.py    # Streamlit UI
│  └─ requirements.txt
│
└─ README.md
🖥️ Installation & Local Setup
1️⃣ Clone or Download the Project
git clone <your-repo-url>
cd resume-screener
2️⃣ Backend Setup (FastAPI)
cd backend
python3 -m venv venv
source venv/bin/activate       # macOS / Linux
# or
venv\Scripts\activate          # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
Backend runs at:
http://127.0.0.1:8000
API Docs available at:
http://127.0.0.1:8000/docs
3️⃣ Frontend Setup (Streamlit)
Open a new terminal:
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
Streamlit will open at:
http://localhost:8501
🌐 API Endpoints
POST /analyze_batch
Analyze multiple resumes simultaneously.
Form-Data:
resumes: List[UploadFile]
job_description: str
📦 Deployment Guide
Backend (Options):
Railway.app
Render.com
Heroku
Frontend
Deploy on Streamlit Cloud:
Go to https://share.streamlit.io
Connect GitHub repo
Select frontend/streamlit_app.py
Deploy 🚀
✨ Future Improvements
Candidate ranking system
JD skill extraction using ML
Export report as PDF
Recruiter dashboard
🧑‍💻 Author
Lubna K
AI & Full-Stack Developer
