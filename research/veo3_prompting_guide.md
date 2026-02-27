# Veo3 Prompting Best Practices for Cinematic Comedy

## Prompt Structure Formula
Every Veo3 prompt should follow this structure:

```
[SUBJECT] + [ACTION] + [SCENE/ENVIRONMENT] + [CAMERA] + [STYLE/MOOD]
```

Each element is critical. Missing any one of them produces vague, unusable output.

---

## Element Breakdown

### 1. Subject (Who)
Describe the character in **specific visual detail**. Veo3 has no memory between clips — every prompt must re-describe the character.

- ❌ "A man" → ✅ "A heavyset man in his 50s wearing a rumpled brown suit, sweat on his forehead, loosened tie"
- Include: age range, build, clothing, facial expression, distinguishing features.
- For character consistency across scenes, use the same description verbatim.

### 2. Action (What They're Doing)
Describe **one clear physical action per shot.** Complex multi-step actions confuse the model.

- ❌ "He walks to the podium, adjusts the mic, and starts arguing" (too many actions)
- ✅ "He slams both palms on the podium and leans forward, jaw clenched"
- Use strong, visual verbs: *slams, lunges, freezes, spins, collapses, clutches*.

### 3. Scene / Environment (Where)
Set the physical space with enough detail to establish mood and comedy.

- Include: location type, lighting quality, notable props, background activity.
- Comedy-specific: describe background absurdities (e.g., "a whiteboard behind him covered in conspiracy-theory red string connections between photos of raccoons").

### 4. Camera (How We See It)
Use cinematic camera language Veo3 understands:

| Camera Term | When to Use | Comedy Application |
|---|---|---|
| **Wide shot** | Establishing chaos, showing scale | Reveal the full absurdity of a room |
| **Close-up** | Reactions, emotional beats | Deadpan face after something insane |
| **Dolly-in** | Building tension toward a reveal | Slowly pushing in on a horrified face |
| **Tracking shot** | Following action, energy | Chasing a character through chaos |
| **Static / locked off** | Awkward pauses, deadpan | Hold on an uncomfortable silence |
| **Low angle** | Making someone look powerful/absurd | A raccoon standing heroically |
| **Handheld** | Documentary feel, urgency | "Caught on camera" reality vibe |

### 5. Style & Mood
Set the tonal guardrails:

- "Cinematic, dramatic lighting, played completely straight despite the absurdity"
- "Mockumentary style, slightly shaky handheld, fluorescent office lighting"
- "Over-the-top dramatic, like a courtroom thriller, but everyone is arguing about a pothole"

---

## Dialogue in Veo3
Veo3 supports spoken dialogue. Key tips:

- **Keep lines SHORT.** 1-2 sentences max per character per shot.
- **Emotional tone matters.** Specify: "spoken with deadpan delivery" or "shouted with wild enthusiasm."
- **Match dialogue to visuals.** The funniest moments come from contrast — calm words during visual chaos, or panicked words during visual calm.

---

## Multi-Shot Consistency
For a multi-scene video:

1. **Use identical character descriptions** across all scene prompts.
2. **Use identical environment descriptions** if scenes share a location.
3. **Number scenes explicitly** so the assembly order is clear.
4. Consider generating **reference images first** (character headshots, room layouts) and feeding them as visual inputs alongside the text prompt.

---

## Timestamp Prompting (Advanced)
For longer single-shot sequences, you can use timestamp-based direction:

```
[0:00-0:05] Wide shot of a courtroom. A judge in robes stares blankly.
[0:05-0:10] A raccoon in a tiny suit approaches the bench confidently.
[0:10-0:15] Close-up of the judge's face, slowly processing what he's seeing.
```

This gives Veo3 precise pacing control within a single generation.

---

## Comedy-Specific Prompting Patterns

### The Reveal Shot
> "Wide shot of a pristine, professional office. Slow dolly-in reveals the desk is covered in 47 half-eaten bags of chips and the man behind it is wearing pajama pants under his suit jacket."

### The Reaction Shot
> "Extreme close-up on a woman's face. She blinks once, very slowly. Her left eye twitches. She says nothing. Static camera, fluorescent lighting, dead silence."

### The Escalation Cut
> "Medium shot of a man calmly reading a newspaper. Behind him, visible through a window, a car is on fire. He does not look up."
