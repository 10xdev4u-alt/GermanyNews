"""
Telegram Sender — Sends messages via the official Telegram Bot API.

Handles:
  - Messages longer than 4000 chars (split into multiple messages)
  - Markdown parse errors (falls back to plain text)

Setup:
    1. Open Telegram, search for @BotFather, send /newbot
    2. Choose a name and username (must end in 'bot')
    3. BotFather gives you an API token
    4. Message your bot, then visit:
       https://api.telegram.org/bot<TOKEN>/getUpdates
       to find your chat_id
    5. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment
"""

import os

import requests

TELEGRAM_API_BASE = "https://api.telegram.org/bot"
MAX_MESSAGE_LENGTH = 4000  # Telegram's hard limit is 4096, we leave buffer


def _split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """
    Split a long message into chunks at newline boundaries.
    Each chunk stays under max_length chars.
    """
    if len(text) <= max_length:
        return [text]

    chunks: list[str] = []
    current_chunk: list[str] = []
    current_len = 0

    for line in text.split("\n"):
        # +1 for the newline we'll add back
        line_len = len(line) + 1

        if current_len + line_len > max_length:
            # Save current chunk and start new one
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                # Add continuation note
                chunks[-1] += "\n\n— continued —"
            current_chunk = [line]
            current_len = line_len
        else:
            current_chunk.append(line)
            current_len += line_len

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    # If a single line exceeds the limit, force-split it
    final_chunks: list[str] = []
    for chunk in chunks:
        if len(chunk) > max_length:
            # Force-split at max_length boundary
            for i in range(0, len(chunk), max_length):
                segment = chunk[i : i + max_length]
                if i + max_length < len(chunk):
                    segment += "\n\n— continued —"
                final_chunks.append(segment)
        else:
            final_chunks.append(chunk)

    return final_chunks


def _send_chunk(token: str, chat_id: str, text: str, parse_mode: str | None) -> bool:
    """
    Send a single message chunk to Telegram.
    If parse_mode causes an error, returns False so caller can retry without it.
    """
    url = f"{TELEGRAM_API_BASE}{token}/sendMessage"
    payload: dict = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        resp = requests.post(url, json=payload, timeout=15)
        data = resp.json()
        return data.get("ok", False)
    except requests.RequestException:
        return False


def send_telegram_message(message: str) -> bool:
    """
    Send a text message to your Telegram chat via the Bot API.

    - Splits long messages (>4000 chars) into multiple parts
    - Tries Markdown formatting first, falls back to plain text on error

    Returns True if all parts were sent successfully.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token:
        print("⚠️  TELEGRAM_BOT_TOKEN not set, skipping Telegram")
        return False
    if not chat_id:
        print("⚠️  TELEGRAM_CHAT_ID not set, skipping Telegram")
        return False

    # Split into chunks if needed
    chunks = _split_message(message)
    total_parts = len(chunks)

    use_markdown = True  # Track whether to try Markdown across chunks

    for i, chunk in enumerate(chunks, 1):
        if total_parts > 1:
            print(f"   📤 Sending part {i}/{total_parts} ({len(chunk)} chars)...")

        if use_markdown:
            sent = _send_chunk(token, chat_id, chunk, parse_mode="Markdown")
            if not sent:
                # Markdown failed — fallback to plain text for this + all remaining chunks
                if total_parts > 1:
                    print(f"   ⚠️  Markdown failed on part {i}, switching to plain text...")
                else:
                    print(f"   ⚠️  Markdown parsing failed, retrying as plain text...")
                use_markdown = False
                sent = _send_chunk(token, chat_id, chunk, parse_mode=None)
        else:
            sent = _send_chunk(token, chat_id, chunk, parse_mode=None)

        if not sent:
            print(f"❌ Failed to send part {i}/{total_parts} to Telegram")
            return False

    print(f"✅ Telegram: {total_parts} message(s) sent to chat {chat_id}")
    return True
