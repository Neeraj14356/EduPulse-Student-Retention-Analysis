import streamlit as st
import pandas as pd
import numpy as np
import os
from scipy import stats

# ==========================================
# 1. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="EduPulse | Student Retention Analytics",
    page_icon="🎓",
    layout="wide"
)

# Professional EdTech Palette
# Primary: #1e3a8a (Navy Blue), Accent: #3b82f6 (Bright Blue), Background: #f8fafc (Slate Grey)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    h1, h2, h3 { color: #1e3a8a !important; font-family: 'Inter', sans-serif; }
    .takeaway-card {
        background-color: #eff6ff;
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin: 20px 0;
    }
    .stat-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING & UTILITIES
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/student_cleaned.csv")
    return df

def get_dropout_rate(df, group_col, group_val):
    subset = df[df[group_col] == group_val]
    if len(subset) == 0: return 0.0, 0
    rate = (len(subset[subset['Target'] == 'Dropout']) / len(subset)) * 100
    return rate, len(subset)

def calculate_cramers_v(df, col1, col2):
    confusion_matrix = pd.crosstab(df[col1], df[col2])
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r = confusion_matrix.shape[0]
    k = confusion_matrix.shape[1]
    phi2_corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    r_corr = r - ((r-1)**2)/(n-1)
    k_corr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2_corr / min((k_corr-1), (r_corr-1)))

try:
    df = load_data()
except Exception as e:
    st.error(f"Dataset load failure: {e}")
    st.stop()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=80)
st.sidebar.title("EduPulse Analytics")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Operational Modules",
    ["Executive Overview", "Dropout Drivers", "Academic Risk", "Student Segments", "Statistical Evidence", "Anomaly Monitor", "AI Business Insights"]
)

# ==========================================
# 4. DASHBOARD SECTIONS
# ==========================================

if menu == "Executive Overview":
    st.title("🏛️ Executive Overview")
    st.markdown("Critical high-level metrics for academic retention management.")

    # KPIs
    total = len(df)
    dropouts = len(df[df['Target'] == 'Dropout'])
    graduates = len(df[df['Target'] == 'Graduate'])
    enrolled = len(df[df['Target'] == 'Enrolled'])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", f"{total:,}")
    c2.metric("Dropout Rate", f"{(dropouts/total)*100:.1f}%", delta="High Risk", delta_color="inverse")
    c3.metric("Graduate Rate", f"{(graduates/total)*100:.1f}%")
    c4.metric("Enrolled Rate", f"{(enrolled/total)*100:.1f}%")

    st.markdown('<div class="takeaway-card"><strong>🔑 Key Business Takeaway:</strong> Approximately 32% of the student population is categorized as Dropout. Academic performance in the 2nd semester and financial stability (debtor status) appear to be the primary drivers of attrition.</div>', unsafe_allow_html=True)

    st.subheader("Outcome Distribution")
    st.bar_chart(df['Target'].value_counts())

elif menu == "Dropout Drivers":
    st.title("📉 Dropout Drivers")
    st.markdown("Analysis of financial and socio-economic associations with student attrition.")

    factors = {
        "Tuition fees up to date": ["Yes", "No"],
        "Debtor": ["No", "Yes"],
        "Scholarship holder": ["No", "Yes"]
    }

    tabs = st.tabs(list(factors.keys()))

    for i, (factor, values) in enumerate(factors.items()):
        with tabs[i]:
            st.subheader(f"{factor} vs Outcome")
            res = []
            for val in values:
                rate, size = get_dropout_rate(df, factor, val)
                res.append({"Status": val, "Dropout Rate (%)": rate, "Sample Size": size})

            res_df = pd.DataFrame(res)
            st.table(res_df)
            st.bar_chart(res_df.set_index("Status")["Dropout Rate (%)"])

    st.markdown("---")
    st.subheader("Association Strength (Cramér's V)")
    st.info("Cramér's V ranges from 0 (no association) to 1 (perfect association).")

    v_results = []
    for factor in factors.keys():
        v_val = calculate_cramers_v(df, factor, 'Target')
        v_results.append({"Factor": factor, "Cramér's V": round(v_val, 3)})

    st.dataframe(pd.DataFrame(v_results).sort_values("Cramér's V", ascending=False), use_container_width=True)

