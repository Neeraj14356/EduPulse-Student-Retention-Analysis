# 🎓 EduPulse: Student Retention & Dropout Analytics

EduPulse is an end-to-end data analytics project designed to analyze student outcomes and identify academic and financial indicators associated with higher observed dropout rates in higher education.

The project combines SQL business analysis, Python-based exploratory data analysis, statistical validation, automated anomaly detection, AI-generated business insights, n8n workflow automation, email notifications, and an interactive Power BI dashboard.

The goal is to help educational institutions understand student outcome patterns and identify student groups that may benefit from earlier academic or financial support.

---

## 📌 Executive Summary

### Business Problem

Student dropout is an important challenge for higher education institutions. Understanding how academic performance, financial circumstances, and student characteristics relate to dropout outcomes can help institutions plan targeted support initiatives.

EduPulse analyzes student academic and financial data to identify patterns associated with student dropout and communicate the findings through an interactive dashboard and an automated reporting workflow.

### Key Validated Findings

- **Academic Performance:** Dropout students had a substantially lower average second-semester grade than graduate students (5.90 versus 12.70). They also had fewer average approved curricular units (1.94 versus 6.18).
- **Financial Indicators:** Students whose tuition fees were not up to date had an observed dropout rate of 86.5%, compared with 24.7% among students whose fees were up to date.
- **Debtor Status:** Students classified as debtors had an observed dropout rate of 62.0%, compared with 28.3% among non-debtors.
- **Scholarship Status:** Scholarship holders had an observed dropout rate of 12.2%, compared with 38.7% among non-scholarship holders.
- **High-Risk Segment:** Students with second-semester grades below 8 and overdue tuition fees had an observed dropout rate of 97.0% in the analyzed dataset.
- **Statistical Validation:** Welch's t-tests, Chi-square tests, and Cramér's V were used to examine differences and associations in the data.

### Business Value

EduPulse helps stakeholders explore dropout patterns, review statistically supported findings, identify student segments with higher observed dropout rates, and consider targeted academic or financial support.

The analysis identifies associations rather than proving causation or predicting an individual student's future outcome.

---

## 🛠️ Technical Highlights

### 1. SQL Business Analysis
Used SQL to investigate business questions related to overall student outcome distribution, financial status, and academic progress. Queries are available in `sql/dropout_analysis.sql`.

### 2. Python EDA and Data Quality
Used Python, Pandas, and NumPy to inspect the dataset, validate data quality, and prepare the data for further analysis.

### 3. Statistical Analysis
Used SciPy and statistical methods to investigate differences and associations:
- Welch's t-tests for numeric group comparisons
- Chi-square tests for categorical associations
- Cramér's V to measure association strength

### 4. Automated Anomaly Detection
Developed a modular anomaly detection pipeline using the Interquartile Range (IQR) method to check numeric anomalies, unexpected categorical values, duplicates, and missing values.

### 5. Dual-Path Notification & Insights Workflow
The project employs two distinct notification paths to handle different types of findings:

- **AI-Powered Insights (Business Report):**
  `Python (main.py)` $\rightarrow$ `n8n Webhook` $\rightarrow$ `AI (GPT-5-mini)` $\rightarrow$ `IF Condition` $\rightarrow$ `Gmail Notification`.
  This path transforms validated statistical results into business-friendly recommendations.

- **Technical Anomaly Alerts (Data Quality):**
  `Python (main.py)` $\rightarrow$ `src/notifier.py` $\rightarrow$ `Gmail Notification`.
  This path provides immediate technical alerts when data anomalies are detected during the pipeline run.

### 6. Interactive Power BI Dashboard
Built a three-page Power BI dashboard:
- **Page 1 — Executive Overview:** Student outcomes, overall dropout rate, age groups, and financial indicators.
- **Page 2 — Dropout Drivers:** Academic performance, approved curricular units, and risk segments.
- **Page 3 — Statistical & AI Insights:** Statistical evidence, Cramér's V, and AI-driven business recommendations.

---

## 📊 Dataset

**Dataset:** Student Dropout and Academic Success — UCI Machine Learning Repository
The cleaned dataset used in the project contains 4,424 student records.

### Overall Student Outcomes

| Outcome | Students | Percentage |
|---|---:|---:|
| Graduate | 2,209 | 49.93% |
| Dropout | 1,421 | 32.12% |
| Enrolled | 794 | 17.95% |
| **Total** | **4,424** | **100%** |

---

## ⚙️ Architecture and Workflow

### Workflow Steps
1. **Data Preparation:** Load the cleaned student dataset.
2. **Business and Statistical Analysis:** Use SQL and Python notebooks to investigate outcomes and validate findings.
3. **Anomaly Detection:** Run `main.py` to detect anomalies and data quality issues.
4. **Webhook Integration:** Send anomaly counts and validated analysis results to the n8n webhook.
5. **AI Interpretation (n8n):** GPT-5-mini produces structured business insights from the results.
6. **Notification Dispatch:**
   - **AI Report:** Sent via n8n when the configured condition is met.
   - **Technical Alert:** Sent directly via Python SMTP if anomalies are found.
7. **Dashboard Reporting:** Use Power BI to explore detailed patterns and findings.

---

## 🗂️ Project Structure

```text
AI_Excel_Analytics_Agent/
│
├── data/
│   └── student_cleaned.csv
│
├── notebooks/
│   └── edupulse_student_retention_analysis.ipynb
│
├── reports/
│   ├── anomaly_report.csv
│   └── EduPulse_Student_Retention_Analysis.pbix
│
├── sql/
│   └── dropout_analysis.sql
│
├── src/
│   ├── anomaly_detection.py
│   ├── categorical_anomaly.py
│   ├── n8n_integration.py
│   ├── notifier.py
│   └── profiler.py
│
├── AI project.pbix
├── main.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.11
- MySQL (for SQL analysis)
- Power BI Desktop
- n8n instance with configured workflow (OpenAI & Gmail nodes)

### 1. Clone and Install
```bash
git clone https://github.com/Neeraj14356/EduPulse-Student-Retention-Analysis.git
cd EduPulse-Student-Retention-Analysis
uv sync
```

### 2. Configure Environment
Set the following environment variables:
- `EDUPULSE_N8N_WEBHOOK_URL`: Your n8n webhook URL.
- `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`: Credentials for the Python SMTP alert system.

### 3. Run the Pipeline
```bash
python main.py
```

### 4. Open the Power BI Dashboard
Open either:
- `reports/EduPulse_Student_Retention_Analysis.pbix`
- `AI project.pbix` (root)

---

## ⚠️ Limitations
- **Association $\neq$ Causation:** Findings identify statistical relationships, not causal links.
- **No Individual Prediction:** The project analyzes groups, not individual student risk.
- **Dashboard Refresh:** The dashboard should not be described as real-time unless a refresh pipeline is implemented.

## 🔮 Future Improvements
- Build and validate a machine-learning model for individual dropout risk estimation.
- Connect Power BI to a repeatable refresh pipeline.
- Track academic or financial interventions and evaluate their outcomes.

---

## 👨‍💻 Author
**Neeraj Singh**
Data Analytics | SQL | Python | Statistics | Power BI | AI Automation
[LinkedIn](https://linkedin.com/in/neeraj-singh-80a25321b)
