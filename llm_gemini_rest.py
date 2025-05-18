import os
import requests
import re

# Load the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

# Google Generative Language API base URL
base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_code(prompt):
    """
    Fetch generated content from the Google Generative Language API.

    Args:
        prompt (str): The user-provided prompt.

    Returns:
        str: The generated Python code.
    """
    # Add the API key as a query parameter
    url = f"{base_url}?key={api_key}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        # Extract the Python code from the response
        try:
            code = response_json['candidates'][0]['content']['parts'][0]['text']
            return markdown_to_plain_text(code)
        except (KeyError, IndexError):
            raise Exception("Unexpected response format from the API.")
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

def markdown_to_plain_text(markdown_text):
    """
    Converts Markdown-formatted text to plain text.

    Args:
        markdown_text (str): The Markdown text to convert.

    Returns:
        str: The plain text.
    """
    # Remove code blocks (e.g., ```python ... ```)
    plain_text = re.sub(r"```[a-zA-Z]*\n(.*?)```", r"\1", markdown_text, flags=re.DOTALL)
    # Remove inline code (e.g., `code`)
    plain_text = re.sub(r"`(.*?)`", r"\1", plain_text)
    # Remove other Markdown formatting (e.g., **bold**, *italic*, etc.), but keep parentheses
    plain_text = re.sub(r"(\*\*|\*|_|~|#|>|-|\+|\[|\])", "", plain_text)
    return plain_text.strip()