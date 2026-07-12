import random
from datetime import date, timedelta
import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st
from src.core.interfaces import ICandidateRepository, IJobRepository, IInterviewRepository


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

    candidates = []
    for idx, name in enumerate(names):
        candidate_skills = random.sample(skills_pool, k=random.randint(3, 5))
        candidates.append(
            {
                "Name": name,
                "Skills": ", ".join(candidate_skills),
                "Experience": f"{random.randint(1, 11)} years",
                "Education": random.choice(education_pool),
                "Match Score": f"{random.randint(72, 98)}%",
                "Status": random.choice(statuses),
                "Resume": "View Resume",
                "Applied Role": random.choice(
                    [
                        "AI Engineer",
                        "HR Analyst",
                        "Product Designer",
                        "Backend Developer",
                        "Talent Partner",
                    ]
                ),
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

    return {
        "candidates": pd.DataFrame(candidates),
        "applications": applications,
        "interviews": interviews,
        "jobs": jobs,
    }


class MockDataRepository(ICandidateRepository, IJobRepository, IInterviewRepository):
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
