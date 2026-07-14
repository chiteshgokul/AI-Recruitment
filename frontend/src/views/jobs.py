# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, IJobRepository
from frontend.src.components.widgets import hero, status_pill, handle_placeholder_button
from frontend.src.core.styles import MUTED_TEXT, DARK_TEXT


class JobOpeningsView(IView):
    """View renderer for Job Openings dashboard."""

    def __init__(self, job_repo: IJobRepository) -> None:
        self._job_repo = job_repo

    def render(self) -> None:
        hero("Job Openings", "Review active and draft roles with applicant counts, required skills, and hiring status.")
        jobs = self._job_repo.get_jobs()

        for start in range(0, len(jobs), 3):
            cols = st.columns(3)
            for col, (_, job) in zip(cols, jobs.iloc[start : start + 3].iterrows()):
                with col:
                    skills = "".join(f"<span class='pill'>{item.strip()}</span>" for item in job["Required Skills"].split(","))
                    st.markdown(
                        f"""
                        <div class="card">
                            <h3 style="margin:0 0 .25rem;">💼 {job['Job Title']}</h3>
                            <p style="margin:.15rem 0; color:{MUTED_TEXT};"><b>{job['Department']}</b> · {job['Location']}</p>
                            <div style="margin:.8rem 0;">{skills}</div>
                            <p style="margin:.6rem 0; color:{DARK_TEXT};"><b>{job['Applicants']}</b> applicants</p>
                            {status_pill(str(job['Status']))}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    handle_placeholder_button("View Details", f"Opening details placeholder for {job['Job Title']}.", f"job_{job['Job Title']}")
            st.write("")
