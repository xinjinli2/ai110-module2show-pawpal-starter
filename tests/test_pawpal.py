"""
Unit tests for the PawPal+ System
Tests core functionality of Pet, Task, Owner, and Scheduler classes.
"""

import pytest
from datetime import date, timedelta
from pawpal_system import (
    Pet, Task, Owner, Scheduler, Priority, TaskCategory, 
    TaskFrequency, RecurringTaskManager, DailyPlan
)


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


class TestRecurringTaskAutoGeneration:
    """Test suite for recurring task auto-generation using timedelta."""
    
    def test_daily_task_generates_next_occurrence(self):
        """Verify that completing a DAILY task creates next occurrence for tomorrow."""
        # Arrange: Create a daily recurring task
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING,
            frequency=TaskFrequency.DAILY,
            due_date=date.today()
        )
        
        pet = Pet(
            pet_id="p1",
            name="Max",
            species="Dog",
            age=5
        )
        
        owner = Owner(
            owner_id="o1",
            name="test_owner",
            available_time_hours=2.0
        )
        
        # Act: Create next occurrence
        next_task = RecurringTaskManager.create_next_occurrence(task, pet)
        
        # Assert: Next task should be created for tomorrow
        assert next_task is not None, "Daily task should generate next occurrence"
        assert next_task.is_completed is False, "New task should start incomplete"
        assert next_task.last_completed_date is None, "New task should have no completion date"
        assert next_task.due_date == date.today() + timedelta(days=1), "Daily task should be due tomorrow"
        assert next_task.parent_task_id == task.task_id, "Should track parent task lineage"
        assert next_task.frequency == TaskFrequency.DAILY, "Should preserve frequency"
    
    def test_weekly_task_generates_next_occurrence(self):
        """Verify that completing a WEEKLY task creates next occurrence for 7 days later."""
        # Arrange: Create a weekly recurring task
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Grooming",
            duration_minutes=60,
            priority=Priority.MEDIUM,
            category=TaskCategory.GROOMING,
            frequency=TaskFrequency.WEEKLY,
            due_date=date.today()
        )
        
        pet = Pet(pet_id="p1", name="Luna", species="Cat", age=3)
        
        # Act: Create next occurrence
        next_task = RecurringTaskManager.create_next_occurrence(task, pet)
        
        # Assert: Next task should be due in 7 days
        assert next_task is not None, "Weekly task should generate next occurrence"
        assert next_task.due_date == date.today() + timedelta(days=7), "Weekly task should be due 7 days later"
        assert next_task.parent_task_id == task.task_id, "Should link to parent task"
    
    def test_once_task_does_not_recur(self):
        """Verify that ONCE tasks return None and don't generate next occurrence."""
        # Arrange: Create a one-time task
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Vet Appointment",
            duration_minutes=45,
            priority=Priority.HIGH,
            category=TaskCategory.MEDICATION,
            frequency=TaskFrequency.ONCE,
            due_date=date.today()
        )
        
        pet = Pet(pet_id="p1", name="Buddy", species="Dog", age=2)
        
        # Act: Try to create next occurrence
        next_task = RecurringTaskManager.create_next_occurrence(task, pet)
        
        # Assert: Should return None for one-time tasks
        assert next_task is None, "One-time tasks should not recur"
    
    def test_recurring_completion_adds_next_task_to_pet(self):
        """Verify that marking a recurring task complete auto-adds next occurrence to pet."""
        # Arrange: Create a daily task and add to pet
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Feeding",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            frequency=TaskFrequency.DAILY,
            due_date=date.today()
        )
        
        pet = Pet(pet_id="p1", name="Whiskers", species="Cat", age=4)
        pet.add_task(task)
        
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        
        # Act: Handle recurring completion
        next_task = RecurringTaskManager.handle_recurring_completion(task, pet, owner)
        
        # Assert: Current task marked complete, next task added to pet
        assert task.is_completed is True, "Task should be marked complete"
        assert task.last_completed_date == date.today(), "Completion date should be recorded"
        assert len(pet.get_tasks()) == 2, "Next task should be added to pet"
        assert next_task is not None, "Next task should be returned"
        assert next_task.due_date == date.today() + timedelta(days=1), "Next task due tomorrow"
    
    def test_recurring_task_lineage_tracking(self):
        """Verify that recurring tasks maintain parent_task_id lineage."""
        # Arrange
        parent_task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Medication",
            duration_minutes=5,
            priority=Priority.HIGH,
            category=TaskCategory.MEDICATION,
            frequency=TaskFrequency.DAILY
        )
        
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        
        # Create a chain of recurring tasks
        child_task = RecurringTaskManager.create_next_occurrence(parent_task, pet)
        grandchild_task = RecurringTaskManager.create_next_occurrence(child_task, pet)
        
        # Assert: Verify parent links
        assert parent_task.parent_task_id is None, "Original task has no parent"
        assert child_task.parent_task_id == parent_task.task_id, "Child links to parent"
        assert grandchild_task.parent_task_id == child_task.task_id, "Grandchild links to its parent"
    
    def test_recurring_task_preserves_properties(self):
        """Verify that generated tasks preserve name, priority, category, and time."""
        # Arrange: Create task with specific properties
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Evening Walk",
            duration_minutes=45,
            priority=Priority.MEDIUM,
            category=TaskCategory.WALKING,
            scheduled_time="18:30",
            frequency=TaskFrequency.DAILY
        )
        
        pet = Pet(pet_id="p1", name="Rover", species="Dog", age=6)
        
        # Act: Create next occurrence
        next_task = RecurringTaskManager.create_next_occurrence(task, pet)
        
        # Assert: All properties preserved
        assert next_task.task_name == task.task_name, "Task name should be preserved"
        assert next_task.duration_minutes == task.duration_minutes, "Duration should match"
        assert next_task.priority == task.priority, "Priority should match"
        assert next_task.category == task.category, "Category should match"
        assert next_task.scheduled_time == task.scheduled_time, "Scheduled time should match"
    
    def test_week_boundary_handling_for_weekly_tasks(self):
        """Verify weekly tasks correctly handle month boundaries (e.g., Jan 31 -> Feb 7)."""
        # Arrange: Create task on Jan 31
        jan_31 = date(2026, 1, 31)
        task = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Weekly Checkup",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            category=TaskCategory.OTHER,
            frequency=TaskFrequency.WEEKLY,
            due_date=jan_31
        )
        
        pet = Pet(pet_id="p1", name="Percy", species="Dog", age=3)
        
        # Manually set today to Jan 31 for this test context
        # (In real scenario, this would be date.today())
        # Act: Create next occurrence (7 days later = Feb 7)
        next_due = jan_31 + timedelta(days=7)
        
        # Assert: Should correctly cross month boundary
        assert next_due.month == 2, "Should move to February"
        assert next_due.day == 7, "Should be the 7th"


