---
title: how_to_research_weird_history_content
description: How to research, validate, and write new topic entries for the Weird History content library, optimized for short-form video production.
---

# Researching Weird History Content

This skill covers how to identify, research, validate, and write entries for new Weird History topic categories. Each category should contain 50 deeply researched entries, written 25 at a time across two files.

## 1. Understanding the Research Library

All research lives in: `weird_history/historic_research/`

The master index at `historic_research/master_index.md` tracks all categories. Each category gets two files:
- `<topic_name>.md` — entries 1-25
- `<topic_name>_2.md` — entries 26-50

## 2. Selecting New Topic Categories

When choosing new research categories, apply these filters:

**DO target topics that are:**
- Genuinely surprising or funny to modern audiences
- Visually rich — can be depicted in short-form video (think: what would this LOOK like?)
- Culturally diverse — span multiple civilizations, eras, and continents
- Absurd, quirky, and entertaining — the "wait, WHAT?" reaction

**DO NOT target topics that are:**
- Grotesque, gory, or disturbing (e.g., "Bizarre Beauty & Body Standards" was rejected for being too gross)
- Depressing without humor (famine, plague, genocide — unless there's a genuinely absurd angle)
- Too niche or academic to be entertaining for a general audience
- Overlapping heavily with existing categories

**Existing categories (do not duplicate):**
- Love & Romance
- Courting & Wooing
- Matchmaking
- Intimacy & Consummation Customs
- Childbearing, Childbirth & Fertility
- Bizarre Laws, Punishments & Legal Customs
- Weird Money & Trade Customs
- (Check master_index.md for the latest list)

## 3. Entry Format (STRICT)

Every entry MUST follow this exact format:

```markdown
## [Number]. [Catchy Title] ([Region/Era])
**Description:** 3-4 sentences written in an engaging, entertaining tone. Should read like a surprised friend telling you an insane fact. Use humor, surprise, and vivid language. Include specific numbers, names, and dates when possible.
**Visual Elements:**
- [What this looks like in a video — describe the scene, characters, setting]
- [A second visual moment — reaction shot, dramatic reveal, comparison]
- [A third visual angle — close-up, split-screen, or before/after]
- [Optional fourth visual — modern comparison or comedic callback]
**Caption Summary:** "[One punchy social media line — the kind that makes someone stop scrolling]"
**Citation & Link:**
- [Source Name - Article Title](URL)
- [Source Name - Article Title](URL)
- [At least 2-3 real, reputable sources per entry]

---
```

## 4. Research Quality Standards

### What counts as a valid source:
- Wikipedia (acceptable as starting point, but cross-reference)
- Academic journals (JSTOR, Oxford Academic, Cambridge Press)
- Museum collections (Smithsonian, Met, British Museum)
- Reputable encyclopedias (Britannica, World History Encyclopedia)
- Quality journalism (Smithsonian Magazine, Atlas Obscura, NPR, BBC)
- Government/institutional archives (Library of Congress, National Archives)

### What does NOT count:
- Unsourced blog posts or listicles
- Social media posts or Reddit threads
- AI-generated content or content farms
- Sources that cannot be verified with a URL

### Verification rules:
- Every historical claim must be traceable to at least one reputable source
- If a fact seems too wild to be true, it probably needs an extra citation
- Note scholarly debates when they exist (e.g., "Scholars debate the historicity of...")
- Do not present legends or myths as confirmed historical fact without noting the distinction

## 5. Content Moderation Pre-Check

Before writing any entry, mentally run it through the content moderation checklist:

- **No banned words** in descriptions or visual elements
- **No minors** in any suggestive or dangerous context
- **No explicit gore or blood** — use metaphors (falling rose petals, red fabric)
- **Intimacy implied, never shown** — "the couple retreated to their chamber" not graphic detail
- **Medical references softened** — clinical language, not graphic descriptions
- **Cultural sensitivity** — present practices with context, not mockery of the culture itself

The humor should target the ABSURDITY of the situation, never the people or culture.

## 6. Writing Process (25 Entries at a Time)

### Step 1: Topic brainstorming
Generate 25 specific entry ideas covering diverse cultures, eras, and regions. Aim for geographic and temporal variety — don't cluster 15 entries from the same civilization.

### Step 2: Parallel research
Use two research agents in parallel:
- Agent 1: Research entries 1-12
- Agent 2: Research entries 13-25

Each agent should use WebSearch to find and verify facts, then format entries in the exact template above.

### Step 3: Assembly
Combine the results into a single markdown file at:
`weird_history/historic_research/<topic_name>.md`

Header format:
```markdown
# [Topic Category Name] (Part 1: Entries 1-25)
```

### Step 4: Verification
After writing, verify:
- [ ] Exactly 25 entries with sequential numbering
- [ ] Each entry has Description, Visual Elements (3-4 bullets), Caption Summary, and Citation & Link
- [ ] No duplicate topics within the category or across other categories
- [ ] Geographic/temporal diversity (not all from one culture)
- [ ] Tone is entertaining and funny, not academic or dry

### Step 5: Repeat for entries 26-50
Same process, writing to `<topic_name>_2.md` with header:
```markdown
# [Topic Category Name] (Part 2: Entries 26-50)
```

### Step 6: Update master index
Add the new category to `historic_research/master_index.md` with links to both files.

## 7. Writing Style Guide

### Voice & Tone
- Write like you're telling a friend the craziest thing you just learned
- Use surprise markers: "But here's the thing...", "The wildest part?", "It gets better..."
- Include modern comparisons: "basically the medieval version of Tinder"
- End descriptions with a punchy closer or ironic observation

### Caption Summaries
- Must be under 150 characters ideally
- Lead with the most shocking detail
- Use CAPS sparingly for emphasis (one word per caption max)
- Format: "[Specific historical fact] -- [shocking consequence or detail]"

### Visual Elements
- Think like a video director — what shots tell this story?
- Include at least one close-up, one wide establishing shot, and one reaction/comparison
- Reference specific objects, clothing, settings, and character expressions
- Modern comparison shots work great: "Split-screen: ancient version vs. modern equivalent"

## 8. Example: Complete Entry

## 1. The Ottoman Coffee Death Penalty (Ottoman Empire, 1633)
**Description:** Sultan Murad IV of the Ottoman Empire was so paranoid about coffeehouses being hotbeds of rebellion that in 1633 he made drinking coffee in public punishable by DEATH. He reportedly disguised himself and roamed Istanbul's streets at night with a 100-pound broadsword, personally decapitating anyone he caught drinking coffee. His successors softened the penalty: a first offense got you beaten, but a second offense meant being sewn into a leather bag and thrown into the Bosporus strait.
**Visual Elements:**
- A sultan in disguise creeping through dark Istanbul streets, peeking into a coffeehouse window where terrified men are hiding their tiny cups
- Cut to a man being literally sewn into a bag near the waterfront
- A modern Starbucks customer sipping a latte, unaware of how lucky they are
**Caption Summary:** "In 1633, the Ottoman Sultan personally roamed the streets with a sword, BEHEADING anyone caught drinking coffee!"
**Citation & Link:**
- [Atlas Obscura - In Istanbul, Drinking Coffee Was Once Punishable by Death](https://www.atlasobscura.com/articles/was-coffee-ever-illegal)
- [NPR - Drink Coffee? Off With Your Head!](https://www.npr.org/sections/thesalt/2012/01/10/144988133/drink-coffee-off-with-your-head)
