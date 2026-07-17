from datetime import datetime
# pyrefly: ignore [missing-import]
import streamlit as st

from frontend.src.core.styles import inject_css
from backend.core.ollama_client import OllamaClient
from backend.data.repository import MockDataRepository
from frontend.src.views.dashboard import DashboardView
from frontend.src.views.candidates import CandidatesView
from frontend.src.views.jobs import JobOpeningsView
from frontend.src.views.resume_screening import ResumeScreeningView
from frontend.src.views.interviews import InterviewManagementView
from frontend.src.views.talent import TalentManagementView
from frontend.src.views.talent_insight import TalentInsightView
from frontend.src.views.ai_mail_generator import AIMailGeneratorView
from frontend.src.views.analytics import AnalyticsView
from frontend.src.views.settings import SettingsView

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


def render_sidebar(is_ai_active: bool) -> None:
    """Render the sidebar navigation controls."""
    pages = [
        "Dashboard",
        "Candidates",
        "Job Openings",
        "Resume Screening",
        "Interview Management",
        "AI Mail Generator",
        "Talent Management",
        "Talent Insight AI",
        "Analytics",
        "Settings",
    ]
    icons = {
        "Dashboard": "📊",
        "Candidates": "👥",
        "Job Openings": "💼",
        "Resume Screening": "📄",
        "Interview Management": "🗓️",
        "AI Mail Generator": "📨",
        "Talent Management": "🌱",
        "Talent Insight AI": "💡",
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
        if is_ai_active:
            st.success("🤖 Local Ollama (Phi-3) Connected")
        else:
            st.warning("⚠️ Local Ollama (Phi-3) Offline\n\nRun `ollama run phi3` in your terminal to activate AI features.")
        st.caption(f"Last refreshed: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")


def main() -> None:
    # 1. Inject global CSS styles
    inject_css()

    # 2. Initialize application state
    init_state()

    # 3. Setup core data repository (Dependency Injection Container)
    repo = MockDataRepository()

    # Setup Ollama client (Dependency Injection)
    ollama = OllamaClient()
    is_ai_active = ollama.is_connected()

    # 4. Define and register view implementations (SOLID: LSP, OCP, DIP)
    # The application routes navigation dynamically through the IView interface.
    views = {
        "Dashboard": DashboardView(candidate_repo=repo, interview_repo=repo),
        "Candidates": CandidatesView(candidate_repo=repo),
        "Job Openings": JobOpeningsView(job_repo=repo),
        "Resume Screening": ResumeScreeningView(job_repo=repo, ollama_client=ollama),
        "Interview Management": InterviewManagementView(interview_repo=repo, candidate_repo=repo, ollama_client=ollama),
        "AI Mail Generator": AIMailGeneratorView(candidate_repo=repo, ollama_client=ollama),
        "Talent Management": TalentManagementView(ollama_client=ollama),
        "Talent Insight AI": TalentInsightView(employee_repo=repo, ollama_client=ollama),
        "Analytics": AnalyticsView(),
        "Settings": SettingsView(),
    }

    # 5. Render layout navigation controls
    render_sidebar(is_ai_active)

    # 6. Resolve and render the active view
    active_page = st.session_state.page
    if active_page in views:
        views[active_page].render()


if __name__ == "__main__":
    main()