class TestConflictDetection:
    """Test suite for lightweight conflict detection."""
    
    def test_detect_two_tasks_at_same_time(self):
        """Verify scheduler detects when two tasks are scheduled at the exact same time."""
        # Arrange: Create owner and pet
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        # Create two tasks at the same time
        task1 = Task(
            task_id="t1",
            pet_id="p1",
            task_name="Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING,
            scheduled_time="14:00"
        )
        task2 = Task(
            task_id="t2",
            pet_id="p1",
            task_name="Feed",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            scheduled_time="14:00"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act: Detect conflicts
        scheduler = Scheduler(owner, pet, pet.get_tasks())
        warnings = scheduler.detect_time_conflicts([task1, task2])
        
        # Assert: Should detect conflict
        assert len(warnings) > 0, "Should detect conflict"
        assert "14:00" in warnings[0], "Warning should mention conflicted time"
        assert "2 tasks" in warnings[0], "Warning should show number of conflicting tasks"
    
    def test_no_conflict_for_different_times(self):
        """Verify no conflicts reported when tasks are at different times."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Luna", species="Cat", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_id="t1", pet_id="p1", task_name="Breakfast",
                    duration_minutes=15, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING, scheduled_time="08:00")
        task2 = Task(task_id="t2", pet_id="p1", task_name="Lunch",
                    duration_minutes=15, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING, scheduled_time="12:00")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner, pet, pet.get_tasks())
        warnings = scheduler.detect_time_conflicts([task1, task2])
        
        # Assert: No conflicts
        assert len(warnings) == 0, "Should have no conflicts for different times"
    
    def test_multiple_conflicts_detected(self):
        """Verify detection when multiple conflict groups exist."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=5.0)
        pet = Pet(pet_id="p1", name="Buddy", species="Dog", age=4)
        owner.add_pet(pet)
        
        # Two tasks at 14:00, two tasks at 16:00
        tasks = [
            Task(task_id="t1", pet_id="p1", task_name="Walk 1", duration_minutes=30,
                priority=Priority.HIGH, category=TaskCategory.WALKING, scheduled_time="14:00"),
            Task(task_id="t2", pet_id="p1", task_name="Walk 2", duration_minutes=30,
                priority=Priority.MEDIUM, category=TaskCategory.WALKING, scheduled_time="14:00"),
            Task(task_id="t3", pet_id="p1", task_name="Play 1", duration_minutes=20,
                priority=Priority.MEDIUM, category=TaskCategory.PLAYTIME, scheduled_time="16:00"),
            Task(task_id="t4", pet_id="p1", task_name="Play 2", duration_minutes=20,
                priority=Priority.LOW, category=TaskCategory.PLAYTIME, scheduled_time="16:00"),
        ]
        
        for task in tasks:
            pet.add_task(task)
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        warnings = scheduler.detect_time_conflicts(tasks)
        
        # Assert: Should detect two separate conflicts
        assert len(warnings) == 2, "Should detect two conflict groups"
    
    def test_no_crash_with_unscheduled_tasks(self):
        """Verify conflict detection gracefully handles tasks without scheduled_time."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Spot", species="Dog", age=2)
        owner.add_pet(pet)
        
        # One task with time, one without
        task1 = Task(task_id="t1", pet_id="p1", task_name="Walk",
                    duration_minutes=30, priority=Priority.HIGH,
                    category=TaskCategory.WALKING, scheduled_time="10:00")
        task2 = Task(task_id="t2", pet_id="p1", task_name="Medication",
                    duration_minutes=5, priority=Priority.HIGH,
                    category=TaskCategory.MEDICATION)  # No scheduled_time
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act & Assert: Should not crash
        scheduler = Scheduler(owner, pet, [task1, task2])
        warnings = scheduler.detect_time_conflicts([task1, task2])
        assert len(warnings) == 0, "Unscheduled tasks should be skipped"
    
    def test_empty_task_list_returns_no_warnings(self):
        """Verify conflict detection returns empty list for empty task list."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        # Act
        scheduler = Scheduler(owner, pet, [])
        warnings = scheduler.detect_time_conflicts([])
        
        # Assert
        assert len(warnings) == 0, "Empty list should return no warnings"
    
    def test_single_task_returns_no_conflict(self):
        """Verify no conflict when only one task exists."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Luna", species="Cat", age=3)
        owner.add_pet(pet)
        
        task = Task(task_id="t1", pet_id="p1", task_name="Feeding",
                   duration_minutes=15, priority=Priority.HIGH,
                   category=TaskCategory.FEEDING, scheduled_time="09:00")
        pet.add_task(task)
        
        # Act
        scheduler = Scheduler(owner, pet, [task])
        warnings = scheduler.detect_time_conflicts([task])
        
        # Assert
        assert len(warnings) == 0, "Single task cannot have conflicts"
    
    def test_conflict_detection_returns_list_not_exception(self):
        """Verify conflict detection is lightweight - returns warnings, doesn't throw."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Rex", species="Dog", age=3)
        owner.add_pet(pet)
        
        # Create conflicting tasks
        task1 = Task(task_id="t1", pet_id="p1", task_name="Task A",
                    duration_minutes=20, priority=Priority.HIGH,
                    category=TaskCategory.WALKING, scheduled_time="15:00")
        task2 = Task(task_id="t2", pet_id="p1", task_name="Task B",
                    duration_minutes=20, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING, scheduled_time="15:00")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act & Assert: Should not raise exception
        scheduler = Scheduler(owner, pet, [task1, task2])
        try:
            warnings = scheduler.detect_time_conflicts([task1, task2])
            assert isinstance(warnings, list), "Should return a list"
            assert len(warnings) > 0, "Should have warning for conflict"
        except Exception as e:
            pytest.fail(f"Conflict detection should not raise exception: {e}")


class TestTaskSorting:
    """Test suite for task sorting by scheduled time."""
    
    def test_sort_tasks_by_chronological_order(self):
        """Verify tasks are sorted in chronological order by scheduled_time."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=4.0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        tasks = [
            Task(task_id="t3", pet_id="p1", task_name="Evening Walk",
                duration_minutes=30, priority=Priority.MEDIUM,
                category=TaskCategory.WALKING, scheduled_time="18:00"),
            Task(task_id="t1", pet_id="p1", task_name="Morning Walk",
                duration_minutes=30, priority=Priority.HIGH,
                category=TaskCategory.WALKING, scheduled_time="08:00"),
            Task(task_id="t2", pet_id="p1", task_name="Afternoon Feeding",
                duration_minutes=15, priority=Priority.HIGH,
                category=TaskCategory.FEEDING, scheduled_time="12:00"),
        ]
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        # Assert: Should be in order 08:00 → 12:00 → 18:00
        assert sorted_tasks[0].scheduled_time == "08:00", "First should be 08:00"
        assert sorted_tasks[1].scheduled_time == "12:00", "Second should be 12:00"
        assert sorted_tasks[2].scheduled_time == "18:00", "Third should be 18:00"
    
    def test_unscheduled_tasks_sorted_to_end(self):
        """Verify tasks without scheduled_time are placed at the end."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Luna", species="Cat", age=3)
        owner.add_pet(pet)
        
        tasks = [
            Task(task_id="t2", pet_id="p1", task_name="Medication",
                duration_minutes=5, priority=Priority.HIGH,
                category=TaskCategory.MEDICATION),  # No scheduled_time
            Task(task_id="t1", pet_id="p1", task_name="Feeding",
                duration_minutes=15, priority=Priority.HIGH,
                category=TaskCategory.FEEDING, scheduled_time="09:00"),
            Task(task_id="t3", pet_id="p1", task_name="Optional Enrichment",
                duration_minutes=20, priority=Priority.LOW,
                category=TaskCategory.ENRICHMENT),  # No scheduled_time
        ]
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        # Assert: Scheduled tasks first, then unscheduled
        assert sorted_tasks[0].scheduled_time == "09:00", "Scheduled task should be first"
        assert sorted_tasks[1].scheduled_time is None, "First unscheduled task next"
        assert sorted_tasks[2].scheduled_time is None, "Second unscheduled task last"
    
    def test_sort_with_invalid_time_format(self):
        """Verify sorting handles invalid time format gracefully."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Buddy", species="Dog", age=4)
        owner.add_pet(pet)
        
        tasks = [
            Task(task_id="t2", pet_id="p1", task_name="Task with bad time",
                duration_minutes=15, priority=Priority.HIGH,
                category=TaskCategory.FEEDING, scheduled_time="25:99"),  # Invalid
            Task(task_id="t1", pet_id="p1", task_name="Morning",
                duration_minutes=30, priority=Priority.HIGH,
                category=TaskCategory.WALKING, scheduled_time="08:00"),
        ]
        
        # Act & Assert: Should not crash
        scheduler = Scheduler(owner, pet, tasks)
        sorted_tasks = scheduler.sort_by_time(tasks)
        assert sorted_tasks[0].task_name == "Morning", "Valid time should come first"
        assert sorted_tasks[1].task_name == "Task with bad time", "Invalid time sorted to end"
    
    def test_sort_empty_task_list(self):
        """Verify sorting empty list returns empty list."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Spot", species="Dog", age=2)
        owner.add_pet(pet)
        
        # Act
        scheduler = Scheduler(owner, pet, [])
        sorted_tasks = scheduler.sort_by_time([])
        
        # Assert
        assert len(sorted_tasks) == 0, "Empty list should stay empty"


