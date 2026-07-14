# pyrefly: ignore [missing-import]
import streamlit as st
from frontend.src.core.styles import (
    DARK_TEXT,
    MUTED_TEXT,
    LIGHT_BLUE,
    MID_BLUE,
    PRIMARY_BLUE,
)


def hero(title: str, subtitle: str) -> None:
    """Render a prominent hero banner."""
    st.markdown(
        f"""
        <div class="app-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None) -> None:
    """Render a standardized section header."""
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="section-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def card(title: str, body: str, footer: str | None = None) -> None:
    """Render a styled visual card."""
    footer_html = f"<p style='color:{MUTED_TEXT}; margin: 0.6rem 0 0;'>{footer}</p>" if footer else ""
    st.markdown(
        f"""
        <div class="card">
            <h3 style="margin:0 0 .55rem; color:{DARK_TEXT}; font-size:1.05rem;">{title}</h3>
            <div style="color:{MUTED_TEXT}; line-height:1.5;">{body}</div>
            {footer_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_pill(status: str) -> str:
    """Generate HTML string for a colored status pill."""
    css_status = status.lower().replace(" ", "-")
    return f'<span class="pill status-{css_status}">{status}</span>'


def handle_placeholder_button(label: str, message: str, key: str, button_type: str = "secondary") -> None:
    """Render a placeholder button with click feedback success message."""
    if st.button(label, key=key, type=button_type):
        st.success(message)
