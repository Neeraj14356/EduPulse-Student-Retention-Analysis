import os
from fpdf import FPDF

class EduPulseReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "EduPulse: Student Retention & Dropout Analytics", 0, 1, "R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | Confidential Business Report", 0, 0, "C")

    def section_title(self, title):
        self.ln(10)
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 51, 102) # Dark Blue
        self.cell(0, 10, title, 0, 1, "L")
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def subsection_title(self, title):
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, 0, 1, "L")

    def body_text(self, text):
        self.set_font("Arial", "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def highlight_box(self, text):
        self.ln(5)
        self.set_fill_color(240, 240, 240)
        self.set_font("Arial", "I", 11)
        self.multi_cell(0, 7, text, fill=True)
        self.ln(5)

def generate_report():
    pdf = EduPulseReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title Page
    pdf.ln(40)
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 20, "EduPulse: Student Retention", 0, 1, "C")
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "& Dropout Analytics", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Strategic Business Analysis Report", 0, 1, "C")
    pdf.ln(20)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Target Audience: Executive Management, Client Stakeholders", 0, 1, "C")
    pdf.cell(0, 10, "Date: October 12, 2026", 0, 1, "C")

    pdf.add_page()

    # A. Executive Summary
    pdf.section_title("A. Executive Summary")
    pdf.body_text("Student attrition presents a significant operational and financial challenge for higher education institutions. The EduPulse project provides a data-driven framework to identify primary academic and financial drivers of dropout.")
    pdf.highlight_box("Key Validated Findings:\n- Financial Criticality: Overdue tuition fees correlate with an 86.5% dropout rate.\n- Academic Warning Signs: Dropout students average a 2nd-semester grade of 5.90 vs 12.70 for graduates.\n- High-Risk Nexus: Combined poor performance (Grade < 8) and overdue fees lead to a 97% attrition rate.\n- Protective Factors: Scholarship holders show only a 12.2% dropout rate.")
    pdf.body_text("Strategic Recommendation: Implement a Dual-Track Intervention System focusing on immediate financial outreach and 2nd-semester academic recovery programs.")

    # B. Business Problem
    pdf.section_title("B. Business Problem and Objectives")
    pdf.body_text("Student dropout is a critical business risk. High attrition leads to lost tuition revenue and decreased institutional prestige. EduPulse aims to identify the earliest reliable indicators of attrition to enable proactive intervention.")

    # C. Data Overview
    pdf.section_title("C. Data Overview")
    pdf.body_text("The analysis is based on 4,424 student records. Distribution of outcomes:\n- Graduates: 49.93%\n- Dropouts: 32.12%\n- Enrolled: 17.95%")

    # D. Key Business Findings
    pdf.section_title("D. Key Business Findings")
    pdf.subsection_title("1. Financial Impact")
    pdf.body_text("Financial stress is the strongest leading indicator. Tuition fees overdue: 86.5% dropout; Debtors: 62% dropout. Scholarship holders: 12.2% dropout.")
    pdf.subsection_title("2. The High-Risk Segment")
    pdf.body_text("Students combining poor academic performance (Grade < 8) and overdue fees exhibit a 97% dropout rate, representing a near-certainty of attrition.")

    # E. Academic Performance
    pdf.section_title("E. Academic Performance")
    pdf.body_text("A statistically significant gap exists in 2nd-semester performance. Graduates averaged 12.70 grades and 6.18 approved units, whereas dropouts averaged 5.90 grades and 1.94 approved units.")

    # F. Financial and Demographic Patterns
    pdf.section_title("F. Financial and Demographic Patterns")
    pdf.body_text("Financial aid acts as a powerful stabilizer. The contrast between scholarship holders (12.2%) and non-holders (38.7%) suggests that removing financial anxiety directly impacts persistence.")

    # G. Power BI Dashboard
    pdf.section_title("G. Power BI Dashboard")
    pdf.body_text("The interactive dashboard enables management to explore these patterns:\n- Executive Overview: Health check of student body by age and financial status.\n- Dropout Drivers: Tracking the 2nd-semester 'danger zone'.\n- Statistical Insights: Validated evidence (p < 0.05) to justify intervention budgets.")

    # H. Recommendations
    pdf.section_title("H. Recommendations and Action Plan")
    pdf.body_text("1. Critical: Tuition Alert System to prevent attrition from immediate financial crises.\n2. High: 2nd-Semester Academic Bridge for students showing early performance dips.\n3. Medium: Expansion of Scholarship programs to stabilize at-risk populations.")

    # I. Reporting Automation
    pdf.section_title("I. Reporting Automation")
    pdf.body_text("The Python-n8n-AI pipeline automates the flow from raw data to stakeholder email. This reduces reporting latency and translates complex statistics into plain-language business insights.")

    # J. Limitations
    pdf.section_title("J. Limitations and Responsible Interpretation")
    pdf.body_text("Analysis identifies associations, not causation. Group patterns do not dictate individual fate. Recommendations should be balanced with institutional context.")

    # K. Conclusion
    pdf.section_title("K. Conclusion")
    pdf.body_text("EduPulse proves that retention is a manageable problem. By addressing financial instability and academic decline in the second semester, the institution can secure revenue and improve student success.")

    pdf.output("reports/EduPulse_Project_Report.pdf")

if __name__ == "__main__":
    generate_report()
