"""
Fetches motivational quotes from ZenQuotes API.
Includes a fallback mechanism in case the API is unavailable.
"""
import requests
from config import STRINGS

def get_quote():
    """Gets a motivational quote from ZenQuotes API or returns a fallback from config."""
    try:
        # Attempt to get a random quote from the API
        response = requests.get("https://zenquotes.io/api/random", timeout=3)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the response and format the quote
        quote_data = response.json()[0]
        return f'"{quote_data["q"]}"\n- {quote_data["a"]}'

    except Exception:
        # Returns the fallback quote if any error occurs
        return STRINGS['fallback_quote']