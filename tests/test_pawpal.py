"""
Unit tests for the PawPal+ System
Tests core functionality of Pet, Task, Owner, and Scheduler classes.
"""

import pytest
from datetime import date
from pawpal_system import Pet, Task, Owner, Scheduler, Priority, TaskCategory


class TestTaskCompletion:
    """Test suite for task completion functionality."""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes task status to True."""
        # Arrange: Create a task that is initially not completed
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Walk the dog",
            duration_minutes=30,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING,
            is_completed=False
        )
        
        # Assert initial state is incomplete
        assert task.is_completed is False, "Task should start as incomplete"
        
        # Act: Mark the task as complete
        task.mark_complete()
        
        # Assert: Task status should now be True
        assert task.is_completed is True, "Task should be marked as complete"
    
    def test_mark_incomplete_changes_status(self):
        """Verify that calling mark_incomplete() changes task status to False."""
        # Arrange: Create a task that is initially completed
        task = Task(
            task_id="t2",
            pet_id="p1",
            task_name="Feed the cat",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            is_completed=True
        )
        
        # Assert initial state is completed
        assert task.is_completed is True, "Task should start as completed"
        
        # Act: Mark the task as incomplete
        task.mark_incomplete()
        
        # Assert: Task status should now be False
        assert task.is_completed is False, "Task should be marked as incomplete"


class TestTaskAddition:
    """Test suite for task addition to pets."""
    
    def test_adding_task_to_pet_increases_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange: Create a pet with no tasks
        pet = Pet(
            pet_id="p1",
            name="Max",
            species="Dog",
            age=5,
            special_care_notes="Energetic dog"
        )
        
        # Assert initial state: no tasks
        assert len(pet.get_tasks()) == 0, "Pet should start with no tasks"
        
        # Act: Create and add a task to the pet
        task1 = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Morning Walk",
            duration_minutes=45,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING
        )
        pet.add_task(task1)
        
        # Assert: Task count should increase to 1
        assert len(pet.get_tasks()) == 1, "Pet should have 1 task after adding one"
        assert pet.get_tasks()[0].task_name == "Morning Walk"
    
    def test_adding_multiple_tasks_to_pet(self):
        """Verify that multiple tasks can be added to a pet."""
        # Arrange: Create a pet
        pet = Pet(
            pet_id="p2",
            name="Luna",
            species="Cat",
            age=3,
            special_care_notes="Indoor cat"
        )
        
        # Act: Add multiple tasks
        task1 = Task(
            task_id="t1",
            pet_id="p2",
            task_name="Breakfast",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING
        )
        task2 = Task(
            task_id="t2",
            pet_id="p2",
            task_name="Playtime",
            duration_minutes=20,
            priority=Priority.MEDIUM,
            category=TaskCategory.PLAYTIME
        )
        task3 = Task(
            task_id="t3",
            pet_id="p2",
            task_name="Dinner",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Assert: All 3 tasks should be in the pet's task list
        assert len(pet.get_tasks()) == 3, "Pet should have 3 tasks"
        task_names = [t.task_name for t in pet.get_tasks()]
        assert "Breakfast" in task_names
        assert "Playtime" in task_names
        assert "Dinner" in task_names
    
    def test_duplicate_tasks_not_added_twice(self):
        """Verify that the same task object is not added twice."""
        # Arrange: Create a pet and task
        pet = Pet(
            pet_id="p3",
            name="Buddy",
            species="Dog",
            age=2
        )
        task = Task(
            task_id="t1",
            pet_id="p3",
            task_name="Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING
        )
        
        # Act: Try to add the same task twice
        pet.add_task(task)
        pet.add_task(task)
        
        # Assert: Task should only appear once
        assert len(pet.get_tasks()) == 1, "Duplicate tasks should not be added"


class TestTaskValidation:
    """Test suite for task validation."""
    
    def test_invalid_duration_raises_error(self):
        """Verify that tasks with invalid durations raise an error."""
        # Assert: Creating a task with zero duration should raise ValueError
        with pytest.raises(ValueError, match="Duration must be positive"):
            Task(
                task_id="t1",
                pet_id="p1",
                task_name="Invalid task",
                duration_minutes=0,
                priority=Priority.HIGH,
                category=TaskCategory.FEEDING
            )
    
    def test_negative_duration_raises_error(self):
        """Verify that tasks with negative durations raise an error."""
        # Assert: Creating a task with negative duration should raise ValueError
        with pytest.raises(ValueError, match="Duration must be positive"):
            Task(
                task_id="t2",
                pet_id="p1",
                task_name="Invalid task",
                duration_minutes=-15,
                priority=Priority.HIGH,
                category=TaskCategory.FEEDING
            )


class TestSchedulerPrioritization:
    """Test suite for scheduler prioritization logic."""
    
    def test_prioritize_tasks_by_priority_level(self):
        """Verify that tasks are prioritized correctly (HIGH > MEDIUM > LOW)."""
        # Arrange: Create pet with tasks of different priorities
        pet = Pet(
            pet_id="p1",
            name="Max",
            species="Dog",
            age=5
        )
        
        low_task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Grooming",
            duration_minutes=45,
            priority=Priority.LOW,
            category=TaskCategory.GROOMING
        )
        high_task = Task(
            task_id="t2",
            pet_id="p1",
            task_name="Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING
        )
        medium_task = Task(
            task_id="t3",
            pet_id="p1",
            task_name="Playtime",
            duration_minutes=20,
            priority=Priority.MEDIUM,
            category=TaskCategory.PLAYTIME
        )
        
        pet.add_task(low_task)
        pet.add_task(high_task)
        pet.add_task(medium_task)
        
        # Arrange: Create owner and scheduler
        owner = Owner(
            owner_id="o1",
            name="test_owner",
            available_time_hours=2.0
        )
        
        # Act: Prioritize tasks
        scheduler = Scheduler(owner, pet, pet.get_tasks())
        prioritized = scheduler.prioritize_tasks()
        
        # Assert: Tasks should be ordered HIGH, MEDIUM, LOW
        assert prioritized[0].priority == Priority.HIGH, "First task should be HIGH priority"
        assert prioritized[1].priority == Priority.MEDIUM, "Second task should be MEDIUM priority"
        assert prioritized[2].priority == Priority.LOW, "Third task should be LOW priority"
    
    def test_scheduler_respects_time_constraints(self):
        """Verify that scheduler only allocates tasks that fit in available time."""
        # Arrange: Create pet with multiple tasks
        pet = Pet(
            pet_id="p1",
            name="Max",
            species="Dog",
            age=5
        )
        
        # Total duration: 30 + 15 + 20 + 30 = 95 minutes
        tasks = [
            Task(
                task_id="t1",
                pet_id="p1",
                task_name="Task 1",
                duration_minutes=30,
                priority=Priority.HIGH,
                category=TaskCategory.WALKING
            ),
            Task(
                task_id="t2",
                pet_id="p1",
                task_name="Task 2",
                duration_minutes=15,
                priority=Priority.HIGH,
                category=TaskCategory.FEEDING
            ),
            Task(
                task_id="t3",
                pet_id="p1",
                task_name="Task 3",
                duration_minutes=20,
                priority=Priority.MEDIUM,
                category=TaskCategory.PLAYTIME
            ),
            Task(
                task_id="t4",
                pet_id="p1",
                task_name="Task 4",
                duration_minutes=30,
                priority=Priority.MEDIUM,
                category=TaskCategory.WALKING
            ),
        ]
        
        for task in tasks:
            pet.add_task(task)
        
        # Arrange: Owner has only 1 hour available
        owner = Owner(
            owner_id="o1",
            name="test_owner",
            available_time_hours=1.0  # 60 minutes
        )
        
        # Act: Create scheduler and allocate tasks
        scheduler = Scheduler(owner, pet, pet.get_tasks())
        allocated = scheduler.allocate_tasks(60)  # 60 minutes
        
        # Assert: Total allocated time should not exceed 60 minutes
        total_allocated_time = sum(t.duration_minutes for t in allocated)
        assert total_allocated_time <= 60, "Allocated tasks should not exceed available time"
        assert total_allocated_time == 45, "Should allocate exactly high-priority tasks (30+15=45)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
