import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Pro Resume Screener", page_icon="📄", layout="wide")
st.title("📄 Pro Batch Resume Screener - Dashboard Mode")

# Upload multiple resumes
uploaded_files = st.file_uploader(
    "Upload multiple resumes (PDF/DOCX)", 
    type=["pdf","docx"], 
    accept_multiple_files=True
)

job_description = st.text_area("Paste Job Description Here", height=200)

if uploaded_files and job_description:
    files = [("resumes", (f.name, f, "application/octet-stream")) for f in uploaded_files]
    data = {"job_description": job_description}

    try:
        response = requests.post("http://127.0.0.1:8000/analyze_batch", files=files, data=data)
        if response.status_code == 200:
            results = response.json()["results"]

            # Prepare ranking dataframe
            df = pd.DataFrame([{
                "Resume": r["file_name"],
                "ATS Score": r["ats_score"],
                "Top Skills": ", ".join(r["top_matches"]["matched_skills"]),
                "Missing Skills": ", ".join(r["gaps"]["missing_skills"]),
                "Suggestions": ", ".join(r["gaps"]["suggestions"]),
                "Skill Match": r["top_matches"]["skill_ratio"],
                "Semantic Sim": r["top_matches"]["semantic_similarity"],
                "Keyword Overlap": r["top_matches"]["keyword_overlap"]
            } for r in results])
            df = df.sort_values(by="ATS Score", ascending=False)

            # Highlight top 3 candidates
            def highlight_top(s):
                if s.name < 3:
                    return ['background-color: #b2fab4']*len(s)
                return ['']*len(s)
            st.subheader("📊 Ranked Resumes")
            st.dataframe(df[["Resume","ATS Score","Top Skills","Missing Skills","Suggestions"]].style.apply(highlight_top, axis=1), use_container_width=True)

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download Results CSV", csv, "resume_results.csv", "text/csv")

            # ATS component bar charts
            st.subheader("📈 ATS Breakdown per Resume")
            for r in results:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=["Skill Match","Semantic Sim","Keyword Overlap"],
                    y=[r["top_matches"]["skill_ratio"],
                       r["top_matches"]["semantic_similarity"],
                       r["top_matches"]["keyword_overlap"]],
                    marker_color=['#636EFA','#EF553B','#00CC96']
                ))
                fig.update_layout(title=f"{r['file_name']} ATS Components", yaxis=dict(title="Score (0-1)"))
                st.plotly_chart(fig, use_container_width=True)

            # Skill heatmap across all resumes
            st.subheader("🔥 Skill Heatmap Across Resumes")
            all_skills = sorted(list(set(sum([r["top_matches"]["matched_skills"] + r["gaps"]["missing_skills"] for r in results], []))))
            heat_data = []
            for r in results:
                row = [1 if skill in r["top_matches"]["matched_skills"] else 0 for skill in all_skills]
                heat_data.append(row)
            heat_df = pd.DataFrame(heat_data, columns=all_skills, index=[r["file_name"] for r in results])
            st.dataframe(heat_df.style.background_gradient(cmap='RdYlGn', axis=None), use_container_width=True)
            
            # Radar chart comparison
            st.subheader("📌 Skill Radar Comparison")
            fig_radar = go.Figure()
            for r in results:
                values = [1 if skill in r["top_matches"]["matched_skills"] else 0 for skill in all_skills]
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=all_skills,
                    fill='toself',
                    name=r["file_name"]
                ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
                                    showlegend=True)
            st.plotly_chart(fig_radar, use_container_width=True)

            # Detailed resume tabs
            st.subheader("🔍 Detailed Resume Analysis")
            for r in results:
                with st.expander(f"{r['file_name']} Details"):
                    st.metric("ATS Score", f"{r['ats_score']*100:.1f}%")
                    
                    st.write("### ✅ Top Skills Matched")
                    for skill in r["top_matches"]["matched_skills"]:
                        st.success(skill)
                    st.write("### ⚠️ Missing Skills")
                    for skill in r["gaps"]["missing_skills"]:
                        st.error(skill)
                    st.write("### 💡 Suggestions")
                    for s in r["gaps"]["suggestions"]:
                        st.info(s)
                    st.write("### 📄 Resume Preview")
                    st.text(r["resume_preview"])

        else:
            st.error("Failed to process resumes")
    except requests.exceptions.ConnectionError:
        st.error("Backend API is not running. Start FastAPI first!")
