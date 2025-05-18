import os
from google import genai
from google.genai import types
import re

# Load the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)
# Initialize the Google Generative AI Model

def generate_code(prompt):
    try:
        # Generate content using the model
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        # Extract the Python code from the response
        text = response.candidates[0].content.parts[0].text
        return markdown_to_plain_text(text)
    except Exception as e:
        raise Exception(f"Error generating code: {str(e)}")

def markdown_to_plain_text(markdown_text):
    # Remove code blocks (e.g., ```python ... ```)
    plain_text = re.sub(r"```[a-zA-Z]*\n(.*?)```", r"\1", markdown_text, flags=re.DOTALL)
    # Remove inline code (e.g., `code`)
    plain_text = re.sub(r"`(.*?)`", r"\1", plain_text)
    # Remove other Markdown formatting (e.g., **bold**, *italic*, etc.), but keep parentheses
    plain_text = re.sub(r"(\*\*|\*|_|~|#|>|-|\+|\[|\])", "", plain_text)
    return plain_text.strip()