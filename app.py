import streamlit as st
from datetime import date
from pawpal_system import Pet, Task, Owner, Scheduler, Priority, TaskCategory, TaskFrequency, RecurringTaskManager


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
# st.session_state acts like a dictionary. Check if objects exist before
# creating them. This way, they persist across page reruns.
# ============================================================================

def initialize_session_state():
    """Initialize Owner, Pet, and Tasks in session_state if they don't exist."""
    
    # Initialize owner if it doesn't exist
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(
            owner_id="owner_001",
            name="Pet Owner",
            available_time_hours=3.0,
            care_preferences=""
        )
    
    # Initialize pet if it doesn't exist
    if "pet" not in st.session_state:
        st.session_state.pet = Pet(
            pet_id="pet_001",
            name="Your Pet",
            species="dog",
            age=3,
            special_care_notes=""
        )
    
    # Add pet to owner if not already added
    if st.session_state.pet not in st.session_state.owner.get_pets():
        st.session_state.owner.add_pet(st.session_state.pet)
    
    # Initialize current_pet to track which pet is being managed
    if "current_pet" not in st.session_state:
        st.session_state.current_pet = st.session_state.owner.get_pets()[0] if st.session_state.owner.get_pets() else None
    
    # Initialize tasks list if it doesn't exist
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    
    # Initialize daily plan if it doesn't exist
    if "daily_plan" not in st.session_state:
        st.session_state.daily_plan = None
    
    # Initialize conflict warnings if they don't exist
    if "conflict_warnings" not in st.session_state:
        st.session_state.conflict_warnings = []

# Call initialization at app start
initialize_session_state()

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is your pet care planning assistant. It helps you schedule care tasks
for your pet(s) based on available time, priority, and preferences.

