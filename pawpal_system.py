from dataclasses import dataclass, field
from typing import List
from datetime import date


@dataclass
class Pet:
    """Represents a pet with basic information and care details."""
    name: str
    species: str
    age: int
    special_care_notes: str = ""
    
    def update_profile(self, name: str, species: str, age: int, notes: str) -> None:
        """Update the pet's profile information."""
        pass
    
    def display_info(self) -> str:
        """Display the pet's information."""
        pass
    
    def get_special_care_notes(self) -> str:
        """Return the pet's special care notes."""
        pass


@dataclass
class Task:
    """Represents a single pet care task."""
    task_name: str
    duration_minutes: float
    priority: str  # e.g., "high", "medium", "low"
    category: str  # e.g., "feeding", "walking", "medication", "grooming", "enrichment"
    is_completed: bool = False
    
    def update_task(self, name: str, duration: float, priority: str, category: str) -> None:
        """Update task details."""
        pass
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        pass
    
    def display_task(self) -> str:
        """Display task information."""
        pass
    
    def get_details(self) -> str:
        """Return a detailed description of the task."""
        pass


class Owner:
    """Represents a pet owner with their constraints and preferences."""
    
    def __init__(self, name: str, available_time_hours: float, care_preferences: str = ""):
        self.name = name
        self.available_time_hours = available_time_hours
        self.care_preferences = care_preferences
    
    def update_info(self, name: str, available_time: float, preferences: str) -> None:
        """Update owner information."""
        pass
    
    def get_available_time(self) -> float:
        """Return the owner's available time in hours."""
        pass
    
    def get_care_preferences(self) -> str:
        """Return the owner's care preferences."""
        pass


@dataclass
class DailyPlan:
    """Represents a daily schedule of pet care tasks."""
    tasks: List[Task] = field(default_factory=list)
    total_scheduled_time: float = 0.0
    plan_explanation: str = ""
    plan_date: date = field(default_factory=date.today)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the daily plan."""
        pass
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the daily plan."""
        pass
    
    def calculate_total_duration(self) -> float:
        """Calculate the total duration of all tasks in the plan."""
        pass
    
    def set_plan_explanation(self, explanation: str) -> None:
        """Set an explanation for why this plan was created."""
        pass
    
    def present_plan(self) -> str:
        """Present the plan as a formatted string."""
        pass
    
    def get_tasks(self) -> List[Task]:
        """Return the list of tasks in the plan."""
        pass


class Scheduler:
    """Generates daily care plans based on owner constraints and task priorities."""
    
    def __init__(self, owner: Owner, pet: Pet, available_tasks: List[Task]):
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks
    
    def generate_daily_plan(self) -> DailyPlan:
        """Generate a daily care plan."""
        pass
    
    def prioritize_tasks(self) -> List[Task]:
        """Sort tasks by priority and other factors."""
        pass
    
    def check_constraints(self, tasks: List[Task]) -> bool:
        """Check if the given tasks fit within owner's available time."""
        pass
    
    def allocate_tasks(self, available_time: float) -> List[Task]:
        """Select and allocate tasks that fit within available time."""
        pass
    
    def create_explanation(self, selected_tasks: List[Task]) -> str:
        """Create an explanation for the selected tasks."""
        pass
