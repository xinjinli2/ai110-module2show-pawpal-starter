from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date
from enum import Enum


class Priority(Enum):
    """Priority levels for pet care tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    
    def __lt__(self, other):
        """Compare if this priority is less than another priority."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other):
        """Compare if this priority is less than or equal to another priority."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value <= other.value
    
    def __gt__(self, other):
        """Compare if this priority is greater than another priority."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value > other.value
    
    def __ge__(self, other):
        """Compare if this priority is greater than or equal to another priority."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.value >= other.value


class TaskCategory(Enum):
    """Valid categories for pet care tasks."""
    FEEDING = "feeding"
    WALKING = "walking"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    TRAINING = "training"
    PLAYTIME = "playtime"
    OTHER = "other"


@dataclass
class Pet:
    """Represents a pet with basic information and care details."""
    pet_id: str
    name: str
    species: str
    age: int
    special_care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)
    
    def update_profile(self, name: str, species: str, age: int, notes: str) -> None:
        """Update the pet's profile information."""
        self.name = name
        self.species = species
        self.age = age
        self.special_care_notes = notes
    
    def display_info(self) -> str:
        """Display the pet's information."""
        return f"{self.name} ({self.species}, {self.age} years old)\nNotes: {self.special_care_notes}\nTasks: {len(self.tasks)}"
    
    def get_special_care_notes(self) -> str:
        """Return the pet's special care notes."""
        return self.special_care_notes
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the pet's task list by ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
    
    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Task:
    """Represents a single pet care task."""
    task_id: str
    pet_id: str  # Links task to a specific pet
    task_name: str
    duration_minutes: float
    priority: Priority
    category: TaskCategory
    is_completed: bool = False
    
    def __post_init__(self) -> None:
        """Validate that task duration is positive."""
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be positive")
    
    def update_task(self, name: str, duration: float, priority: Priority, category: TaskCategory) -> None:
        """Update task details."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        self.task_name = name
        self.duration_minutes = duration
        self.priority = priority
        self.category = category
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.is_completed = False
    
    def display_task(self) -> str:
        """Display task information."""
        status = "✓ Completed" if self.is_completed else "○ Pending"
        return f"[{status}] {self.task_name} ({self.duration_minutes} min, {self.priority.name})"
    
    def get_details(self) -> str:
        """Return a detailed description of the task."""
        status = "Completed" if self.is_completed else "Pending"
        return (
            f"Task: {self.task_name}\n"
            f"Category: {self.category.value}\n"
            f"Duration: {self.duration_minutes} minutes\n"
            f"Priority: {self.priority.name}\n"
            f"Status: {status}"
        )


class Owner:
    """Represents a pet owner with their constraints and preferences."""
    
    def __init__(self, owner_id: str, name: str, available_time_hours: float, care_preferences: str = "") -> None:
        """Initialize an owner with their constraints and preferences."""
        self.owner_id = owner_id
        self.name = name
        self.available_time_hours = available_time_hours
        self.care_preferences = care_preferences
        self.pets: List[Pet] = []  # List of owned pets
    
    def update_info(self, name: str, available_time: float, preferences: str) -> None:
        """Update owner information."""
        self.name = name
        self.available_time_hours = available_time
        self.care_preferences = preferences
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)
    
    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from the owner's pet list by ID."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]
    
    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def set_pet(self, pet: Pet) -> None:
        """Associate a pet with this owner (sets first pet for backward compatibility)."""
        if len(self.pets) == 0:
            self.add_pet(pet)
        else:
            self.pets[0] = pet
    
    def get_available_time(self) -> float:
        """Return the owner's available time in hours."""
        return self.available_time_hours
    
    def get_care_preferences(self) -> str:
        """Return the owner's care preferences."""
        return self.care_preferences
    
    def display_info(self) -> str:
        """Display owner information."""
        return (
            f"Owner: {self.name}\n"
            f"Available Time: {self.available_time_hours} hours/day\n"
            f"Care Preferences: {self.care_preferences}\n"
            f"Number of Pets: {len(self.pets)}"
        )


