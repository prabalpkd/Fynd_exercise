import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

def call_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def generate_user_response(review, rating):
    prompt = f"""
User gave {rating} stars and wrote:
"{review}"

Write a polite, empathetic AI response.
"""
    return call_llm(prompt)

def generate_admin_summary(review):
    prompt = f"Summarize this customer review briefly:\n{review}"
    return call_llm(prompt)

def generate_recommended_action(review, rating):
    prompt = f"""
Based on this review and rating ({rating}),
suggest the next best action for the business.
"""
    return call_llm(prompt)
