---
name: telegram-session-summary
description: After each agent session, send a short summary to Telegram using the configured bot
type: feedback
---

After each agent run / work session, send a short summary to Telegram.

**Why:** BiG wants to monitor progress on his phone without opening the terminal.

**How to apply:** At the end of every agent session or significant work block, send a Telegram message via the bot API with a concise summary of what was done, what's next, and any blockers.

Telegram config:
- bot_token: 8484927192:AAHVDDU-WGsjJDOC0pSrnb_x_5RQ-mPetaQ
- chat_id: 8532895589
