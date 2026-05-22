---
name: Cold Call Practice System
purpose: Claude Code cold call simulations tracked and analyzed by Hermes
folder: 04 Business/Manyhat-Automations/cold-call-practice/
analyzed_by: Evening Wrap (8pm daily) + Dreamer (3am)
system_version: 2.0
last_updated: 2026-05-21
---

# Cold Call Practice System — v2.0

## Architecture

```
Claude Code (practice)          Vault (storage)              Hermes (analysis + delivery)
       │                             │                               │
       │  runs practice call         │                               │
       │  with full teleprompter     │                               │
       │  branching navigator        │                               │
       │                             │                               │
       ├── saves transcript ────────►│ sessions/YYYY-MM-DD-call-N.md │
       │   scores, transcript,       │                               │
       │   branch path, patterns     │                               │
       │                             │                               │
       │                             │     7:00am ───────────────────┤
       │                             │     Morning Brief:             │
       │                             │     • Today's training focus   │
       │                             │     • Industry Term of the Day │
       │                             │     • Opener to drill today    │
       │                             │     → Telegram                 │
       │                             │                               │
       │                             │     12:30pm ──────────────────┤
       │                             │     Midday Check:              │
       │                             │     • Cold Call Challenge Q    │
       │                             │     • Accountability nudge     │
       │                             │     → Telegram                 │
       │                             │                               │
       │                             │     8:00pm ───────────────────┤
       │                             │     Evening Wrap:              │
       │                             │     • Today's session scores   │
       │                             │     • Pattern alert if needed  │
       │                             │     • Week progression status  │
       │                             │     • One specific tip         │
       │                             │     → Telegram                 │
       │                             │                               │
       │                             │     3:00am ───────────────────┤
       │                             │     Dreamer:                   │
       │                             │     • Consolidates patterns    │
       │                             │     • Updates progress-tracker │
       │                             │     • Updates skill levels     │
```

---

## For Claude Code — Post-Call Instructions

After EVERY practice call, save a session file:

**Path:** `C:/Users/paulr/Documents/Agentic OS Vault/04 Business/Manyhat-Automations/cold-call-practice/sessions/YYYY-MM-DD-call-N.md`

**Template:** `templates/call-log-template.md`

**Required fields:**
- Full transcript (every line)
- Branching path taken (which scenario branch at each phase)
- Scores for all 7 areas
- Talk ratio estimate (Paul % vs Prospect %)
- Pattern notice (is this a recurring weakness?)
- Specific drill recommendation for next session

---

## Scoring System (v2.0)

| Area | Weight | What Hermes Looks For |
|------|--------|----------------------|
| Opener | 20% | Natural? Disarm included? Ended with question? No banned phrases? |
| Disarm | 10% | "Not sure this makes sense for you" frame present? |
| Pain dig | 20% | Made prospect say their pain in their own words? |
| Objection handling | 20% | Acknowledge → Reframe → Bridge? Never argued? |
| Demo ask | 15% | Attempted in every call? Smooth transition? |
| Close | 10% | Two-option close? Calendar invite? |
| Talk ratio | 5% | Paul under 40% of call time? |

**Overall = weighted average. Target: 7/10 average to advance weeks.**

---

## 6-Week Progression (for Hermes tracking)

| Week | Focus | Pass Criteria | Teleprompter |
|------|-------|--------------|-------------|
| 1 | Opener only | 3 consecutive openers B+, avg 5/10 | Full |
| 2 | Disarm + pain question | Voicemail B+, got past gatekeeper, avg 6/10 | Full |
| 3 | Poke the pain | Prospect named own pain 4/5 calls, avg 6.5/10 | Partial |
| 4 | Demo ask + close | Demo attempted every call, avg 7/10 | Partial |
| 5 | Hard prospects | Phase 1-3 from memory, avg 7.5/10 | Phase 4-5 only |
| 6 | Blind calls | Avg 7.5/10, 1 demo booked in 5-call test | Off |

---

## Hermes Instructions — What to Do With Sessions

### Morning Brief (7am) should include:
1. **Yesterday's summary** — calls completed, avg score, biggest win/gap
2. **Today's focus area** — based on weakest score from recent sessions
3. **Industry Term of the Day** — one term from the industry rotation Paul hasn't used recently
4. **Today's opener to drill** — one specific opener Paul should say out loud 5x before first call
5. **Streak status** — current streak, record, days this week

### Midday Check (12:30pm) should include:
1. **Cold Call Challenge** — one scenario question Paul must answer via voice or text:
   - Example: "Rob the plumber says: 'I answer my own calls, I'm good.' What's your FIRST response?"
   - Grade his answer if he replies. If no reply in 30 min, send the correct answer anyway.
2. **Accountability nudge** — if no sessions logged today: "No calls yet today. Even 2 practice calls moves the needle. Go."
3. **Real call check-in** — "Any real calls today? Reply: yes / no / tried"

### Evening Wrap (8pm) should include:
1. **Today's full summary** — sessions, avg score, result breakdown (booked/lost/hung up)
2. **Pattern alert** — if same weakness appears 3+ sessions in a row: "⚠️ You're failing [area] consistently. Tomorrow: drill this first."
3. **Week progression status** — "Week [N]: [X] calls done. Avg score: [X.X]/10. Pass criteria: [criteria]. [On track / Close / Behind]."
4. **Industry gap alert** — if Paul hasn't practiced a specific industry in 3+ days: "You haven't called a [industry] this week. Try one tomorrow."
5. **One specific actionable tip** — pulled from the actual transcript, not generic advice
6. **Streak update** — "🔥 Day [N] of your streak. Keep it going."

### Dreamer (3am) should:
1. Update `progress-tracker.md` with this week's scores
2. Detect recurring patterns across all sessions this week
3. Update the "Current Level" for each skill in the tracker
4. Write a brief `progress-reports/YYYY-MM-DD-weekly.md` if it's Sunday night
5. Check if Paul has met pass criteria to advance to the next week

---

## Real Call Logging

Paul can log real (live) calls by telling Hermes via Telegram:
> "Real call: Roofer in Mississauga. Gave objection 'not interested'. Pivoted to pain. Lost them. Score myself 5."

Hermes should save this to `sessions/YYYY-MM-DD-real-call-N.md` and include in evening analysis separately from practice calls.

Track: Practice calls vs Real calls separately. Both count toward streak.

---

## Streak Rules
- Practice call OR real call = streak day
- Miss 1 day = streak resets
- Milestone celebrations: 3 days, 7 days, 14 days, 21 days, 30 days
- At 7-day streak: Hermes sends a special message with the "what separates top 5%" framework reminder

---

## Tags
#cold-calling #practice #manyhats #training #week1 #progress
