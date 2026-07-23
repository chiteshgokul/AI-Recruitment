# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, IJobRepository
from frontend.src.components.widgets import hero, section_header, status_pill
from frontend.src.core.styles import MUTED_TEXT, DARK_TEXT


class JobOpeningsView(IView):
    """View renderer for Job Openings dashboard."""

    def __init__(self, job_repo: IJobRepository) -> None:
        self._job_repo = job_repo

    def render(self) -> None:
        hero("Job Openings", "Review active and draft roles with applicant counts, required skills, and hiring status.")
        jobs = self._job_repo.get_jobs()

        # Top Bar: Add New Job
        with st.expander("➕ Post New Job Opening"):
            with st.form("new_job_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    new_title = st.text_input("Job Title", placeholder="e.g. Senior Frontend Developer")
                    new_dept = st.selectbox("Department", ["Engineering", "People", "Design", "HR Strategy", "Sales", "Product"])
                    new_loc = st.text_input("Location", value="Bengaluru / Remote")
                with col2:
                    new_skills = st.text_input("Required Skills (comma separated)", value="React, TypeScript, CSS, REST APIs")
                    new_status = st.selectbox("Initial Status", ["Open", "Active", "Draft"])
                
                submit_job = st.form_submit_button("💼 Publish Job Opening", type="primary", use_container_width=True)
                if submit_job and new_title:
                    job_entry = {
                        "Job Title": new_title,
                        "Department": new_dept,
                        "Location": new_loc,
                        "Required Skills": new_skills,
                        "Applicants": 0,
                        "Status": new_status,
                    }
                    if hasattr(self._job_repo, "add_job"):
                        self._job_repo.add_job(job_entry)
                    st.success(f"✓ Job opening **'{new_title}'** created successfully!")
                    st.rerun()

        st.write("")
        # Job Cards Layout
        for start in range(0, len(jobs), 3):
            cols = st.columns(3)
            for col, (_, job) in zip(cols, jobs.iloc[start : start + 3].iterrows()):
                with col:
                    with st.container(border=True):
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
                        st.write("")
                        view_key = f"view_details_{job['Job Title']}"
                        if st.button("📋 Manage Opening", key=view_key, use_container_width=True):
                            st.session_state[f"active_job_{job['Job Title']}"] = not st.session_state.get(f"active_job_{job['Job Title']}", False)
                        
                        if st.session_state.get(f"active_job_{job['Job Title']}", False):
                            st.markdown("---")
                            st.markdown(f"**Required Skills:** {job['Required Skills']}")
                            st.markdown(f"**Department:** {job['Department']}")
                            st.markdown(f"**Location:** {job['Location']}")
                            st.markdown(f"**Current Status:** {job['Status']}")
                            
                            status_opts = ["Open", "Active", "Draft", "On Hold", "Closed"]
                            current_idx = status_opts.index(job['Status']) if job['Status'] in status_opts else 0
                            new_st = st.selectbox("Update Status", status_opts, index=current_idx, key=f"st_sel_{job['Job Title']}")
                            if new_st != job['Status']:
                                if hasattr(self._job_repo, "update_job_status"):
                                    self._job_repo.update_job_status(job['Job Title'], new_st)
                                st.success(f"Updated status to {new_st}")
                                st.rerun()

            st.write("")
