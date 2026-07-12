import random
from datetime import date, timedelta
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from src.core.interfaces import IView, IInterviewRepository, ICandidateRepository
from src.components.widgets import hero, section_header
from src.core.styles import MUTED_TEXT


class InterviewManagementView(IView):
    """View renderer for Interview Management screen."""

    def __init__(
        self,
        interview_repo: IInterviewRepository,
        candidate_repo: ICandidateRepository,
    ) -> None:
        self._interview_repo = interview_repo
        self._candidate_repo = candidate_repo

    def render(self) -> None:
        hero("Interview Management", "Coordinate interview schedules, candidate status, and future question generation.")

        calendar_col, status_col = st.columns([1.25, 0.75])
        with calendar_col:
            with st.container(border=True):
                section_header("🗓️ Interview Calendar", "Calendar-style placeholder for scheduled interviews.")
                days = st.columns(5)
                # Seed randomly for determinism per page load if needed, or keep standard
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
            section_header("Candidate List")
            candidates = self._candidate_repo.get_candidates()
            st.dataframe(
                candidates[["Name", "Applied Role", "Status", "Match Score"]].head(8),
                use_container_width=True,
                hide_index=True,
            )
            st.button("✨ Generate Questions", disabled=True, help="Disabled placeholder for Milestone 1.")
