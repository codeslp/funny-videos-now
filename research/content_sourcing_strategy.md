# Content Sourcing Strategy: Finding the Perfect Headlines

## The Ideal Headline Profile
Not every news story makes a good comedy video. We're looking for a very specific type:

### ✅ What We Want
| Criteria | Why |
|---|---|
| **Absurd but real** | The humor is that this *actually happened* |
| **Behind closed doors** | No existing footage → we create the visual |
| **Clear human characters** | We need people to put "in the room" |
| **Low stakes / victimless** | Nobody got seriously hurt; it's safe to laugh |
| **Self-contained premise** | Explainable in one sentence; no context needed |

### ❌ What We Avoid
| Criteria | Why |
|---|---|
| Tragedy, violence, death | Not funny. Will get us banned. |
| Political partisanship | Alienates half the audience |
| Anything involving minors | Absolute no-go |
| Stories requiring deep context | Short-form doesn't have time to explain |
| Celebrity gossip / personal drama | Legal risk, not our lane |

---

## Source 1: Reddit r/nottheonion (Primary)
- **What it gives us:** Real news headlines that read like satire. Pre-curated by the community (upvotes = validation of absurdity).
- **Endpoint:** `https://www.reddit.com/r/nottheonion/top.json?t=day&limit=15`
- **Freshness:** Top posts from the last 24 hours.
- **Signal:** Reddit score indicates how many people found it absurd enough to upvote.

## Source 2: Google News RSS — "Florida Man" (Supplemental)
- **What it gives us:** A goldmine of bizarre local news from Florida, which has an unusually high rate of absurd public records due to Florida's open government ("Sunshine") laws.
- **Endpoint:** `https://news.google.com/rss/search?q=Florida+Man&hl=en-US&gl=US&ceid=US:en`
- **Freshness:** Rolling recent articles.
- **Signal:** Google News ranking; look for stories that are covered by multiple outlets (higher virality).

## Future Sources to Consider
| Source | What It Offers | API/Method |
|---|---|---|
| **GDELT Project** | Global event monitoring, updated every 15 min | Free API |
| **Google Trends** | Trending search queries in real-time | SerpAPI / unofficial |
| **Exploding Topics** | Emerging trends with growth data | Paid API |
| **NewsWhip Spike** | Predicts virality with AI scoring | Paid |
| **X/Twitter Trending** | Real-time meme culture | Paid API (v2) |
| **TikTok Trending** | Visual meme trends | Third-party scrapers |

---

## Content Moderation / Banned Topics

### Banned Word List (Applied Pre-Script)
Every headline is filtered through `is_safe_content()` before it reaches the script generator. Headlines containing any of the following terms are **automatically dropped:**

> murder, kill, death, dead, died, suicide, rape, assault, sexual, child abuse, terrorist, terrorism, bomb, shooting, shooter, massacre, racist, slur, nazi, hitler, holocaust, pedophile, drugs, cocaine, heroin, meth, fentanyl, dung, excrement, poop, feces

### Platform Policy Awareness
Most short-form video platforms (YouTube Shorts, TikTok, Instagram Reels) will suppress or ban content that:
- Depicts or glorifies violence
- Contains hate speech or discrimination
- Shows drug use or substance abuse
- Involves minors in any negative context
- Contains misinformation presented as fact
- Uses copyrighted music/footage without license

### Our Safety Philosophy
> **If you have to ask "is this okay?", it's not okay.** Default to safe. There are enough absurd, harmless, hilarious headlines every single day. We never need to touch a risky one.

---

## The SNL Model: How Topical Comedy Gets Written Fast

We draw direct inspiration from SNL's Weekend Update process:

1. **Continuous monitoring:** Writers track news all week, not just once.
2. **Speed to script:** Jokes are written the same day as the news event.
4. **Point of view matters:** The best topical comedy has a clear "take" on the situation — not just restating what happened, but framing *why* it's absurd.
5. **Character-driven segments:** The funniest bits are the characters reacting to the news with a strong, exaggerated perspective.

### Applied to Our Pipeline
- Our "writers room" is the LLM.
- Our "rehearsal" is reviewing the script output before sending to Veo3.
- Our "character segments" are the people we put "in the room where it happened."
