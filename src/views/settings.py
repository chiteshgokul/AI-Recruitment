# pyrefly: ignore [missing-import]
import streamlit as st
from src.core.interfaces import IView
from src.components.widgets import hero, section_header, handle_placeholder_button
from src.core.styles import PRIMARY_BLUE


class SettingsView(IView):
    """View renderer for the Settings screen."""

    def render(self) -> None:
        hero("Settings", "Configure company profile, placeholder AI controls, notifications, user preferences, and theme options.")

        company_col, profile_col = st.columns(2)
        with company_col:
            with st.container(border=True):
                section_header("🏢 Company Information")
                st.text_input("Company Name", value="Acme Talent Systems")
                st.text_input("Industry", value="Technology")
                st.text_input("Company Location", value="Bengaluru, India")
                handle_placeholder_button("Save Company Info", "Company information placeholder saved.", "save_company")

        with profile_col:
            with st.container(border=True):
                section_header("👤 User Profile")
                st.text_input("Full Name", value="Recruitment Lead")
                st.text_input("Email", value="lead@acmetalentsystems.com")
                st.selectbox("Role", ["Admin", "Recruiter", "Hiring Manager", "HR Analyst"])
                handle_placeholder_button("Update Profile", "User profile placeholder updated.", "save_profile")

        st.write("")
        ai_col, notify_col, theme_col = st.columns(3)
        with ai_col:
            with st.expander("🤖 AI Configuration (placeholder)", expanded=True):
                st.selectbox("Preferred AI Mode", ["Balanced", "Strict", "Exploratory"], disabled=True)
                st.slider("Match Threshold", 0, 100, 82, disabled=True)
                st.info("AI configuration controls are disabled in Milestone 1.")

        with notify_col:
            with st.expander("🔔 Notification Settings", expanded=True):
                st.checkbox("Interview reminders", value=True)
                st.checkbox("Candidate status changes", value=True)
                st.checkbox("Weekly hiring report", value=False)
                handle_placeholder_button("Save Notifications", "Notification settings placeholder saved.", "save_notifications")

        with theme_col:
            with st.expander("🎨 Theme Selection", expanded=True):
                st.radio("Theme", ["Professional Blue", "Light Minimal", "High Contrast"], index=0)
                st.color_picker("Accent color", value=PRIMARY_BLUE)
                handle_placeholder_button("Apply Theme", "Theme placeholder applied.", "apply_theme")
