import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# -------------------------
# 1. Extract Metrics
# -------------------------
def extract_health_metrics(text):
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
        'Vitamin B12': r'Vitamin\s*B12.*?:\s*[<?]?\s*([\d.]+)',
        'PSA': r'Prostate Specific Antigen.*?:\s*([\d.]+)',
        'IgE': r'IgE.*?:\s*([\d.]+)',
        'Blood Pressure': r'(?:Blood Pressure|BP).*?:?\s*(\d+/\d+)',
    }
    metrics = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = match.group(1).replace(",", "").strip()
            try:
                if '/' in val:
                    metrics[key] = val
                else:
                    metrics[key] = float(val)
            except ValueError:
                continue
    return metrics

# -------------------------
# 2. Disease Risk Prediction
# -------------------------
def predict_conditions(metrics):
    risks = []
    if 'Hemoglobin' in metrics and metrics['Hemoglobin'] < 12:
        risks.append("Anemia")
    if 'Glucose' in metrics and metrics['Glucose'] > 125:
        risks.append("Diabetes")
    if 'HbA1c' in metrics and metrics['HbA1c'] > 6.5:
        risks.append("Poor Glycemic Control")
    if 'Cholesterol' in metrics and metrics['Cholesterol'] > 200:
        risks.append("High Cholesterol")
    if 'Triglycerides' in metrics and metrics['Triglycerides'] > 150:
        risks.append("High Triglycerides")
    if 'Vitamin B12' in metrics and metrics['Vitamin B12'] < 200:
        risks.append("Vitamin B12 Deficiency")
    if 'IgE' in metrics and metrics['IgE'] > 300:
        risks.append("Possible Allergy")
    return risks

# -------------------------
# 3. Smart Report Comparator
# -------------------------
def compare_reports(report1, report2):
    df = pd.DataFrame([report1, report2], index=['Report 1', 'Report 2'])
    df.fillna(0, inplace=True)
    df_numeric = df.select_dtypes(include=[float, int])
    sim_score = cosine_similarity([df_numeric.loc['Report 1']], [df_numeric.loc['Report 2']])[0][0]
    return sim_score

# -------------------------
# 4. User Dashboard
# -------------------------
def display_user_dashboard(metrics, risks):
    st.subheader("👤 User Health Dashboard")
    df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.dataframe(df.set_index("Metric"))
    if risks:
        st.warning("⚠️ Risks Detected: " + ", ".join(risks))
    else:
        st.success("✅ No major risks found.")

# -------------------------
# 5. Population Insights
# -------------------------
def population_insights(all_user_data):
    st.subheader("🏥 Population Insights")
    df = pd.DataFrame(all_user_data)
    if df.empty:
        st.info("No population data to analyze.")
        return
    st.bar_chart(df.mean(numeric_only=True))
    st.write("Distribution:")
    st.dataframe(df.describe())

# -------------------------
# 6. Hospital Analytics
# -------------------------
def hospital_analytics(df):
    st.subheader("🏨 Hospital Analytics")
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# -------------------------
# Entry Point (for external use)
# -------------------------
def analyze_report(text, user_id=None):
    metrics = extract_health_metrics(text)
    risks = predict_conditions(metrics)
    return metrics, risks
