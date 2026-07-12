# pyrefly: ignore [missing-import]
import streamlit as st
from src.core.interfaces import IView
from src.components.widgets import hero, section_header


class ResumeScreeningView(IView):
    """View renderer for the Resume Screening workspace."""

    def render(self) -> None:
        hero("Resume Screening", "A polished upload and screening workspace for future AI resume intelligence.")

        upload_col, insight_col = st.columns([1, 1])
        with upload_col:
            with st.container(border=True):
                section_header("📄 Resume Upload", "Drag and drop files for the future screening workflow.")
                uploaded_file = st.file_uploader(
                    "Drag and drop upload area",
                    type=["pdf", "doc", "docx"],
                    label_visibility="collapsed",
                )
                if uploaded_file:
                    st.success(f"Uploaded file preview: {uploaded_file.name}")
                    st.caption(f"File size: {uploaded_file.size / 1024:.1f} KB")
                else:
                    st.info("No file uploaded yet. This area is a frontend placeholder.")
                st.button("✨ Extract Skills", disabled=True, help="Disabled in Milestone 1.")

        with insight_col:
            with st.container(border=True):
                section_header("🎯 AI Match Score", "Placeholder result area for future model output.")
                st.metric("Predicted Match", "Pending", "Upload required")
                st.progress(0)
                st.info("AI scoring is intentionally disabled for this UI milestone.")

            st.write("")
            with st.container(border=True):
                section_header("📝 Resume Summary", "Future extracted summary preview.")
                st.text_area(
                    "Resume summary placeholder",
                    value="Candidate summary, relevant experience, education highlights, and role fit notes will appear here.",
                    height=150,
                    disabled=True,
                    label_visibility="collapsed",
                )
