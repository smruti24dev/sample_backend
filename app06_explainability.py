import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

# -------------------------
# Load env variables
# -------------------------

load_dotenv()

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

if not api_key:

    raise ValueError(

        "GOOGLE_API_KEY missing in .env"

    )

# -------------------------
# Gemini Model
# -------------------------

llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    google_api_key=api_key,

    temperature=0.2
)

# -------------------------
# Explainability Function
# -------------------------

def explain(

    risk,

    reason

):

    prompt = f"""

Risk Score:

{risk}

Evidence:

{reason}

Explain banking fraud indicators
in simple terms.
"""

    response = llm.invoke(
        prompt
    )

    return response.content


# -------------------------
# Test
# -------------------------

if __name__ == "__main__":

    output = explain(

        88,

        "Replay attack, unknown device"

    )

    print(
        output
    )