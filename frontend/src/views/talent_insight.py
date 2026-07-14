# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from backend.core.interfaces import IView, IEmployeeRepository
from backend.core.ollama_client import OllamaClient
from frontend.src.components.widgets import hero, section_header
from frontend.src.core.styles import MUTED_TEXT


class TalentInsightView(IView):
    """View renderer for the Talent Insight AI dashboard."""

    def __init__(self, employee_repo: IEmployeeRepository, ollama_client: OllamaClient) -> None:
        self._employee_repo = employee_repo
        self._ollama_client = ollama_client

    def render(self) -> None:
        hero(
            "Talent Insight AI",
            "Perform workforce flight risk modeling, team analytics, and draft retention strategies locally using Ollama (Phi-3)."
        )

        # 1. Fetch current employees
        employees = self._employee_repo.get_employees()

        # 2. Render summary KPIs
        total_staff = len(employees)
        high_risk_count = len(employees[employees["Flight Risk"] == "High"])
        med_risk_count = len(employees[employees["Flight Risk"] == "Medium"])

        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.metric("Total Workforce", f"{total_staff} Staff", "Active employees")
        with kpi_col2:
            st.metric("High Flight Risk", f"{high_risk_count}", "Requires immediate attention", delta_color="inverse")
        with kpi_col3:
            st.metric("Medium Flight Risk", f"{med_risk_count}", "Monitor closely", delta_color="off")

        st.write("")

        # 3. Main layout
        left_col, right_col = st.columns([1, 1])

        with left_col:
            with st.container(border=True):
                section_header("👤 Select Employee", "Pick an employee to run a personalized flight risk analysis.")
                
                selected_name = st.selectbox(
                    "Employee Name",
                    options=employees["Name"].tolist(),
                    label_visibility="collapsed"
                )
                
                # Fetch details for the selected employee
                emp_data = employees[employees["Name"] == selected_name].iloc[0]
                
                st.markdown("---")
                
                col_dept, col_ten = st.columns(2)
                with col_dept:
                    st.markdown(f"**Department:**  \n{emp_data['Department']}")
                with col_ten:
                    st.markdown(f"**Tenure:**  \n{emp_data['Tenure']}")
                    
                st.markdown("---")
                st.markdown(f"**Skills:**  \n{emp_data['Skills']}")
                
                risk = emp_data["Flight Risk"]
                if risk == "High":
                    st.error(f"🚨 Assessed Flight Risk: **{risk}**")
                elif risk == "Medium":
                    st.warning(f"⚠️ Assessed Flight Risk: **{risk}**")
                else:
                    st.success(f"✅ Assessed Flight Risk: **{risk}**")

                st.write("")
                
                analyze_btn = st.button("✨ Analyze Retention Strategy", use_container_width=True, type="primary")

                if "last_retention_analysis" not in st.session_state:
                    st.session_state.last_retention_analysis = None

                if analyze_btn:
                    if not self._ollama_client.is_connected():
                        st.error("Ollama connection error: Please ensure your local Ollama server is running and the `phi3` model is loaded.")
                    else:
                        with st.spinner(f"Analyzing flight risk signals for {selected_name}..."):
                            analysis = self._ollama_client.generate_retention_strategy(
                                employee_name=selected_name,
                                department=emp_data["Department"],
                                skills=emp_data["Skills"],
                                tenure=emp_data["Tenure"],
                                risk_level=emp_data["Flight Risk"]
                            )
                            st.session_state.last_retention_analysis = (selected_name, analysis)

        with right_col:
            # Display risk analysis if employee matches selection
            if st.session_state.last_retention_analysis:
                saved_name, analysis_text = st.session_state.last_retention_analysis
                if saved_name == selected_name:
                    with st.container(border=True):
                        section_header(f"📋 AI Retention Plan: {selected_name}")
                        st.write(analysis_text)
                else:
                    st.session_state.last_retention_analysis = None
                    st.info("Awaiting analysis trigger. Select an employee and click 'Analyze Retention Strategy'.")
            else:
                with st.container(border=True):
                    section_header("📊 Workforce Risk Distribution")
                    # Display a bar chart of flight risk categories
                    risk_counts = employees["Flight Risk"].value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
                    chart_df = pd.DataFrame({"Employees": risk_counts})
                    st.bar_chart(chart_df)
                    st.caption("Distribution of flight risk tags across the currently loaded mock workforce database.")
