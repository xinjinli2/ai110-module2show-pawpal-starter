"""
Recurring Task System Demo
Demonstrates the new recurring task functionality with automatic next-occurrence generation.

Features shown:
1. Creating recurring tasks (DAILY, WEEKLY, ONCE)
2. Using timedelta for date calculations
3. Marking recurring tasks complete → auto-generates next occurrence
4. Tracking task lineage with parent_task_id
5. Displaying recurring task metadata (due_date, last_completed_date)
"""

from pawpal_system import (
    Pet, Task, Owner, Scheduler, Priority, TaskCategory, 
    TaskFrequency, RecurringTaskManager
)
from datetime import date, timedelta


def main():
    print("\n" + "="*80)
    print("🔄 RECURRING TASK SYSTEM DEMO 🔄".center(80))
    print("="*80)
    
    # Create owner and pet
    owner = Owner(
        owner_id="owner_001",
        name="Sarah Johnson",
        available_time_hours=4.0,
        care_preferences="Morning routine preferred"
    )
    
    max_dog = Pet(
        pet_id="pet_001",
        name="Max",
        species="Golden Retriever",
        age=5,
        special_care_notes="Energetic, needs daily exercise"
    )
    
    owner.add_pet(max_dog)
    
    # ========================================================================
    # DEMO 1: CREATE RECURRING TASKS
    # ========================================================================
    print("\n" + "="*80)
    print("📋 DEMO 1: CREATING RECURRING TASKS".center(80))
    print("="*80)
    
    today = date.today()
    
    # Create daily tasks
    daily_walk = Task(
        task_id="t001",
        pet_id="pet_001",
        task_name="Morning Walk",
        duration_minutes=45,
        priority=Priority.HIGH,
        category=TaskCategory.WALKING,
        scheduled_time="07:00",
        frequency=TaskFrequency.DAILY,
        due_date=today
    )
    
    daily_meds = Task(
        task_id="t002",
        pet_id="pet_001",
        task_name="Medication",
        duration_minutes=5,
        priority=Priority.HIGH,
        category=TaskCategory.MEDICATION,
        scheduled_time="08:00",
        frequency=TaskFrequency.DAILY,
        due_date=today
    )
    
    # Create a weekly task
    weekly_grooming = Task(
        task_id="t003",
        pet_id="pet_001",
        task_name="Full Grooming",
        duration_minutes=60,
        priority=Priority.MEDIUM,
        category=TaskCategory.GROOMING,
        scheduled_time="14:00",
        frequency=TaskFrequency.WEEKLY,
        due_date=today
    )
    
    # Create a one-time task
    one_time_vet = Task(
        task_id="t004",
        pet_id="pet_001",
        task_name="Vet Appointment",
        duration_minutes=120,
        priority=Priority.HIGH,
        category=TaskCategory.OTHER,
        scheduled_time="10:00",
        frequency=TaskFrequency.ONCE,
        due_date=today
    )
    
    max_dog.add_task(daily_walk)
    max_dog.add_task(daily_meds)
    max_dog.add_task(weekly_grooming)
    max_dog.add_task(one_time_vet)
    
    print("\n✅ Created 4 tasks:\n")
    for task in max_dog.get_tasks():
        freq_tag = f"[{task.frequency.value.upper()}]" if task.frequency != TaskFrequency.ONCE else "[ONE-TIME]"
        print(f"  {task.task_id:5} | {freq_tag:10} | {task.task_name:20} | Due: {task.due_date}")
    
    # ========================================================================
    # DEMO 2: UNDERSTAND TIMEDELTA DATE CALCULATIONS
    # ========================================================================
    print("\n" + "="*80)
    print("📅 DEMO 2: TIMEDELTA DATE CALCULATIONS".center(80))
    print("="*80)
    
    print(f"\nToday's date: {today} ({today.strftime('%A')})")
    print("\nTimedelta calculations for next occurrences:")
    print("-" * 80)
    
    # Daily task: today + 1 day
    tomorrow = today + timedelta(days=1)
    print(f"\n  DAILY task (Morning Walk):")
    print(f"    today + timedelta(days=1)")
    print(f"    {today} → {tomorrow} ({tomorrow.strftime('%A')})")
    
    # Weekly task: today + 7 days
    next_week = today + timedelta(days=7)
    print(f"\n  WEEKLY task (Grooming):")
    print(f"    today + timedelta(days=7)")
    print(f"    {today} → {next_week} ({next_week.strftime('%A')})")
    
    # One-time task: doesn't recur
    print(f"\n  ONCE task (Vet Appointment):")
    print(f"    No recurrence - task does not repeat")
    
    # ========================================================================
    # DEMO 3: MARK RECURRING TASK COMPLETE → AUTO-GENERATE NEXT OCCURRENCE
    # ========================================================================
    print("\n" + "="*80)
    print("✨ DEMO 3: MARK COMPLETE & AUTO-GENERATE NEXT OCCURRENCE".center(80))
    print("="*80)
    
    print(f"\n🐕 Current tasks for {max_dog.name}:")
    print("-" * 80)
    for i, task in enumerate(max_dog.get_tasks(), 1):
        status = "✓ DONE" if task.is_completed else "○ PENDING"
        print(f"  {i}. [{status}] {task.task_name} ({task.frequency.value})")
    
    print(f"\n\n🎯 MARKING RECURRING TASK COMPLETE: '{daily_walk.task_name}'")
    print("-" * 80)
    
    # This triggers automatic next-occurrence generation!
    next_occurrence = RecurringTaskManager.handle_recurring_completion(
        daily_walk,
        max_dog,
        owner
    )
    
    print(f"\n✅ Task '{daily_walk.task_name}' marked complete!")
    print(f"   - Completion date recorded: {daily_walk.last_completed_date}")
    print(f"   - is_completed set to: {daily_walk.is_completed}")
    
    if next_occurrence:
        print(f"\n📅 NEW OCCURRENCE AUTO-GENERATED:")
        print(f"   - Task ID: {next_occurrence.task_id} (auto-incremented)")
        print(f"   - Name: {next_occurrence.task_name}")
        print(f"   - Due date: {next_occurrence.due_date} (tomorrow via timedelta)")
        print(f"   - Status: {next_occurrence.is_completed} (fresh, not complete)")
        print(f"   - Parent task: {next_occurrence.parent_task_id} (lineage tracking)")
    
    print(f"\n📊 Task count after completion:")
    print(f"   - Before: 4 tasks")
    print(f"   - After: {len(max_dog.get_tasks())} tasks (new occurrence added)")
    
    # ========================================================================
    # DEMO 4: DISPLAY UPDATED TASK LIST WITH NEW OCCURRENCE
    # ========================================================================
    print("\n" + "="*80)
    print("📋 DEMO 4: UPDATED TASK LIST WITH NEW OCCURRENCE".center(80))
    print("="*80)
    
    print(f"\n🐕 Current tasks for {max_dog.name}:")
    print("-" * 80)
    for i, task in enumerate(max_dog.get_tasks(), 1):
        status = "✓ DONE" if task.is_completed else "○ PENDING"
        lineage = f" (child of {task.parent_task_id})" if task.parent_task_id else " (original)"
        print(f"  {i}. [{status}] {task.task_name:20} | Due: {task.due_date} | Freq: {task.frequency.value:6}{lineage}")
    
    # ========================================================================
    # DEMO 5: MARK ANOTHER RECURRING TASK - ONE-TIME DOESN'T GENERATE
    # ========================================================================
    print("\n" + "="*80)
    print("🎯 DEMO 5: ONE-TIME TASK COMPLETION (NO RECURRENCE)".center(80))
    print("="*80)
    
    print(f"\n⚠️  Completing ONE-TIME task: '{one_time_vet.task_name}'")
    print("-" * 80)
    
    result = RecurringTaskManager.handle_recurring_completion(
        one_time_vet,
        max_dog,
        owner
    )
    
    print(f"\n✅ Task '{one_time_vet.task_name}' marked complete!")
    print(f"   - Last completed: {one_time_vet.last_completed_date}")
    print(f"   - Frequency: {one_time_vet.frequency.value}")
    
    if result is None:
        print(f"\n❌ No new occurrence generated (one-time task)")
        print(f"   Task count: {len(max_dog.get_tasks())} (unchanged)")
    
    # ========================================================================
    # DEMO 6: FILTER AND DISPLAY RECURRING TASKS INTELLIGENTLY
    # ========================================================================
    print("\n" + "="*80)
    print("🔍 DEMO 6: FILTERING RECURRING TASKS BY STATUS & RECURRENCE".center(80))
    print("="*80)
    
    all_tasks = max_dog.get_tasks()
    
    print(f"\n📊 Task Breakdown:")
    print("-" * 80)
    
    pending = [t for t in all_tasks if not t.is_completed]
    completed = [t for t in all_tasks if t.is_completed]
    recurring = [t for t in all_tasks if t.frequency != TaskFrequency.ONCE]
    
    print(f"\n  Total tasks: {len(all_tasks)}")
    print(f"  Pending: {len(pending)}")
    print(f"  Completed: {len(completed)}")
    print(f"  Recurring (DAILY/WEEKLY): {len(recurring)}")
    
    print(f"\n✅ PENDING RECURRING TASKS:")
    for task in [t for t in pending if t.frequency != TaskFrequency.ONCE]:
        print(f"  - {task.task_name} [{task.frequency.value}] due {task.due_date}")
    
    print(f"\n✓ COMPLETED TASKS:")
    for task in completed:
        print(f"  - {task.task_name} (completed on {task.last_completed_date})")
    
    # ========================================================================
    # DEMO 7: USE OWNER'S NEW METHOD FOR DATE-BASED FILTERING
    # ========================================================================
    print("\n" + "="*80)
    print("📆 DEMO 7: GET TASKS DUE ON SPECIFIC DATE".center(80))
    print("="*80)
    
    target_date = today
    due_tasks = owner.get_pending_tasks_for_date(target_date)
    
    print(f"\n📅 Tasks due on {target_date} (today):")
    print("-" * 80)
    for task in due_tasks:
        print(f"  - {task.task_name:20} | Due: {task.due_date} | {task.frequency.value}")
    
    print(f"\n💡 This method filters by:")
    print(f"   1. Completed status (pending only)")
    print(f"   2. Due date (due_date <= {target_date})")
    print(f"   3. Supports advanced scheduling without explicit scheduling")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("🎉 SUMMARY: RECURRING TASK SYSTEM KEY FEATURES".center(80))
    print("="*80)
    
    print("""
✅ FEATURES DEMONSTRATED:

1. TASK FREQUENCY TYPES:
   • ONCE: Single completion (e.g., vet appointment)
   • DAILY: Repeats every day (e.g., morning walk)
   • WEEKLY: Repeats every 7 days (e.g., grooming)

2. AUTOMATIC NEXT-OCCURRENCE GENERATION:
   • RecurringTaskManager.handle_recurring_completion()
   • Creates new Task instance with incremented ID
   • Tracks parent_task_id for lineage
   • Automatically added to pet's task list

3. TIMEDELTA DATE CALCULATIONS:
   • DAILY: next_date = today + timedelta(days=1)
   • WEEKLY: next_date = today + timedelta(days=7)
   • Simple, readable, maintains day-of-week semantics

4. COMPLETION TRACKING:
   • last_completed_date: When task was last done
   • due_date: When task is next due
   • is_completed: Current status

5. SMART FILTERING:
   • Owner.get_pending_tasks_for_date(date)
   • Filters by completion status
   • Filters by due date
   • Perfect for daily schedule planning

6. LINEAGE TRACKING:
   • parent_task_id: Links recurring instances
   • Useful for UI to group related tasks
   • Enables "task family" history viewing

ALGORITHM SUMMARY:
  mark_complete() → last_completed_date = today, is_completed = True
  ↓
  check if frequency != ONCE
  ↓
  calculate next_due = today + timedelta(days=frequency_days)
  ↓
  create_next_occurrence() with new task_id
  ↓
  add to pet.tasks automatically
  """)
    
    print("\n" + "="*80)
    print("Demo complete!".center(80))
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
