# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header
from frontend.src.core.styles import MUTED_TEXT


class TalentManagementView(IView):
    """View renderer for the Talent Management and growth planning screen."""

    def __init__(self, ollama_client: OllamaClient) -> None:
        self._ollama_client = ollama_client

    def render(self) -> None:
        hero("Talent Management", "Explore employee skills, growth signals, and generate AI learning roadmaps locally.")

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
                st.caption("Select team and target role below to plan:")
                
                selected_team = st.selectbox(
                    "Team Profile",
                    options=[team for team, _, _ in skill_cards],
                    key="growth_team"
                )
                target_role = st.text_input("Target Level-Up Role", value="Lead Practitioner")
                
                gen_btn = st.button("✨ Create Growth Plan", use_container_width=True, type="primary")

                if "last_growth_plan" not in st.session_state:
                    st.session_state.last_growth_plan = None
                    
                if gen_btn:
                    if not self._ollama_client.is_connected():
                        st.error("Ollama connection error: Please ensure your local Ollama server is running and the `phi3` model is loaded.")
                    else:
                        current_skills = next(skills for t, skills, _ in skill_cards if t == selected_team)
                        with st.spinner(f"Creating career roadmap for {selected_team} to {target_role}..."):
                            plan_text = self._ollama_client.generate_growth_plan(
                                team_name=selected_team,
                                current_skills=current_skills,
                                target_role=target_role
                            )
                            st.session_state.last_growth_plan = (selected_team, target_role, plan_text)

        # Render generated plan underneath if matches selections
        if st.session_state.last_growth_plan:
            saved_team, saved_role, plan_text = st.session_state.last_growth_plan
            if saved_team == selected_team and saved_role == target_role:
                st.write("")
                with st.container(border=True):
                    section_header(f"📋 AI Career Growth Roadmap: {selected_team} ➔ {target_role}")
                    st.write(plan_text)
            else:
                st.session_state.last_growth_plan = None
