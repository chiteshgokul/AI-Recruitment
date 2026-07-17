# pyrefly: ignore [missing-import]
import streamlit as st
from backend.core.interfaces import IView, ICandidateRepository
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header


class AIMailGeneratorView(IView):
    """View renderer for the AI Mail Generator workspace."""

    def __init__(self, candidate_repo: ICandidateRepository, ollama_client: OllamaClient) -> None:
        self._candidate_repo = candidate_repo
        self._ollama_client = ollama_client

    def render(self) -> None:
        hero(
            "AI Mail Generator",
            "Draft personalized candidate outreach, interview invitations, and job offer letters using local Ollama (Phi-3) intelligence."
        )

        # 1. Fetch available candidates
        candidates = self._candidate_repo.get_candidates()
        candidate_names = ["Custom Recipient..."] + candidates["Name"].tolist()

        # Check for state changes to reset generated email if parameters change
        if "generated_email" not in st.session_state:
            st.session_state.generated_email = None

        form_col, preview_col = st.columns([5, 6])

        with form_col:
            with st.container(border=True):
                section_header("🎯 Select Recipient", "Choose a candidate profile or create a custom one.")
                selected_name = st.selectbox(
                    "Candidate Profile Selector",
                    options=candidate_names,
                    label_visibility="collapsed"
                )

                # Determine default values based on selected profile
                default_name = ""
                default_role = ""
                if selected_name != "Custom Recipient...":
                    cand_row = candidates[candidates["Name"] == selected_name].iloc[0]
                    default_name = cand_row["Name"]
                    default_role = cand_row["Applied Role"]

                st.write("")
                st.markdown("**Recipient Information**")
                candidate_name = st.text_input(
                    "Full Name",
                    value=default_name,
                    key=f"name_{selected_name}"
                )
                candidate_role = st.text_input(
                    "Job Title / Role",
                    value=default_role,
                    key=f"role_{selected_name}"
                )

            st.write("")
            with st.container(border=True):
                section_header("📝 Email Settings", "Select email type, tone, and additional context.")
                
                email_type = st.selectbox(
                    "Email Type",
                    options=["Interview Invitation", "Job Offer", "Rejection & Feedback", "Follow-up / Check-in"]
                )
                
                tone = st.selectbox(
                    "Tone",
                    options=["Professional", "Friendly", "Encouraging", "Direct"]
                )
                
                extra_context = st.text_area(
                    "Additional Details / Context",
                    placeholder="Enter details like date, time, salary range, interviewers, or custom notes...",
                    height=120
                )

                # Button to generate
                generate_btn = st.button(
                    "✨ Generate Email",
                    type="primary",
                    use_container_width=True
                )

                if generate_btn:
                    if not candidate_name.strip():
                        st.error("Please enter a recipient name.")
                    elif not candidate_role.strip():
                        st.error("Please enter a job title/role.")
                    elif not self._ollama_client.is_connected():
                        st.error("Ollama connection error: Please ensure your local Ollama server is running and the `phi3` model is loaded.")
                    else:
                        with st.spinner("Generating email using local Ollama (Phi-3)..."):
                            email_text = self._ollama_client.generate_email(
                                candidate_name=candidate_name,
                                job_title=candidate_role,
                                email_type=email_type,
                                tone=tone,
                                extra_context=extra_context
                            )
                            st.session_state.generated_email = {
                                "text": email_text,
                                "name": candidate_name,
                                "role": candidate_role,
                                "type": email_type
                            }
                            st.rerun()

        with preview_col:
            with st.container(border=True):
                section_header("📧 Email Preview", "View and refine the generated email draft.")
                
                gen_data = st.session_state.generated_email
                if gen_data:
                    email_text = gen_data["text"]
                    recipient_name = gen_data["name"]
                    
                    # Parse subject and body
                    subject = f"Update regarding your application for {gen_data['role']}"
                    body = email_text
                    
                    if "subject:" in email_text.lower():
                        lines = email_text.split("\n")
                        for line in lines:
                            if line.lower().startswith("subject:"):
                                subject = line.split(":", 1)[-1].strip()
                                # Remove the subject line and any surrounding empty lines from the body
                                body = email_text.replace(line, "").strip()
                                break
                    
                    # Display the email inside the custom container classes
                    email_html = f"""
                    <div class="email-container">
                        <div class="email-subject"><strong>Subject:</strong> {subject}</div>
                        <div>{body}</div>
                    </div>
                    """
                    st.markdown(email_html, unsafe_allow_html=True)
                    
                    st.write("")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("📋 Copy to Clipboard", use_container_width=True):
                            st.success("Draft copied to clipboard! (Simulated)")
                    with c2:
                        if st.button("✉️ Send Email", type="primary", use_container_width=True):
                            st.success(f"Email successfully dispatched to {recipient_name}! (Simulated)")
                else:
                    st.info("No email generated yet. Configure the recipient and settings on the left, then click **Generate Email**.")
                    
                    st.write("")
                    st.markdown("**Outreach Best Practices:**")
                    st.markdown("- **Interview Invitation:** Include date, time, timezone, and video link details.")
                    st.markdown("- **Job Offer:** Outline high-level base pay, equity, target start date, and signing bonuses.")
                    st.markdown("- **Rejection:** Keep it empathetic, appreciate their time, and offer constructive feedback.")
