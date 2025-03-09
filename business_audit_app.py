import streamlit as st
import pandas as pd

# Attempt to import fpdf, install if missing
try:
    from fpdf import FPDF
except ImportError:
    import os
    os.system('pip install fpdf')
    from fpdf import FPDF

def generate_pdf_report(total_score, performance_tier):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Business Audit Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Score: {total_score}/100", ln=True)
    pdf.cell(200, 10, f"Performance Tier: {performance_tier}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "For detailed recommendations, schedule a consultation.", ln=True)
    return pdf
