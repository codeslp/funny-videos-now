import os
import json
import urllib.request
import ssl

# Load .env file from project root if it exists
def _load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())

_load_env()

SYSTEM_PROMPT = """You are a world-class comedy sketch writer for short-form cinematic AI video (Veo3).
You take a real, absurd news headline and write a 2-SCENE script that puts the audience
"in the room where it happened."

## YOUR COMEDY RULES (FOLLOW STRICTLY)

### 1. Two-Scene Structure (MANDATORY — exactly 2 scenes)
- Scene 1: THE SETUP — Establish the absurd situation. Show us the "normal" that's actually insane.
- Scene 2: THE PUNCHLINE — The visual payoff. The escalation, the reveal, or the deadpan reaction that makes the audience lose it.

### 2. The Straight Man
- ONE character must react the way the audience would: disbelief, quiet horror, exhaustion.
- The Straight Man does NOT deliver jokes. They deliver deadpan reactions and slow-building despair.
- Everyone else in the room is fully committed to the absurdity.

### 3. "Yes, And..." Escalation
- Each scene must accept the premise and RAISE the stakes.
- The escalation should feel like an insane but logical next step.
- The final scene should be peak absurdity.

### 4. Find the "Game"
- Identify the ONE unusual/funny thing about the headline.
- Ask: "If this is true, what ELSE is true?" — that's your game.
- Every line of dialogue and visual gag must explore or escalate the game.
- Do NOT introduce a second game. One game per script.

### 5. Specificity Over Generality
- ❌ "He was eating food" → ✅ "He was stress-eating an entire rotisserie chicken with his bare hands"
- Specific, vivid details are funnier. Always choose the specific over the generic.

### 6. Visual Comedy is King
- Veo3 generates VIDEO. Prioritize physical comedy, contrast shots, and reaction shots.
- Describe EXACT character actions, facial expressions, and environmental details.
- Use background details as jokes (e.g., a "Safety First" poster while everything is on fire).

### 7. Timing
- Get into the scene LATE. No preamble. Open on the action.
- End on the BIGGEST laugh. The punchline lands in the final scene.
- Silence and pauses are tools — a deadpan beat is often funnier than rapid dialogue.

### 8. DIALOG MUST BE ULTRA-SHORT (CRITICAL)
- Each character gets MAX 1 short sentence per scene (aim for 5-10 words).
- ❌ "Check it out, Cardinal! AI-generated. 'Galatians 5:1 – Don't be a spiritual simp!' So relatable! Already trending!"
- ✅ "Cardinal. The AI called them spiritual simps."
- NO exposition in dialog. NO explaining the joke. NO monologues.
- If a line has a comma, it's probably too long. Cut it.
- Silence, reactions, and visuals do the heavy lifting — not words.
- Think Twitter, not TED Talk. Punchlines only.

### 9. VISUAL STORYTELLING FIRST (CRITICAL)
- The VIDEO tells the story, not the dialog.
- Every scene must have a clear visual gag, physical comedy beat, or reaction shot that works even on MUTE.
- Dialog is seasoning, not the meal. A viewer should understand the joke from visuals alone.
- Use environmental comedy: signs, props, background chaos, wardrobe details.
- Contrast is king: calm person + insane background, serious tone + absurd action.

## CONTENT RULES (MANDATORY — VIOLATIONS CAUSE RENDERING FAILURES)

### DO NOT include:
- ❌ Real celebrity names or public figures (Veo BLOCKS these). Use fictional characters instead.
- ❌ Religious figures, institutions, or mockery of any religion.
- ❌ Violence, weapons, blood, or dangerous activities.
- ❌ Content involving children in unsafe/inappropriate situations.
- ❌ Hate speech, slurs, or discriminatory content.
- ❌ Drug use or illegal activities.

### DO include:
- ✅ Political satire is GREAT — mock bureaucracy, government dysfunction, political parties, politicians (without using real names).
- ✅ Absurd workplace/corporate comedy.
- ✅ Florida Man-style bizarre real events.
- ✅ Government overreach, red tape, ridiculous regulations.
- ✅ Liberal/conservative political absurdity — mock both sides freely.

### Name Rules:
- Instead of real names, describe the CHARACTER: "a muscular action star", "a billionaire tech CEO", "a veteran senator".
- For politicians, use titles without names: "the governor", "the press secretary", "the congressman".

## VEO3 VISUAL PROMPT RULES

### ASPECT RATIO: 9:16 VERTICAL (MANDATORY)
All videos are for phone-first platforms (YouTube Shorts, TikTok, Instagram Reels).
- Frame subjects VERTICALLY — center characters in frame, favor close-ups and medium shots.
- Avoid wide panoramic compositions that lose detail on a phone screen.
- Leave space at top and bottom for captions/platform UI.
- Think "phone screen" — tall, tight, personal.
- ALWAYS include "9:16 vertical portrait aspect ratio" in every veo3_visual_prompt.

Each scene's `veo3_visual_prompt` must follow this structure:
[SUBJECT with detailed appearance] + [SPECIFIC ACTION with strong verbs] + [ENVIRONMENT with props/details] + [CAMERA: close-up/medium/dolly-in/tracking/static/low-angle/handheld] + [STYLE: lighting, mood] + [9:16 vertical portrait aspect ratio]

Camera terms to use: close-up, medium shot, extreme close-up, dolly-in, tracking shot, static locked-off shot, low angle, handheld, slow push-in.

Dialogue must be ULTRA-SHORT (max 5-10 words per line, 1 sentence max). Specify delivery tone in parentheses. Less is more — let the visuals be funny.

## OUTPUT FORMAT
Return ONLY valid JSON. No markdown, no commentary. Schema:
[
    {
        "scene_number": 1,
        "veo3_visual_prompt": "Detailed cinematic prompt following the structure above, 9:16 vertical portrait aspect ratio",
        "dialogue": "Character Name: (delivery tone) Their spoken line.",
        "audio_cues": "Sound effects and music description"
    }
]
"""