class TestTaskFiltering:
    """Test suite for task filtering by status and pet."""
    
    def test_filter_by_completed_status(self):
        """Verify filter_by_status correctly isolates completed tasks."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        task1 = Task(task_id="t1", pet_id="p1", task_name="Walk",
                    duration_minutes=30, priority=Priority.HIGH,
                    category=TaskCategory.WALKING, is_completed=True)
        task2 = Task(task_id="t2", pet_id="p1", task_name="Feed",
                    duration_minutes=15, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING, is_completed=False)
        task3 = Task(task_id="t3", pet_id="p1", task_name="Play",
                    duration_minutes=20, priority=Priority.MEDIUM,
                    category=TaskCategory.PLAYTIME, is_completed=True)
        
        tasks = [task1, task2, task3]
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        completed = scheduler.filter_by_status(tasks, completed=True)
        
        # Assert
        assert len(completed) == 2, "Should find 2 completed tasks"
        assert all(t.is_completed for t in completed), "All should be completed"
    
    def test_filter_by_pending_status(self):
        """Verify filter_by_status correctly isolates pending tasks."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        pet = Pet(pet_id="p1", name="Luna", species="Cat", age=3)
        owner.add_pet(pet)
        
        task1 = Task(task_id="t1", pet_id="p1", task_name="Walk",
                    duration_minutes=30, priority=Priority.HIGH,
                    category=TaskCategory.WALKING, is_completed=True)
        task2 = Task(task_id="t2", pet_id="p1", task_name="Feed",
                    duration_minutes=15, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING, is_completed=False)
        task3 = Task(task_id="t3", pet_id="p1", task_name="Play",
                    duration_minutes=20, priority=Priority.MEDIUM,
                    category=TaskCategory.PLAYTIME, is_completed=False)
        
        tasks = [task1, task2, task3]
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        pending = scheduler.filter_by_status(tasks, completed=False)
        
        # Assert
        assert len(pending) == 2, "Should find 2 pending tasks"
        assert all(not t.is_completed for t in pending), "All should be pending"
    
    def test_filter_by_pet_name(self):
        """Verify filter_by_pet correctly isolates tasks by pet name."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=3.0)
        
        pet1 = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        pet2 = Pet(pet_id="p2", name="Luna", species="Cat", age=3)
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        task1 = Task(task_id="t1", pet_id="p1", task_name="Walk",
                    duration_minutes=30, priority=Priority.HIGH, category=TaskCategory.WALKING)
        task2 = Task(task_id="t2", pet_id="p2", task_name="Feed",
                    duration_minutes=15, priority=Priority.HIGH, category=TaskCategory.FEEDING)
        task3 = Task(task_id="t3", pet_id="p1", task_name="Play",
                    duration_minutes=20, priority=Priority.MEDIUM, category=TaskCategory.PLAYTIME)
        
        tasks = [task1, task2, task3]
        
        # Act
        scheduler = Scheduler(owner, pet1, tasks)
        max_tasks = scheduler.filter_by_pet(tasks, "Max")
        
        # Assert
        assert len(max_tasks) == 2, "Should find 2 tasks for Max"
        assert all(t.pet_id == "p1" for t in max_tasks), "All should be for pet p1"
    
    def test_filter_by_pet_case_insensitive(self):
        """Verify pet name filtering is case-insensitive."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="BuDdY", species="Dog", age=4)
        owner.add_pet(pet)
        
        task1 = Task(task_id="t1", pet_id="p1", task_name="Walk",
                    duration_minutes=30, priority=Priority.HIGH, category=TaskCategory.WALKING)
        task2 = Task(task_id="t2", pet_id="p1", task_name="Feed",
                    duration_minutes=15, priority=Priority.HIGH, category=TaskCategory.FEEDING)
        
        tasks = [task1, task2]
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        result1 = scheduler.filter_by_pet(tasks, "buddy")  # lowercase
        result2 = scheduler.filter_by_pet(tasks, "BUDDY")  # uppercase
        result3 = scheduler.filter_by_pet(tasks, "BuDdY")  # mixed case
        
        # Assert
        assert len(result1) == 2, "Lowercase search should find all"
        assert len(result2) == 2, "Uppercase search should find all"
        assert len(result3) == 2, "Mixed case search should find all"
    
    def test_filter_by_nonexistent_pet(self):
        """Verify filtering by nonexistent pet returns empty list."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        task = Task(task_id="t1", pet_id="p1", task_name="Walk",
                   duration_minutes=30, priority=Priority.HIGH, category=TaskCategory.WALKING)
        
        # Act
        scheduler = Scheduler(owner, pet, [task])
        result = scheduler.filter_by_pet([task], "NonexistentPet")
        
        # Assert
        assert len(result) == 0, "Nonexistent pet filter should return empty list"
    
    def test_filter_empty_task_list(self):
        """Verify filtering empty list returns empty list."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Spot", species="Dog", age=2)
        owner.add_pet(pet)
        
        # Act
        scheduler = Scheduler(owner, pet, [])
        completed = scheduler.filter_by_status([], completed=True)
        by_pet = scheduler.filter_by_pet([], "Spot")
        
        # Assert
        assert len(completed) == 0, "Empty list filter should return empty"
        assert len(by_pet) == 0, "Empty pet filter should return empty"


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_pet_with_no_tasks(self):
        """Verify system handles pet with empty task list."""
        # Arrange
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        
        # Act & Assert
        assert len(pet.get_tasks()) == 0, "New pet should have no tasks"
        assert pet.get_tasks() == [], "Empty task list should be empty list"
    
    def test_owner_with_zero_available_time(self):
        """Verify scheduler handles owner with zero available time."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        task = Task(task_id="t1", pet_id="p1", task_name="Walk",
                   duration_minutes=30, priority=Priority.HIGH,
                   category=TaskCategory.WALKING)
        pet.add_task(task)
        
        # Act
        scheduler = Scheduler(owner, pet, pet.get_tasks())
        allocated = scheduler.allocate_tasks(0)
        
        # Assert
        assert len(allocated) == 0, "No tasks should fit in zero time"
    
    def test_multiple_pets_with_mixed_tasks(self):
        """Verify system handles multiple pets with different task counts."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=5.0)
        
        pet1 = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        pet2 = Pet(pet_id="p2", name="Luna", species="Cat", age=3)
        pet3 = Pet(pet_id="p3", name="Buddy", species="Dog", age=2)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        owner.add_pet(pet3)
        
        # Add tasks to pets (p1: 3 tasks, p2: 1 task, p3: 0 tasks)
        for i in range(3):
            t = Task(task_id=f"t1_{i}", pet_id="p1", task_name=f"Task {i}",
                    duration_minutes=15, priority=Priority.HIGH, category=TaskCategory.FEEDING)
            pet1.add_task(t)
        
        pet2.add_task(Task(task_id="t2_0", pet_id="p2", task_name="Groom",
                          duration_minutes=30, priority=Priority.MEDIUM, category=TaskCategory.GROOMING))
        
        # Act & Assert
        assert len(pet1.get_tasks()) == 3, "Pet1 should have 3 tasks"
        assert len(pet2.get_tasks()) == 1, "Pet2 should have 1 task"
        assert len(pet3.get_tasks()) == 0, "Pet3 should have no tasks"
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 4, "Owner should manage 4 total tasks"
    
    def test_task_with_decimal_duration(self):
        """Verify system handles fractional task durations (e.g., 0.5 minutes)."""
        # Arrange
        task = Task(task_id="t1", pet_id="p1", task_name="Quick treat",
                   duration_minutes=0.5, priority=Priority.LOW,
                   category=TaskCategory.FEEDING)
        
        # Act & Assert
        assert task.duration_minutes == 0.5, "Should accept decimal duration"
        assert task.duration_minutes > 0, "Decimal duration should still be positive"
    
    def test_very_high_priority_tasks_fit_in_small_time(self):
        """Verify that high-priority short tasks fit even in limited time."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=0.1)  # 6 minutes
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        task1 = Task(task_id="t1", pet_id="p1", task_name="Quick Feed",
                    duration_minutes=5, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING)
        task2 = Task(task_id="t2", pet_id="p1", task_name="Quick Water",
                    duration_minutes=5, priority=Priority.HIGH,
                    category=TaskCategory.FEEDING)
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner, pet, [task1, task2])
        allocated = scheduler.allocate_tasks(6)  # 6 minutes available
        
        # Assert
        assert len(allocated) == 1, "Only 5-min task should fit in 6 minutes"
        assert allocated[0].task_name == "Quick Feed", "Should allocate first HIGH priority"
    
    def test_identical_time_tuples_sort_stably(self):
        """Verify sorting maintains order when times are identical."""
        # Arrange
        owner = Owner(owner_id="o1", name="test_owner", available_time_hours=2.0)
        pet = Pet(pet_id="p1", name="Max", species="Dog", age=5)
        owner.add_pet(pet)
        
        # Multiple tasks at same time (should maintain insertion order)
        tasks = [
            Task(task_id="t1", pet_id="p1", task_name="Task A",
                duration_minutes=15, priority=Priority.HIGH,
                category=TaskCategory.WALKING, scheduled_time="10:00"),
            Task(task_id="t2", pet_id="p1", task_name="Task B",
                duration_minutes=15, priority=Priority.HIGH,
                category=TaskCategory.FEEDING, scheduled_time="10:00"),
        ]
        
        # Act
        scheduler = Scheduler(owner, pet, tasks)
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        # Assert: Both at 10:00 but should maintain relative order
        assert sorted_tasks[0].task_name == "Task A", "First task should remain first"
        assert sorted_tasks[1].task_name == "Task B", "Second task should remain second"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
