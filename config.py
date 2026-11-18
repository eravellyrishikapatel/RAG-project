import os

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# ===========================================
# Load Environment Variables
# ===========================================

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ===========================================
# Configure OpenRouter Client
# ===========================================

client = None

if OPENROUTER_API_KEY:
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )


# ===========================================
# OpenRouter Model
# ===========================================

MODEL_NAME = "openrouter/free"


# ===========================================
# LLM Helper Function
# ===========================================

def generate_response(prompt: str) -> str:
    """
    Send a prompt to OpenRouter
    and return the generated text.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# ===========================================
# Load Embedding Model
# ===========================================

print("\nLoading Embedding Model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding Model Loaded Successfully!")


# ===========================================
# Embedding Helper Function
# ===========================================

def get_embedding(text):
    """
    Generate a sentence embedding using
    SentenceTransformer.
    """

    return embedding_model.encode(text)