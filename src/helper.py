import pymupdf
import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")


client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file: Uploaded PDF file.

    Returns:
        str: The extracted text.
    """
    doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    return text


def ask_groq(prompt, max_tokens=500, reasoning_effort=None):
    """
    Sends a prompt to the Groq API and returns the response.

    Args:
        prompt (str): The prompt to send to the Groq API.
        max_tokens (int): Maximum number of tokens in the response.

    Returns:
        str: The response from the model.
    """

    request_options = {}
    if reasoning_effort is not None:
        request_options["reasoning_effort"] = reasoning_effort

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=max_tokens,
        **request_options
    )

    return response.choices[0].message.content