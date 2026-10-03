import os
import pandas as pd
import logging
from openai import OpenAI

# Configure logging for AI insights
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
# The SDK automatically reads OPENAI_API_KEY from environment variables
client = OpenAI()

def generate_report_insight(all_anomalies):
    """
    Generates AI-driven insights from anomaly data using OpenAI API.
    Optimized to send grouped summaries instead of raw rows to avoid token overflow.

    Args:
        all_anomalies: A pandas DataFrame containing all detected anomalies.

    Returns:
        A string containing the AI analysis or an error/status message.
    """
    # 1. Handle empty anomaly report
    if all_anomalies is None or (isinstance(all_anomalies, pd.DataFrame) and all_anomalies.empty):
        return "No anomalies detected in the dataset; no AI insights generated."

    if isinstance(all_anomalies, str):
        if not all_anomalies.strip() or "Empty DataFrame" in all_anomalies:
            return "No anomalies detected in the dataset; no AI insights generated."
        # If it's a string, we can't group it, but the pipeline is updated to pass DataFrame.
        summary_data = all_anomalies
    else:
        # 2. Group anomalies by column and type to reduce token count
        # We count occurrences and sum the anomaly scores to give the AI a sense of magnitude.
        grouped = all_anomalies.groupby(['column', 'anomaly_type']).size().reset_index(name='count')

        # Also get the average anomaly score for context
        if 'anomaly_score' in all_anomalies.columns:
            scores = all_anomalies.groupby(['column', 'anomaly_type'])['anomaly_score'].mean().reset_index(name='avg_score')
            grouped = grouped.merge(scores, on=['column', 'anomaly_type'])

        summary_data = grouped.to_string(index=False)

    # 3. Refine the prompt with strict constraints
    prompt = f"""
You are a professional data analyst.

Analyze this SUMMARY of anomalies from a student academic dataset:

{summary_data}

Provide the following:
1. Key anomaly patterns identified in the grouped data.
2. Most important findings based strictly on the provided counts and scores.
3. Possible explanations for these patterns.
4. Recommended investigation/actions.

STRICT CONSTRAINTS:
- Use ONLY the provided results.
- NEVER invent numbers, facts, or data points not present in the summary.
- NEVER claim causation (e.g., do not say "X caused Y"). Use correlation terms like "associated with" or "observed alongside".
- Do NOT automatically treat anomalies as errors; they are legitimate statistical outliers and may be legitimate data.
- Keep the analysis concise, objective, and professional.
"""

    try:
        # Use OpenAI Chat Completions API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API failure: {e}")
        return f"AI Insight generation failed due to a connection or API error: {str(e)}"
