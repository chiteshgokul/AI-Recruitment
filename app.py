from datetime import datetime
# pyrefly: ignore [missing-import]
import streamlit as st

from src.core.styles import inject_css
from src.data.repository import MockDataRepository
from src.views.dashboard import DashboardView
from src.views.candidates import CandidatesView
from src.views.jobs import JobOpeningsView
from src.views.resume_screening import ResumeScreeningView
from src.views.interviews import InterviewManagementView
from src.views.talent import TalentManagementView
from src.views.analytics import AnalyticsView
from src.views.settings import SettingsView

st.set_page_config(
    page_title="AI Recruitment and Talent Management Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_state() -> None:
    """Initialize Streamlit session state keys."""
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"


def render_sidebar() -> None:
    """Render the sidebar navigation controls."""
    pages = [
        "Dashboard",
        "Candidates",
        "Job Openings",
        "Resume Screening",
        "Interview Management",
        "Talent Management",
        "Analytics",
        "Settings",
    ]
    icons = {
        "Dashboard": "📊",
        "Candidates": "👥",
        "Job Openings": "💼",
        "Resume Screening": "📄",
        "Interview Management": "🗓️",
        "Talent Management": "🌱",
        "Analytics": "📈",
        "Settings": "⚙️",
    }

    with st.sidebar:
        st.markdown("## 🤖 AI Talent Copilot")
        st.caption("Milestone 1 UI Prototype")
        st.radio(
            "Navigation",
            pages,
            key="page",
            format_func=lambda page: f"{icons[page]}  {page}",
            label_visibility="collapsed",
        )

        st.divider()
        st.markdown("### Workspace")
        st.info("Demo mode: placeholder data only. AI and backend integrations are intentionally disabled.")
        st.caption(f"Last refreshed: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")


def main() -> None:
    # 1. Inject global CSS styles
    inject_css()

    # 2. Initialize application state
    init_state()

    # 3. Setup core data repository (Dependency Injection Container)
    repo = MockDataRepository()

    # 4. Define and register view implementations (SOLID: LSP, OCP, DIP)
    # The application routes navigation dynamically through the IView interface.
    views = {
        "Dashboard": DashboardView(candidate_repo=repo, interview_repo=repo),
        "Candidates": CandidatesView(candidate_repo=repo),
        "Job Openings": JobOpeningsView(job_repo=repo),
        "Resume Screening": ResumeScreeningView(),
        "Interview Management": InterviewManagementView(interview_repo=repo, candidate_repo=repo),
        "Talent Management": TalentManagementView(),
        "Analytics": AnalyticsView(),
        "Settings": SettingsView(),
    }

    # 5. Render layout navigation controls
    render_sidebar()

    # 6. Resolve and render the active view
    active_page = st.session_state.page
    if active_page in views:
        views[active_page].render()


if __name__ == "__main__":
    main()