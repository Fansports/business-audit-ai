import streamlit as st
import pandas as pd

# Attempt to import fpdf, install if missing
try:
    from fpdf import FPDF
except ImportError:
    import os
    os.system('pip install fpdf')
    from fpdf import FPDF

def generate_recommendations(use_seo, use_social_media, use_analytics, use_email_marketing, use_chatbots, use_crm):
    recommendations = []

    if not use_seo:
        recommendations.append(
            "Your business is not currently utilizing SEO, which can be a powerful driver for organic traffic "
            "and long-term customer acquisition. Consider using AI-powered SEO tools such as **SEMrush**, **Ahrefs**, "
            "or **Surfer SEO** to analyze search trends, optimize your content, and improve search engine rankings. "
            "These platforms can provide keyword recommendations, content suggestions, and backlink strategies to "
            "enhance your digital presence."
        )

    if not use_social_media:
        recommendations.append(
            "Leveraging social media can significantly increase brand visibility and engagement. AI-powered tools like "
            "**Hootsuite**, **Buffer**, and **Sprout Social** can automate your social media posts, analyze audience "
            "engagement, and suggest optimal posting times. Additionally, platforms like **ChatGPT for Social Media** or "
            "**Canva’s AI-powered design tools** can generate high-performing content effortlessly."
        )

    if not use_email_marketing:
        recommendations.append(
            "Email marketing is one of the most effective ways to nurture leads and retain customers. AI-driven tools like "
            "**Mailchimp**, **HubSpot Email Marketing**, and **ActiveCampaign** can automate your campaigns, personalize content "
            "based on user behavior, and optimize send times for maximum engagement. Adding AI to your email marketing strategy "
            "can increase open rates and conversions."
        )

    if not use_chatbots:
        recommendations.append(
            "AI-powered chatbots can enhance customer interactions, provide instant responses, and automate customer service. "
            "Tools like **Drift**, **Intercom**, and **ChatGPT-powered assistants** can handle common inquiries, qualify leads, "
            "and improve customer satisfaction. Implementing a chatbot can free up your team while improving response times and user experience."
        )

    if not use_crm:
        recommendations.append(
            "Managing business performance manually via spreadsheets can be time-consuming and inefficient. AI-driven CRMs like "
            "**Salesforce Einstein AI**, **HubSpot CRM**, and **Zoho CRM** can automate data entry, provide predictive analytics, "
            "and help you track customer interactions effectively. Moving to a CRM can enhance efficiency and improve business decision-making."
        )

    return recommendations

def generate_pdf_report(total_score, performance_tier, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Business Audit Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Score: {total_score}/100", ln=True)
    pdf.cell(200, 10, f"Performance Tier: {performance_tier}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Recommended AI Tools & Strategies:", ln=True, style='B')
    pdf.ln(5)
    
    for rec in recommendations:
        pdf.multi_cell(0, 10, rec)
        pdf.ln(5)
    
    pdf.ln(10)
    pdf.cell(200, 10, "For detailed recommendations, schedule a consultation.", ln=True)
    return pdf

def main():
    st.title("Business Audit Report Generator")

    # User details
    email = st.text_input("Business Email (Required)", "")
    use_seo = st.checkbox("Are you using SEO in your marketing strategy?")
    use_social_media = st.checkbox("Are you using Social Media for marketing?")
    use_email_marketing = st.checkbox("Are you using AI-powered Email Marketing?")
    use_chatbots = st.checkbox("Are you using AI Chatbots for customer interaction?")
    use_crm = st.checkbox("Are you using a CRM to track business performance?")

    if not email:
        st.warning("Please enter your business email to generate the report.")
        return

    if st.button("Generate Report"):
        total_score = 70  # Placeholder for scoring logic
        performance_tier = "Moderate Performer"  # Placeholder for performance category
        recommendations = generate_recommendations(use_seo, use_social_media, True, use_email_marketing, use_chatbots, use_crm)

        st.subheader("Audit Results")
        st.write(f"**Total Score:** {total_score}/100")
        st.write(f"**Performance Tier:** {performance_tier}")
        st.subheader("Recommended AI Tools & Strategies")
        for rec in recommendations:
            st.write(f"- {rec}")

        # Generate PDF report
        pdf = generate_pdf_report(total_score, performance_tier, recommendations)
        pdf.output("business_audit_report.pdf")
        with open("business_audit_report.pdf", "rb") as file:
            st.download_button("Download Report", file, file_name="Business_Audit_Report.pdf")

if __name__ == "__main__":
    main()
