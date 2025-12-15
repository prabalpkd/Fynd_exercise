import os
import pandas as pd
import json
from tqdm import tqdm
from groq import Groq
from dotenv import load_dotenv

# Load environment variables

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please set it in .env or environment variables.")

# Configuration

DATA_PATH = "yelp.csv"
SAMPLE_SIZE = 50
MODEL_NAME = "llama-3.1-8b-instant"

client = Groq(api_key=GROQ_API_KEY)

# Prompt Versions

PROMPTS = {
    "v1_basic": {
        "system": "",
        "user": """Classify the Yelp review into a star rating from 1 to 5.

Review:
"{review_text}"

Return JSON:
{{"predicted_stars": <1-5>, "explanation": "Brief reasoning"}}
"""
    },

    "v2_rules": {
        "system": """You are a sentiment classification assistant.

Rating scale:
1 = very negative
2 = negative
3 = neutral
4 = positive
5 = very positive
""",
        "user": """Review:
"{review_text}"

Return ONLY valid JSON:
{{"predicted_stars": <1-5>, "explanation": "Brief reasoning"}}
"""
    },

    "v3_cot": {
        "system": """You are an expert Yelp review analyst.
Think carefully before answering.
""",
        "user": """Review:
"{review_text}"

Return ONLY this JSON:
{{"predicted_stars": <1-5>, "explanation": "Brief reasoning"}}
"""
    }
}

# LLM Call

def run_prompt(review_text, prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": prompt["system"]},
            {
                "role": "user",
                "content": prompt["user"].format(
                    review_text=review_text.replace('"', "'")
                )
            }
        ],
        temperature=0
    )

    output = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(output)
        valid_json = True
    except json.JSONDecodeError:
        parsed = {"predicted_stars": None, "explanation": None}
        valid_json = False

    return parsed, valid_json


# Main Function

def main():
    df = pd.read_csv(DATA_PATH)[["text", "stars"]]
    df = df.sample(n=SAMPLE_SIZE, random_state=42)

    summary = []

    for version, prompt in PROMPTS.items():
        correct = 0
        valid_json_count = 0

        for _, row in tqdm(df.iterrows(), total=len(df), desc=version):
            result, valid_json = run_prompt(row["text"], prompt)

            if valid_json:
                valid_json_count += 1
                if result["predicted_stars"] == row["stars"]:
                    correct += 1

        summary.append({
            "Prompt Version": version,
            "Accuracy": round(correct / SAMPLE_SIZE, 3),
            "JSON Validity Rate": round(valid_json_count / SAMPLE_SIZE, 3)
        })

    summary_df = pd.DataFrame(summary)
    print("\nPrompt Comparison Results:\n")
    print(summary_df)

    summary_df.to_csv("prompt_comparison_results.csv", index=False)

if __name__ == "__main__":
    main()
