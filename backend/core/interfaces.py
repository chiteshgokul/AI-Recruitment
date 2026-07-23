from abc import ABC, abstractmethod
import pandas as pd


class ICandidateRepository(ABC):
    """Abstraction for candidate and application data access."""

    @abstractmethod
    def get_candidates(self) -> pd.DataFrame:
        """Retrieve candidate records."""
        pass

    @abstractmethod
    def get_applications(self) -> pd.DataFrame:
        """Retrieve recent applications."""
        pass

    def update_candidate_status(self, candidate_name: str, new_status: str) -> None:
        """Update a candidate's status."""
        pass


class IJobRepository(ABC):
    """Abstraction for job openings data access."""

    @abstractmethod
    def get_jobs(self) -> pd.DataFrame:
        """Retrieve job openings."""
        pass

    def update_job_status(self, job_title: str, new_status: str) -> None:
        """Update job status."""
        pass

    def add_job(self, job_dict: dict) -> None:
        """Add a new job opening."""
        pass


class IInterviewRepository(ABC):
    """Abstraction for interview schedule data access."""

    @abstractmethod
    def get_interviews(self) -> pd.DataFrame:
        """Retrieve scheduled interviews."""
        pass

    def add_interview(self, interview_dict: dict) -> None:
        """Add a new scheduled interview."""
        pass


class IEmployeeRepository(ABC):
    """Abstraction for employee and workforce data access."""

    @abstractmethod
    def get_employees(self) -> pd.DataFrame:
        """Retrieve current employee records."""
        pass


class IView(ABC):
    """Abstraction for renderable UI screens."""

    @abstractmethod
    def render(self) -> None:
        """Render the view logic."""
        pass
