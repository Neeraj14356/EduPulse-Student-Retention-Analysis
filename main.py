import pandas as pd
import os

from src.anomaly_detection import detect_numeric_anomalies
from src.categorical_anomaly import (
    detect_categorical_anomalies,
    detect_duplicate_rows,
    detect_missing_values
)
from src.notifier import send_anomaly_notification
from src.n8n_integration import send_to_n8n

# =========================
# 1. Load Dataset
# =========================

file_path = "data/student_cleaned.csv"
df = pd.read_csv(file_path)



# =========================
# 2. Run Anomaly Detection
# =========================

numeric_anomalies = detect_numeric_anomalies(df)

categorical_anomalies = detect_categorical_anomalies(df)

duplicate_anomalies = detect_duplicate_rows(df)

missing_anomalies = detect_missing_values(df)


# =========================
# 3. Combine All Anomalies
# =========================

all_anomalies = pd.concat(
    [
        numeric_anomalies,
        categorical_anomalies,
        duplicate_anomalies,
        missing_anomalies
    ],
    ignore_index=True
)


# =========================
# 4. Summary
# =========================

print("\n===== FINAL ANOMALY SUMMARY =====")

print("Numeric anomalies:", len(numeric_anomalies))
print("Categorical anomalies:", len(categorical_anomalies))
print("Duplicate rows:", len(duplicate_anomalies))
print("Missing values:", len(missing_anomalies))
print("Total anomalies:", len(all_anomalies))


# =========================
# 5. Save Report
# =========================

report_path = "reports/anomaly_report.csv"

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

all_anomalies.to_csv(
    report_path,
    index=False
)

print(f"\nAnomaly report saved: {report_path}")

# =========================
# 6. n8n Integration
# =========================

print("\nSending summary to n8n...")
anomaly_counts = {
    "total": len(all_anomalies),
    "numeric": len(numeric_anomalies),
    "categorical": len(categorical_anomalies),
    "duplicates": len(duplicate_anomalies),
    "missing": len(missing_anomalies)
}

# Validated analysis results for the n8n GPT node
validated_analysis = (
    "Key Validated Findings:\n"
    "- Academic Decline: Strong statistical association between falling grades in the 2nd semester and dropout status.\n"
    "- Financial Stress: Significant association between debtor status, unpaid tuition fees, and higher dropout rates.\n"
    "- High-Risk Segment: Students with poor academic performance (Grade < 8) and financial constraints show markedly higher attrition.\n"
    "- Validation: All findings validated using Welch's t-tests and Chi-square tests (p-values < 0.05)."
)

send_to_n8n(anomaly_counts, validated_analysis)

# =========================
# 7. Email Notification
# =========================

print("\nChecking for anomaly notifications...")
send_anomaly_notification(all_anomalies)


# =========================
# 6. Preview
# =========================

print("\n===== REPORT PREVIEW =====")
print(all_anomalies.head(10))