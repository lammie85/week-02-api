
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key exists
if GROQ_API_KEY:
    print("Groq API key loaded successfully!")
else:
    print("API key not found. Please check your .env file.")


    
import os
import json
import requests
from dotenv import load_dotenv

# STEP 1: Load API key
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY is missing.")
    raise SystemExit(1)


# STEP 2: Collect user information
print("\n=== AI SOLAR POWERED BACKPACK ===")

business_type = input("Enter Business Type / Industry: ")
target_audience = input("Enter Target Audience: ")
location = input("Enter Location: ")

if not all([business_type.strip(),
            target_audience.strip(),
            location.strip()]):
    print("Error: All fields are required.")
    raise SystemExit(1)


# STEP 3: Create the AI prompt
prompt = f"""
You are an expert business consultant.

Generate a creative business idea using these details:

Business Type: {business_type}
Target Audience: {target_audience}
Location: {location}

Return ONLY valid JSON with exactly these three keys:
- business_name: A creative business name.
- description: A two-sentence business summary.
- marketing_idea: A high-impact launch tactic.
"""


# STEP 4: Configure Groq API
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-oss-120b",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.7,
    "response_format": {
        "type": "json_object"
    }
}


# STEP 5: Send API request
response = None

try:
    print("\nGenerating your business idea...")

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    # Extract AI response
    ai_content = result["choices"][0]["message"]["content"]

    # Convert JSON text to Python dictionary
    business_data = json.loads(ai_content)

    # STEP 6: Display business information
    print("\n====== AI BUSINESS RESULTS ======")

    print("\nBusiness Name:")
    print(business_data["business_name"])

    print("\nDescription:")
    print(business_data["description"])

    print("\nMarketing Idea:")
    print(business_data["marketing_idea"])

    # STEP 7: Display token usage
    usage = result.get("usage", {})

    print("\n====== TOKEN USAGE ======")
    print("Prompt Tokens:", usage.get("prompt_tokens", 0))
    print("Completion Tokens:", usage.get("completion_tokens", 0))
    print("Total Tokens:", usage.get("total_tokens", 0))

    print("\nBusiness idea generated successfully!")

except requests.exceptions.HTTPError as error:
    print("\nHTTP Error:", error)
    if response is not None:
        print("Details:", response.text)

except requests.exceptions.RequestException as error:
    print("\nNetwork Error:", error)

except json.JSONDecodeError:
    print("\nError: Invalid JSON response.")

except (KeyError, IndexError, TypeError) as error:
    print("\nUnexpected API response:", error)
