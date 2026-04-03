# Context Trim — CLAUDE.md Snippets

Copy the relevant sections below into your project's `CLAUDE.md`.
Each section reduces token waste in a specific way.

---

## 1. Response Conciseness

Add to CLAUDE.md to stop Claude from adding filler, summaries, and restating what you said:

```markdown
## Response Style
- Answer directly — skip preamble ("Sure!", "Great question!", "I'll now...")
- Don't restate the task before doing it
- Skip closing summaries ("I've now completed...") unless explicitly asked
- If you can say it in one sentence, don't use three
- Code explanations: one line per non-obvious thing, not every line
```

---

## 2. File Reading Efficiency

Prevents Claude from re-reading the same files repeatedly:

```markdown
## File Access
- Read each file once per session — cache the content in context, don't re-read
- When editing, read only the relevant section if the file is >200 lines
- Don't read files to "verify" something you already know from context
- Prefer Grep over Read when looking for a specific value in a large file
```

---

## 3. Tool Call Verbosity

Reduces verbose tool call output that floods context:

```markdown
## Tool Output
- After running tests, report: pass/fail count + any failures. Don't paste all output.
- After a bash command, report the result in one line unless there's an error
- Don't show directory listings in full — summarize what's relevant
- For search results, report what was found, not the raw match output
```

---

## 4. Known Patterns

Stops Claude from explaining patterns it already knows from CLAUDE.md:

```markdown
## Known Patterns
The conventions in this CLAUDE.md are already known. Don't explain them back to me.
When you follow a convention, just follow it — no need to say "as per CLAUDE.md, I'm using..."
```

---

## 5. Session Continuity

Tells Claude to trust context carried from Memory OS files:

```markdown
## Memory OS
At session start: read memory-bank/*.md — this is your full context. Trust it.
Don't re-explore the codebase if memory-bank/ tells you what you need to know.
At session end: update memory-bank/activeContext.md and memory-bank/progress.md in 5 lines each.
```

---

## 6. Decision Autonomy (reduces back-and-forth)

Cuts the number of "should I...?" turns:

```markdown
## Decision Making
Make implementation decisions autonomously based on CLAUDE.md conventions.
Only ask if:
- The task involves money, external accounts, or production systems
- Two valid approaches exist and they have meaningfully different tradeoffs
- You hit a genuine blocker (missing dependency, missing credential)
Don't ask permission to: create files, refactor, rename, add tests, fix style issues.
```

---

## 7. Summarize-Before-Truncate

Tells Claude to summarize rather than truncate when context fills:

```markdown
## Context Management
If you sense context is filling up:
1. Summarize completed work into 3 bullets
2. Note the current state in one sentence
3. Continue with fresh context
Never silently drop earlier context — always summarize first.
```

---

## Measuring Impact

Before adding these snippets, note:
- Average tokens used per session (visible in usage dashboard)
- How many turns Claude takes before starting actual work

After: the "wasted turns" at session start should drop from 3–5 to 0–1.
