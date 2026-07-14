import random
from datetime import date, timedelta
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, IInterviewRepository, ICandidateRepository
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header
from frontend.src.core.styles import MUTED_TEXT


class InterviewManagementView(IView):
    """View renderer for Interview Management screen."""

    def __init__(
        self,
        interview_repo: IInterviewRepository,
        candidate_repo: ICandidateRepository,
        ollama_client: OllamaClient,
    ) -> None:
        self._interview_repo = interview_repo
        self._candidate_repo = candidate_repo
        self._ollama_client = ollama_client

    def render(self) -> None:
        hero("Interview Management", "Coordinate interview schedules, candidate status, and generate AI interview questions locally.")

        calendar_col, status_col = st.columns([1.25, 0.75])
        with calendar_col:
            with st.container(border=True):
                section_header("🗓️ Interview Calendar", "Calendar-style placeholder for scheduled interviews.")
                days = st.columns(5)
                # Seed randomly for determinism per page load
                random.seed(42)
                for i, day_col in enumerate(days):
                    current = date.today() + timedelta(days=i)
                    with day_col:
                        st.markdown(
                            f"""
                            <div class="mini-card">
                                <b>{current.strftime('%a')}</b><br>
                                <span style="font-size:1.8rem; font-weight:800;">{current.day}</span><br>
                                <span style="color:{MUTED_TEXT};">{random.randint(2, 7)} interviews</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        with status_col:
            with st.container(border=True):
                section_header("📌 Interview Status")
                st.metric("Confirmed", "18", "4 today")
                st.metric("Awaiting Feedback", "9", "2 overdue")
                st.metric("Reschedule Requests", "3", "-1 vs yesterday")

        st.write("")
        left, right = st.columns([1.2, 1])
        with left:
            section_header("Upcoming Interviews")
            interviews = self._interview_repo.get_interviews()
            st.dataframe(interviews, use_container_width=True, hide_index=True)
            
        with right:
            section_header("Candidate List & Prep")
            candidates = self._candidate_repo.get_candidates()
            st.dataframe(
                candidates[["Name", "Applied Role", "Status", "Match Score"]].head(8),
                use_container_width=True,
                hide_index=True,
            )
            
            st.write("")
            selected_cand = st.selectbox(
                "Select Candidate for Interview Prep",
                options=candidates["Name"].tolist(),
            )
            
            gen_btn = st.button("✨ Generate Interview Questions", use_container_width=True, type="primary")
            
            # State management for generated questions
            if "last_generated_questions" not in st.session_state:
                st.session_state.last_generated_questions = None
                
            if gen_btn:
                if not self._ollama_client.is_connected():
                    st.error("Ollama connection error: Please ensure your local Ollama server is running and the `phi3` model is loaded.")
                else:
                    cand_row = candidates[candidates["Name"] == selected_cand].iloc[0]
                    with st.spinner(f"Generating interview questions for {selected_cand}..."):
                        questions = self._ollama_client.generate_interview_questions(
                            candidate_name=selected_cand,
                            job_title=cand_row["Applied Role"],
                            skills=cand_row["Skills"]
                        )
                        st.session_state.last_generated_questions = (selected_cand, questions)
            
            # Display generated questions if the selected candidate matches
            if st.session_state.last_generated_questions:
                saved_cand, saved_questions = st.session_state.last_generated_questions
                if saved_cand == selected_cand:
                    st.write("")
                    with st.container(border=True):
                        st.markdown(f"### 📋 Interview Questions for {selected_cand}")
                        st.write(saved_questions)
                else:
                    st.session_state.last_generated_questions = None