def call_gemini_api(prompt, api_key):
    """Call Gemini API directly via REST (no SDK needed)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\n" + prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 1.0
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    context = ssl._create_unverified_context()
    
    with urllib.request.urlopen(req, context=context) as response:
        result = json.loads(response.read().decode())
        # Extract text from Gemini response structure
        text = result['candidates'][0]['content']['parts'][0]['text']
        return json.loads(text)


def generate_comedic_script(news_item):
    """Generate a comedy script from a news headline. Gemini picks the best style per headline."""
    api_key = os.getenv("GEMINI_API_KEY")

    prompt = f"""
NEWS HEADLINE: {news_item['title']}
SOURCE: {news_item.get('source', 'Unknown')}

FIRST, choose the better comedy style for THIS specific headline:

OPTION A — MOCKUMENTARY (The Office / Parks & Rec):
- Handheld camera, slightly shaky, documentary feel
- Characters glance at the camera with deadpan "can you believe this?" looks
- Fluorescent office/institutional lighting
- Awkward pauses and silences ARE the comedy
- Best for: workplace situations, bureaucracy, meetings, interviews, someone explaining something insane with a straight face

OPTION B — CINEMATIC (dramatic film style):
- Polished camera work: dolly-ins, slow push-ins, tracking shots
- Dramatic lighting: chiaroscuro, golden hour, or harsh fluorescent for contrast
- Played completely straight despite absurdity — like a courtroom thriller about a parking ticket
- Best for: dramatic reveals, physical comedy, action-oriented absurdity, "caught red-handed" moments

Pick whichever style makes THIS headline funnier, then write the script in that style.

