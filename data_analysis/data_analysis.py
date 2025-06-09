import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from PyPDF2 import PdfReader

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

# Extract metrics from text using updated regex
def extract_health_metrics(text):
    metrics = {}
    patterns = {
        'Hemoglobin': r"Hemoglobin\s+([\d.]+)",
        'RBC Count': r"RBC\s+Count\s+([\d.]+)",
        'Hematocrit': r"Hematocrit\s+([\d.]+)",
        'MCV': r"MCV\s+([\d.]+)",
        'MCH': r"MCH\s+([\d.]+)",
        'MCHC': r"MCHC\s+([\d.]+)",
        'RDW CV': r"RDW\s+CV\s+([\d.]+)",
        'WBC': r"WBC\s+Count\s+([\d,]+)",
        'Neutrophils': r"Neutrophils\s+([\d]+)",
        'Lymphocytes': r"Lymphocytes\s+([\d]+)",
        'Eosinophils': r"Eosinophils\s+([\d]+)",
        'Monocytes': r"Monocytes\s+([\d]+)",
        'Basophils': r"Basophils\s+([\d]+)",
        'Platelets': r"Platelet\s+Count\s+([\d,]+)",
        'MPV': r"MPV\s+([\d.]+)",
        'ESR': r"ESR\s+([\d.]+)",
        'Cholesterol': r"Cholesterol\s+([\d.]+)",
        'Triglycerides': r"Triglyceride[s]?\s+([\d.]+)",
        'HDL': r"HDL\s+Cholesterol\s+([\d.]+)",
        'LDL': r"Direct\s+LDL\s+([\d.]+)",
        'VLDL': r"VLDL\s+([\d.]+)",
        'CHOL/HDL Ratio': r"CHOL/HDL\s+Ratio\s+([\d.]+)",
        'LDL/HDL Ratio': r"LDL/HDL\s+Ratio\s+([\d.]+)",
        'ABO Type': r"ABO\s+Type\s+\"?([ABO]+)\"?",
        'Rh (D) Type': r"Rh\s+\(D\)\s+Type\s+(Positive|Negative)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1).replace(",", "").strip()
            try:
                if "/" in val:
                    metrics[key] = val
                else:
                    metrics[key] = float(val)
            except ValueError:
                continue
    return metrics

# Display metrics in a table and bar chart
def display_metric_summary(metrics):
    if not metrics:
        st.warning("⚠️ No recognizable health metrics found.")
        return

    st.subheader("📊 Extracted Health Metrics")
    df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.table(df)

    numeric_df = df[df['Value'].apply(lambda x: isinstance(x, (int, float)))]
    st.bar_chart(numeric_df.set_index("Metric"))

# Health condition prediction logic
def predict_conditions(metrics):
    st.subheader("🧠 AI-based Risk Assessment")

    if 'Hemoglobin' in metrics:
        if metrics['Hemoglobin'] < 12:
            st.error("🔴 Possible Anemia (Low Hemoglobin)")
        else:
            st.success("🟢 Hemoglobin looks normal")

    if 'Glucose' in metrics:
        if metrics['Glucose'] > 125:
            st.error("🔴 Possible Diabetes (High Glucose)")
        elif metrics['Glucose'] > 100:
            st.warning("🟡 Pre-diabetic range")
        else:
            st.success("🟢 Glucose level is normal")

    if 'HbA1c' in metrics:
        if metrics['HbA1c'] >= 6.5:
            st.error("🔴 Diabetes Confirmed (HbA1c)")
        elif metrics['HbA1c'] >= 5.7:
            st.warning("🟡 Pre-diabetes (HbA1c)")
        else:
            st.success("🟢 HbA1c is in normal range")

    if 'Cholesterol' in metrics and metrics['Cholesterol'] > 200:
        st.warning("🟡 Elevated Total Cholesterol - Watch diet")

    if 'Triglycerides' in metrics and metrics['Triglycerides'] > 150:
        st.warning("🟡 Elevated Triglycerides - Reduce sugars/fats")

    if 'Vitamin B12' in metrics and metrics['Vitamin B12'] < 200:
        st.error("🔴 Possible Vitamin B12 Deficiency")

    if 'IgE' in metrics and metrics['IgE'] > 300:
        st.warning("🟡 Elevated IgE - Possible Allergy or Parasitic Infection")

# Optional: Download analytics as CSV
def download_metrics(metrics):
    if metrics:
        df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Report", csv, "health_metrics.csv", "text/csv")

# Streamlit UI
st.title("🩺 Health Metrics Extractor from PDF")
uploaded_file = st.file_uploader("📄 Upload Your Health Report (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    metrics = extract_health_metrics(text)
    display_metric_summary(metrics)
    predict_conditions(metrics)
    download_metrics(metrics)
