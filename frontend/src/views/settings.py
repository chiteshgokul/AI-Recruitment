# pyrefly: ignore [missing-import]
import streamlit as st
from backend.core.interfaces import IView
from frontend.src.components.widgets import hero, section_header
from frontend.src.core.styles import PRIMARY_BLUE


class SettingsView(IView):
    """View renderer for the Settings screen."""

    def render(self) -> None:
        hero("Settings", "Configure company profile, AI controls, notification preferences, and workspace options.")

        # Initialize session settings defaults if not present
        if "company_info" not in st.session_state:
            st.session_state.company_info = {
                "name": "Acme Talent Systems",
                "industry": "Technology",
                "location": "Bengaluru, India"
            }
        if "user_profile" not in st.session_state:
            st.session_state.user_profile = {
                "name": "Recruitment Lead",
                "email": "lead@acmetalentsystems.com",
                "role": "Admin"
            }

        company_col, profile_col = st.columns(2)
        with company_col:
            with st.container(border=True):
                section_header("🏢 Company Information")
                c_name = st.text_input("Company Name", value=st.session_state.company_info["name"])
                c_ind = st.text_input("Industry", value=st.session_state.company_info["industry"])
                c_loc = st.text_input("Company Location", value=st.session_state.company_info["location"])
                if st.button("Save Company Info", type="primary", use_container_width=True):
                    st.session_state.company_info = {"name": c_name, "industry": c_ind, "location": c_loc}
                    st.success("✓ Company information updated successfully!")

        with profile_col:
            with st.container(border=True):
                section_header("👤 User Profile")
                u_name = st.text_input("Full Name", value=st.session_state.user_profile["name"])
                u_email = st.text_input("Email", value=st.session_state.user_profile["email"])
                u_role = st.selectbox("Role", ["Admin", "Recruiter", "Hiring Manager", "HR Analyst"], index=0)
                if st.button("Update Profile", type="primary", use_container_width=True):
                    st.session_state.user_profile = {"name": u_name, "email": u_email, "role": u_role}
                    st.success("✓ User profile updated successfully!")

        st.write("")
        ai_col, notify_col, theme_col = st.columns(3)
        with ai_col:
            with st.expander("🤖 Local AI Configuration", expanded=True):
                ai_mode = st.selectbox("Preferred AI Screening Mode", ["Balanced", "Strict Quality", "High Velocity"])
                threshold = st.slider("Match Score Threshold (%)", 0, 100, 75)
                if st.button("Save AI Preferences", use_container_width=True):
                    st.session_state.ai_config = {"mode": ai_mode, "threshold": threshold}
                    st.success(f"✓ AI Preferences saved ({ai_mode} mode, {threshold}% threshold)!")

        with notify_col:
            with st.expander("🔔 Notification Settings", expanded=True):
                r1 = st.checkbox("Interview reminders", value=True)
                r2 = st.checkbox("Candidate status changes", value=True)
                r3 = st.checkbox("Weekly hiring report", value=False)
                if st.button("Save Notifications", use_container_width=True):
                    st.session_state.notifications = {"reminders": r1, "status": r2, "weekly": r3}
                    st.success("✓ Notification preferences saved!")

        with theme_col:
            with st.expander("🎨 Theme Selection", expanded=True):
                theme = st.radio("Theme Preset", ["Professional Blue", "Light Minimal", "Dark Modern"], index=0)
                color = st.color_picker("Accent color", value=PRIMARY_BLUE)
                if st.button("Apply Theme", use_container_width=True):
                    st.session_state.theme = {"preset": theme, "accent": color}
                    st.success(f"✓ Applied '{theme}' theme preset!")