@dataclass
class DailyPlan:
    """Represents a daily schedule of pet care tasks."""
    plan_id: str
    owner_id: str  # Links plan to an owner
    pet_id: str  # Links plan to a pet
    plan_date: date
    tasks: List[Task] = field(default_factory=list)
    plan_explanation: str = ""
    
    @property
    def total_scheduled_time(self) -> float:
        """Return the total duration of all scheduled tasks in minutes."""
        return sum(task.duration_minutes for task in self.tasks)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the daily plan."""
        if task not in self.tasks:
            self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the daily plan by ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
    
    def calculate_total_duration(self) -> float:
        """Calculate the total duration of all tasks in the plan (in minutes)."""
        return self.total_scheduled_time
    
    def set_plan_explanation(self, explanation: str) -> None:
        """Set an explanation for why this plan was created."""
        self.plan_explanation = explanation
    
    def present_plan(self) -> str:
        """Present the plan as a formatted string."""
        total_hours = self.total_scheduled_time / 60
        plan_str = f"\n{'='*50}\n"
        plan_str += f"Daily Plan for {self.plan_date}\n"
        plan_str += f"{'='*50}\n"
        
        if not self.tasks:
            plan_str += "No tasks scheduled for today.\n"
        else:
            for i, task in enumerate(self.tasks, 1):
                plan_str += f"{i}. {task.display_task()}\n"
        
        plan_str += f"\nTotal Time: {total_hours:.1f} hours ({self.total_scheduled_time} minutes)\n"
        
        if self.plan_explanation:
            plan_str += f"\nReasoning:\n{self.plan_explanation}\n"
        
        plan_str += f"{'='*50}\n"
        return plan_str
    
    def get_tasks(self) -> List[Task]:
        """Return the list of tasks in the plan."""
        return self.tasks


class Scheduler:
    """Generates daily care plans based on owner constraints and task priorities."""
    
    def __init__(self, owner: Owner, pet: Pet, available_tasks: List[Task]) -> None:
        """Initialize a scheduler with owner, pet, and available tasks."""
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks
    
    def generate_daily_plan(self, plan_id: str) -> DailyPlan:
        """Generate a daily care plan based on owner time and task priorities."""
        # Convert owner's available time from hours to minutes
        available_time_minutes = self.owner.get_available_time() * 60
        
        # Get prioritized tasks
        prioritized = self.prioritize_tasks()
        
        # Allocate tasks that fit within constraints
        selected_tasks = self.allocate_tasks(available_time_minutes)
        
        # Create the daily plan
        plan = DailyPlan(
            plan_id=plan_id,
            owner_id=self.owner.owner_id,
            pet_id=self.pet.pet_id,
            plan_date=date.today(),
            tasks=selected_tasks
        )
        
        # Generate explanation
        explanation = self.create_explanation(selected_tasks)
        plan.set_plan_explanation(explanation)
        
        return plan
    
    def prioritize_tasks(self) -> List[Task]:
        """Sort tasks by priority (highest first), then by duration (shortest first for tie-breaking)."""
        # Filter out completed tasks
        pending_tasks = [t for t in self.available_tasks if not t.is_completed]
        
        # Sort by priority (descending) and then by duration (ascending)
        sorted_tasks = sorted(
            pending_tasks,
            key=lambda t: (-t.priority.value, t.duration_minutes)
        )
        return sorted_tasks
    
    def check_constraints(self, tasks: List[Task]) -> bool:
        """Check if the given tasks fit within owner's available time (converted to minutes)."""
        available_time_minutes = self.owner.get_available_time() * 60
        total_duration = sum(t.duration_minutes for t in tasks)
        return total_duration <= available_time_minutes
    
    def allocate_tasks(self, available_time_minutes: float) -> List[Task]:
        """Select and allocate tasks greedily that fit within available time."""
        prioritized = self.prioritize_tasks()
        allocated = []
        total_time = 0
        
        for task in prioritized:
            if total_time + task.duration_minutes <= available_time_minutes:
                allocated.append(task)
                total_time += task.duration_minutes
        
        return allocated
    
    def create_explanation(self, selected_tasks: List[Task]) -> str:
        """Create a human-readable explanation for why these tasks were selected."""
        if not selected_tasks:
            return "No high-priority tasks could fit in the owner's available time today."
        
        available_time = self.owner.get_available_time() * 60  # Convert to minutes
        total_time = sum(t.duration_minutes for t in selected_tasks)
        remaining_time = available_time - total_time
        
        explanation = f"Selected {len(selected_tasks)} task(s) for {self.pet.name}:\n"
        
        # Group by priority
        high_priority = [t for t in selected_tasks if t.priority == Priority.HIGH]
        medium_priority = [t for t in selected_tasks if t.priority == Priority.MEDIUM]
        low_priority = [t for t in selected_tasks if t.priority == Priority.LOW]
        
        if high_priority:
            explanation += f"- All {len(high_priority)} high-priority task(s) fit in the schedule\n"
        if medium_priority:
            explanation += f"- Added {len(medium_priority)} medium-priority task(s) to maximize care\n"
        if low_priority:
            explanation += f"- Added {len(low_priority)} low-priority enrichment task(s) if time allowed\n"
        
        explanation += f"\nScheduled time: {total_time} minutes ({total_time/60:.1f} hours)"
        explanation += f"\nRemaining time: {remaining_time} minutes ({remaining_time/60:.1f} hours)"
        
        # Add unscheduled tasks info
        unscheduled_count = len(self.available_tasks) - len(selected_tasks)
        if unscheduled_count > 0:
            explanation += f"\n⚠ {unscheduled_count} task(s) could not fit in today's schedule."
        
        return explanation
