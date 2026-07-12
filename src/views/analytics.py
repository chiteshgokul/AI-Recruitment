from datetime import date
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from src.core.interfaces import IView
from src.components.widgets import hero, section_header


class AnalyticsView(IView):
    """View renderer for the Analytics dashboards and charts."""

    def render(self) -> None:
        hero("Analytics", "Placeholder charts for hiring velocity, funnel performance, and workforce distribution.")

        months = pd.date_range(end=date.today(), periods=8, freq="ME").strftime("%b")
        hiring_trend = pd.DataFrame(
            {
                "Applications": [120, 134, 156, 148, 171, 198, 214, 226],
                "Interviews": [42, 49, 57, 52, 61, 73, 79, 84],
                "Hires": [8, 10, 12, 9, 14, 16, 18, 21],
            },
            index=months,
        )

        top_left, top_right = st.columns(2)
        with top_left:
            with st.container(border=True):
                section_header("📈 Hiring Trend")
                st.line_chart(hiring_trend)
        with top_right:
            with st.container(border=True):
                section_header("👥 Candidate Distribution")
                st.bar_chart(pd.DataFrame({"Candidates": [310, 245, 198, 176]}, index=["Engineering", "People", "Design", "Sales"]))

        bottom_left, bottom_mid, bottom_right = st.columns(3)
        with bottom_left:
            with st.container(border=True):
                section_header("🧩 Skill Distribution")
                st.bar_chart(pd.DataFrame({"Profiles": [118, 97, 86, 74, 61]}, index=["Python", "SQL", "React", "AWS", "Tableau"]))
        with bottom_mid:
            with st.container(border=True):
                section_header("🚦 Recruitment Funnel")
                st.area_chart(pd.DataFrame({"Candidates": [420, 260, 140, 54, 21]}, index=["Applied", "Screened", "Interview", "Offer", "Hired"]))
        with bottom_right:
            with st.container(border=True):
                section_header("🏢 Department-wise Hiring")
                st.bar_chart(pd.DataFrame({"Hires": [9, 5, 4, 3]}, index=["Engineering", "People", "Design", "Sales"]))
