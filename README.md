# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Smarter Scheduling

Beyond the basics, PawPal+ also includes some smarter scheduling features that make planning feel more effortless. Tasks are automatically sorted by time, so it’s easy to see your pet’s day at a glance. You can filter tasks by status or by pet to focus on what matters most, and recurring tasks like daily feeding will automatically carry over to the next day.

There’s also simple conflict detection built in. It warns you if two tasks end up at the same time. It doesn’t interrupt anything, just gives helpful feedback to keep your pet’s routine organized and running smoothly.

## Testing PawPal+

I wrote a set of tests to make sure the main features of PawPal+ work as expected. The tests cover things like marking tasks as complete or incomplete, making sure the scheduler prioritizes tasks correctly based on priority and available time, and checking that recurring tasks (like daily or weekly ones) generate properly.

I also tested conflict detection to make sure the system gives warnings when tasks overlap in time without crashing. On top of that, I included tests for sorting and filtering tasks, sucsh as organizing them by time or filtering by status or pet. Finally, I added some edge case tests, like handling empty task lists, zero available time, and unusual inputs, to make sure the system behaves reliably in different situations.

Based on the test results, I would rate the system’s reliability as 5 out of 5. All 39 tests passed, including both normal use cases and edge cases, which gives me strong confidence that the core functionality—especially scheduling, recurrence, and conflict handling—is working correctly and consistently.

## Features
### Task Management
1. Create and manage tasks with attributes such as duration, priority, category, and scheduled time  
2. Mark tasks as complete or incomplete, with completion date tracking  
3. Prevent duplicate tasks from being added to a pet  

### Priority-Based Scheduling
1. Tasks are prioritized using a simple rule: HIGH → MEDIUM → LOW  
2. Within the same priority level, shorter tasks are scheduled first  
3. A greedy allocation approach selects tasks that fit within the owner's available time  

### Time-Based Sorting
1. Tasks can be sorted by scheduled time using "HH:MM" format  
2. Internally converts time strings into comparable values for accurate ordering  
3. Tasks without a scheduled time or with invalid formats are placed at the end  

### Recurring Tasks
1. Supports ONCE, DAILY, and WEEKLY task frequencies  
2. Automatically generates the next occurrence of recurring tasks using date offsets  
3. Maintains links between tasks using parent_task_id for tracking recurrence  
4. Preserves task properties such as name, priority, and scheduled time across generations  

### Conflict Detection
1. Detects tasks scheduled at the exact same time  
2. Returns warning messages instead of stopping execution  
3. Handles multiple conflicts and ignores tasks without scheduled times  

### Task Filtering
1. Filter tasks by completion status (completed or pending)  
2. Filter tasks by pet name (case-insensitive matching)  
3. Works across multiple pets and combined task lists  

### Multi-Pet Support
1. An owner can manage multiple pets  
2. Each pet maintains its own list of tasks  
3. The owner can retrieve all tasks across pets or filter by pet  

### Daily Plan Generation
1. Generates a daily plan based on available time and task priorities  
2. Ensures the total scheduled time does not exceed the owner's time constraint  
3. Outputs a list of selected tasks along with a basic explanation of the plan  

<a href="/demo.png" target="_blank"> <img src='/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /> </a>