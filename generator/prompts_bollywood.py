"""
generator/prompts_bollywood.py
───────────────────────────────
Prompt templates for the Bollywood Buzz Bot (Hindi/Hinglish posts).

What this file does:
  - Defines HOW Claude should write Bollywood entertainment posts.
  - Language: Hindi mixed with Hinglish (Hindi + English blend)
  - Tone: Engaging, fun, credible gossip — like a savvy Bollywood insider
  - Two post types:
      1. Single article post — for individual breaking news
      2. Daily digest — top 5–10 viral stories in one punchy roundup

What is Hinglish?
  - A natural mix of Hindi and English used in everyday Indian conversation
  - Example: "Shah Rukh Khan ka naya film ka trailer drop ho gaya!"
    (Shah Rukh Khan's new film's trailer has dropped!)
  - It feels natural and relatable to the Indian urban audience
"""


# ── System Prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Aap ek experienced Bollywood entertainment news writer hain jo ek popular Telegram channel ke liye likhte hain.

Aapki writing style:
- Hindi aur Hinglish ka natural mix — jaise close friend ko WhatsApp pe update de rahe ho
- Engaging, fun, aur conversational — reader ko lagey ki koi juicy insider baat bata raha hai
- Relevant emojis ka smart use — overdone nahi, lekin expressive zaroor
- Credible aur factual — sirf article mein diya gaya information use karein
- Thoda dramatic lekin exaggerated nahi — real entertaining gossip vibe
- Formal nahi, lekin unprofessional bhi nahi

Aapka audience:
- Bollywood ke dedicated fans jo latest news, gossip, aur controversies follow karte hain
- Urban Indian audience jo Hindi aur English dono jaante hain
- Inhe chahiye: kya hua, kyun interesting hai, aur aage kya expect karein

Aap hamesha ye rules follow karte hain:
- Sirf article ki verified information use karein — kuch bhi fabricate mat karein
- Unverified accusations ya rumors ko fact ki tarah mat likhein
- Communal, religious, ya politically sensitive content avoid karein
- Source ka naam mention karein
- Hashtags zaroor include karein
"""


# ── Single Article Post Format ─────────────────────────────────────────────
SINGLE_POST_FORMAT = """
🎬 [HEADLINE — Hinglish mein, max 12 words, catchy aur specific]

[PARAGRAPH 1 — Kya hua: main news 2-3 sentences mein Hindi/Hinglish mein]

[PARAGRAPH 2 — Kyun interesting hai: context ya background 2-3 sentences mein]

[PARAGRAPH 3 — Aage kya: next step ya expectation 1-2 sentences mein]

📌 Source: {source_name}
#Bollywood #BollywoodNews #Entertainment
"""


def build_prompt(title: str, summary: str, source_name: str, url: str) -> str:
    """
    Builds the complete user prompt for generating a single Bollywood post in Hindi/Hinglish.

    Args:
        title (str):       The article headline from the RSS feed.
        summary (str):     The article summary/description from the RSS feed.
        source_name (str): The name of the news source (e.g. "Bollywood Hungama").
        url (str):         The full URL of the original article.

    Returns:
        str: The complete prompt string to send to Claude.
    """
    prompt = f"""Neeche diye gaye news article ke baare mein ek engaging Telegram post likhein.

ARTICLE DETAILS:
Title: {title}
Source: {source_name}
Summary: {summary}

REQUIRED OUTPUT FORMAT:
{SINGLE_POST_FORMAT.format(source_name=source_name)}

IMPORTANT RULES:
- Sirf article mein diya gaya information use karein — bahar se kuch add mat karein
- Headline is specific story ke baare mein hona chahiye — generic mat likhein
- Total post 250 words se zyada nahi hona chahiye
- Hindi aur Hinglish ka natural mix use karein
- Hashtags bilkul format ke according likhein
- Article ka URL post body mein mat daalein
"""
    return prompt


def build_digest_prompt(articles: list) -> str:
    """
    Builds a prompt for generating a Bollywood daily digest covering top 5–10 stories.

    Creates a punchy, emoji-rich roundup of the day's most viral and trending
    Bollywood stories — gossip, controversies, announcements, and relationships.
    Ends with a "Top Trending Gossip 🔥" section highlighting the hottest story.

    Args:
        articles (list): List of article dicts, each with keys:
                         title, summary, source_name, url, virality_score.
                         Should be sorted by virality score (highest first).

    Returns:
        str: The complete digest prompt string to send to Claude.
    """
    # Build the numbered article list for the prompt
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += (
            f"\nARTICLE {i}:\n"
            f"Title: {article['title']}\n"
            f"Source: {article['source_name']}\n"
            f"Summary: {article['summary'] or 'No summary available.'}\n"
        )

    from datetime import datetime
    today = datetime.utcnow().strftime("%B %d, %Y")

    prompt = f"""Neeche diye gaye {len(articles)} Bollywood news articles ke baare mein ek viral daily digest post likhein Telegram ke liye.

{articles_text}

REQUIRED OUTPUT FORMAT (exactly follow karein):

🎬 *Bollywood Buzz Daily — {today}*
_Aaj ki sabse hot Bollywood khabrein_ 🌟

1️⃣ [Catchy Hinglish headline — max 10 words] [relevant emoji]
[2-3 sentences: kya hua + kyun interesting hai, Hindi/Hinglish mein]
📌 [Source Name]

