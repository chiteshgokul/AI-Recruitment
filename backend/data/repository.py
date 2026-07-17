import random
from datetime import date, timedelta
import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st
from backend.core.interfaces import ICandidateRepository, IJobRepository, IInterviewRepository, IEmployeeRepository


@st.cache_data
def _generate_sample_data() -> dict[str, pd.DataFrame]:
    """Generate deterministic placeholder data for Milestone 1 UI screens."""
    random.seed(42)

    names = [
        "Aarav Mehta",
        "Sophia Carter",
        "Liam Johnson",
        "Maya Rao",
        "Noah Williams",
        "Isha Kapoor",
        "Ethan Brown",
        "Olivia Chen",
        "Rohan Shah",
        "Emma Davis",
        "Arjun Nair",
        "Ava Thompson",
    ]
    skills_pool = [
        "Python",
        "React",
        "SQL",
        "AWS",
        "NLP",
        "People Analytics",
        "Figma",
        "Tableau",
        "Django",
        "Leadership",
        "Power BI",
        "Data Engineering",
    ]
    education_pool = ["Bachelor's", "Master's", "MBA", "PhD", "Diploma"]
    statuses = ["New", "In Review", "Interview", "Selected", "On Hold"]

    role_skills_map = {
        "AI Engineer": ["Python", "NLP", "LLMs", "AWS", "PyTorch", "SQL", "MLOps"],
        "Product Designer": ["Figma", "UI/UX Design", "Wireframing", "Prototyping", "Design Systems", "User Research"],
        "HR Analyst": ["People Analytics", "Tableau", "Power BI", "SQL", "Data Analysis", "Excel"],
        "Backend Developer": ["Python", "Django", "SQL", "AWS", "REST APIs", "Git", "Docker"],
        "Talent Partner": ["Recruiting", "Sourcing", "ATS", "Leadership", "Communication", "HR Strategy"],
    }

    candidates = []
    for idx, name in enumerate(names):
        applied_role = random.choice(
            [
                "AI Engineer",
                "HR Analyst",
                "Product Designer",
                "Backend Developer",
                "Talent Partner",
            ]
        )
        role_skills = role_skills_map[applied_role]
        candidate_skills = random.sample(role_skills, k=min(random.randint(3, 4), len(role_skills)))
        candidates.append(
            {
                "Name": name,
                "Skills": ", ".join(candidate_skills),
                "Experience": f"{random.randint(1, 11)} years",
                "Education": random.choice(education_pool),
                "Match Score": f"{random.randint(72, 98)}%",
                "Status": random.choice(statuses),
                "Resume": "View Resume",
                "Applied Role": applied_role,
                "Applied Date": (date.today() - timedelta(days=idx + random.randint(1, 14))).isoformat(),
            }
        )

    applications = pd.DataFrame(candidates)[
        ["Name", "Applied Role", "Applied Date", "Match Score", "Status"]
    ].head(8)

    interviews = pd.DataFrame(
        [
            {
                "Candidate": random.choice(names),
                "Role": random.choice(
                    ["AI Engineer", "HR Analyst", "UX Researcher", "Talent Partner"]
                ),
                "Interviewer": random.choice(
                    ["Priya Sharma", "Daniel Lee", "Fatima Noor", "Marcus Green"]
                ),
                "Date": (date.today() + timedelta(days=i + 1)).isoformat(),
                "Time": random.choice(["10:00 AM", "12:30 PM", "2:00 PM", "4:30 PM"]),
                "Status": random.choice(["Scheduled", "Pending Feedback", "Confirmed"]),
            }
            for i in range(8)
        ]
    )

    jobs = pd.DataFrame(
        [
            {
                "Job Title": "Senior AI Engineer",
                "Department": "Engineering",
                "Location": "Bengaluru / Remote",
                "Required Skills": "Python, LLMs, AWS, MLOps",
                "Applicants": 84,
                "Status": "Open",
            },
            {
                "Job Title": "Talent Acquisition Partner",
                "Department": "People",
                "Location": "Mumbai",
                "Required Skills": "Sourcing, ATS, Interviewing",
                "Applicants": 46,
                "Status": "Open",
            },
            {
                "Job Title": "Product Designer",
                "Department": "Design",
                "Location": "Pune / Hybrid",
                "Required Skills": "Figma, UX Research, Prototyping",
                "Applicants": 58,
                "Status": "Active",
            },
            {
                "Job Title": "People Analytics Lead",
                "Department": "HR Strategy",
                "Location": "Delhi",
                "Required Skills": "Tableau, SQL, Workforce Planning",
                "Applicants": 29,
                "Status": "Open",
            },
            {
                "Job Title": "Backend Developer",
                "Department": "Engineering",
                "Location": "Hyderabad",
                "Required Skills": "Django, APIs, PostgreSQL",
                "Applicants": 73,
                "Status": "Draft",
            },
            {
                "Job Title": "Learning Program Manager",
                "Department": "Talent Development",
                "Location": "Remote",
                "Required Skills": "L&D, Coaching, LMS",
                "Applicants": 22,
                "Status": "On Hold",
            },
        ]
    )

    employees = pd.DataFrame(
        [
            {
                "Name": "Aarav Mehta",
                "Department": "Engineering",
                "Tenure": "3.5 years",
                "Skills": "Python, AWS, Django",
                "Flight Risk": "Low",
            },
            {
                "Name": "Sophia Carter",
                "Department": "Design",
                "Tenure": "1.2 years",
                "Skills": "Figma, UX Research",
                "Flight Risk": "High",
            },
            {
                "Name": "Maya Rao",
                "Department": "People",
                "Tenure": "4.0 years",
                "Skills": "Sourcing, SPHR",
                "Flight Risk": "Medium",
            },
            {
                "Name": "Isha Kapoor",
                "Department": "Engineering",
                "Tenure": "2.1 years",
                "Skills": "React, TypeScript",
                "Flight Risk": "Low",
            },
            {
                "Name": "Ethan Brown",
                "Department": "Sales",
                "Tenure": "0.8 years",
                "Skills": "CRM, Sales Strategy",
                "Flight Risk": "High",
            },
        ]
    )

    return {
        "candidates": pd.DataFrame(candidates),
        "applications": applications,
        "interviews": interviews,
        "jobs": jobs,
        "employees": employees,
    }


class MockDataRepository(ICandidateRepository, IJobRepository, IInterviewRepository, IEmployeeRepository):
    """Concrete repository using deterministic mock data generators."""

    def __init__(self) -> None:
        self._data = _generate_sample_data()

    def get_candidates(self) -> pd.DataFrame:
        return self._data["candidates"]

    def get_applications(self) -> pd.DataFrame:
        return self._data["applications"]

    def get_jobs(self) -> pd.DataFrame:
        return self._data["jobs"]

    def get_interviews(self) -> pd.DataFrame:
        return self._data["interviews"]

    def get_employees(self) -> pd.DataFrame:
        return self._data["employees"]
