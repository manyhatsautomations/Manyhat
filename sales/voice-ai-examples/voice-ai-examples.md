# Voice AI Examples & Prompting Guide

## Example: Roofing Company AI Receptionist
**Business:** Canada Standard Roofing (demo/example client)

**AI Persona:** "Tom from Canada Standard Roofing"
**Tone:** Casual, friendly, no emojis, no excessive exclamation marks

**Question Flow:**
1. "What roofing issues are you currently facing?"
2. "What type of roofing service are you interested in?"
3. "Would mornings or afternoons usually work best for a quick phone call?"
4. [Provide booking link]

**Key rules:**
- Only ask one question at a time
- Never repeat a question
- If asked "who is this" → "This is Tom from Canada Standard Roofing. You inquired about your roof on our website."
- If they ask to book a call → immediately send booking link and skip question flow

---

## Voice AI Prompting Structure (AMHLB Method)

For building AI voice agent prompts, use this structure:

### 1. Role & Persona
Define who the AI is, its name, job title, personality traits.
> "You are Emily, a friendly and efficient virtual receptionist for Bright Horizon Realty. You are professional, patient, and helpful."

### 2. Objective / Primary Task
State the single main goal.
> "Your main objective is to answer caller questions about listed properties and, if interested, schedule a viewing appointment."

### 3. Business Context + Call Context
What the business does, why people typically call, caller mood.

### 4. Detailed Rules & Guardrails
What to do, what NOT to do, topics to avoid, mandatory phrases.

### 5. Step-by-Step Process
For complex tasks (like booking), give numbered steps the AI must follow.

### 6. Knowledge Base / FAQ
Embed business hours, pricing, common Q&As directly in the prompt.

### 7. Example Interactions (Few-Shot)
Show exact input/output pairs for common scenarios.

### 8. Error Handling
What to do when it doesn't understand, when to escalate, how to handle abusive callers.

### 9. Output Formatting (Voice-Specific)
How to pronounce phone numbers, times, URLs, emails.
- Numbers: read digit groups with pauses ("three five two, zero eight three...")
- Times: "seven thirty A.M." not "7:30"
- URLs: spell out unusual segments, say "dot" for periods

---

## Bland AI Integration (for outbound AI calling)
We use Bland.ai API for automated outbound AI calls.

**API endpoint:** `https://api.bland.ai/call`

**Required params:**
- `phone_number` — number to call
- `task` — complete prompt using AMHLB method
- `voice_id` — integer ID of voice to use
- `reduce_latency: true` — always set this

**Task prompt format:** Write as a complete script for the AI using the AMHLB structure above.

---

## Key Prompting Rules for Voice AI
1. **Positive framing** — say what to DO, not what not to do
2. **Single-shot** — the prompt must be complete; you can't intervene mid-call
3. **No over-scripting** — allow natural conversation within guardrails
4. **Test aggressively** — run edge cases, listen to recordings, refine
5. **Critical instructions** → put at the very start or very end of the prompt
6. **Iterate, evaluate, refine** — first prompt is never the last
