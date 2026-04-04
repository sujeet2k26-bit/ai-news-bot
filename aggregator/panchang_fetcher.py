"""
aggregator/panchang_fetcher.py
───────────────────────────────
Fetches today's Hindu Panchang (tithi, nakshatra, etc.) from Drik Panchang
and creates an Article record in the DB for the Astrology bot to use.

What this file does:
  - Scrapes today's panchang data from drikpanchang.com (tithi, nakshatra,
    yoga, karana, paksha, vara, sunrise/sunset, festivals if any)
  - Falls back to a date-only article if scraping fails — the AI can then
    calculate the panchang from the date itself
  - Saves the panchang data as an Article in the DB (bot_id='astrology')
  - Returns the Article object ready for generate_and_save_post()

Why scrape instead of an API?
  - Drik Panchang has no free public API
  - Their web page is the most accurate free panchang source
  - BeautifulSoup parses the key fields from the HTML table

How to use:
  >>> from aggregator.panchang_fetcher import get_today_panchang_article
  >>> article = get_today_panchang_article()
  >>> if article:
  ...     print(article.summary)  # panchang fields as a string
"""

import logging
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

from db.database import get_session
from db.models import Article

logger = logging.getLogger(__name__)

# IST timezone for date calculation
IST = timezone(timedelta(hours=5, minutes=30))

# Drik Panchang daily panchang URL — date format is MM/DD/YYYY
DRIK_URL = "https://www.drikpanchang.com/panchang/day-panchang.html"

# Reference sources shown in the post
SOURCE_NAME = "Drik Panchang"

# Panchang fields we want to extract, in display order
PANCHANG_FIELDS = [
    "Tithi", "Paksha", "Nakshatra", "Yoga", "Karana",
    "Vara", "Sunrise", "Sunset", "Festival"
]


def get_today_panchang_article() -> "Article | None":
    """
    Fetches today's panchang and returns it as an Article DB object.

    This is the main function called by the pipeline for the astrology bot.
    It scrapes Drik Panchang for today's IST date. If scraping fails,
    it falls back to a date-only article so the AI can calculate
    the panchang from the date.

    Returns:
        Article: A saved Article object with panchang data in the summary field.
        None:    If the DB save failed.
    """
    now_ist = datetime.now(IST)
    date_str     = now_ist.strftime("%m/%d/%Y")       # for URL: 04/04/2026
    display_date = now_ist.strftime("%B %d, %Y")       # for title: April 04, 2026

    # Try to scrape live panchang data
    panchang_summary = _scrape_drik_panchang(date_str)

    if panchang_summary:
        logger.info("Panchang data fetched successfully for %s", display_date)
    else:
        # Fallback: give the AI the date and let it calculate
        logger.warning(
            "Panchang scraping failed for %s — using date-only fallback.", display_date
        )
        panchang_summary = (
            f"Date: {display_date} (IST). "
            f"Please identify today's Hindu Panchang including: "
            f"Tithi name and number, Paksha (Shukla or Krishna), "
            f"Nakshatra, Yoga, Karana, and any significant festivals or vrats."
        )

    title = f"Aaj ka Panchang — {display_date}"
    url   = f"{DRIK_URL}?date={date_str}"

    return _save_panchang_article(title, panchang_summary, SOURCE_NAME, url)


def _scrape_drik_panchang(date_str: str) -> "str | None":
    """
    Scrapes tithi and panchang fields from Drik Panchang.

    Tries two extraction strategies:
      1. Table-row scanning — finds rows where the first cell matches
         a known panchang field name.
      2. CSS class scanning — looks for elements with "panchang" in
         their class name as a fallback.

    Args:
        date_str (str): Date in MM/DD/YYYY format for the URL parameter.

    Returns:
        str:  Panchang fields as a pipe-separated string, e.g.
              "Tithi: Tritiya | Paksha: Shukla | Nakshatra: Rohini | ..."
        None: If the page could not be fetched or parsed.
    """
    url = f"{DRIK_URL}?date={date_str}"
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=12)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.warning("HTTP request to Drik Panchang failed: %s", str(e))
        return None

    try:
        soup = BeautifulSoup(response.text, "lxml")
        fields = {}

        # ── Strategy 1: Scan table rows for known field names ───────────────
        for row in soup.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue
            key_text = cells[0].get_text(separator=" ", strip=True)
            val_text = cells[1].get_text(separator=" ", strip=True)

            for field in PANCHANG_FIELDS:
                if field.lower() in key_text.lower() and field not in fields:
                    # Take only the first meaningful value (e.g. "Tritiya" not the full paragraph)
                    val_clean = val_text.split("\n")[0].strip()[:120]
                    if val_clean:
                        fields[field] = val_clean

        if fields:
            parts = [f"{k}: {v}" for k, v in fields.items()]
            return " | ".join(parts)

        # ── Strategy 2: Look for panchang-named elements ─────────────────────
        for elem in soup.find_all(
            class_=lambda c: c and any(
                kw in c.lower() for kw in ["panchang", "tithi", "nakshatra"]
            )
        ):
            text = elem.get_text(separator=" ", strip=True)
            if len(text) > 30:
                return text[:600]

        logger.warning("Could not extract structured fields from Drik Panchang page.")
        return None

    except Exception as e:
        logger.warning("Failed to parse Drik Panchang HTML: %s", str(e))
        return None


def _save_panchang_article(
    title: str, summary: str, source_name: str, url: str
) -> "Article | None":
    """
    Saves the panchang data as an Article record in the database.

    Checks if today's panchang article already exists before inserting
    to avoid duplicates when the pipeline runs multiple times.

    Args:
        title (str):       e.g. "Aaj ka Panchang — April 04, 2026"
        summary (str):     Panchang fields string (tithi, nakshatra, etc.)
        source_name (str): "Drik Panchang"
        url (str):         The Drik Panchang URL for today's date.

    Returns:
        Article: The saved (or existing) Article object.
        None:    If the DB operation failed.
    """
    try:
        with get_session() as session:
            # Re-use today's panchang article if it already exists
            existing = (
                session.query(Article)
                .filter_by(bot_id="astrology", title=title)
                .first()
            )
            if existing:
                session.expunge(existing)
                logger.info("Reusing existing panchang article (id=%d)", existing.id)
                return existing

            article = Article(
                bot_id="astrology",
                title=title,
                summary=summary,
                source_name=source_name,
                url=url,
                status="new",
                published_at=datetime.utcnow(),
                virality_score=80.0,   # Always publish — it's today's panchang
            )
            session.add(article)
            session.flush()
            session.expunge(article)

        logger.info("Panchang article saved to DB: '%s'", title)
        return article

    except Exception as e:
        logger.error("Failed to save panchang article to DB: %s", str(e))
        return None
