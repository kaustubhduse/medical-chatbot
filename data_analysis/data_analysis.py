# data_analysis/data_analysis.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

# Extract metrics from text using regex
def extract_health_metrics(text):
    metrics = {}
    patterns = {
      'Hemoglobin': r'Hemoglobin.*?:\s*([\d.]+)',                # allows anything between Hemoglobin and colon
      'RBC': r'RBC.*?:\s*([\d.]+)',
      'WBC': r'WBC.*?:\s*([\d,]+)',                            # allow commas in numbers (e.g. 10,570)
      'Platelets': r'Platelet.*?:\s*([\d,]+)',
      'Glucose': r'Glucose.*?:\s*([\d.]+)',
      'Creatinine': r'Creatinine.*?:\s*([\d.]+)',
      'Urea': r'Urea.*?:\s*([\d.]+)',
      'Cholesterol': r'Cholesterol.*?:\s*([\d.]+)',
      'Blood Pressure': r'(?:Blood Pressure|BP).*?:?\s*(\d+/\d+)',
    }

    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1).replace(",", "").strip()
            val = re.match(r"[\d.]+", val).group()
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

    if 'Cholesterol' in metrics and metrics['Cholesterol'] > 200:
        st.warning("🟡 Elevated Cholesterol - Watch diet")

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
