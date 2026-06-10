"""
WhatsApp Sender — Sends messages via the free CallMeBot WhatsApp API.

Usage:
    1. Add +34 644 03 87 31 to your WhatsApp contacts
    2. Send "I allow callmebot to send me messages" to that contact
    3. You'll receive your API key via reply
    4. Set CALLMEBOT_API_KEY and WHATSAPP_PHONE in environment
"""

import os
import urllib.parse

import requests

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def send_whatsapp_message(message: str) -> bool:
    """
    Send a text message to your WhatsApp number via CallMeBot.

    Returns True if the message was sent successfully.
    """
    phone = os.environ.get("WHATSAPP_PHONE")
    apikey = os.environ.get("CALLMEBOT_API_KEY")

    if not phone:
        raise ValueError("WHATSAPP_PHONE environment variable is not set")
    if not apikey:
        raise ValueError("CALLMEBOT_API_KEY environment variable is not set")

    # CallMeBot expects phone without leading '+'
    phone = phone.lstrip("+")

    encoded_message = urllib.parse.quote(message)
    url = f"{CALLMEBOT_URL}?phone={phone}&text={encoded_message}&apikey={apikey}"

    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            print(f"✅ WhatsApp message sent successfully to +{phone}")
            return True
        else:
            print(f"❌ CallMeBot error {resp.status_code}: {resp.text}")
            return False
    except requests.RequestException as e:
        print(f"❌ Failed to send WhatsApp message: {e}")
        return False
