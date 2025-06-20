import os
import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel

# Load the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

# Initialize the Google Generative AI client
genai.configure(api_key=api_key)
# Initialize the model
model = GenerativeModel(model_name="gemini-2.0-flash-001")
# remove the API key from the environment to avoid accidental exposure
del api_key
os.environ.pop("GOOGLE_API_KEY", None)

def generate_response(prompt):
    try:
        # Generate content using the GenerativeModel
        response = model.generate_content(prompt)
        # Extract the Python code from the response
        return markdown_to_plain_text(response.text)
    except Exception as e:
        raise Exception(f"Error generating code: {str(e)}")

def markdown_to_plain_text(markdown_text):
    # Remove Markdown code block delimiters
    text = markdown_text
    if markdown_text.startswith("```python") and markdown_text.endswith("```\n"):
        text = markdown_text[10:-4].strip()  # Remove the delimiters and any extra whitespace
    return text