This app uses **Streamlit Session State** to persist your owner, pet, and task data
across page refreshes. Try it out below!
"""
)

# ============================================================================
# OWNER & PET SETUP
# ============================================================================
# DATA FLOW EXPLANATION:
# 1. User submits form (Owner.update_info or Pet.update_profile)
# 2. Method updates the object stored in session_state
# 3. Streamlit detects session_state change and reruns the app
# 4. Widgets read the updated values and display them
# ============================================================================

with st.expander("👤 Owner & Pet Management", expanded=True):
    
    # OWNER SETUP
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍👩‍👧 Owner Information")
        st.caption("Update your profile to get started")
        
        owner_name = st.text_input(
            "Owner Name",
            value=st.session_state.owner.name,
            key="owner_name_input"
        )
        
        available_time = st.slider(
            "Available Time (hours/day)",
            min_value=0.5,
            max_value=12.0,
            value=st.session_state.owner.available_time_hours,
            step=0.5,
            key="available_time_slider"
        )
        
        care_prefs = st.text_area(
            "Care Preferences (optional)",
            value=st.session_state.owner.care_preferences,
            placeholder="e.g., Prefer morning walks, avoid medication after 6 PM",
            key="care_prefs_input",
            height=80
        )
        
        # Call Owner.update_info() method when any field changes
        if st.button("💾 Save Owner Info", use_container_width=True):
            st.session_state.owner.update_info(
                name=owner_name,
                available_time=available_time,
                preferences=care_prefs
            )
            st.success("✓ Owner information updated!")
    
    # PET MANAGEMENT
    with col2:
        st.subheader("🐾 Your Pets")
        st.caption(f"You have {len(st.session_state.owner.get_pets())} pet(s)")
        
        # Select which pet to manage
        if st.session_state.owner.get_pets():
            pet_options = {pet.pet_id: f"{pet.name} ({pet.species})" for pet in st.session_state.owner.get_pets()}
            
            selected_pet_id = st.selectbox(
                "Select a pet to manage:",
                options=list(pet_options.keys()),
                format_func=lambda x: pet_options[x],
                key="pet_selector"
            )
            
            # Find the selected pet
            st.session_state.current_pet = next(
                (p for p in st.session_state.owner.get_pets() if p.pet_id == selected_pet_id),
                st.session_state.owner.get_pets()[0]
            )
        else:
            st.session_state.current_pet = None
        
        # Add new pet form
        st.markdown("#### ➕ Add a New Pet")
        with st.form(key="add_pet_form"):
            new_pet_name = st.text_input("Pet Name", placeholder="e.g., Buddy, Luna")
            new_pet_species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "hamster", "other"])
            new_pet_age = st.number_input("Age (years)", min_value=0, max_value=50, value=2)
            new_pet_notes = st.text_area("Special Care Notes (optional)", placeholder="Allergies, medications, special needs...")
            
            add_pet_submit = st.form_submit_button("Add Pet", use_container_width=True)
            
            # Call Owner.add_pet() method
            if add_pet_submit and new_pet_name:
                new_pet = Pet(
                    pet_id=f"pet_{len(st.session_state.owner.get_pets()) + 1}",
                    name=new_pet_name,
                    species=new_pet_species,
                    age=new_pet_age,
                    special_care_notes=new_pet_notes
                )
                st.session_state.owner.add_pet(new_pet)
                st.session_state.current_pet = new_pet
                st.success(f"✓ Added {new_pet_name}!")
                st.rerun()

# Show current pet details
if st.session_state.current_pet:
    st.divider()
    st.subheader(f"📋 Edit {st.session_state.current_pet.name}")
    
    col_pet1, col_pet2 = st.columns(2)
    
    with col_pet1:
        pet_name_edit = st.text_input(
            "Pet Name",
            value=st.session_state.current_pet.name,
            key="pet_name_edit"
        )
        
        pet_species_edit = st.selectbox(
            "Species",
            ["dog", "cat", "bird", "rabbit", "hamster", "other"],
            index=["dog", "cat", "bird", "rabbit", "hamster", "other"].index(st.session_state.current_pet.species),
            key="pet_species_edit"
        )
        
        pet_age_edit = st.number_input(
            "Age (years)",
            min_value=0,
            max_value=50,
            value=st.session_state.current_pet.age,
            key="pet_age_edit"
        )
    
    with col_pet2:
        pet_notes_edit = st.text_area(
            "Special Care Notes",
            value=st.session_state.current_pet.special_care_notes,
            key="pet_notes_edit",
            height=100
        )
    
    # Call Pet.update_profile() method
    if st.button("💾 Save Pet Info", use_container_width=True, key="save_pet_btn"):
        st.session_state.current_pet.update_profile(
            name=pet_name_edit,
            species=pet_species_edit,
            age=pet_age_edit,
            notes=pet_notes_edit
        )
        st.success("✓ Pet information updated!")
    
    # Display current pet info
    st.markdown(f"#### Pet Summary")
    st.info(st.session_state.current_pet.display_info())
else:
    st.warning("⚠️ Add a pet to get started!")

# ============================================================================
# TASK MANAGEMENT
# ============================================================================
# DATA FLOW: Add Task Form
# 1. User fills out form (task_name, duration, priority, category)
# 2. Click "Add Task" button
# 3. Form submit creates Task object by calling Task() constructor
# 4. Calls Pet.add_task(new_task) → updates st.session_state.current_pet.tasks
# 5. Calls st.session_state.tasks.append(new_task) → updates scheduler task list
# 6. st.rerun() triggers page rerun → widgets read updated values
# 7. UI displays new task in the table
# ============================================================================

st.divider()

if not st.session_state.current_pet:
    st.warning("⚠️ Please add a pet first to manage tasks.")
else:
    with st.expander("📝 Manage Tasks", expanded=True):
        st.write(f"**{st.session_state.current_pet.name}'s Tasks** — Total: {len(st.session_state.current_pet.get_tasks())}")
        
        # Add new task form
        with st.form(key="add_task_form", border=True):
            st.markdown("#### ➕ Add a New Task")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                task_name = st.text_input("Task Name", placeholder="e.g., Morning Walk")
            
            with col2:
                duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=30)
            
            with col3:
                priority = st.selectbox("Priority", [p.name for p in Priority])
            
            col4, col5 = st.columns(2)
            with col4:
                category = st.selectbox(
                    "Category",
                    [c.name for c in TaskCategory]
                )
            
            with col5:
                frequency = st.selectbox(
                    "Recurrence",
                    [f.value.capitalize() for f in TaskFrequency],
                    help="Once = single task, Daily = repeats daily, Weekly = repeats weekly"
                )
            
            submit = st.form_submit_button("➕ Add Task", use_container_width=True)
            
            # Form submission: Call Task() constructor and Pet.add_task()
            if submit and task_name:
                freq_map = {f.value.capitalize(): f for f in TaskFrequency}
                new_task = Task(
                    task_id=f"t{len(st.session_state.current_pet.get_tasks()) + 1}",
                    pet_id=st.session_state.current_pet.pet_id,
                    task_name=task_name,
                    duration_minutes=float(duration),
                    priority=Priority[priority],
                    category=TaskCategory[category],
                    is_completed=False,
                    frequency=freq_map[frequency],
                    due_date=date.today() if freq_map[frequency] != TaskFrequency.ONCE else None
                )
                # Call Pet.add_task() method to update pet's task list
                st.session_state.current_pet.add_task(new_task)
                # Also add to scheduler task list
                st.session_state.tasks.append(new_task)
                st.success(f"✓ Added task: {task_name} ({frequency})")
                st.rerun()
        
        # Display and manage existing tasks
        if st.session_state.current_pet.get_tasks():
            st.markdown("### Current Tasks")
            
            # Create a table view
            task_data = []
            for idx, task in enumerate(st.session_state.current_pet.get_tasks(), 1):
                task_data.append({
                    "ID": idx,
                    "Task": task.task_name,
                    "Duration (min)": int(task.duration_minutes),
                    "Priority": task.priority.name,
                    "Category": task.category.value,
                    "Status": "✓ Done" if task.is_completed else "⏳ Pending"
                })
            
            st.table(task_data)
            
            # Task detail view - show full info for each task
            st.markdown("### Task Details")
            selected_task_idx = st.selectbox(
                "Select a task to view details:",
                range(len(st.session_state.current_pet.get_tasks())),
                format_func=lambda i: f"{i+1}. {st.session_state.current_pet.get_tasks()[i].task_name}",
                key="task_details_select"
            )
            
            selected_task = st.session_state.current_pet.get_tasks()[selected_task_idx]
            st.info(selected_task.get_details())
            
            # Task management buttons
            col_manage1, col_manage2, col_manage3 = st.columns(3)
            
            with col_manage1:
                if st.button("✓ Mark Complete", use_container_width=True, key="mark_complete_btn"):
                    # Handle recurring task completion with auto-generation
                    next_task = RecurringTaskManager.handle_recurring_completion(
                        selected_task,
                        st.session_state.current_pet,
                        st.session_state.owner
                    )
                    
                    if next_task:
                        st.success(f"✓ {selected_task.task_name} marked complete!")
                        st.info(f"📅 Next occurrence created for {next_task.due_date} ({selected_task.frequency.value})")
                        st.session_state.tasks.append(next_task)
                    else:
                        st.success(f"✓ {selected_task.task_name} marked as complete!")
                    st.rerun()
            
            with col_manage2:
                if st.button("⏳ Mark Incomplete", use_container_width=True, key="mark_incomplete_btn"):
                    selected_task.mark_incomplete()
                    st.info(f"{selected_task.task_name} marked as incomplete.")
                    st.rerun()
            
            with col_manage3:
                if st.button("🗑️ Delete Task", use_container_width=True, key="delete_task_btn"):
                    task_to_delete_id = selected_task.task_id
                    st.session_state.current_pet.remove_task(task_to_delete_id)
                    st.session_state.tasks = [t for t in st.session_state.tasks if t.task_id != task_to_delete_id]
                    st.warning(f"Deleted: {selected_task.task_name}")
                    st.rerun()
        else:
            st.info("No tasks yet. Add one above to get started!")

# ============================================================================
# TASK VIEWING & FILTERING
# ============================================================================
# Use Scheduler methods to sort, filter, and display tasks professionally
# ============================================================================

if st.session_state.current_pet and len(st.session_state.current_pet.get_tasks()) > 0:
    st.divider()
    
    with st.expander("🔍 View & Filter Tasks", expanded=False):
        st.markdown("#### Task Organization & Analysis")
        
        # Create scheduler for filtering/sorting methods
        scheduler = Scheduler(
            st.session_state.owner,
            st.session_state.current_pet,
            st.session_state.current_pet.get_tasks()
        )
        
        # Filter options
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            filter_status = st.radio(
                "Filter by Status:",
                ["All", "Pending", "Completed"],
                horizontal=True,
                key="filter_status_radio"
            )
        
        with col_filter2:
            sort_option = st.selectbox(
                "Sort by:",
                ["Chronological (by time)", "Priority (HIGH → LOW)", "Duration (shortest first)"],
                key="sort_option_select"
            )
        
        # Apply filters
        tasks_to_display = st.session_state.current_pet.get_tasks()
        
        if filter_status == "Pending":
            tasks_to_display = scheduler.filter_by_status(tasks_to_display, completed=False)
        elif filter_status == "Completed":
            tasks_to_display = scheduler.filter_by_status(tasks_to_display, completed=True)
        
        # Apply sorting
        if sort_option == "Chronological (by time)":
            tasks_to_display = scheduler.sort_by_time(tasks_to_display)
        elif sort_option == "Priority (HIGH → LOW)":
            tasks_to_display = sorted(tasks_to_display, key=lambda t: -t.priority.value)
        elif sort_option == "Duration (shortest first)":
            tasks_to_display = sorted(tasks_to_display, key=lambda t: t.duration_minutes)
        
        # Display filtered/sorted tasks in a professional table
        if tasks_to_display:
            display_data = []
            for idx, task in enumerate(tasks_to_display, 1):
                time_str = task.scheduled_time if task.scheduled_time else "Unscheduled"
                status_icon = "✅" if task.is_completed else "⏳"
                due_date_str = task.due_date.strftime("%m/%d") if task.due_date else "—"
                
                display_data.append({
                    "#": idx,
                    "Status": status_icon,
                    "Task Name": task.task_name,
                    "Time": time_str,
                    "Duration (min)": int(task.duration_minutes),
                    "Priority": task.priority.name,
                    "Category": task.category.value,
                    "Recurrence": task.frequency.value,
                    "Due Date": due_date_str
                })
            
            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Status": st.column_config.TextColumn(width="small"),
                    "Priority": st.column_config.TextColumn(width="small"),
                    "Task Name": st.column_config.TextColumn(width="large"),
                }
            )
            
            # Show summary stats
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                pending_count = sum(1 for t in tasks_to_display if not t.is_completed)
                st.metric("Pending Tasks", pending_count, label_visibility="collapsed")
            
            with col_stat2:
                completed_count = sum(1 for t in tasks_to_display if t.is_completed)
                st.metric("Completed Tasks", completed_count, label_visibility="collapsed")
            
            with col_stat3:
                total_duration = sum(t.duration_minutes for t in tasks_to_display)
                st.metric("Total Duration", f"{total_duration}min", label_visibility="collapsed")
            
            with col_stat4:
                recurring_count = sum(1 for t in tasks_to_display if t.frequency.value != "once")
                st.metric("Recurring", recurring_count, label_visibility="collapsed")
        else:
            st.info(f"📭 No tasks match your filter criteria.")

# ============================================================================
# SCHEDULE GENERATION
# ============================================================================
# DATA FLOW: Generate Schedule
# 1. User clicks "Generate Schedule" button
# 2. Creates Scheduler object with (owner, pet, tasks)
# 3. Calls Scheduler.generate_daily_plan(plan_id)
# 4. Scheduler internally calls:
#    - prioritize_tasks() → sorts by priority & duration
#    - allocate_tasks() → fits tasks in available time
#    - create_explanation() → builds reasoning
# 5. Returns DailyPlan object stored in st.session_state.daily_plan
# 6. UI displays plan with metrics, tasks, and reasoning
# ============================================================================

st.divider()

if not st.session_state.current_pet:
    st.warning("⚠️ Please add a pet first to generate a schedule.")
elif len(st.session_state.current_pet.get_tasks()) == 0:
    st.warning("⚠️ Add at least one task before generating a schedule.")
else:
    with st.expander("📅 Generate Daily Schedule", expanded=True):
        st.write(
            f"Generate an optimized daily schedule for {st.session_state.current_pet.name} "
            f"based on {st.session_state.owner.name}'s available time "
            f"({st.session_state.owner.available_time_hours} hours/day)."
        )
        
        if st.button("🎯 Generate Schedule", use_container_width=True, type="primary"):
            # Create scheduler with current state objects
            scheduler = Scheduler(
                st.session_state.owner,
                st.session_state.current_pet,
                st.session_state.current_pet.get_tasks()
            )
            
            # CONFLICT DETECTION - Get warnings before generating plan
            all_owner_tasks = st.session_state.owner.get_all_tasks()
            conflict_warnings = scheduler.detect_time_conflicts(all_owner_tasks)
            
            # Call Scheduler.generate_daily_plan() method
            # This internally calls: prioritize_tasks(), allocate_tasks(), create_explanation()
            plan = scheduler.generate_daily_plan(f"plan_{st.session_state.current_pet.pet_id}_{date.today().isoformat()}")
            st.session_state.daily_plan = plan
            
            # Store conflict warnings in session state
            st.session_state.conflict_warnings = conflict_warnings
            
            st.success("✓ Schedule generated!")
            
            # Display any conflicts immediately
            if conflict_warnings:
                st.warning("⚠️ Time conflicts detected!")
                for warning in conflict_warnings:
                    st.warning(warning)

# Display the generated plan
if st.session_state.daily_plan:
    st.markdown("### 📋 Today's Optimized Schedule")
    
    plan = st.session_state.daily_plan
    scheduler = Scheduler(
        st.session_state.owner,
        st.session_state.current_pet,
        st.session_state.current_pet.get_tasks()
    )
    
    # Display conflict warnings if they exist
    if "conflict_warnings" in st.session_state and st.session_state.conflict_warnings:
        for warning_msg in st.session_state.conflict_warnings:
            st.warning(warning_msg)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Tasks Scheduled",
            len(plan.get_tasks()),
            f"of {len(st.session_state.current_pet.get_tasks())}"
        )
    with col2:
        st.metric(
            "Total Time",
            f"{plan.total_scheduled_time / 60:.1f} hrs",
            f"({int(plan.total_scheduled_time)} min)"
        )
    with col3:
        available = st.session_state.owner.available_time_hours * 60
        remaining = available - plan.total_scheduled_time
        status = "✓ Fits!" if remaining >= 0 else "⚠ Over!"
        st.metric(
            "Time Remaining",
            f"{remaining / 60:.1f} hrs",
            status
        )
    with col4:
        priority_high = sum(1 for t in plan.get_tasks() if t.priority.name == "HIGH")
        st.metric(
            "High Priority",
            priority_high,
            "tasks scheduled"
        )
    
    st.divider()
    
    # SORTED TASKS VIEW - Use sort_by_time() for chronological display
    st.markdown("#### ⏰ Tasks in Chronological Order")
    sorted_tasks = scheduler.sort_by_time(plan.get_tasks())
    
    if sorted_tasks:
        schedule_data = []
        for i, task in enumerate(sorted_tasks, 1):
            status = "✅ Done" if task.is_completed else "⏳ Pending"
            time_str = task.scheduled_time if task.scheduled_time else "Unscheduled"
            
            schedule_data.append({
                "#": i,
                "Task": task.task_name,
                "Time": time_str,
                "Duration": f"{int(task.duration_minutes)} min",
                "Priority": task.priority.name,
                "Category": task.category.value,
                "Status": status
            })
        
        st.dataframe(
            schedule_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority": st.column_config.TextColumn(width="small"),
                "Status": st.column_config.TextColumn(width="small"),
                "Task": st.column_config.TextColumn(width="large"),
            }
        )
    
    st.divider()
    
    # FILTERED VIEWS - Show different perspectives
    col_view1, col_view2 = st.columns(2)
    
    with col_view1:
        st.markdown("#### 🎯 High Priority Tasks")
        high_priority = scheduler.filter_by_status(
            [t for t in plan.get_tasks() if t.priority.name == "HIGH"],
            completed=False
        )
        if high_priority:
            for task in high_priority:
                st.success(f"✓ **{task.task_name}** ({task.duration_minutes} min)")
        else:
            st.info("No high-priority tasks scheduled today.")
    
    with col_view2:
        st.markdown("#### 📋 By Category")
        categories = {}
        for task in plan.get_tasks():
            cat = task.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(task)
        
        if categories:
            for category, tasks in sorted(categories.items()):
                st.write(f"**{category.capitalize()}** ({len(tasks)} tasks)")
                for task in tasks:
                    st.caption(f"  • {task.task_name} ({task.duration_minutes} min)")
        else:
            st.info("No tasks by category.")
    
    st.divider()
    
    # Display reasoning
    if plan.plan_explanation:
        st.markdown("#### 🤖 Scheduling Reasoning")
        st.info(plan.plan_explanation)

# ============================================================================
# DEBUG INFO (Optional)
# ============================================================================

with st.expander("🔧 Debug: View Session State"):
    st.write("Current session_state contents:")
    st.json({
        "owner": {
            "name": st.session_state.owner.name,
            "available_time_hours": st.session_state.owner.available_time_hours,
            "care_preferences": st.session_state.owner.care_preferences,
            "num_pets": len(st.session_state.owner.get_pets())
        },
        "pet": {
            "name": st.session_state.pet.name,
            "species": st.session_state.pet.species,
            "age": st.session_state.pet.age,
            "num_tasks": len(st.session_state.tasks)
        },
        "num_tasks_in_state": len(st.session_state.tasks),
        "daily_plan_exists": st.session_state.daily_plan is not None
    })
