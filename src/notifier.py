import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_anomaly_notification(all_anomalies: pd.DataFrame):
    """
    Sends an email notification if anomalies are detected.

    Args:
        all_anomalies (pd.DataFrame): The combined DataFrame containing all detected anomalies.
    """
    # 1. Conditional Trigger: Send ONLY when anomalies are found
    if all_anomalies is None or all_anomalies.empty:
        logger.info("No anomalies found. Skipping email notification.")
        return

    # 2. Retrieve credentials from environment variables
    sender_email = os.environ.get("EMAIL_SENDER")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = os.environ.get("EMAIL_RECEIVER")

    if not all([sender_email, sender_password, receiver_email]):
        logger.error("Email credentials missing in environment variables. Notification skipped.")
        return

    # 3. Generate Email Content
    total_count = len(all_anomalies)
    affected_cols = all_anomalies["column"].unique().tolist() if "column" in all_anomalies.columns else []

    # Create a short summary (top 5 anomalies)
    summary_df = all_anomalies.head(5).to_string(index=False)

    subject = f"ALERT: {total_count} Anomalies Detected in Academic Dataset"
    body = f"""
Hello,

The automated anomaly detection pipeline has completed.

Summary of Findings:
--------------------------------------------------
Total Anomalies Found: {total_count}
Affected Columns: {', '.join(affected_cols) if affected_cols else 'None'}

Top Anomalies Preview:
{summary_df}
--------------------------------------------------

Please refer to the generated reports for the full analysis.

This is an automated message.
"""

    # 4. Construct the Email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # 5. Send Email with Error Handling
    try:
        # Using Gmail as a common default; this can be adjusted for other SMTP servers
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        logger.info(f"Anomaly notification email sent successfully to {receiver_email}.")
    except Exception as e:
        logger.error(f"Failed to send anomaly notification email: {e}")
