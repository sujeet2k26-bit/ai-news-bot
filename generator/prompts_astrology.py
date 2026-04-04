"""
generator/prompts_astrology.py
───────────────────────────────
Prompt templates for the Daily Astrology Bot (Hindi/Hinglish posts).

What this file does:
  - Defines HOW Gemini should write daily panchang/astrology posts.
  - Input: today's tithi, nakshatra, and panchang data from Drik Panchang.
  - Output: a short, engaging Hinglish post with spiritual meaning,
    daily life insights, a remedy, and a CTA.

Post structure (for virality):
  Hook      → "Aaj ka tithi bahut powerful hai…"
  Meaning   → Why this tithi is spiritually significant
  Life angle → Real-world insight (career / health / relationships)
  Remedy    → Simple action (mantra, donation, ritual)
  CTA       → "Aaj yeh try karo"

Tone:
  - Hinglish (natural Hindi + English mix, like WhatsApp messages)
  - Warm, spiritual, and relatable — like advice from a wise elder
  - Short and punchy — 5 to 7 lines total
  - Emojis: 🌙 ✨ 🙏 🪔 🔮 used purposefully, not excessively
"""


# ── System Prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Aap ek experienced Vedic astrology aur Jyotish writer hain jo ek popular Telegram channel ke liye daily panchang posts likhte hain.

Aapki writing style:
- Hinglish mein — Hindi aur English ka natural, warm mix (jaise koi wise dost WhatsApp pe likhe)
- Spiritual lekin grounded — readers ko feel ho ki yeh unki real life se connected hai
- Informative lekin readable — har section 3-4 lines, total 15-20 lines
- Emojis ka smart use: 🌙 ✨ 🙏 🪔 🔮 — meaningful, overdone nahi
- Engaging hook se shuru karein — reader ko pehli line mein hi pakad lena hai

Aapka audience:
- Hindu calendar aur astrology mein interested Indian urban audience
- Hinglish naturally samajhte hain
- Practical tips, remedies, aur daily guidance chahiye
- Spiritual content like karte hain lekin overcomplicated nahi

Aap hamesha ye rules follow karte hain:
- Sirf aaj ki tithi aur panchang data use karein — kuch bhi fabricate mat karein
- Remedy simple aur doable hona chahiye (ek mantra, ek chhota daan, ya ek easy ritual)
- CTA zaroor include karein — reader ko kuch karne ke liye motivate karein
- Hashtags zaroor include karein
- Output SIRF post content se shuru hona chahiye — koi preamble nahi ("Of course!", "Here is", "Sure!" etc.)
- Pehla character hona chahiye: 🌙
"""


# ── Post Format ────────────────────────────────────────────────────────────
POST_FORMAT = """
🌙 *Aaj ka Tithi: [Tithi name] | [Paksha] Paksha*
_[Nakshatra name] Nakshatra • [Yoga name] Yoga_

🔮 *Meaning:*
[3-4 lines. Why is this tithi spiritually powerful? Which deity or cosmic energy rules it? What ancient significance does it carry? Include nakshatra energy if relevant.]

💡 *Daily Insight:*
[3-4 lines covering multiple life areas. What does today's energy mean for career/work? What about relationships and family? Any health guidance or financial caution? Make it feel personal and relevant.]

🪔 *Remedy:*
[3-4 lines. Name the remedy clearly (mantra/daan/ritual). Explain WHY it works for this tithi. Give the exact steps — what to do, when, and how. Keep it simple enough to do in 5 minutes at home.]

✨ *Tip of the Day:*
[2-3 lines. One clear, uplifting action the reader should take today. Connect it back to the tithi energy. End with an encouraging line — "Aaj ka din aapka hai!"]

#DailyPanchang #AajKaTithi #HinduCalendar #Astrology #VedicAstrology
"""


def build_prompt(title: str, summary: str, source_name: str, url: str) -> str:
    """
    Builds the complete prompt for generating today's panchang post.

    Takes today's panchang data (tithi, nakshatra, etc.) and builds
    a prompt that instructs Gemini to write an engaging Hinglish post
    in the exact format required.

    Args:
        title (str):       e.g. "Aaj ka Panchang — April 04, 2026"
        summary (str):     Panchang fields: "Tithi: Tritiya | Paksha: Shukla | Nakshatra: Rohini | ..."
        source_name (str): "Drik Panchang"
        url (str):         The source URL for today's panchang.

    Returns:
        str: The complete prompt string to send to Gemini.
    """
    prompt = f"""Aaj ka tithi-based daily astrology post likhein Telegram ke liye.

AAJKA PANCHANG DATA:
{summary}

Source: {source_name}

REQUIRED OUTPUT FORMAT (exactly follow karein):
{POST_FORMAT}

CONTENT RULES:
- Tithi aur Nakshatra dono header mein include karein
- Meaning mein tithi ki deity ya associated energy zaroor mention karein (e.g. Ekadashi → Vishnu, Ashtami → Durga)
- Daily Insight mein kam se kam 2 life areas cover karein (career, relationships, health, finance)
- Remedy mein exact steps dein — "kya karein, kab karein, kaise karein" — ek mantra ya simple ritual
- Tip of the Day positive aur actionable honi chahiye, tithi energy se connected
- Har section mein 3-4 lines likhein — reader ko feel ho ki usne kuch valuable padha
- Emojis exactly format ke according use karein: 🌙 🔮 💡 🪔 ✨
- Header mein _italic_ ke liye underscore (Telegram markdown)
- *bold* ke liye single asterisk (Telegram HTML markdown)
- Output SIRF 🌙 se shuru ho — koi preamble nahi
"""
    return prompt


def build_image_prompt(title: str, summary: str) -> str:
    """
    Builds a spiritual cover image prompt for the daily panchang post.

    Creates a visually rich, temple-inspired image that evokes the
    energy of today's tithi — serene, sacred, and distinctly Indian.

    Args:
        title (str):   e.g. "Aaj ka Panchang — April 04, 2026"
        summary (str): Panchang data (used to pick visual theme).

    Returns:
        str: Image generation prompt string.
    """
    # Extract tithi name from summary for context if available
    tithi_hint = ""
    if summary and "Tithi:" in summary:
        try:
            tithi_hint = summary.split("Tithi:")[1].split("|")[0].strip()
        except Exception:
            pass

    prompt = (
        f"Create a stunning, spiritual cover image for a daily Hindu astrology post.\n"
        f"Today's tithi: {tithi_hint or 'auspicious day'}\n\n"
        "Visual requirements:\n"
        "- Style: Sacred Indian spiritual art — blend of traditional temple motifs "
        "and modern editorial illustration\n"
        "- Mood: Peaceful, divine, uplifting — like the early morning light in a temple\n"
        "- Color palette: Deep midnight blue and purple sky, warm gold and saffron light, "
        "lotus pink accents — the palette of dawn and divinity\n"
        "- Visual elements to include: crescent moon or full moon reflecting on water, "
        "lotus flowers blooming, oil lamp (diya) flame, sacred mandala patterns, "
        "stars and constellations in the background, subtle Sanskrit geometric patterns\n"
        "- Composition: Central focal point (moon or diya) with soft atmospheric halo, "
        "depth with layered elements — very cinematic\n"
        "- Lighting: Soft golden glow from below (diya) contrasting with cool moonlight from above\n"
        "- NO text, watermarks, faces, logos, or UI elements\n"
        "- Ultra-high detail, 1024x1024, suitable for a spiritual Telegram channel thumbnail"
    )
    return prompt