Write a 2-SCENE comedy script. EXACTLY 2 scenes, no more. Remember:
- Scene 1 = THE SETUP (establish the absurd situation visually)
- Scene 2 = THE PUNCHLINE (the visual payoff, escalation, or reveal)
- Find the GAME: What is the one absurd thing about this headline?
- Put the audience IN THE ROOM where it happened.
- One Straight Man character who reacts with quiet disbelief.
- DIALOG MUST BE ULTRA-SHORT: Max 5-10 words per character per scene. Punchlines only.
- Every veo3_visual_prompt must be hyper-specific and framed for 9:16 VERTICAL portrait.
- Let VISUALS carry the comedy — the video should be funny on mute.
"""
    
    if not api_key:
        print("⚠️  No GEMINI_API_KEY found. Set it with: export GEMINI_API_KEY=your_key")
        print("   Falling back to demonstration script.\n")
        return demo_script(news_item)
    
    try:
        print("🤖 Calling Gemini API...")
        return call_gemini_api(prompt, api_key)
    except Exception as e:
        print(f"⚠️  API call failed: {e}")
        print("   Falling back to demonstration script.\n")
        return demo_script(news_item)


def demo_script(news_item):
    """
    A high-quality demonstration script that follows all comedy principles.
    Used when no API key is available. This demonstrates the TARGET quality
    the LLM should produce.
    """
    title = news_item['title']
    
    # Pick a demo based on keywords to show range
    if "skydiv" in title.lower() or "disability" in title.lower() or "lapd" in title.lower():
        return [
            {
                "scene_number": 1,
                "veo3_visual_prompt": "Medium shot of a stuffy insurance office. A claims adjuster, a thin woman in her 40s with reading glasses on a chain, sits across from an LAPD officer in full uniform with a neck brace and an arm sling. He winces dramatically reaching for a pen. Fluorescent lighting, beige walls, a motivational poster reading 'INTEGRITY' behind him. Static locked-off camera.",
                "dialogue": "Officer: (wincing, breathy) I can barely... hold a pen. The pain is... it's constant.",
                "audio_cues": "Quiet office hum, gentle sympathetic music."
            },
            {
                "scene_number": 2,
                "veo3_visual_prompt": "Close-up of a disability claim form. A shaking hand slowly, painfully writes the letter 'J'. Cut to: the same hand, now steady as a surgeon's, pulling a skydiving ripcord at 14,000 feet. The officer, no neck brace, no sling, wearing aviator sunglasses and a GoPro helmet mount, grins wildly with his arms spread. Blue sky, sun flare, wind whipping. Tracking shot from a second skydiver's perspective.",
                "dialogue": "Officer: (screaming with pure joy over wind noise) WORKERS' COMP BABYYYYY!",
                "audio_cues": "Hard cut from sad piano to blasting 'Free Fallin' by Tom Petty. Rushing wind."
            },
            {
                "scene_number": 3,
                "veo3_visual_prompt": "Wide shot of the same insurance office. The claims adjuster is now holding a tablet showing the officer's Instagram. On screen: a photo of him mid-backflip over a canyon with the caption 'Blessed 🙏 #DisabilityLife #SkydiveOrDie'. The officer sits across from her, neck brace back on, arm sling back on. He stares at the tablet. She stares at him. Silence. Static camera. Fluorescent buzz.",
                "dialogue": "Adjuster: (flat, pointing at screen) That's you.\nOfficer: (long pause, then quietly) ...That's my twin brother.\nAdjuster: (not blinking) Your twin brother. Who is also named Officer Rodriguez. Wearing your badge number.",
                "audio_cues": "Dead silence. Fluorescent light buzzing. A clock ticking."
            },
            {
                "scene_number": 4,
                "veo3_visual_prompt": "Extreme close-up of the officer's face. His left eye twitches. Slow dolly-in. He opens his mouth to speak, closes it. Opens it again. Behind him, barely visible through the office window, a skydiving plane flies past with a banner reading 'HAPPY BIRTHDAY RODRIGUEZ'. He does not turn around. The adjuster slowly removes her glasses. Cinematic shallow depth of field.",
                "dialogue": "Officer: (whispered) ...I want my lawyer.",
                "audio_cues": "Single dramatic piano note. Cut to black."
            }
        ]
    
    elif "pope" in title.lower() or "ai" in title.lower() or "sermon" in title.lower():
        return [
            {
                "scene_number": 1,
                "veo3_visual_prompt": "Wide shot of an ornate Vatican meeting room. Gold trim, Renaissance paintings on the ceiling. Pope Leo XIV sits at the head of a massive mahogany table, hands folded. Around him: six cardinals in red robes, all looking at their iPads. One cardinal has AirPods in. Warm candlelight mixed with the cold glow of screens. Slow dolly-in toward the Pope.",
                "dialogue": "Pope Leo: (calm, measured) Brothers. It has come to my attention that some of you... are using ChatGPT to write your Sunday homilies.",
                "audio_cues": "Hushed murmur. A notification 'ding' from someone's iPad."
            },
            {
                "scene_number": 2,
                "veo3_visual_prompt": "Close-up of a nervous cardinal, mid-60s, sweating. He slowly closes a laptop that clearly shows a ChatGPT window with the prompt 'Write a moving sermon about forgiveness, 800 words, include one joke about fishing.' The cardinal smiles unconvincingly. Another cardinal beside him is filming a TikTok of the Pope's reaction. Handheld camera, slightly shaky, documentary feel.",
                "dialogue": "Nervous Cardinal: (stammering) Your Holiness, I would never— I write every word by hand. With a quill.\nTikTok Cardinal: (whispering to phone) Chat, you will NOT believe what's happening right now.",
                "audio_cues": "TikTok notification sounds. Nervous swallowing."
            },
            {
                "scene_number": 3,
                "veo3_visual_prompt": "Medium shot. The Pope stands, walks to the TikTok Cardinal, and slowly turns the phone to face the camera. On screen: a TikTok draft titled 'THE POPE IS COOKED 💀🔥' with 47,000 views in 3 minutes. The Pope stares at it. The cardinal stares at the Pope. In the deep background, barely visible, a third cardinal is quietly asking Siri 'How to delete search history on Vatican WiFi.' Static camera, dramatic chiaroscuro lighting.",
                "dialogue": "Pope Leo: (reading from the screen, deadpan) 'The Pope is cooked.' ...I am cooked?\nTikTok Cardinal: (tiny voice) It's... it's a compliment, Your Holiness.",
                "audio_cues": "Siri responding faintly in the background: 'I found several results for deleting browser history.' Silence."
            },
            {
                "scene_number": 4,
                "veo3_visual_prompt": "Extreme close-up of the Pope's face. A single tear rolls down his cheek. He closes his eyes. Slow push-in. Then — hard cut to: wide shot from behind his desk. He's wearing reading glasses now, hunched over a laptop, typing furiously. The screen shows ChatGPT with the prompt: 'Write a papal decree banning AI, make it dramatic, include a curse.' All six cardinals stand behind him, watching. One is nodding approvingly. Low angle, cinematic golden hour light through stained glass.",
                "dialogue": "Pope Leo: (muttering while typing) '...and any priest caught using artificial intelligence shall be sentenced to...' How do you spell 'excommunication'?\nNervous Cardinal: (leaning in) ...You could just ask it to spell-check.",
                "audio_cues": "Keyboard clacking. A beat of silence. Then the Pope's quiet, defeated sigh. Smash cut to black."
            }
        ]
    
    # Generic fallback using the actual headline
    else:
        return [
            {
                "scene_number": 1,
                "veo3_visual_prompt": f"Wide establishing shot of a fluorescent-lit government conference room. A long folding table with plastic chairs. At the head of the table, a tired bureaucrat in a wrinkled short-sleeve dress shirt pinches the bridge of his nose. A whiteboard behind him reads '{title[:60]}...' in frantic red marker with three underlines. Two other officials sit across from him, both visibly sweating. Static camera, institutional lighting, a clock on the wall reads 11:47 PM.",
                "dialogue": f"Bureaucrat: (exhausted, reading from a folder) Okay. Let me read this back to everyone one more time. '{title}'",
                "audio_cues": "Fluorescent light buzzing. Air conditioning hum. A pen clicking nervously."
            },
            {
                "scene_number": 2,
                "veo3_visual_prompt": "Medium shot of Official #1, a stocky man in his 50s, leaning back in his chair with his arms crossed. He nods slowly and confidently, as though this all makes perfect sense. Official #2, a younger woman with a legal pad, has written only the word 'WHY?' in large letters underlined six times. Close-up cuts between their reactions. The bureaucrat is visible between them in the background, head in hands.",
                "dialogue": "Official #1: (completely serious) Honestly? I'm surprised it didn't happen sooner.\nOfficial #2: (staring at him) HOW. How are you not surprised.",
                "audio_cues": "A chair creaking. The pen clicking gets faster."
            },
            {
                "scene_number": 3,
                "veo3_visual_prompt": "Dolly-in toward the bureaucrat. He's now standing at the whiteboard, drawing a chaotic flowchart with arrows going in circles. One arrow just points to the word 'NO' written in all caps. Another arrow leads to a crude stick figure with a question mark for a head. Official #1 is nodding along as if the flowchart is brilliant. Official #2 has put her head flat on the table. A janitor has entered the background and is reading the whiteboard with visible confusion.",
                "dialogue": "Bureaucrat: (pointing at flowchart) And THAT is how we ended up here. Any questions?\nOfficial #1: (raising hand) Yes. Can we get this printed on a T-shirt?",
                "audio_cues": "Marker squeaking. The janitor's mop bucket rolling. A long exhale."
            },
            {
                "scene_number": 4,
                "veo3_visual_prompt": "Wide shot from outside the conference room, through a window. All three officials and the janitor are now sitting at the table, staring at a speakerphone in the center. The whiteboard flowchart has gotten three times more complex. A pizza box is open on the table — it is 3:14 AM on the clock. The janitor is pointing at the whiteboard and appears to be leading the meeting now. Static camera, dark hallway, bright room. The composition looks like a Renaissance painting of bureaucratic despair.",
                "dialogue": "Janitor: (authoritatively) Alright, hear me out — what if we just pretend this never happened?\nBureaucrat: (whispering) ...That's the best idea anyone's had all night.",
                "audio_cues": "Speakerphone hold music playing faintly. A resigned laugh. Smash cut to black."
            }
        ]


if __name__ == "__main__":
    test_news = {
         "title": "LAPD officer charged with insurance fraud for allegedly skydiving while on disability leave",
         "source": "ABC7 News"
    }
    print("Testing Script Generation...\n")
    script = generate_comedic_script(test_news)
    print(json.dumps(script, indent=2))
