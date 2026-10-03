# 🎓 EduPulse: Student Retention Analytics

EduPulse is a professional end-to-end data analytics project designed to identify key drivers of student attrition in higher education. By combining statistical validation, automated anomaly detection, and LLM-powered insights, the project provides a scalable framework for academic institutions to implement early-warning systems.

---

## 🚀 Executive Summary

**The Challenge:** High student dropout rates lead to significant academic and financial losses. The goal was to pinpoint the most critical indicators of attrition.

**Key Validated Findings:**
- **Academic Decline:** A strong statistical association exists between falling grades in the 2nd semester and dropout status. Dropout students showed a significant decline in average grades and approved curricular units compared to graduates.
- **Financial Stress:** There is a statistically significant association between financial instability—specifically **debtor status** and **unpaid tuition fees**—and higher dropout rates.
- **High-Risk Segment:** Students exhibiting both poor academic performance (Grade < 8) and financial constraints show a markedly higher probability of attrition.
- **Validation:** All key findings were validated using **Welch's t-tests** (for numeric grade differences) and **Chi-square tests** (for categorical financial factors), with p-values < 0.05.

**Business Impact:** By monitoring these indicators in real-time, institutions can shift from reactive reporting to proactive intervention, targeting "at-risk" students before the point of no return.

---

## 🛠️ Technical Highlights

This project demonstrates a full-stack data engineering and analytics pipeline:

- **SQL Analysis**: Performed deep-dive business queries to extract specific dropout patterns.
- **Python EDA**: Used Pandas and NumPy for comprehensive data cleaning and exploratory analysis.
- **Statistical Validation**: Implemented inferential statistics (Welch's t-tests, Chi-square, Cramér's V) to ensure findings were not due to random chance.
- **Anomaly Detection**: Built a custom IQR-based outlier detection system to monitor data quality and identify extreme student cases.
- **AI Automation (Ollama)**: Integrated a local LLM (via Ollama) to automatically translate raw statistical anomalies into professional business insights.
- **Automated Notification**: Developed an SMTP-based alert system to notify administrators instantly when data anomalies are detected.
- **Interactive Dashboard**: Created a professional Streamlit application for stakeholder data exploration.

---

## ⚙️ Architecture & Workflow

### Data $\to$ Insight $\to$ Action
`Raw Data` $\to$ `Statistical Analysis` $\to$ `Anomaly Detection` $\to$ `AI Interpretation` $\to$ `Stakeholder Notification` $\to$ `Executive Dashboard`

**Detailed Workflow:**
1. **Data Cleaning**: Raw student data is pre-processed into a cleaned, analysis-ready format.
2. **Statistical Validation**: Jupyter Notebooks are used to validate hypotheses and calculate p-values.
3. **Anomaly Pipeline**: `main.py` runs automated checks for numeric and categorical outliers.
4. **AI Layer**: The LLM analyzes the anomaly report and generates a strategic summary in `reports/ai_insight.txt`.
5. **Alerting**: If anomalies are found, the system triggers an automated email notification.
6. **Visualization**: Findings are surfaced in a professional Streamlit dashboard for business users.

---

## 📊 Project Details

### Dataset
A comprehensive student academic dataset containing:
- **Demographics**: Age, Gender, Nationality, Marital Status.
- **Academic Performance**: Curricular units approved/enrolled, grades for 1st and 2nd semesters.
- **Financial Status**: Tuition fee status, Scholarship holder, Debtor status.
- **Socio-Economic Factors**: GDP, Inflation rate, Unemployment rate.
- **Outcome**: Graduate, Dropout, or Enrolled.

### Tech Stack
- **Language**: Python 3.11
- **Analysis**: Pandas, NumPy, SciPy, SQL
- **AI**: Ollama (Local LLM)
- **UI**: Streamlit
- **Package Management**: UV
- **Notification**: smtplib (SMTP SSL)

### Project Structure
```text
.
├── app.py               # Professional Streamlit Dashboard
├── main.py              # Automation & AI Pipeline
├── data/                # Cleaned datasets
├── notebooks/           # Validated Statistical Research
├── reports/             # AI Insights & Anomaly Reports
├── sql/                # Business Analysis Queries
├── src/                 # Modular Logic
│   ├── ai_insights.py   # LLM Integration
│   ├── anomaly_detection.py # IQR Outlier Logic
│   ├── categorical_anomaly.py # Categorical Checks
│   ├── notifier.py      # SMTP Email System
│   └── profiler.py      # Data Profiling Tools
└── README.md            # Project Documentation
```

---

## 🏃 How to Run

1. **Setup Environment**:
   ```bash
   uv sync
   ```
2. **Run Automation Pipeline**:
   (Ensures reports are generated and AI insights are updated)
   ```bash
   python main.py
   ```
3. **Launch Executive Dashboard**:
   ```bash
   streamlit run app.py
   ```

## ⚠️ Important Limitations
- **Association $\neq$ Causation**: This project identifies statistical correlations. It does not prove that a specific factor (e.g., debtor status) directly *caused* a student to drop out.
- **Local AI**: Requires a local Ollama instance running the specified model for the AI Insights section to function.

---
*Developed as a professional data analyst portfolio project.*
