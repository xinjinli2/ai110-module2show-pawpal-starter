# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

*Answer* 
1. A user need to enter and review basic information about the pet and owner, such as the pet's name and time available for care. 
2. A user can edit and manage care tasks such as feeding, walks, medication, and grooming, including each task's duration and priority
3. A user can generate a daily plan that fits the most important tasks into their available time and explains the decisions.

For my initial UML design, I tried to focus on the main objects a user would actually interact with in the app and the ones needed behind the scenes to generate a plan. I wanted to design to feel simple but still clear enough to separate responsibilities across the system. I included `Pet`, `Task`, `Ownder`, `DailyPlan`, and `Scheduler`. `Pet` is for storing the pet's profile and care notes. `Task` is for each care activity, and stores information like the task name, duration, priority, category, and their complete status. `Owner` is to store user's basic information, and their time availability for pet care. `DailyPlan` is for the final schedule for the day, it displays selected tasks, and keeps track of the time, and store the explanantion shown to the user. It also sorts tasks by their priorities with owner's time limit. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

1. Yes, I did change the design. 
2. I fixed the pet and task linkage, tasks did not specify which pet they belong to. With multiple pets, this becomes non-clear. I added pet name and pet id to the Task. 
3. I also fixed some logic problems. In the past, the priority system is undefined that we cannot compare high vs. medium vs. low. I added Enum for the priority level. I also added check for data validation such as checking for negative duration and invalid priorities. I also added the tie breaking logic for two tasks have the equal priority. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Our conflict detection is pretty simple right now—we only check if two tasks have the exact same start time, instead of checking whether their durations overlap. So if two tasks are both at 3 PM, we flag a conflict, but if one is 3:00–3:45 and another is 3:30–4:00, we don’t catch that overlap.

This tradeoff makes sense for our case because it keeps the logic much simpler and faster. Most pet owners think in terms of specific times like “feed at 6 PM,” not detailed time ranges, so exact matching aligns with how the app is used. It also avoids adding more complex logic and keeps performance efficient. If we needed more precise scheduling in the future, we could add start and end times and handle overlaps, but for this app, the simpler approach works well.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I also thought about making the conflict detection code more “Pythonic” using things like defaultdict and list comprehensions, but I ended up sticking with the more explicit version. The main reason is readability. Since this is more of an educational project, I wanted the logic to be easy to follow step by step, especially for someone who might not be very familiar with Python.

The explicit version is also easier to debug, since you can clearly see how the dictionary is being built and where things might go wrong. The more compact version looks cleaner, but it’s a bit harder to trace and requires extra concepts like defaultdict.

Overall, I felt that simple and clear code was more valuable here than writing something more concise but harder to understand.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
