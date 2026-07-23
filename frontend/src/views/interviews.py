import random
from datetime import date, timedelta
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, IInterviewRepository, ICandidateRepository
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header
from frontend.src.core.styles import MUTED_TEXT


class InterviewManagementView(IView):
    """View renderer for Interview Management screen."""

    def __init__(
        self,
        interview_repo: IInterviewRepository,
        candidate_repo: ICandidateRepository,
        ollama_client: OllamaClient,
    ) -> None:
        self._interview_repo = interview_repo
        self._candidate_repo = candidate_repo
        self._ollama_client = ollama_client

    def render(self) -> None:
        hero("Interview Management", "Coordinate interview schedules, candidate status, and generate AI interview questions locally.")

        # Initialize dictionary to store question banks per candidate
        if "candidate_question_bank" not in st.session_state:
            st.session_state.candidate_question_bank = {}

        calendar_col, status_col = st.columns([1.25, 0.75])
        with calendar_col:
            with st.container(border=True):
                section_header("🗓️ Interview Calendar", "Calendar-style overview for scheduled candidate sessions.")
                days = st.columns(5)
                random.seed(42)
                for i, day_col in enumerate(days):
                    current = date.today() + timedelta(days=i)
                    with day_col:
                        st.markdown(
                            f"""
                            <div class="mini-card">
                                <b>{current.strftime('%a')}</b><br>
                                <span style="font-size:1.8rem; font-weight:800;">{current.day}</span><br>
                                <span style="color:{MUTED_TEXT};">{random.randint(2, 7)} interviews</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        with status_col:
            with st.container(border=True):
                section_header("📌 Interview Status")
                st.metric("Confirmed", "18", "4 today")
                st.metric("Awaiting Feedback", "9", "2 overdue")
                st.metric("Reschedule Requests", "3", "-1 vs yesterday")

        st.write("")
        left, right = st.columns([1.2, 1])
        with left:
            section_header("Upcoming Interviews", "Latest candidate interview schedules across active roles.")
            interviews = self._interview_repo.get_interviews()
            st.dataframe(interviews, use_container_width=True, hide_index=True)
            
        with right:
            section_header("Candidate Selection & AI Prep", "Generate targeted interview questions using local Ollama (Phi-3).")
            candidates = self._candidate_repo.get_candidates()
            st.dataframe(
                candidates[["Name", "Applied Role", "Status", "Match Score"]].head(8),
                use_container_width=True,
                hide_index=True,
            )
            
            st.write("")
            selected_cand = st.selectbox(
                "Select Candidate for AI Question Bank",
                options=candidates["Name"].tolist(),
                key="prep_selected_candidate"
            )
            
            has_existing = selected_cand in st.session_state.candidate_question_bank
            btn_label = f"✨ Regenerate Questions for {selected_cand}" if has_existing else f"✨ Generate Interview Questions for {selected_cand}"
            gen_btn = st.button(btn_label, use_container_width=True, type="primary")

            if gen_btn:
                if not self._ollama_client.is_connected():
                    st.error("Ollama connection error: Please ensure your local Ollama server is running and the `phi3` model is loaded.")
                else:
                    cand_row = candidates[candidates["Name"] == selected_cand].iloc[0]
                    with st.spinner(f"Generating tailored interview questions for {selected_cand}..."):
                        questions = self._ollama_client.generate_interview_questions(
                            candidate_name=selected_cand,
                            job_title=cand_row["Applied Role"],
                            skills=cand_row["Skills"]
                        )
                        st.session_state.candidate_question_bank[selected_cand] = {
                            "role": cand_row["Applied Role"],
                            "text": questions,
                            "skills": cand_row["Skills"]
                        }
                        st.rerun()

        # Display candidate's question bank in a dedicated full-width container below
        if selected_cand in st.session_state.candidate_question_bank:
            q_data = st.session_state.candidate_question_bank[selected_cand]
            st.write("")
            with st.container(border=True):
                self._render_interview_questions_clean(
                    questions_text=q_data["text"],
                    candidate_name=selected_cand,
                    job_role=q_data["role"]
                )

    def _render_interview_questions_clean(self, questions_text: str, candidate_name: str, job_role: str) -> None:
        """Cleanly format and render interview questions in responsive styled cards."""
        clean_text = self._sanitize_ollama_output(questions_text)

        st.markdown(f"### 📋 AI Question Bank: {candidate_name} ({job_role})")
        st.caption("Tailored technical and behavioral evaluation questions powered by local Ollama (Phi-3).")
        st.write("")

        lines = [l.strip() for l in clean_text.split("\n") if l.strip()]
        questions_list = []
        current_q = ""
        current_note = ""

        for line in lines:
            # Detect numbered questions (e.g. 1., 2., Q1, Question 1)
            is_new_q = (len(line) > 2 and line[0].isdigit() and line[1] in [".", ")", ":"]) or line.lower().startswith("question")
            if is_new_q:
                if current_q:
                    questions_list.append((current_q, current_note))
                    current_note = ""
                current_q = line
            elif any(k in line.lower() for k in ["looking for", "evaluat", "assess", "note:", "what to look for", "seeking"]):
                current_note = line
            elif current_q:
                if "note:" in line.lower() or "looking for" in line.lower():
                    current_note = line
                else:
                    current_q += " " + line

        if current_q:
            questions_list.append((current_q, current_note))

        if questions_list and len(questions_list) >= 1:
            for idx, (q_text, n_text) in enumerate(questions_list, start=1):
                note_html = ""
                if n_text:
                    clean_n = n_text.replace("(", "").replace(")", "").strip()
                    note_html = f'<div class="question-note">💡 <b>Evaluation Criteria:</b> {clean_n}</div>'
                
                # Strip leading "1.", "2." from q_text to avoid double numbering if header has Q1.
                clean_q_title = q_text
                if len(clean_q_title) > 3 and clean_q_title[0].isdigit() and clean_q_title[1] in [".", ")", ":"]:
                    clean_q_title = clean_q_title[2:].strip()
                elif clean_q_title.lower().startswith("question"):
                    clean_q_title = clean_q_title.split(":", 1)[-1].strip()

                card_html = f"""
                <div class="question-card">
                    <div class="question-title"><b>Q{idx}.</b> {clean_q_title}</div>
                    {note_html}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            # Fallback formatting
            st.markdown(f'<div class="question-card">{clean_text}</div>', unsafe_allow_html=True)

        st.write("")
        c1, c2 = st.columns([1.2, 4])
        with c1:
            if st.button("📋 Copy Question Bank", use_container_width=True):
                st.success("✓ Question bank copied!")

    def _sanitize_ollama_output(self, raw_text: str) -> str:
        """Strip prompt preambles, echoes, and trailing requirement blocks from Ollama."""
        text = raw_text.strip()

        # 1. Remove preamble prompt echoes (before Question 1)
        first_q_idx = -1
        for i in range(1, 10):
            p1 = text.find(f"{i}.")
            p2 = text.find(f"Question {i}")
            p = p1 if p1 != -1 else p2
            if p != -1 and (first_q_idx == -1 or p < first_q_idx):
                first_q_idx = p
                break

        if first_q_idx > 0:
            text = text[first_q_idx:].strip()

        # 2. Stop parsing at trailing requirement / system prompt markers
        stop_markers = [
            "requirements:",
            "requirement:",
            "additionally:",
            "as a hiring manager",
            "generate 5 open-ended",
            "create a list of 5",
            "the questions must be",
            "note: ensure each question",
        ]

        clean_lines = []
        for line in text.split("\n"):
            line_lower = line.strip().lower()
            if any(line_lower.startswith(m) for m in stop_markers):
                break
            clean_lines.append(line)

        return "\n".join(clean_lines).strip()
