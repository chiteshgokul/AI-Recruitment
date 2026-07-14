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


class IJobRepository(ABC):
    """Abstraction for job openings data access."""

    @abstractmethod
    def get_jobs(self) -> pd.DataFrame:
        """Retrieve job openings."""
        pass


class IInterviewRepository(ABC):
    """Abstraction for interview schedule data access."""

    @abstractmethod
    def get_interviews(self) -> pd.DataFrame:
        """Retrieve scheduled interviews."""
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
