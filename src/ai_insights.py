import ollama

def generate_report_insight(numeric_anomalies):
    prompt = f"""
You are a data analyst.

Analyze this anomaly report from a student academic dataset:

{numeric_anomalies}

Provide:
1. Key anomaly patterns
2. Most important findings
3. Possible explanations
4. Recommended investigation/actions

Do not assume an anomaly is an error.
Do not invent facts.
Keep the analysis concise and professional.
"""

    response = ollama.chat(
        model="rafw007/qwen35-claude-coder:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]