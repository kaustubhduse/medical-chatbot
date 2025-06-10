import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

# Extract metrics from text using regex
def extract_health_metrics(text):
    metrics = {}
    patterns = {
        'Hemoglobin': r'Hemoglobin.*?:\s*([\d.]+)',
        'WBC': r'(?:White\s*Blood\s*Cell.*?|WBC.*?)[:\s]*([\d,]+)',
        'Platelets': r'Platelet.*?:\s*([\d,]+)',
        'RBC': r'RBC.*?:\s*([\d.]+)',
        'Cholesterol': r'Total\s*Cholesterol.*?:\s*([\d.]+)',
        'HDL': r'HDL\s*Cholesterol.*?:\s*([\d.]+)',
        'LDL': r'LDL\s*Cholesterol.*?:\s*([\d.]+)',
        'Triglycerides': r'Triglycerides.*?:\s*([\d.]+)',
        'Glucose': r'(?:Fasting\s*Blood\s*Sugar|Glucose).*?:\s*([\d.]+)',
        'HbA1c': r'HbA1c.*?:\s*([\d.]+)',
        'T3': r'T3.*?:\s*([\d.]+)',
        'T4': r'T4.*?:\s*([\d.]+)',
        'TSH': r'TSH.*?:\s*([\d.]+)',
        'Vitamin B12': r'Vitamin\s*B12.*?:\s*[<]?\s*([\d.]+)',
        'PSA': r'Prostate Specific Antigen.*?:\s*([\d.]+)',
        'IgE': r'IgE.*?:\s*([\d.]+)',
        'Blood Pressure': r'(?:Blood Pressure|BP).*?:?\s*(\d+/\d+)',
    }

    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1).replace(",", "").strip()
            val_match = re.match(r"[\d./]+", val)
            if not val_match:
                continue
            val = val_match.group()
            try:
                if '/' in val:
                    metrics[metric] = val  # BP case
                else:
                    metrics[metric] = float(val)
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

# Simple rule-based prediction system
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

    if 'Blood Pressure' in metrics:
        try:
            sys, dia = map(int, metrics['Blood Pressure'].split('/'))
            if sys >= 140 or dia >= 90:
                st.error("🔴 Hypertension Detected")
            elif sys >= 120 or dia >= 80:
                st.warning("🟡 Prehypertension")
            else:
                st.success("🟢 Blood Pressure is normal")
        except:
            st.warning("❌ Could not parse blood pressure reading.")

# Optional: Download analytics as a report (CSV)
def download_metrics(metrics):
    if metrics:
        df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Report", csv, "health_metrics.csv", "text/csv")
