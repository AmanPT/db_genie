# utils/query_optimizer.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def optimize_query(query):
    prompt = f"""Optimize the following SQL query for performance. Add indexes or rewrite if needed:

{query}

Return only the optimized SQL query."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

