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
    
    # Create tasks for Max (Dog)
    max_tasks = [
        Task(
            task_id="t001",
            pet_id="pet_001",
            task_name="Morning Walk",
            duration_minutes=45,
            priority=Priority.HIGH,
            category=TaskCategory.WALKING
        ),
        Task(
            task_id="t002",
            pet_id="pet_001",
            task_name="Breakfast",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING
        ),
        Task(
            task_id="t003",
            pet_id="pet_001",
            task_name="Playtime & Training",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            category=TaskCategory.PLAYTIME
        ),
        Task(
            task_id="t004",
            pet_id="pet_001",
            task_name="Afternoon Walk",
            duration_minutes=30,
            priority=Priority.MEDIUM,
            category=TaskCategory.WALKING
        ),
        Task(
            task_id="t005",
            pet_id="pet_001",
            task_name="Dinner",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING
        ),
    ]
    
    # Create tasks for Luna (Cat)
    luna_tasks = [
        Task(
            task_id="t006",
            pet_id="pet_002",
            task_name="Morning Medication",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.MEDICATION
        ),
        Task(
            task_id="t007",
            pet_id="pet_002",
            task_name="Breakfast",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING
        ),
        Task(
            task_id="t008",
            pet_id="pet_002",
            task_name="Interactive Playtime",
            duration_minutes=20,
            priority=Priority.MEDIUM,
            category=TaskCategory.PLAYTIME
        ),
        Task(
            task_id="t009",
            pet_id="pet_002",
            task_name="Evening Medication",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.MEDICATION
        ),
        Task(
            task_id="t010",
            pet_id="pet_002",
            task_name="Dinner",
            duration_minutes=10,
            priority=Priority.HIGH,
            category=TaskCategory.FEEDING
        ),
        Task(
            task_id="t011",
            pet_id="pet_002",
            task_name="Grooming/Nail Trim",
            duration_minutes=25,
            priority=Priority.LOW,
            category=TaskCategory.GROOMING
        ),
    ]
    
    # Add tasks to pets
    for task in max_tasks:
        max_dog.add_task(task)
    
    for task in luna_tasks:
        luna_cat.add_task(task)
    
    # Display owner information
    print("\n📋 OWNER PROFILE:")
    print("-" * 70)
    print(owner.display_info())
    
    # Display pets and their tasks
    print("\n🐕 PET #1 - MAX (Dog):")
    print("-" * 70)
    print(max_dog.display_info())
    print("\nTasks available:")
    for task in max_dog.get_tasks():
        print(f"  • {task.display_task()}")
    
    print("\n🐱 PET #2 - LUNA (Cat):")
    print("-" * 70)
    print(luna_cat.display_info())
    print("\nTasks available:")
    for task in luna_cat.get_tasks():
        print(f"  • {task.display_task()}")
    
    # Generate daily schedules using Scheduler
    print("\n" + "="*70)
    print("TODAY'S SCHEDULE".center(70))
    print("="*70)
    
    # Schedule for Max
    print("\n🐕 MAX'S DAILY SCHEDULE:")
    print("-" * 70)
    scheduler_max = Scheduler(owner, max_dog, max_dog.get_tasks())
    plan_max = scheduler_max.generate_daily_plan("plan_max_001")
    print(plan_max.present_plan())
    
    # Schedule for Luna
    print("\n🐱 LUNA'S DAILY SCHEDULE:")
    print("-" * 70)
    scheduler_luna = Scheduler(owner, luna_cat, luna_cat.get_tasks())
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
