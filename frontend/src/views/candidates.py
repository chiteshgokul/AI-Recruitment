# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, ICandidateRepository
from frontend.src.components.widgets import hero, section_header, handle_placeholder_button


class CandidatesView(IView):
    """View renderer for the Candidates search and management screen."""

    def __init__(self, candidate_repo: ICandidateRepository) -> None:
        self._candidate_repo = candidate_repo

    def render(self) -> None:
        hero("Candidates", "Search, filter, and review sample candidate profiles for active hiring pipelines.")
        candidates = self._candidate_repo.get_candidates()

        with st.container(border=True):
            search_col, skill_col, exp_col, edu_col = st.columns([1.4, 1, 1, 1])
            with search_col:
                search = st.text_input("Search candidates", placeholder="Search by name, skill, or role")
            with skill_col:
                all_skills = sorted({s.strip() for row in candidates["Skills"] for s in row.split(",")})
                skill = st.selectbox("Filter by skills", ["All"] + all_skills)
            with exp_col:
                experience = st.selectbox("Filter by experience", ["All", "0-2 years", "3-5 years", "6-8 years", "9+ years"])
            with edu_col:
                education = st.selectbox("Filter by education", ["All"] + sorted(candidates["Education"].unique()))

        filtered = candidates.copy()
        if search:
            query = search.lower()
            filtered = filtered[
                filtered.apply(lambda row: query in " ".join(row.astype(str)).lower(), axis=1)
            ]
        if skill != "All":
            filtered = filtered[filtered["Skills"].str.contains(skill, case=False)]
        if education != "All":
            filtered = filtered[filtered["Education"] == education]
        if experience != "All":
            years = filtered["Experience"].str.extract(r"(\d+)").astype(int)[0]
            if experience == "0-2 years":
                filtered = filtered[years <= 2]
            elif experience == "3-5 years":
                filtered = filtered[(years >= 3) & (years <= 5)]
            elif experience == "6-8 years":
                filtered = filtered[(years >= 6) & (years <= 8)]
            else:
                filtered = filtered[years >= 9]

        st.write("")
        section_header("👥 Candidate Table", f"{len(filtered)} candidates match the current filters.")
        display_cols = ["Name", "Skills", "Experience", "Education", "Match Score", "Status", "Resume"]
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

        with st.expander("Candidate actions"):
            action_cols = st.columns(4)
            with action_cols[0]:
                handle_placeholder_button("📄 View Resume", "Resume preview placeholder opened.", "candidate_resume")
            with action_cols[1]:
                handle_placeholder_button("⭐ Shortlist", "Candidate shortlist placeholder updated.", "candidate_shortlist")
            with action_cols[2]:
                handle_placeholder_button("🗓️ Schedule", "Interview scheduling placeholder started.", "candidate_schedule")
            with action_cols[3]:
                handle_placeholder_button("✉️ Message", "Candidate messaging placeholder opened.", "candidate_message")
