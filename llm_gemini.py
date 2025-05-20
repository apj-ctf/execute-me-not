import os
from google import genai

# Load the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)
# Initialize the Google Generative AI Model

def generate_response(prompt):
    try:
        # Generate content using the model
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        # Extract the Python code from the response
        text = response.candidates[0].content.parts[0].text
        return text
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
