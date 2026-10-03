import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_to_n8n(counts, analysis_summary):
    """
    Sends a summary of anomalies and validated analysis results to an n8n webhook.

    Args:
        counts (dict): A dictionary containing anomaly counts.
        analysis_summary (str): The validated business analysis results.
    """
    webhook_url = os.environ.get("EDUPULSE_N8N_WEBHOOK_URL")

    if not webhook_url:
        logger.warning("EDUPULSE_N8N_WEBHOOK_URL environment variable not set. Skipping n8n notification.")
        return

    # Construct the compact JSON payload as requested
    payload = {
        "project": "EduPulse",
        "total_anomalies": counts.get("total", 0),
        "numeric_anomalies": counts.get("numeric", 0),
        "categorical_anomalies": counts.get("categorical", 0),
        "duplicate_rows": counts.get("duplicates", 0),
        "missing_values": counts.get("missing", 0),
        "analysis_summary": analysis_summary
    }

    try:
        logger.info("Sending summary to n8n webhook...")
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        # Raise an HTTPError if the response was an error
        response.raise_for_status()
        logger.info("Successfully sent EduPulse summary to n8n.")
    except requests.exceptions.RequestException as e:
        # Log the error but do not raise it, ensuring the pipeline continues
        logger.error(f"Failed to send data to n8n: {e}")
