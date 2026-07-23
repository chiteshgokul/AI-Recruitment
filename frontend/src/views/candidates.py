# pyrefly: ignore [missing-import]
from datetime import datetime, date, timedelta
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, ICandidateRepository
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header, status_pill
from frontend.src.core.styles import MUTED_TEXT, DARK_TEXT


class CandidatesView(IView):
    """View renderer for the Candidates search and management screen."""

    def __init__(self, candidate_repo: ICandidateRepository, ollama_client: OllamaClient = None) -> None:
        self._candidate_repo = candidate_repo
        self._ollama_client = ollama_client or OllamaClient()

    def render(self) -> None:
        hero("Candidates", "Search, filter, shortlist, schedule, and review candidate profiles for active hiring pipelines.")
        candidates = self._candidate_repo.get_candidates()

        # Initialize session storage for sent emails if missing
        if "sent_emails" not in st.session_state:
            st.session_state.sent_emails = []

        # 1. Filters Bar
        with st.container(border=True):
            search_col, skill_col, exp_col, edu_col = st.columns([1.4, 1, 1, 1])
            with search_col:
                search = st.text_input("Search candidates", placeholder="Search by name, skill, or role")
            with skill_col:
                all_skills = sorted({s.strip() for row in candidates["Skills"] for s in row.split(",")})
                skill = st.selectbox("Filter by skills", ["All"] + all_skills)
            with exp_col:
                experience = st.selectbox("Filter by experience", ["All", "0-2 years", "3-5 years", "6-8 years", "9+ years"])
            with edu_col:
                education = st.selectbox("Filter by education", ["All"] + sorted(candidates["Education"].unique()))

        # Filter logic
        filtered = candidates.copy()
        if search:
            query = search.lower()
            filtered = filtered[
                filtered.apply(lambda row: query in " ".join(row.astype(str)).lower(), axis=1)
            ]
        if skill != "All":
            filtered = filtered[filtered["Skills"].str.contains(skill, case=False)]
        if education != "All":
            filtered = filtered[filtered["Education"] == education]
        if experience != "All":
            years = filtered["Experience"].str.extract(r"(\d+)").astype(int)[0]
            if experience == "0-2 years":
                filtered = filtered[years <= 2]
            elif experience == "3-5 years":
                filtered = filtered[(years >= 3) & (years <= 5)]
            elif experience == "6-8 years":
                filtered = filtered[(years >= 6) & (years <= 8)]
            else:
                filtered = filtered[years >= 9]

        st.write("")
        section_header("👥 Candidate Table", f"{len(filtered)} candidates match the current filters.")
        display_cols = ["Name", "Applied Role", "Skills", "Experience", "Education", "Match Score", "Status"]
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

        st.write("")
        # 2. Interactive Candidate Actions Section
        with st.expander("⚡ Candidate Actions & Management", expanded=True):
            section_header("🎯 Candidate Selector", "Choose a candidate below to view resume, shortlist, schedule interviews, or message.")
            
            cand_names = candidates["Name"].tolist()
            if "selected_candidate_name" not in st.session_state or st.session_state.selected_candidate_name not in cand_names:
                st.session_state.selected_candidate_name = cand_names[0] if cand_names else ""
                
            selected_cand_name = st.selectbox(
                "Select Candidate",
                options=cand_names,
                key="selected_candidate_name"
            )

            cand_row = candidates[candidates["Name"] == selected_cand_name].iloc[0]
            cand_email_default = f"{selected_cand_name.lower().replace(' ', '.')}@example.com"
            
            # Candidate Info Summary Bar
            c_info1, c_info2, c_info3, c_info4 = st.columns(4)
            with c_info1:
                st.markdown(f"**Candidate:** {cand_row['Name']}")
                st.markdown(f"**Applied Role:** {cand_row['Applied Role']}")
            with c_info2:
                st.markdown(f"**Match Score:** {cand_row['Match Score']}")
                st.markdown(f"**Applied Date:** {cand_row['Applied Date']}")
            with c_info3:
                st.markdown(f"**Current Status:** {status_pill(str(cand_row['Status']))}", unsafe_allow_html=True)
                st.markdown(f"**Education:** {cand_row['Education']}")
            with c_info4:
                st.markdown(f"**Experience:** {cand_row['Experience']}")
                st.markdown(f"**Skills:** {cand_row['Skills']}")

            st.markdown("---")
            action_cols = st.columns(4)
            
            # Action 1: View Resume
            with action_cols[0]:
                view_resume_btn = st.button("📄 View Resume", key="act_view_resume", use_container_width=True, type="secondary")
            
            # Action 2: Shortlist Candidate
            with action_cols[1]:
                shortlist_btn = st.button(
                    "⭐ Shortlist Candidate", 
                    key="act_shortlist", 
                    use_container_width=True, 
                    type="primary" if cand_row["Status"] != "Shortlisted" else "secondary"
                )

            # Action 3: Schedule Interview
            with action_cols[2]:
                schedule_btn = st.button("🗓️ Schedule Interview", key="act_schedule", use_container_width=True, type="secondary")

            # Action 4: Send Message / Email
            with action_cols[3]:
                message_btn = st.button("✉️ Send Message / Email", key="act_message", use_container_width=True, type="secondary")

            # Handle Shortlist Action
            if shortlist_btn:
                new_status = "Shortlisted" if cand_row["Status"] != "Shortlisted" else "In Review"
                if hasattr(self._candidate_repo, "update_candidate_status"):
                    self._candidate_repo.update_candidate_status(selected_cand_name, new_status)
                st.success(f"✓ Status for **{selected_cand_name}** updated to **{new_status}**!")
                st.rerun()

            # Handle Active Views for Buttons
            if "active_candidate_tab" not in st.session_state:
                st.session_state.active_candidate_tab = "message"  # default to message tab if requested

            if view_resume_btn:
                st.session_state.active_candidate_tab = "resume"
            elif schedule_btn:
                st.session_state.active_candidate_tab = "schedule"
            elif message_btn:
                st.session_state.active_candidate_tab = "message"

            # Render Sub-Panels based on Active Tab
            current_tab = st.session_state.active_candidate_tab

            if current_tab == "resume":
                st.write("")
                with st.container(border=True):
                    section_header(f"📄 Resume Preview: {selected_cand_name}", f"Extracted overview for {cand_row['Applied Role']} applicant.")
                    col_left, col_right = st.columns([1.2, 1])
                    with col_left:
                        st.markdown(f"### Profile & Credentials")
                        st.markdown(f"- **Full Name:** {cand_row['Name']}")
                        st.markdown(f"- **Target Role:** {cand_row['Applied Role']}")
                        st.markdown(f"- **Total Experience:** {cand_row['Experience']}")
                        st.markdown(f"- **Education Level:** {cand_row['Education']}")
                        st.markdown(f"- **Contact Email:** {cand_email_default}")
                        st.markdown("#### Skills & Competencies")
                        skills_list = [s.strip() for s in cand_row['Skills'].split(',')]
                        st.markdown("".join(f"<span class='pill'>{s}</span>" for s in skills_list), unsafe_allow_html=True)
                    with col_right:
                        st.markdown("### Executive Summary")
                        st.write(
                            f"{cand_row['Name']} is a seasoned candidate with {cand_row['Experience']} of experience, "
                            f"holding a {cand_row['Education']} degree. They possess core strength in {cand_row['Skills']} "
                            f"and have an estimated AI job alignment score of {cand_row['Match Score']} for the {cand_row['Applied Role']} role."
                        )
                        st.info(f"Status: {cand_row['Status']} | Applied Date: {cand_row['Applied Date']}")
                        if st.button("Close Resume Preview", key="close_resume"):
                            st.session_state.active_candidate_tab = None
                            st.rerun()

            elif current_tab == "schedule":
                st.write("")
                with st.container(border=True):
                    section_header(f"🗓️ Schedule Interview for {selected_cand_name}")
                    sched_col1, sched_col2 = st.columns(2)
                    with sched_col1:
                        interview_date = st.date_input("Interview Date", min_value=date.today(), value=date.today() + timedelta(days=2))
                        interview_time = st.selectbox("Time Slot", ["10:00 AM", "11:30 AM", "02:00 PM", "04:30 PM"])
                    with sched_col2:
                        interviewer = st.selectbox("Interviewer", ["Priya Sharma (Engineering Lead)", "Daniel Lee (Recruitment Head)", "Fatima Noor (HR Director)", "Marcus Green (Product Lead)"])
                        target_role = st.text_input("Interview Role", value=cand_row['Applied Role'])
                    
                    if st.button("🚀 Confirm & Schedule Interview", type="primary", use_container_width=True):
                        interviewer_clean = interviewer.split(" (")[0]
                        interview_entry = {
                            "Candidate": selected_cand_name,
                            "Role": target_role,
                            "Interviewer": interviewer_clean,
                            "Date": interview_date.isoformat(),
                            "Time": interview_time,
                            "Status": "Confirmed",
                        }
                        if hasattr(self._candidate_repo, "add_interview"):
                            self._candidate_repo.add_interview(interview_entry)
                        st.success(f"🗓️ Interview successfully scheduled for **{selected_cand_name}** with **{interviewer_clean}** on **{interview_date} at {interview_time}**!")
                        st.session_state.active_candidate_tab = None
                        st.rerun()

            elif current_tab == "message":
                st.write("")
                with st.container(border=True):
                    section_header(f"✉️ Direct Mail Composer: {selected_cand_name}", "Draft and send emails directly to candidates.")
                    
                    recip_col, subj_col = st.columns([1, 1.2])
                    with recip_col:
                        recipient_email = st.text_input("Recipient Email Address", value=cand_email_default, key=f"recip_email_{selected_cand_name}")
                    with subj_col:
                        email_subject = st.text_input(
                            "Subject Line",
                            value=f"Interview Invitation: {cand_row['Applied Role']} Role - Acme Talent Systems",
                            key=f"subj_{selected_cand_name}"
                        )
                    
                    opt_col1, opt_col2 = st.columns(2)
                    with opt_col1:
                        msg_type = st.selectbox("Message Type", ["Interview Invitation", "Shortlist Update", "Offer Proposal", "Rejection & Feedback"], key=f"mtype_{selected_cand_name}")
                    with opt_col2:
                        tone = st.selectbox("Tone / Style", ["Professional", "Friendly", "Encouraging", "Direct"], key=f"tone_{selected_cand_name}")

                    default_body = (
                        f"Dear {selected_cand_name},\n\n"
                        f"We have reviewed your profile for the {cand_row['Applied Role']} role and were very impressed with your experience in {cand_row['Skills']}.\n\n"
                        f"We would love to invite you for a discussion regarding next steps in our recruitment process.\n\n"
                        f"Best regards,\nRecruitment Team\nAcme Talent Systems"
                    )

                    # Store AI generated body draft in session state if user clicks AI generate
                    draft_key = f"draft_body_{selected_cand_name}"
                    if draft_key not in st.session_state:
                        st.session_state[draft_key] = default_body

                    ai_col, _ = st.columns([1.2, 1])
                    with ai_col:
                        if st.button("✨ Draft / Polish with Ollama (Phi-3)", key=f"ai_gen_{selected_cand_name}"):
                            if self._ollama_client and self._ollama_client.is_connected():
                                with st.spinner("Ollama (Phi-3) is composing a personalized email..."):
                                    ai_mail = self._ollama_client.generate_email(
                                        candidate_name=selected_cand_name,
                                        job_title=cand_row['Applied Role'],
                                        email_type=msg_type,
                                        tone=tone,
                                        extra_context=f"Candidate Skills: {cand_row['Skills']}, Match Score: {cand_row['Match Score']}"
                                    )
                                    if "subject:" in ai_mail.lower():
                                        lines = ai_mail.split("\n")
                                        body_lines = [l for l in lines if not l.lower().startswith("subject:")]
                                        ai_mail = "\n".join(body_lines).strip()
                                    st.session_state[draft_key] = ai_mail
                                    st.success("✓ Email draft updated with Ollama AI!")
                                    st.rerun()
                            else:
                                st.warning("Local Ollama server is offline. Using default email template.")

                    email_body = st.text_area(
                        "Email Content (Editable)",
                        value=st.session_state[draft_key],
                        height=160,
                        key=f"text_area_{selected_cand_name}"
                    )

                    send_col1, send_col2 = st.columns(2)
                    with send_col1:
                        send_email_now = st.button("📨 Send Direct Email", type="primary", use_container_width=True, key=f"send_now_{selected_cand_name}")
                    with send_col2:
                        open_ai_page = st.button("🤖 Open in AI Mail Generator Workspace", use_container_width=True, key=f"open_workspace_{selected_cand_name}")

                    if send_email_now:
                        if not recipient_email.strip():
                            st.error("Please enter a valid recipient email address.")
                        elif not email_subject.strip():
                            st.error("Please enter an email subject line.")
                        else:
                            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            sent_record = {
                                "candidate": selected_cand_name,
                                "email": recipient_email,
                                "subject": email_subject,
                                "body": email_body,
                                "type": msg_type,
                                "timestamp": now_str,
                            }
                            st.session_state.sent_emails.append(sent_record)
                            
                            # Log activity
                            if hasattr(self._candidate_repo, "add_activity"):
                                self._candidate_repo.add_activity(f"Direct email '{email_subject}' sent to {selected_cand_name} ({recipient_email}).")
                            
                            st.session_state[f"last_sent_mail_{selected_cand_name}"] = sent_record
                            st.success(f"✓ Direct Email dispatched successfully to **{selected_cand_name}** (<{recipient_email}>)!")
                            st.rerun()

                    if open_ai_page:
                        st.session_state.pending_page = "AI Mail Generator"
                        st.rerun()

                    # Display Sent Email Confirmation Banner if last sent matches this candidate
                    last_sent = st.session_state.get(f"last_sent_mail_{selected_cand_name}")
                    if last_sent:
                        st.write("")
                        with st.container(border=True):
                            st.markdown("### ✅ Sent Email Confirmation")
                            st.markdown(f"- **Recipient:** `{last_sent['candidate']}` &lt;{last_sent['email']}&gt;")
                            st.markdown(f"- **Subject:** `{last_sent['subject']}`")
                            st.markdown(f"- **Dispatched At:** `{last_sent['timestamp']}`")
                            st.markdown(f"- **Status:** `Delivered (Simulated Direct Dispatch)`")
                            with st.expander("View Sent Email Body"):
                                st.code(last_sent['body'])

                    # Show previous sent email log for this candidate
                    cand_sent_log = [m for m in st.session_state.sent_emails if m["candidate"] == selected_cand_name]
                    if cand_sent_log:
                        st.write("")
                        st.markdown(f"#### 📜 Communication History ({len(cand_sent_log)} sent messages)")
                        for item in reversed(cand_sent_log):
                            st.caption(f"📅 **{item['timestamp']}** | Subject: **{item['subject']}** → `{item['email']}`")
