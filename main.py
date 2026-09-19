import pandas as pd

from src.anomaly_detection import detect_numeric_anomalies
from src.categorical_anomaly import (
    detect_categorical_anomalies,
    detect_duplicate_rows,
    detect_missing_values
)

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

all_anomalies.to_csv(
    report_path,
    index=False
)

print(f"\nAnomaly report saved: {report_path}")


# =========================
# 6. Preview
# =========================

print("\n===== REPORT PREVIEW =====")
print(all_anomalies.head(10))