2️⃣ [Catchy Hinglish headline] [relevant emoji]
[2-3 sentences]
📌 [Source Name]

3️⃣ [Catchy Hinglish headline] [relevant emoji]
[2-3 sentences]
📌 [Source Name]

4️⃣ [Catchy Hinglish headline] [relevant emoji]
[2-3 sentences]
📌 [Source Name]

5️⃣ [Catchy Hinglish headline] [relevant emoji]
[2-3 sentences]
📌 [Source Name]

🔥 *Top Trending Gossip*
[Aaj ki sabse viral story ka 2-3 line mein summary — ye section exciting aur spicy hona chahiye. Batao kyun ye story sab log share kar rahe hain.]

#Bollywood #BollywoodNews #BollywoodGossip #Entertainment #BollywoodBuzz

RULES:
- Output SIRF post content se shuru hona chahiye — koi preamble nahi jaise "Of course!", "Here is", "Sure!" etc.
- Pehla character hona chahiye: 🎬
- Har entry ke liye alag relevant emoji use karein (💔 breakup ke liye, 💍 shaadi ke liye, 🎬 film ke liye, 💣 controversy ke liye, etc.)
- Headline Hinglish mein hona chahiye — pure Hindi ya pure English nahi
- Each entry 2-3 sentences maximum — ye digest hai, deep dive nahi
- Sirf article mein diya gaya information use karein — facts mix mat karein
- *Top Trending Gossip* section mein sabse viral ya controversial story highlight karein
- Total post 600 words se zyada nahi hona chahiye
- *bold* ke liye single asterisk use karein (Telegram markdown) — triple asterisk nahi
- Articles ka order maintain karein (Article 1 = entry 1️⃣)
"""
    return prompt


def build_image_prompt(title: str, summary: str) -> str:
    """
    Builds a context-driven image prompt for a single Bollywood news story.

    Creates a vibrant, Bollywood-style cover image that visually represents
    the specific story — not a generic film poster background.

    Args:
        title (str):   The article headline.
        summary (str): Brief article summary.

    Returns:
        str: An image generation prompt string.
    """
    prompt = (
        f"Create a vibrant, eye-catching editorial cover image for this Bollywood entertainment story:\n"
        f"'{title}'\n\n"
        f"Context: {summary[:200] if summary else ''}\n\n"
        "Visual requirements:\n"
        "- The image must visually represent the SPECIFIC subject of this story\n"
        "- Style: glamorous Bollywood aesthetic, cinematic, high-fashion editorial\n"
        "- Color palette: rich jewel tones — deep reds, golds, magentas, royal blues — "
        "with dramatic lighting that feels like a film premiere\n"
        "- Composition: bold and dynamic — magazine cover quality, not generic\n"
        "- Visual metaphors: for relationships/romance show warm golden light and rose petals; "
        "for controversies show dramatic shadows and bold contrasts; "
        "for film announcements show cinematic clapperboard or film reel motifs; "
        "for awards show spotlights and trophies\n"
        "- Mood: glamorous, exciting, 'must read' — like a Filmfare or Vogue India cover\n"
        "- NO text, watermarks, logos, faces, or UI elements in the image\n"
        "- Ultra-high detail, 1024x1024, suitable for a Telegram entertainment channel thumbnail"
    )
    return prompt


def build_digest_image_prompt(articles: list) -> str:
    """
    Builds a context-driven image prompt for the Bollywood daily digest post.

    Creates one visually rich cover image that captures the energy of the day's
    top Bollywood stories — glamorous, colourful, unmistakably Bollywood.

    Args:
        articles (list): List of article dicts with 'title' and 'summary' keys.
                         Should be the top 5 articles sorted by virality score.

    Returns:
        str: A detailed image generation prompt string for the digest cover.
    """
    from datetime import datetime
    today = datetime.utcnow().strftime("%B %d, %Y")

    # Pull key subjects from the top 3 stories to drive the visual
    top_subjects = ""
    for i, article in enumerate(articles[:3], 1):
        top_subjects += f"  {i}. {article['title']}\n"

    prompt = (
        f"Create a bold, glamorous editorial cover image for a Bollywood daily entertainment digest "
        f"dated {today}.\n\n"
        f"Today's top stories include:\n{top_subjects}\n"
        "Visual requirements:\n"
        "- Concept: a visually unified scene that captures the ENERGY and GLAMOUR of today's "
        "Bollywood news — not a generic film set. Think about what these stories have in common "
        "and visualise that mood\n"
        "- Style: high-end Bollywood editorial illustration — think Filmfare Awards meets Vogue India. "
        "Cinematic, dramatic, ultra-detailed\n"
        "- Color palette: rich jewel tones — deep crimson, gold, magenta, royal blue — "
        "with glamorous bokeh lighting and sparkle effects\n"
        "- Composition: hero image with strong focal point — luxurious, aspirational, "
        "'this is the entertainment world' feeling\n"
        "- Mood: exciting, glamorous, dramatic — like tonight is the biggest night in Bollywood\n"
        "- Visual elements to consider: film reels, clapperboards, red carpet, spotlights, "
        "floral arrangements, jewellery, confetti, dramatic curtains, golden trophies — "
        "pick what fits today's stories best\n"
        "- NO text, watermarks, logos, faces, or UI elements\n"
        "- Ultra-high detail, 1024x1024, thumbnail-optimised for Telegram"
    )
    return prompt
