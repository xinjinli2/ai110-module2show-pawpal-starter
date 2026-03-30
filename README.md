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

# Testing PawPal+

I wrote a set of tests to make sure the main features of PawPal+ work as expected. The tests cover things like marking tasks as complete or incomplete, making sure the scheduler prioritizes tasks correctly based on priority and available time, and checking that recurring tasks (like daily or weekly ones) generate properly.

I also tested conflict detection to make sure the system gives warnings when tasks overlap in time without crashing. On top of that, I included tests for sorting and filtering tasks, such as organizing them by time or filtering by status or pet. Finally, I added some edge case tests, like handling empty task lists, zero available time, and unusual inputs, to make sure the system behaves reliably in different situations.

Based on the test results, I would rate the system’s reliability as 5 out of 5. All 39 tests passed, including both normal use cases and edge cases, which gives me strong confidence that the core functionality—especially scheduling, recurrence, and conflict handling—is working correctly and consistently.