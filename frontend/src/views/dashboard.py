# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, ICandidateRepository, IInterviewRepository
from frontend.src.components.widgets import hero, section_header


class DashboardView(IView):
    """View renderer for the main Dashboard screen."""

    def __init__(
        self,
        candidate_repo: ICandidateRepository,
        interview_repo: IInterviewRepository,
    ) -> None:
        self._candidate_repo = candidate_repo
        self._interview_repo = interview_repo

    def render(self) -> None:
        hero(
            "AI Recruitment and Talent Management Copilot",
            "A modern command center for hiring teams to track candidates, roles, interviews, talent development, and workforce signals.",
        )

        kpi_rows = [
            ("👥 Total Candidates", "1,248", "+12.4% this month"),
            ("💼 Active Job Openings", "32", "+5 new roles"),
            ("🗓️ Interviews Scheduled", "86", "+18 this week"),
            ("✅ Candidates Selected", "21", "7 awaiting offer"),
            ("🎯 AI Match Accuracy", "94%", "+2.1% confidence"),
            ("⏱️ Average Hiring Time", "24 days", "3 days faster"),
        ]
        top_cols = st.columns(3)
        bottom_cols = st.columns(3)
        for idx, (label, value, delta) in enumerate(kpi_rows):
            with (top_cols + bottom_cols)[idx]:
                st.metric(label, value, delta)

        st.write("")
        left, right = st.columns([1.25, 1])
        with left.container():
            section_header("📥 Recent Applications", "Latest candidate applications across priority roles.")
            applications_df = self._candidate_repo.get_applications()
            st.dataframe(applications_df, use_container_width=True, hide_index=True)

        with right.container():
            section_header("🗓️ Upcoming Interviews", "Near-term interviews requiring recruiter attention.")
            interviews_df = self._interview_repo.get_interviews()
            st.dataframe(interviews_df.head(6), use_container_width=True, hide_index=True)

        st.write("")
        pipeline_col, activity_col = st.columns([1.15, 0.85])
        with pipeline_col:
            with st.container(border=True):
                section_header("🚦 Recruitment Pipeline", "Candidate movement by stage.")
                stages = [
                    ("Applied", 420, 100),
                    ("Screened", 260, 62),
                    ("Interview", 140, 33),
                    ("Offer", 54, 13),
                    ("Hired", 21, 5),
                ]
                for stage, count, pct in stages:
                    st.markdown(f"**{stage}** · {count} candidates")
                    st.markdown(
                        f'<div class="progress-track"><div class="progress-fill" style="width:{pct}%"></div></div>',
                        unsafe_allow_html=True,
                    )
                    st.write("")

        with activity_col:
            with st.container(border=True):
                section_header("🔔 Live Activity Stream", "Real-time log of recruiter and system operations.")
                activities = (
                    self._candidate_repo.get_activities()
                    if hasattr(self._candidate_repo, "get_activities")
                    else [
                        "New resume uploaded for Senior AI Engineer.",
                        "Interview feedback submitted for Maya Rao.",
                        "Offer approved for Product Designer role.",
                    ]
                )
                for activity in activities:
                    st.info(activity)
