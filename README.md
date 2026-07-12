# 🤖 AI Recruitment and Talent Management Copilot

A modern recruitment dashboard and talent management command center built with **Streamlit** and **Pandas**. 

This repository has been fully refactored to adhere to **SOLID Design Principles** for high modularity, scalability, and ease of testing.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8 or higher installed on your system.

### 1. Install Dependencies
Install all required libraries using the project's dependencies list:
```bash
pip install -r requirements.txt
```

### 2. Run the App
Since Streamlit executables are often installed inside user script directories that are not on the system's `PATH`, execute Streamlit using Python's module wrapper:
```bash
python -m streamlit run app.py
```
Alternatively, on Windows using the Python launcher:
```bash
py -m streamlit run app.py
```

---

## 🛠️ Architecture & SOLID Principles

The monolithic codebase was split into clean layers with single responsibilities:

1. **Single Responsibility Principle (SRP)**:
   - Extracted styling functions and constants into [styles.py](src/core/styles.py).
   - Extracted shared components into [widgets.py](src/components/widgets.py).
   - Each dashboard screen is separated into its own module under [src/views/](src/views/).
   - Mock data generation logic is isolated within [repository.py](src/data/repository.py).

2. **Open-Closed Principle (OCP)**:
   - Page routing in [app.py](app.py) maps a dictionary of views implementing the `IView` interface. To add a new view page, you simply register a new class implementing the interface without modifying routing logic.

3. **Liskov Substitution Principle (LSP)**:
   - All page views (e.g., `DashboardView`, `CandidatesView`, `AnalyticsView`) subclass and implement the `IView` interface, allowing the router to render them interchangeably.

4. **Interface Segregation Principle (ISP)**:
   - Separate interfaces are defined for `ICandidateRepository`, `IJobRepository`, and `IInterviewRepository` under [interfaces.py](src/core/interfaces.py), ensuring clients only depend on the data access methods they actually utilize.

5. **Dependency Inversion Principle (DIP)**:
   - The view layer depends strictly on repository abstractions (`ICandidateRepository`, `IJobRepository`, `IInterviewRepository`) instead of concrete implementations. The concrete `MockDataRepository` is injected from the entry point [app.py](app.py).

---

## 📂 Project Directory Structure

```text
AI Recruitment/
├── app.py                      # Main entrypoint and router
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git untracked pattern file
├── README.md                   # Project documentation
└── src/
    ├── components/
    │   └── widgets.py          # Shared UI widgets (hero, cards, pills)
    ├── core/
    │   ├── interfaces.py       # Base view and repository abstractions
    │   └── styles.py           # Color scheme and global CSS styles
    ├── data/
    │   └── repository.py       # Concrete Mock Repository
    └── views/
        ├── analytics.py        # Analytics and charts page
        ├── candidates.py       # Candidate search and management page
        ├── dashboard.py        # Main command center KPIs & pipeline page
        ├── interviews.py       # Interview schedule and status page
        ├── jobs.py             # Active and draft job openings page
        ├── resume_screening.py # Resume upload and future AI scoring page
        ├── settings.py         # App configuration settings page
        └── talent.py           # Employee skills & learning recommendations
```

---

## 🌟 Key Features

* **Dashboard**: KPI command center showing candidate volumes, active openings, average hiring time, and pipeline progression.
* **Candidate Tracker**: Comprehensive candidate search filterable by skills, experience, and education levels.
* **Job Openings Manager**: View active, draft, and on-hold roles with applicant counts.
* **Resume Screening Workspace**: Interactive file uploader screen set up for future AI resume extraction.
* **Interview coordinator**: Weekly schedule and calendar overview tracking interview states.
* **Talent Development Planner**: Skill coverage tracker, gap analysis charts, and learning pathways.
* **Analytics Commands**: Visual trend lines, candidate distribution charts, and recruitment funnel statistics.
