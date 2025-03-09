import streamlit as st
import pandas as pd

# Attempt to import fpdf, install if missing
try:
    from fpdf import FPDF
except ImportError:
    import os
    os.system('pip install fpdf')
    from fpdf import FPDF

def score_website_marketing(update_frequency, lead_methods, marketing_effectiveness, seo_score):
    update_scores = {"Weekly": 10, "Monthly": 8, "Every few months": 5, "Rarely/Never": 2, "Other": 4}
    marketing_effectiveness_scores = {"Very effective": 10, "Somewhat effective": 8, "Neutral": 5, "Not very effective": 3, "Not effective at all": 1}
    seo_scores = {"Excellent": 10, "Good": 7, "Average": 5, "Poor": 2}

    update_score = update_scores.get(update_frequency, 0)
    lead_score = min(len(lead_methods) * 2, 10)
    marketing_score = marketing_effectiveness_scores.get(marketing_effectiveness, 0)
    seo_score = seo_scores.get(seo_score, 0)

    return update_score + lead_score + marketing_score + seo_score

def score_ai_automation(ai_marketing, ai_tools, ai_operations):
    ai_marketing_scores = {"Yes, extensively": 10, "Yes, but only in specific areas": 7, "No, but I’m interested": 5, "No, not applicable": 2}
    ai_operations_scores = {"Yes, extensively": 10, "Yes, but only in specific areas": 7, "No, but interested": 5, "No, not applicable": 2}

    ai_marketing_score = ai_marketing_scores.get(ai_marketing, 0)
    ai_tools_score = min(len(ai_tools) * 2, 10)
    ai_operations_score = ai_operations_scores.get(ai_operations, 0)

    return ai_marketing_score + ai_tools_score + ai_operations_score

def score_operational_management(performance_tracking, operational_challenges, efficiency_score):
    tracking_scores = {"Business intelligence dashboards": 10, "CRM": 8, "Spreadsheets / Manual tracking": 5, "Not tracking performance data": 0}
    efficiency_scores = {"Excellent": 10, "Good": 7, "Average": 5, "Poor": 2}

    tracking_score = tracking_scores.get(performance_tracking, 0)
    challenges_penalty = min(len(operational_challenges) * 2, 6)
    efficiency_score = efficiency_scores.get(efficiency_score, 0)

    return tracking_score + (10 - challenges_penalty) + efficiency_score

def generate_pdf_report(total_score, performance_tier, email, name, business, industry, website):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Business Audit Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Score: {total_score}/100", ln=True)
    pdf.cell(200, 10, f"Performance Tier: {performance_tier}", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, f"Business Email: {email}", ln=True)
    if name:
        pdf.cell(200, 10, f"Name: {name}", ln=True)
    if business:
        pdf.cell(200, 10, f"Business: {business}", ln=True)
    if industry:
        pdf.cell(200, 10, f"Industry: {industry}", ln=True)
    if website:
        pdf.cell(200, 10, f"Website: {website}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, "For detailed recommendations, schedule a consultation.", ln=True)
    return pdf

def main():
    st.title("Business Audit Report Generator")

    # User details
    email = st.text_input("Business Email (Required)", "")
    name = st.text_input("Your Name (Optional)", "")
    business = st.text_input("Business Name (Optional)", "")
    industry = st.text_input("Industry (Optional)", "")
    website = st.text_input("Website URL (Optional)", "")
    
    if not email:
        st.warning("Please enter your business email to generate the report.")
        return

    # User inputs
    update_frequency = st.selectbox("How frequently do you update your website?", ["", "Weekly", "Monthly", "Every few months", "Rarely/Never", "Other"])
    lead_methods = st.multiselect("How do you generate leads?", [])
    marketing_effectiveness = st.selectbox("How effective is your marketing?", ["", "Very effective", "Somewhat effective", "Neutral", "Not very effective", "Not effective at all"])
    seo_score = st.selectbox("How would you rate your SEO & digital presence?", ["", "Excellent", "Good", "Average", "Poor"])
    ai_marketing = st.selectbox("Are you using AI in marketing?", ["", "Yes, extensively", "Yes, but only in specific areas", "No, but I’m interested", "No, not applicable"])
    ai_tools = st.multiselect("Which AI-powered tools do you use?", [])
    ai_operations = st.selectbox("Are you using AI automation in operations?", ["", "Yes, extensively", "Yes, but only in specific areas", "No, but interested", "No, not applicable"])
    performance_tracking = st.selectbox("How do you track business performance?", ["", "Business intelligence dashboards", "CRM", "Spreadsheets / Manual tracking", "Not tracking performance data"])
    operational_challenges = st.multiselect("What are your biggest operational challenges? (Choose up to 3)", [])
    efficiency_score = st.selectbox("How efficient are your processes?", ["", "Excellent", "Good", "Average", "Poor"])

    if st.button("Generate Report"):
        website_marketing_score = score_website_marketing(update_frequency, lead_methods, marketing_effectiveness, seo_score)
        ai_automation_score = score_ai_automation(ai_marketing, ai_tools, ai_operations)
        operational_management_score = score_operational_management(performance_tracking, operational_challenges, efficiency_score)

        total_score = website_marketing_score + ai_automation_score + operational_management_score

        if total_score >= 85:
            performance_tier = "Strong Performer"
        elif total_score >= 70:
            performance_tier = "Moderate Performer"
        elif total_score >= 50:
            performance_tier = "Needs Improvement"
        else:
            performance_tier = "At Risk"

        st.subheader("Audit Results")
        st.write(f"**Total Score:** {total_score}/100")
        st.write(f"**Performance Tier:** {performance_tier}")

        # Generate PDF report
        pdf = generate_pdf_report(total_score, performance_tier, email, name, business, industry, website)
        pdf.output("business_audit_report.pdf")
        with open("business_audit_report.pdf", "rb") as file:
            st.download_button("Download Report", file, file_name="Business_Audit_Report.pdf")

if __name__ == "__main__":
    main()
