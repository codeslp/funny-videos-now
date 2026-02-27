import urllib.request
import json
import ssl
import os
import re

# Load .env
def _load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())

try:
    import feedparser
except ImportError:
    feedparser = None

# ─── CONTENT GUARDRAILS ─────────────────────────────────────────

BANNED_WORDS = [
    # Violence & death
    "murder", "kill", "death", "dead", "died", "suicide", "rape", "assault",
    "shooting", "shooter", "massacre", "stabbing", "execution", "homicide",
    "manslaughter", "bloodshed", "bomb", "bombing", "explosion",
    # Sexual content
    "sexual", "porn", "nude", "naked",
    # Child safety (Veo hard-blocks these)
    "child abuse", "child labor", "child labour", "minors", "pedophile",
    "underage", "trafficking children",
    # Hate speech
    "racist", "slur", "nazi", "hitler", "holocaust", "white supremac",
    "hate crime",
    # Drugs
    "drugs", "cocaine", "heroin", "meth", "fentanyl", "overdose",
    # Terrorism
    "terrorist", "terrorism", "isis", "al qaeda", "jihad",
    # Religion (avoid making fun of religion per user preference)
    "pope", "priest", "pastor", "sermon", "church scandal", "mosque",
    "imam", "rabbi", "fatwa",
    # Sensitive international topics (Veo filters these)
    "war crime", "genocide", "ethnic cleansing", "concentration camp",
    "slave", "slavery",
]

BANNED_TOPICS = [
    "child labor", "child labour", "minors working", "underage work",
    "school shooting", "mass shooting", "serial killer",
    "religious leader", "church abuse",
]

def is_safe_content(text):
    """Returns True if the text does NOT contain any banned words or topics."""
    if not text:
        return True
    text_lower = text.lower()
    for word in BANNED_WORDS:
        if word in text_lower:
            return False
    for topic in BANNED_TOPICS:
        if topic in text_lower:
            return False
    return True


# ─── NEWS SOURCES ────────────────────────────────────────────────

def fetch_absurd_news():
    """Fetches top stories from r/nottheonion."""
    url = "https://www.reddit.com/r/nottheonion/top.json?t=day&limit=15"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) auto-video-pipeline/1.0'}
    )
    context = ssl._create_unverified_context()

    news_items = []
    try:
        with urllib.request.urlopen(req, context=context) as response:
            data = json.loads(response.read().decode())
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                if post.get('stickied'):
                    continue
                title = post.get('title')
                if is_safe_content(title):
                    news_items.append({
                        "title": title,
                        "url": post.get('url'),
                        "score": post.get('score', 0),
                        "source": "Reddit - r/nottheonion"
                    })
    except Exception as e:
        print(f"  ⚠️  Error fetching Reddit news: {e}")
    return news_items


def fetch_ap_oddities():
    """
    Fetches oddity/weird news from AP News RSS feed.
    These are professionally written, absurd-but-real stories — perfect for comedy.
    """
    rss_url = "https://rsshub.app/apnews/topics/oddities"
    # Fallback: try AP's own feed format
    fallback_urls = [
        "https://news.google.com/rss/search?q=site:apnews.com+oddities&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=%22oddities%22+OR+%22weird+news%22+OR+%22bizarre%22&hl=en-US&gl=US&ceid=US:en",
    ]

    news_items = []

    # Try feedparser first
    if feedparser:
        for url in [rss_url] + fallback_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:15]:
                    title = entry.title
                    link = entry.link
                    if is_safe_content(title):
                        news_items.append({
                            "title": title,
                            "url": link,
                            "score": 0,
                            "source": "AP News Oddities"
                        })
                if news_items:
                    break
            except Exception:
                continue

    # If feedparser failed or unavailable, scrape AP directly
    if not news_items:
        try:
            req = urllib.request.Request(
                "https://apnews.com/oddities",
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            )
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=context) as response:
                html = response.read().decode()
                # Extract headlines from AP News HTML
                # AP uses links like /article/... with headline text
                matches = re.findall(
                    r'<a[^>]*href="(/article/[^"]+)"[^>]*>([^<]+)</a>',
                    html
                )
                seen = set()
                for path, title in matches:
                    title = title.strip()
                    if len(title) > 30 and title not in seen and is_safe_content(title):
                        seen.add(title)
                        news_items.append({
                            "title": title,
                            "url": f"https://apnews.com{path}",
                            "score": 0,
                            "source": "AP News Oddities"
                        })
                    if len(news_items) >= 15:
                        break
        except Exception as e:
            print(f"  ⚠️  Error fetching AP News: {e}")

    return news_items


def fetch_florida_man_news():
    """Fetches recent Florida Man stories from Google News RSS."""
    if not feedparser:
        return []

    rss_url = "https://news.google.com/rss/search?q=Florida+Man&hl=en-US&gl=US&ceid=US:en"
    news_items = []
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:10]:
            title = entry.title
            if is_safe_content(title):
                news_items.append({
                    "title": title,
                    "url": entry.link,
                    "score": 0,
                    "source": "Google News - Florida Man"
                })
    except Exception as e:
        print(f"  ⚠️  Error fetching Florida Man news: {e}")
    return news_items


