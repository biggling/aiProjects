# Notion Side Project Dashboard

## What This Is

A Notion template for solo developers running multiple side projects.
One dashboard to track all projects, revenue targets, milestones, and weekly focus.

---

## Template Link

The Notion template is available at:
**[Duplicate this template →]** *(link provided in template-link.txt)*

Click "Duplicate" in the top-right corner of the Notion page.
The template will be copied to your workspace with all views and properties intact.

---

## Views Included

### 1. Kanban Board — Projects by Status
All projects displayed as cards, grouped by status:
`Not Started` → `Research` → `Building` → `Active` → `Revenue` → `Paused`

Each card shows: project name, priority, phase, next step, revenue target.

### 2. Timeline — Milestones
Gantt-style view of milestones across all projects.
See at a glance which projects have upcoming deadlines.

### 3. Revenue Tracker
Table view with:
- Monthly revenue target per project
- Actual revenue (update weekly)
- Status: On Track / Behind / Ahead
- Notes on what to do to hit target

### 4. Weekly Focus
Filtered view: top 3 tasks across all projects this week.
Manually curated — drag your top priority items here.

### 5. Research Log
Log of research findings per project.
Each entry: project, date, source, finding, action item.

---

## How to Use

### First Setup (15 minutes)
1. Duplicate the template into your Notion workspace
2. Add your projects to the Projects database (one row per project)
3. Set priority, current phase, and revenue target for each
4. Add your top 3 milestones per project to the Milestones database

### Weekly Ritual (10 minutes, Sunday)
1. Update Revenue Tracker with actual numbers
2. Move projects to correct status column
3. Add top 3 tasks to Weekly Focus view
4. Add any new research findings to Research Log

### Daily (2 minutes)
1. Check Weekly Focus — work on the top item
2. Update the task status when done

---

## Properties Reference

### Projects Database
| Property | Type | Purpose |
|---|---|---|
| Name | Title | Project name |
| Priority | Number | 1 = highest |
| Status | Select | Current lifecycle stage |
| Phase | Text | Phase N — description |
| Next Step | Text | Single most important next action |
| Revenue Target | Number | Monthly target (USD) |
| Revenue Actual | Number | This month's actual (USD) |
| Stack | Multi-select | Technologies used |
| Notes | Text | Anything else |

### Milestones Database
| Property | Type | Purpose |
|---|---|---|
| Milestone | Title | What gets completed |
| Project | Relation | Links to Projects |
| Target Date | Date | When you plan to hit it |
| Actual Date | Date | When you actually hit it |
| Status | Select | Planned / In Progress / Done / Missed |

---

## Tips

- Use the Revenue Tracker as motivation — seeing $0 across 12 projects creates urgency
- Be honest with the Status column — "Building" means you worked on it this week
- Weekly Focus should have 3 items max — if you can't pick 3, you're not prioritizing
- Research Log is a permanent record — never delete entries, just add new ones
