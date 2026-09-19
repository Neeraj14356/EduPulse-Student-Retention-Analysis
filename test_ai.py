import pandas as pd

from src.ai_insights import generate_report_insight


report = pd.read_csv("reports/anomaly_report.csv")

# Limit data sent to local LLM
summary = report.groupby(
    ["column", "anomaly_type"]
).size().reset_index(name="count")

result = generate_report_insight(
    summary.to_string(index=False)
)

with open("reports/ai_insight.txt", "w", encoding="utf-8") as file:
    file.write(result)

print("\nAI insight saved successfully.")