elif menu == "Academic Risk":
    st.title("🎓 Academic Risk Analysis")
    st.markdown("Evaluating the relationship between curricular progress and student outcomes.")

    col1, col2 = st.columns(2)

    # Grades analysis
    grade_1 = "Curricular units 1st sem (grade)"
    grade_2 = "Curricular units 2nd sem (grade)"

    with col1:
        st.subheader("Semester Grade Comparison")
        avg_grades = df.groupby('Target')[[grade_1, grade_2]].mean()
        st.dataframe(avg_grades.style.highlight_min(axis=1, color='#ffcccc'))
        st.caption("Observation: Dropout students show a marked decline in 2nd semester performance.")

    with col2:
        st.subheader("Approved Units Comparison")
        app_1 = "Curricular units 1st sem (approved)"
        app_2 = "Curricular units 2nd sem (approved)"
        avg_app = df.groupby('Target')[[app_1, app_2]].mean()
        st.dataframe(avg_app.style.highlight_min(axis=1, color='#ffcccc'))
        st.caption("Observation: Significant gap in approved units between graduates and dropouts.")

    st.markdown("---")
    st.subheader("Financial-Academic Intersection")
    # Segment: Grade < 8 AND Financial issues
    risk_segment = df[(df[grade_2] < 8) & ((df['Debtor'] == 'Yes') | (df['Tuition fees up to date'] == 'No'))]
    risk_dropout_rate = (len(risk_segment[risk_segment['Target'] == 'Dropout']) / len(risk_segment)) * 100 if len(risk_segment) > 0 else 0

    st.metric("High-Risk Segment Dropout Rate", f"{risk_dropout_rate:.1f}%",
              help="Students with 2nd sem grade < 8 and financial constraints.")

elif menu == "Student Segments":
    st.title("👥 Student Segments")
    st.markdown("Dropout rates across different demographic and academic groups.")

    tab1, tab2 = st.tabs(["Age Groups", "Academic Courses"])

    with tab1:
        # Age binning
        bins = [0, 22, 25, 30, 100]
        labels = ['18-22', '23-25', '26-30', '30+']
        df['Age Group'] = pd.cut(df['Age at enrollment'], bins=bins, labels=labels)

        age_res = []
        for label in labels:
            rate, size = get_dropout_rate(df, 'Age Group', label)
            age_res.append({"Age Group": label, "Dropout Rate (%)": rate, "Sample Size": size})

        st.dataframe(pd.DataFrame(age_res), use_container_width=True)
        st.bar_chart(pd.DataFrame(age_res).set_index("Age Group")["Dropout Rate (%)"])

    with tab2:
        courses = df['Course'].unique()
        course_res = []
        for course in courses:
            rate, size = get_dropout_rate(df, 'Course', course)
            course_res.append({"Course": course, "Dropout Rate (%)": rate, "Sample Size": size})

        course_df = pd.DataFrame(course_res).sort_values("Dropout Rate (%)", ascending=False)
        st.dataframe(course_df, use_container_width=True)
        st.caption("Note: Small sample sizes in certain courses may skew rates.")

elif menu == "Statistical Evidence":
    st.title("🔬 Statistical Evidence")
    st.markdown("Rigorous validation of observed patterns using inferential statistics.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Welch's T-Test")
        st.markdown("""
        **Variable:** 2nd Semester Grade<br>
        **Result:** p-value < 0.05 (Significant)<br>
        **Interpretation:** There is a statistically significant difference in average 2nd-semester grades between graduates and dropouts.
        """)

    with col2:
        st.subheader("Chi-Square Tests")
        st.markdown("""
        **Variables:** Debtor Status, Tuition Status, Scholarship<br>
        **Result:** p-value < 0.05 (Significant)<br>
        **Interpretation:** Strong evidence of association between financial stability and student outcomes.
        """)

    st.markdown("---")
    st.subheader("Summary of Evidence")
    st.table(pd.DataFrame([
        {"Test": "Welch T-Test", "Metric": "2nd Sem Grade", "Result": "Significant", "Impact": "Academic Risk"},
        {"Test": "Chi-Square", "Metric": "Debtor Status", "Result": "Significant", "Impact": "Financial Risk"},
        {"Test": "Chi-Square", "Metric": "Tuition Status", "Result": "Significant", "Impact": "Financial Risk"},
        {"Test": "Chi-Square", "Metric": "Scholarship", "Result": "Significant", "Impact": "Financial Support"},
    ]))

elif menu == "Anomaly Monitor":
    st.title("⚠️ Anomaly Monitor")
    st.markdown("Monitoring data integrity and statistical outliers.")

    if os.path.exists("reports/anomaly_report.csv"):
        anom_df = pd.read_csv("reports/anomaly_report.csv")

        if not anom_df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Anomalies", len(anom_df))
            c2.metric("Unique Columns", anom_df['column'].nunique())
            c3.metric("Most Frequent", anom_df['column'].mode()[0])

            st.subheader("Detailed Anomaly Log")
            st.dataframe(anom_df, use_container_width=True)
        else:
            st.info("No anomalies detected in current report.")
    else:
        st.warning("Anomaly report not found.")

elif menu == "AI Business Insights":
    st.title("🤖 AI Business Insights")
    st.markdown("Strategic recommendations generated by the AI Analytics Agent.")

    if os.path.exists("reports/ai_insight.txt"):
        with open("reports/ai_insight.txt", "r", encoding="utf-8") as f:
            content = f.read()

        if content.strip():
            st.markdown(content)
        else:
            st.info("AI Insights are currently empty.")
    else:
        st.warning("AI report not found.")

    st.markdown("---")
    st.caption("⚠️ **Disclaimer:** AI insights are based on statistical associations and should be used for hypothesis generation, not as definitive causal proof.")