# ─── VISUAL COMEDY SCORER (Gemini-powered) ───────────────────────

SCORING_PROMPT = """You are a comedy video producer. Rate each news headline on how well it works as a SHORT-FORM COMEDY VIDEO (15-60 seconds for TikTok/YouTube Shorts).

Score each headline 1-10 on these criteria:
1. VISUAL POTENTIAL (1-10): Can you picture a funny scene? Is there a clear visual situation?
2. ONE-LINER POTENTIAL (1-10): Can the punchline land in under 10 words?
3. VEO-SAFE (1-10): No real celebrities, no violence, no religion, no children at risk? (10 = totally safe)
4. UNIVERSALITY (1-10): Will a general audience immediately get the joke without context?

Return ONLY valid JSON array. Each item:
{"title": "exact headline", "visual": N, "oneliner": N, "veo_safe": N, "universal": N, "total": N, "pitch": "One sentence describing the visual comedy scene"}

Headlines to score:
"""


def score_stories_with_gemini(news_items):
    """
    Uses Gemini to score news stories by visual comedy potential.
    Returns the items sorted by total score (highest first).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  ⚠️  No GEMINI_API_KEY — skipping AI scoring, returning unsorted.")
        return news_items

    # Build the headlines list for scoring
    headlines = "\n".join([f"- {item['title']}" for item in news_items[:25]])  # Cap at 25
    prompt = SCORING_PROMPT + headlines

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.3
        }
    }

    context = ssl._create_unverified_context()
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            result = json.loads(response.read().decode())
            text = result['candidates'][0]['content']['parts'][0]['text']
            scores = json.loads(text)

        # Build a lookup by title
        score_lookup = {}
        for s in scores:
            score_lookup[s['title']] = s

        # Merge scores back into news items
        scored_items = []
        for item in news_items:
            s = score_lookup.get(item['title'], {})
            item['visual_score'] = s.get('visual', 0)
            item['oneliner_score'] = s.get('oneliner', 0)
            item['veo_safe_score'] = s.get('veo_safe', 0)
            item['universal_score'] = s.get('universal', 0)
            item['total_comedy_score'] = s.get('total', 0)
            item['pitch'] = s.get('pitch', '')
            scored_items.append(item)

        # Sort by total comedy score (highest first)
        scored_items.sort(key=lambda x: x.get('total_comedy_score', 0), reverse=True)
        return scored_items

    except Exception as e:
        print(f"  ⚠️  Gemini scoring failed: {e}")
        return news_items


# ─── MAIN PIPELINE ───────────────────────────────────────────────

def fetch_all_curated_news(score=True):
    """
    Fetches from all sources, applies safety filters, and optionally
    scores stories by visual comedy potential using Gemini.
    """
    print("  📡 Fetching from Reddit r/nottheonion...")
    reddit_news = fetch_absurd_news()
    print(f"     Found {len(reddit_news)} safe stories")

    print("  📡 Fetching from AP News Oddities...")
    ap_news = fetch_ap_oddities()
    print(f"     Found {len(ap_news)} safe stories")

    print("  📡 Fetching Florida Man stories...")
    florida_news = fetch_florida_man_news()
    print(f"     Found {len(florida_news)} safe stories")

    combined = reddit_news + ap_news + florida_news

    # Deduplicate by title similarity
    seen_titles = set()
    unique = []
    for item in combined:
        short_title = item['title'][:50].lower()
        if short_title not in seen_titles:
            seen_titles.add(short_title)
            unique.append(item)

    if score and unique:
        print(f"\n  🤖 Scoring {len(unique)} stories with Gemini for visual comedy potential...")
        unique = score_stories_with_gemini(unique)

    return unique


if __name__ == "__main__":
    _load_env()
    print("\n" + "=" * 60)
    print("  🕵️  SMART NEWS SCOUT  🕵️")
    print("=" * 60 + "\n")

    news = fetch_all_curated_news(score=True)

    if not news:
        print("No valid news found.")
    else:
        print(f"\n{'─' * 60}")
        print(f"  📊 TOP {min(len(news), 10)} STORIES BY VISUAL COMEDY POTENTIAL")
        print(f"{'─' * 60}\n")

        for i, item in enumerate(news[:10], 1):
            total = item.get('total_comedy_score', '?')
            visual = item.get('visual_score', '?')
            oneliner = item.get('oneliner_score', '?')
            safe = item.get('veo_safe_score', '?')
            pitch = item.get('pitch', '')

            print(f"  {i}. [{item['source'][:15]}] {item['title']}")
            print(f"     🎬 Visual:{visual} | 💬 OneLiner:{oneliner} | 🛡️ Safe:{safe} | ⭐ TOTAL: {total}")
            if pitch:
                print(f"     💡 Pitch: {pitch}")
            print()
