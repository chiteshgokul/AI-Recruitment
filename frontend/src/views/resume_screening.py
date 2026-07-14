# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
from pypdf import PdfReader
# pyrefly: ignore [missing-import]
from docx import Document

from backend.core.interfaces import IView, IJobRepository
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header


class ResumeScreeningView(IView):
    """View renderer for the Resume Screening workspace."""

    def __init__(self, job_repo: IJobRepository, ollama_client: OllamaClient) -> None:
        self._job_repo = job_repo
        self._ollama_client = ollama_client

    def render(self) -> None:
        hero("Resume Screening", "A polished upload and screening workspace powered by local Ollama (Phi-3) intelligence.")

        # 1. Fetch available jobs
        jobs = self._job_repo.get_jobs()
        
        upload_col, insight_col = st.columns([1, 1])
        with upload_col:
            with st.container(border=True):
                section_header("🎯 Select Target Job", "Select which open position to screen candidates against.")
                selected_job = st.selectbox(
                    "Target Job Opening",
                    options=jobs["Job Title"].tolist(),
                    label_visibility="collapsed"
                )
                
            st.write("")
            with st.container(border=True):
                section_header("📄 Resume Upload", "Upload a candidate's resume (PDF, DOCX, or TXT).")
                uploaded_file = st.file_uploader(
                    "Drag and drop upload area",
                    type=["pdf", "docx", "txt"],
                    label_visibility="collapsed",
                )
                
                # Check for state changes to reset screening result
                current_state_key = f"{uploaded_file.name if uploaded_file else ''}_{selected_job}"
                if "last_screened" not in st.session_state or st.session_state.last_screened != current_state_key:
                    st.session_state.screening_result = None
                    st.session_state.last_screened = current_state_key
                
                resume_text = ""
                if uploaded_file:
                    st.success(f"Loaded file: {uploaded_file.name}")
                    st.caption(f"File size: {uploaded_file.size / 1024:.1f} KB")
                    try:
                        if uploaded_file.name.endswith(".pdf"):
                            reader = PdfReader(uploaded_file)
                            resume_text = "".join(page.extract_text() or "" for page in reader.pages)
                        elif uploaded_file.name.endswith(".docx"):
                            doc = Document(uploaded_file)
                            resume_text = "\n".join(p.text for p in doc.paragraphs)
                        else:
                            resume_text = str(uploaded_file.read(), "utf-8")
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
                else:
                    st.info("No file uploaded yet. Upload a resume to enable AI analysis.")

                # Button is active only when a file is uploaded
                analyze_btn = st.button(
                    "✨ Screen Candidate",
                    disabled=(uploaded_file is None),
                    type="primary",
                    use_container_width=True
                )
                
                if analyze_btn and resume_text:
                    if not self._ollama_client.is_connected():
                        st.error("Ollama connection error: Please ensure your local Ollama server is running and the `phi3` model is loaded.")
                    else:
                        with st.spinner("Ollama is analyzing the resume using Phi-3..."):
                            # Retrieve job requirements
                            job_row = jobs[jobs["Job Title"] == selected_job].iloc[0]
                            job_desc = (
                                f"Title: {job_row['Job Title']}. "
                                f"Department: {job_row['Department']}. "
                                f"Location: {job_row['Location']}. "
                                f"Required Skills: {job_row['Required Skills']}"
                            )
                            # Call Ollama
                            result = self._ollama_client.screen_resume(resume_text, selected_job, job_desc)
                            st.session_state.screening_result = result
                            st.rerun()

        # Insight Column (Ollama Outputs)
        res = st.session_state.screening_result
        with insight_col:
            with st.container(border=True):
                section_header("🎯 AI Match Evaluation", "Automated compatibility assessment.")
                if res:
                    match_score = int(res.get("match_score", 50))
                    delta_label = "Strong Fit" if match_score >= 80 else ("Moderate Fit" if match_score >= 60 else "Low Match")
                    
                    st.metric("Predicted Match", f"{match_score}%", delta_label)
                    st.progress(match_score / 100)
                else:
                    st.metric("Predicted Match", "Pending", "Upload and click screen")
                    st.progress(0)
                    st.info("Awaiting resume submission and AI extraction.")

            st.write("")
            with st.container(border=True):
                section_header("📝 Extracted Skills & Overview", "Skills identified in resume.")
                if res:
                    skills = res.get("extracted_skills", [])
                    if skills:
                        pills_html = "".join(f"<span class='pill'>{s.strip()}</span>" for s in skills)
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.caption("No specific skills extracted.")
                    
                    st.markdown("---")
                    st.markdown("**Executive Summary**")
                    st.write(res.get("summary", "No summary generated."))
                else:
                    st.caption("Extracted skills and summary will appear here after screening.")

            st.write("")
            with st.container(border=True):
                section_header("📋 Fit Assessment (Pros & Cons)", "Key hiring signals.")
                if res:
                    notes = res.get("fit_notes", [])
                    if isinstance(notes, list):
                        for note in notes:
                            st.markdown(f"• {note}")
                    else:
                        st.write(notes)
                else:
                    st.caption("Pros, cons, and alignment notes will appear here after screening.")
