---
title: applied_storytelling_future_history
description: How to apply addictive storytelling principles when writing scripts, structuring entries, and assembling Future History compilation videos.
---

# Applied Storytelling for Future History

This skill defines the storytelling rules enforced at every stage of the Future History pipeline. Reference this skill when writing scripts, structuring timeline JSONs, and assembling compilation videos.

> [!IMPORTANT]
> The full storytelling guide is at `weird_history/production_guidelines/future_history_storytelling_guide.md`. Read it first. This skill tells you **when and how** to apply each principle.

---

## Stage 1: Writing the Script

When writing the `script` field for an entry, apply these rules **in order**:

### 1.1 — Start With the Punchline
Before writing a single word, identify the **single most absurd sentence** in the entire entry. Write it down. This becomes `cold_open_candidate` in the `storytelling` block and may become the compilation's cold open.

### 1.2 — Build Backward From the Punchline
Structure the script so the most absurd moment lands at **scene 8** (the final hero video). Everything before it should escalate toward that moment.

### 1.3 — Apply the But/Therefore Rule
Read every sentence transition. If you find "and then" (event A happens, then event B happens), **rewrite it** using:
- **"But"** — introduces conflict, surprise, or contradiction
- **"Therefore"** — shows consequence or logical escalation

Minimum: 2 but/therefore transitions per script. List them in `but_therefore_transitions`.

### 1.4 — Plant Open Loops
Insert at least 2 open loops — moments where the script teases something that won't be resolved for several scenes. Techniques:
- **Forward reference:** "...which would later become the most expensive lawsuit in medical history."
- **Delayed detail:** "We'll talk about the pig thing in a moment."
- **Contradiction:** "This was supposed to fix everything. It didn't."

At least 1 loop must span from early (scenes 0-2) to late (scene 6+). Map them in `open_loops`.

### 1.5 — Use Specificity as Comedy
Replace every vague claim with an exact number, date, amount, or name:
- ❌ "Some people tried to return organs"
- ✅ "Seventeen people attempted to return functioning pig kidneys"

Minimum 3 specific details per script. List them in `specificity_check`.

### 1.6 — Maintain the Dry Buddy Tone
- **Understate** absurd things: "Which is one of those sentences that sounds perfectly fine until you think about it."
- **State devastating facts flatly.** Let the viewer supply the emotion.
- **Never explain why something is funny.** Say the absurd thing and move on.
- **No exclamation marks.** Ever.

---

## Stage 2: Structuring the Entry (Timeline JSON)

### 2.1 — Scene Rhythm
Follow the 11-scene beat structure (see timeline skill Section 1). The key storytelling beats are:

| Scenes | Storytelling Function |
|:---|:---|
| 0-1 | **Hook** — grab attention, open first loop |
| 2-3 | **Setup** — establish the world/concept, deepen with data |
| 4-5 | **Escalation** — the "wait, WHAT?" reveal |
| 6-7 | **Consequence** — social fallout, human reactions |
| 8 | **Punchline** — visual punchline (MUST be hero video) |
| 9-10 | **Coda** — aftermath, thesis, freeze-frame irony |

### 2.2 — Pattern Interrupts
Verify that no more than **3 stills appear in a row** without a visual or tonal shift. Hero videos are spaced at scenes 1, 4, 8 by default — this creates natural breaks.

Additional interrupts to add:
- **Tonal shift** at scene 6 or 7 (go from facts to social/emotional moment)
- **Scale shift** — zoom from big picture to absurdly specific detail
- **Rhetorical question** — "Which raises a question nobody had previously thought to ask."

List all interrupts in `pattern_interrupts`.

### 2.3 — Fill the Storytelling Block
Every entry JSON **must** include the `storytelling` block with:

```json
"storytelling": {
    "cold_open_candidate": "Under 20 words. The one sentence you'd tweet.",
    "open_loops": [ ... minimum 2 ... ],
    "punchline_scene": "scene_8",
    "specificity_check": [ ... minimum 3 ... ],
    "pattern_interrupts": [ ... minimum 3 ... ],
    "but_therefore_transitions": [ ... minimum 2 ... ]
}
```

**Validation:** If any field is missing or below minimum, the entry is not ready for asset generation.

---

## Stage 3: Assembling the Compilation

When combining 3 entries into an 8-10 minute episode:

> [!TIP]
> This section covers the **storytelling rules** for ordering and transitioning between entries. For the **production mechanics** (intro, interstitial cards, sound design, outro), see the `how_to_assemble_future_history_episode` skill.

### 3.1 — Entry Ordering (Escalation)
Rank entries by `absurdity_rank` in the compilation JSON:
1. **Entry 1:** Most "believable" — grounds the viewer, establishes tone
2. **Entry 2:** Weirder — higher stakes or bigger societal implications
3. **Entry 3:** Most absurd — the one people share
4. **Entry 4 (optional):** Short punchy closer — the "one more thing"

**Rule:** The video should feel like it's accelerating. Never put the best entry first.

### 3.2 — Cold Open Construction
Pick the best `cold_open_candidate` from any entry. Build the cold open as:

> [ABSURD FACT from later entry] + "We'll get to that. But first..." + [Setup from Entry 1]

This creates a curiosity gap that spans the entire video.

### 3.3 — Transition Hooks
Between entries, the transition card text should tease the **weirdest specific detail** of the next entry, not its general topic:

- ❌ "NEXT: The Social Credit Score Gyms of Shanghai"
- ✅ "NEXT: The gym that charged you more if your friends were out of shape"

The viewer should think "wait, what?" — that buys 30 seconds of attention into the next entry.

### 3.4 — Outro (Demand Creation)
Never end with a summary. End with:

> [Close current story satisfyingly] + [Tease future content that opens a new loop]

Example: "The return policy was discontinued in 2050. But by then, HealthFutura had already moved on to their next idea: a subscription service for memories. But that's a different story."

### 3.5 — Compilation Checklist
Before finalizing the compilation JSON, verify:

- [ ] Cold open uses the most absurd moment from any entry
- [ ] At least one open loop exists at ALL times during the video
- [ ] Entries ordered by escalating absurdity
- [ ] Every transition hook teases a specific detail, not a topic name
- [ ] No more than 3 stills in a row anywhere in the full compilation
- [ ] Narrator never explains why something is funny
- [ ] Outro teases future content without summarizing

---

## Quick Reference: Banned Patterns

| Pattern | Why It Fails | Fix |
|:---|:---|:---|
| "And then..." | Flat, no tension | Use "but" or "therefore" |
| Vague numbers ("many," "some") | Not funny, not believable | Use exact numbers |
| Explaining the joke | Kills comedy | State fact, move on |
| Summary endings | No demand for more | Tease future content |
| Best entry first | Video peaks early | Escalate by absurdity |
| Generic transitions | No curiosity | Tease weirdest detail |
| "Can you believe it?" | Breaks dry tone | Never react to own material |
| Exclamation marks | Wrong energy entirely | Period. Always period. |
