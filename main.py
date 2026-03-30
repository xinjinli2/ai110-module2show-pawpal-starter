"""
PawPal+ Main Application
Demonstrates the pet care scheduling system in action.
"""

from pawpal_system import Pet, Task, Owner, Scheduler, Priority, TaskCategory
from datetime import date

def main():
    print("\n" + "="*70)
    print("🐾 PAWPAL+ PET CARE SCHEDULER 🐾".center(70))
    print("="*70)
    
    # Create an owner
    owner = Owner(
        owner_id="owner_001",
        name="Sarah Johnson",
        available_time_hours=3.5,
        care_preferences="Morning routine preferred, avoid medication after 6 PM"
    )
    
    # Create first pet: Dog named Max
    max_dog = Pet(
        pet_id="pet_001",
        name="Max",
        species="Golden Retriever",
        age=5,
        special_care_notes="Very energetic, needs lots of exercise. Allergic to chicken."
    )
    
    # Create second pet: Cat named Luna
    luna_cat = Pet(
        pet_id="pet_002",
        name="Luna",
        species="Siamese Cat",
        age=3,
        special_care_notes="Indoor cat, needs playtime. Takes medication twice daily."
    )
    
    # Add pets to owner
    owner.add_pet(max_dog)
    owner.add_pet(luna_cat)
    
    # Create tasks for Max (Dog) - DELIBERATELY OUT OF CHRONOLOGICAL ORDER + CONFLICTS
    max_tasks = [
        Task(
            task_id="t001",
            pet_id="pet_001",
            task_name="Afternoon Walk",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            category=TaskCategory.WALKING,
            scheduled_time="15:00"
        ),
        Task(
            task_id="t002",
            pet_id="pet_001",
            task_name="Breakfast",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            scheduled_time="08:15"
        ),
        Task(
            task_id="t003",
            pet_id="pet_001",
            task_name="Dinner",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            scheduled_time="18:30"
        ),
        Task(
            task_id="t004",
            pet_id="pet_001",
            task_name="Playtime & Training",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            category=TaskCategory.PLAYTIME,
            scheduled_time="14:00"
        ),
        Task(
            task_id="t005",
            pet_id="pet_001",
            task_name="Morning Walk",
            duration_minutes=45,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING,
            scheduled_time="07:00"
        ),
    ]
    
    # Create tasks for Luna (Cat) - DELIBERATELY OUT OF CHRONOLOGICAL ORDER + CONFLICTS
    luna_tasks = [
        Task(
            task_id="t006",
            pet_id="pet_002",
            task_name="Evening Medication",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.MEDICATION,
            scheduled_time="19:00"
        ),
        Task(
            task_id="t007",
            pet_id="pet_002",
            task_name="Breakfast",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            scheduled_time="08:00"
        ),
        Task(
            task_id="t008",
            pet_id="pet_002",
            task_name="Grooming/Nail Trim",
            duration_minutes=25,
            priority=Priority.LOW,
            category=TaskCategory.GROOMING,
            scheduled_time="17:00"
        ),
        Task(
            task_id="t009",
            pet_id="pet_002",
            task_name="Morning Medication",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.MEDICATION,
            scheduled_time="07:30"
        ),
        Task(
            task_id="t010",
            pet_id="pet_002",
            task_name="Interactive Playtime",
            duration_minutes=20,
            priority=Priority.MEDIUM,
            category=TaskCategory.PLAYTIME,
            scheduled_time="14:30"
        ),
        Task(
            task_id="t011",
            pet_id="pet_002",
            task_name="Dinner",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING,
            scheduled_time="18:00"
        ),
        # CONFLICT #1: Same time as Max's Afternoon Walk (15:00)
        Task(
            task_id="t012",
            pet_id="pet_002",
            task_name="Luna Afternoon Snack",
            duration_minutes=5,
            priority=Priority.MEDIUM,
            category=TaskCategory.FEEDING,
            scheduled_time="15:00"  # CONFLICT with Max's Afternoon Walk t001 at 15:00
        ),
    ]
    
    # Add a cross-pet conflict: both pets have tasks at the same time (18:00)
    # Max already has dinner at 18:30, but we'll add one at 18:00
    max_tasks.append(Task(
        task_id="t013",
        pet_id="pet_001",
        task_name="Max Evening Playtime",
        duration_minutes=10,
        priority=Priority.LOW,
        category=TaskCategory.PLAYTIME,
        scheduled_time="18:00"  # Max task at 18:00
    ))
    
    # Luna has a task at 18:00 (Dinner from t011)
    # This will create CONFLICT #2: Both pets have tasks at 18:00
    
    # Add tasks to pets
    for task in max_tasks:
        max_dog.add_task(task)
    
    for task in luna_tasks:
        luna_cat.add_task(task)
    
    # Mark some tasks as completed for filtering demo
    luna_tasks[1].mark_complete()  # Luna's breakfast
    max_tasks[1].mark_complete()   # Max's breakfast
    
    # Display owner information
    print("\n📋 OWNER PROFILE:")
    print("-" * 70)
    print(owner.display_info())
    
    # Display pets and their tasks
    print("\n🐕 PET #1 - MAX (Dog):")
    print("-" * 70)
    print(max_dog.display_info())
    print("\nTasks (in order added - OUT OF CHRONOLOGICAL ORDER):")
    for i, task in enumerate(max_dog.get_tasks(), 1):
        print(f"  {i}. {task.display_task()}")
    
    print("\n🐱 PET #2 - LUNA (Cat):")
    print("-" * 70)
    print(luna_cat.display_info())
    print("\nTasks (in order added - OUT OF CHRONOLOGICAL ORDER):")
    for i, task in enumerate(luna_cat.get_tasks(), 1):
        print(f"  {i}. {task.display_task()}")
    
    # ========================================================================
    # CONFLICT DETECTION - LIGHTWEIGHT WARNING SYSTEM
    # ========================================================================
    print("\n" + "="*70)
    print("🔍 CONFLICT DETECTION - LIGHTWEIGHT WARNING SYSTEM".center(70))
    print("="*70)
    
    # Create a scheduler to detect conflicts
    scheduler_detector = Scheduler(owner, max_dog, max_dog.get_tasks())
    
    # Get ALL tasks from all pets to check for conflicts
    all_owner_tasks = owner.get_all_tasks()
    
    print(f"\n✅ Scanning {len(all_owner_tasks)} tasks for time conflicts...")
    print("-" * 70)
    
    # Detect conflicts (lightweight - just returns warnings, doesn't crash)
    conflicts = scheduler_detector.detect_time_conflicts(all_owner_tasks)
    
    if conflicts:
        print(f"\n⚠️  CONFLICTS DETECTED ({len(conflicts)} conflict(s)):\n")
        for i, warning in enumerate(conflicts, 1):
            print(f"   {i}. {warning}\n")
    else:
        print(f"\n✓ No time conflicts detected!")
    
    print(f"\n📊 Conflict Summary:")
    print(f"   • Total warnings: {len(scheduler_detector.get_conflict_warnings())}")
    print(f"   • Has conflicts: {scheduler_detector.has_conflicts()}")
    print(f"   • Program status: ✓ RUNNING (non-crashing design)")
    
    print("\n💡 Lightweight Conflict Detection:")
    print("   • Time complexity: O(n)")
    print("   • Groups tasks by scheduled_time using a dictionary")
    print("   • Returns friendly warning messages")
    print("   • No exceptions or program crashes")
    print("   • Warnings stored in scheduler for later retrieval")
    
    # ========================================================================
    # FEATURE 1: SORT BY TIME
    # ========================================================================
    print("\n" + "="*70)
    print("✨ FEATURE 1: SORTING TASKS BY TIME (NEW!)".center(70))
    print("="*70)
    
    # Create a scheduler to access sorting methods
    scheduler_max = Scheduler(owner, max_dog, max_dog.get_tasks())
    
    print("\n📅 MAX'S TASKS - SORTED BY SCHEDULED TIME:")
    print("-" * 70)
    max_sorted_by_time = scheduler_max.sort_by_time(max_dog.get_tasks())
    
    for i, task in enumerate(max_sorted_by_time, 1):
        time_display = task.scheduled_time if task.scheduled_time else "[Not scheduled]"
        status = "✓" if task.is_completed else "○"
        print(f"{i}. {time_display:12} | [{status}] {task.task_name:30} | {task.duration_minutes:2.0f} min")
    
    print("\n💡 How it works:")
    print("   Lambda converts 'HH:MM' → (hours, minutes) tuples")
    print("   sorted(tasks, key=lambda task: time_to_tuple(task.scheduled_time))")
    print("   Unscheduled tasks float to end")
    
    # ========================================================================
    # NEW FEATURE 2: FILTER BY STATUS
    # ========================================================================
    print("\n" + "="*70)
    print("✨ FEATURE 2: FILTERING BY COMPLETION STATUS (NEW!)".center(70))
    print("="*70)
    
    all_tasks = owner.get_all_tasks()
    
    print("\n✅ ALL PENDING TASKS (not completed):")
    print("-" * 70)
    pending_tasks = scheduler_max.filter_by_status(all_tasks, completed=False)
    for i, task in enumerate(pending_tasks, 1):
        pet_info = "Max" if task.pet_id == "pet_001" else "Luna"
        print(f"{i}. {task.task_name:30} ({pet_info}) - {task.priority.name} priority")
    
    print(f"\n⏳ Pending count: {len(pending_tasks)}")
    
    print("\n✓ ALL COMPLETED TASKS:")
    print("-" * 70)
    completed_tasks = scheduler_max.filter_by_status(all_tasks, completed=True)
    for i, task in enumerate(completed_tasks, 1):
        pet_info = "Max" if task.pet_id == "pet_001" else "Luna"
        print(f"{i}. {task.task_name:30} ({pet_info}) ✓")
    
    print(f"\n✓ Completed count: {len(completed_tasks)}")
    
    print("\n💡 How it works:")
    print("   return [t for t in tasks if t.is_completed == completed]")
    print("   Simple list comprehension for efficient filtering")
    
    # ========================================================================
    # NEW FEATURE 3: FILTER BY PET NAME
    # ========================================================================
    print("\n" + "="*70)
    print("✨ FEATURE 3: FILTERING BY PET NAME (NEW!)".center(70))
    print("="*70)
    
    print("\n🐕 MAX'S TASKS (filtered by name):")
    print("-" * 70)
    max_filtered = scheduler_max.filter_by_pet(all_tasks, "Max")
    for i, task in enumerate(max_filtered, 1):
        status = "✓" if task.is_completed else "○"
        print(f"{i}. [{status}] {task.task_name:30} - {task.priority.name:6} - {task.duration_minutes:2.0f} min")
    
    print("\n🐱 LUNA'S TASKS (filtered by name):")
    print("-" * 70)
    luna_filtered = scheduler_max.filter_by_pet(all_tasks, "Luna")
    for i, task in enumerate(luna_filtered, 1):
        status = "✓" if task.is_completed else "○"
        print(f"{i}. [{status}] {task.task_name:30} - {task.priority.name:6} - {task.duration_minutes:2.0f} min")
    
    print("\n💡 How it works:")
    print("   1. Find pet IDs matching the given name (case-insensitive)")
    print("   2. Return tasks whose pet_id is in that list")
    
    # ========================================================================
    # COMBINED: FILTER + SORT (Powerful!)
    # ========================================================================
    print("\n" + "="*70)
    print("🎯 COMBINED: MAX'S PENDING TASKS SORTED BY TIME".center(70))
    print("="*70)
    
    print("\n📋 MAX'S DAILY SCHEDULE (pending tasks only, chronologically ordered):")
    print("-" * 70)
    
    # Chain the methods together!
    max_pending = scheduler_max.filter_by_pet(all_tasks, "Max")
    max_pending = scheduler_max.filter_by_status(max_pending, completed=False)
    max_pending_sorted = scheduler_max.sort_by_time(max_pending)
    
    total_minutes = 0
    for i, task in enumerate(max_pending_sorted, 1):
        time_display = task.scheduled_time if task.scheduled_time else "[Flexible]"
        print(f"{i}. {time_display:12} | {task.task_name:30} | {task.duration_minutes:2.0f} min")
        total_minutes += task.duration_minutes
    
    print(f"\n📊 Total time for Max's pending tasks: {total_minutes} min ({total_minutes/60:.1f} hours)")
    
    # ========================================================================
    # COMBINED: LUNA'S PENDING TASKS SORTED BY TIME
    # ========================================================================
    print("\n" + "="*70)
    print("🎯 COMBINED: LUNA'S PENDING TASKS SORTED BY TIME".center(70))
    print("="*70)
    
    print("\n📋 LUNA'S DAILY SCHEDULE (pending tasks only, chronologically ordered):")
    print("-" * 70)
    
    # Create a scheduler for Luna to access her specific scheduling context
    scheduler_luna = Scheduler(owner, luna_cat, luna_cat.get_tasks())
    
    # Chain the methods together!
    luna_pending = scheduler_luna.filter_by_pet(all_tasks, "Luna")
    luna_pending = scheduler_luna.filter_by_status(luna_pending, completed=False)
    luna_pending_sorted = scheduler_luna.sort_by_time(luna_pending)
    
    total_minutes_luna = 0
    for i, task in enumerate(luna_pending_sorted, 1):
        time_display = task.scheduled_time if task.scheduled_time else "[Flexible]"
        print(f"{i}. {time_display:12} | {task.task_name:30} | {task.duration_minutes:2.0f} min")
        total_minutes_luna += task.duration_minutes
    
    print(f"\n📊 Total time for Luna's pending tasks: {total_minutes_luna} min ({total_minutes_luna/60:.1f} hours)")
    
    # ========================================================================
    # GENERATE DAILY SCHEDULES (Original functionality)
    # ========================================================================
    print("\n" + "="*70)
    print("TODAY'S OPTIMIZED SCHEDULE (using Scheduler algorithm)".center(70))
    print("="*70)
    
    # Schedule for Max
    print("\n🐕 MAX'S OPTIMIZED DAILY SCHEDULE:")
    print("-" * 70)
    plan_max = scheduler_max.generate_daily_plan("plan_max_001")
    print(plan_max.present_plan())
    
    # Schedule for Luna
    print("\n🐱 LUNA'S OPTIMIZED DAILY SCHEDULE:")
    print("-" * 70)
    plan_luna = scheduler_luna.generate_daily_plan("plan_luna_001")
    print(plan_luna.present_plan())
    
    # Combined summary
    print("\n📊 COMBINED DAILY SUMMARY:")
    print("-" * 70)
    total_max_time = plan_max.total_scheduled_time
    total_luna_time = plan_luna.total_scheduled_time
    total_combined = total_max_time + total_luna_time
    
    print(f"Max's scheduled time:   {total_max_time:>3.0f} minutes ({total_max_time/60:.1f} hours)")
    print(f"Luna's scheduled time:  {total_luna_time:>3.0f} minutes ({total_luna_time/60:.1f} hours)")
    print(f"Combined time needed:   {total_combined:>3.0f} minutes ({total_combined/60:.1f} hours)")
    print(f"Owner's available time: {owner.get_available_time()*60:>3.0f} minutes ({owner.get_available_time():.1f} hours)")
    
    available_in_minutes = owner.get_available_time() * 60
    if total_combined <= available_in_minutes:
        margin = available_in_minutes - total_combined
        print(f"✓ All tasks scheduled! Buffer: {margin:.0f} minutes ({margin/60:.1f} hours)")
    else:
        shortage = total_combined - available_in_minutes
        print(f"⚠ Not enough time! Shortage: {shortage:.0f} minutes ({shortage/60:.1f} hours)")
    
    print("\n" + "="*70)
    print("Schedule generation complete!".center(70))
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
