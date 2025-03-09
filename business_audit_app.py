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

def generate_recommendations(update_frequency, lead_methods, marketing_effectiveness, seo_score, ai_marketing, ai_tools, ai_operations, performance_tracking):
    recommendations = []

    if seo_score == "Poor":
        recommendations.append("Your SEO presence is lacking. Consider using tools like SEMrush, Ahrefs, or Google Search Console to optimize your website for better search engine ranking.")
    if "Social Media Engagement" not in lead_methods:
        recommendations.append("You're not leveraging social media. AI tools like Hootsuite or Buffer can help automate and optimize your social media marketing.")
    if ai_marketing in ["No, but I’m interested", "No, not applicable"]:
        recommendations.append("You’re not currently using AI in marketing. Tools like ChatGPT for content creation, Adzooma for AI-driven ads, and HubSpot’s AI analytics could improve efficiency.")
    if performance_tracking == "Not tracking performance data":
        recommendations.append("You're not tracking performance data. Consider adopting a CRM like HubSpot or Salesforce to streamline and monitor key business metrics.")

    return recommendations

def generate_pdf_report(total_score, performance_tier, email, name, business, industry, website, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    
    def safe_text(text):
        """Ensure text is encoded in a PDF-safe format (latin-1)."""
        return text.encode("latin-1", "replace").decode("latin-1")
    
    pdf.cell(200, 10, safe_text("Business Audit Report"), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, safe_text(f"Total Score: {total_score}/100"), ln=True)
    pdf.cell(200, 10, safe_text(f"Performance Tier: {performance_tier}"), ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, safe_text(f"Business Email: {email}"), ln=True)
    if name:
        pdf.cell(200, 10, safe_text(f"Name: {name}"), ln=True)
    if business:
        pdf.cell(200, 10, safe_text(f"Business: {business}"), ln=True)
    if industry:
        pdf.cell(200, 10, safe_text(f"Industry: {industry}"), ln=True)
    if website:
        pdf.cell(200, 10, safe_text(f"Website: {website}"), ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, safe_text("Recommendations:"), ln=True)
    pdf.ln(5)

    for rec in recommendations:
        pdf.multi_cell(0, 10, safe_text(rec))
        pdf.ln(5)
    
    pdf.cell(200, 10, safe_text("For detailed recommendations, schedule a consultation."), ln=True)
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
    
    if st.button("Generate Report"):
        total_score = score_website_marketing(update_frequency, lead_methods, marketing_effectiveness, seo_score)
        performance_tier = "Moderate Performer" if total_score >= 70 else "Needs Improvement"
        recommendations = generate_recommendations(update_frequency, lead_methods, marketing_effectiveness, seo_score, ai_marketing, ai_tools, ai_operations, performance_tracking)

        st.subheader("Audit Results")
        st.write(f"**Total Score:** {total_score}/100")
        st.write(f"**Performance Tier:** {performance_tier}")
        st.subheader("Recommendations")
        for rec in recommendations:
            st.write(f"- {rec}")

        # Generate PDF report
        pdf = generate_pdf_report(total_score, performance_tier, email, name, business, industry, website, recommendations)
        pdf.output("business_audit_report.pdf")
        with open("business_audit_report.pdf", "rb") as file:
            st.download_button("Download Report", file, file_name="Business_Audit_Report.pdf")

if __name__ == "__main__":
    main()
