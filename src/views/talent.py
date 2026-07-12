# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from src.core.interfaces import IView
from src.components.widgets import hero, section_header, handle_placeholder_button
from src.core.styles import MUTED_TEXT


class TalentManagementView(IView):
    """View renderer for the Talent Management and growth planning screen."""

    def render(self) -> None:
        hero("Talent Management", "Explore employee skills, growth signals, and learning recommendations with sample data.")

        skill_cards = [
            ("Engineering", "Python, Cloud, APIs", 88),
            ("Design", "Research, Prototyping, Systems", 76),
            ("People", "Sourcing, Coaching, Analytics", 82),
            ("Sales", "CRM, Forecasting, Negotiation", 71),
        ]
        cols = st.columns(4)
        for col, (team, skills, score) in zip(cols, skill_cards):
            with col:
                st.markdown(
                    f"""
                    <div class="card">
                        <h3 style="margin:0;">🌱 {team}</h3>
                        <p style="color:{MUTED_TEXT}; min-height:48px;">{skills}</p>
                        <b>Skill coverage</b>
                        <div class="progress-track" style="margin-top:.45rem;">
                            <div class="progress-fill" style="width:{score}%"></div>
                        </div>
                        <p style="color:{MUTED_TEXT}; margin:.5rem 0 0;">{score}% readiness</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")
        gap_col, learning_col, career_col = st.columns(3)
        with gap_col:
            with st.container(border=True):
                section_header("📉 Skill Gap Analysis")
                st.bar_chart(pd.DataFrame({"Gap Score": [34, 27, 22, 18]}, index=["MLOps", "Leadership", "SQL", "UX Research"]))
        with learning_col:
            with st.container(border=True):
                section_header("🎓 Recommended Learning")
                for item in ["Advanced People Analytics", "Cloud Architecture Basics", "Inclusive Interviewing", "Product Strategy"]:
                    st.info(item)
        with career_col:
            with st.container(border=True):
                section_header("🚀 Career Progress")
                st.progress(0.68)
                st.caption("Placeholder progress toward next role readiness.")
                handle_placeholder_button("Create Growth Plan", "Growth plan placeholder created.", "growth_plan")
