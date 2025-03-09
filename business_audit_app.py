import streamlit as st
import pandas as pd

# Attempt to import fpdf, install if missing
try:
    from fpdf import FPDF
except ImportError:
    import os
    os.system('pip install fpdf')
    from fpdf import FPDF

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
    update_frequency = st.selectbox("How frequently do you update your website?", ["Weekly", "Monthly", "Every few months", "Rarely/Never", "Other"])
    lead_methods = st.multiselect("How do you generate leads?", ["SEO / Organic Traffic", "Paid Ads (Google, Facebook, etc.)", "Social Media Engagement", "Email Marketing", "Word-of-mouth / Referrals", "Other"])
    marketing_effectiveness = st.selectbox("How effective is your marketing?", ["Very effective", "Somewhat effective", "Neutral", "Not very effective", "Not effective at all"])
    seo_score = st.selectbox("How would you rate your SEO & digital presence?", ["Excellent", "Good", "Average", "Poor"])
    ai_marketing = st.selectbox("Are you using AI in marketing?", ["Yes, extensively", "Yes, but only in specific areas", "No, but I’m interested", "No, not applicable"])
    ai_tools = st.multiselect("Which AI-powered tools do you use?", ["AI chatbots for customer service", "AI-driven content generation", "AI-powered analytics & insights", "AI-based SEO tools", "AI-driven advertising optimization", "Not using AI", "Other"])
    ai_operations = st.selectbox("Are you using AI automation in operations?", ["Yes, extensively", "Yes, but only in specific areas", "No, but interested", "No, not applicable"])
    performance_tracking = st.selectbox("How do you track business performance?", ["Business intelligence dashboards", "CRM", "Spreadsheets / Manual tracking", "Not tracking performance data"])
    operational_challenges = st.multiselect("What are your biggest operational challenges? (Choose up to 3)", ["Inefficient workflows", "Customer retention issues", "High acquisition costs", "Lack of automation", "Lack of data-driven decision-making", "Employee productivity & training", "Other"])
    efficiency_score = st.selectbox("How efficient are your processes?", ["Excellent", "Good", "Average", "Poor"])

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
