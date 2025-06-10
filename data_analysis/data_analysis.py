import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO

def extract_health_metrics(text):
    metrics = {}
    table_metrics = extract_tabular_data(text)
    metrics.update(table_metrics)
    text_metrics = extract_from_unstructured_text(text)
    metrics.update(text_metrics)
    return metrics

def extract_tabular_data(text):
    metrics = {}
    table_pattern = r'\\begin{tabular}.*?\\end{tabular}'
    tables = re.findall(table_pattern, text, re.DOTALL)
    
    for table in tables:
        rows = re.findall(r'\\hline\s*(.*?)\s*\\\\', table, re.DOTALL)
        for row in rows:
            cols = re.split(r'[&|]', row)
            if len(cols) >= 2:
                metric_name = clean_metric_name(cols[0])
                metric_value = parse_value(cols[1])
                if metric_name and metric_value is not None:
                    metrics[metric_name] = metric_value
    return metrics

def clean_metric_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\b(Calculated|Count|Total)\b', '', name).strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def parse_value(value):
    try:
        value = value.replace(',', '').replace(' ', '')
        if '/' in value:
            return value
        return float(value) if '.' in value else int(value)
    except:
        return None

def extract_from_unstructured_text(text):
    metrics = {}
    patterns = {
        'Hemoglobin': r'Hemoglobin[^:\n]*[:&]?\s*([\d.]+)',
        'WBC': r'(?:White\s*Blood\s*Cell|WBC)[^:\n]*[:&]?\s*([\d,]+)',
        'Platelets': r'Platelet[^:\n]*[:&]?\s*([\d,]+)',
        'RBC': r'RBC[^:\n]*[:&]?\s*([\d.]+)',
        'Cholesterol': r'(?:Total\s*)?Cholesterol[^:\n]*[:&]?\s*([\d.]+)',
        'HDL': r'HDL[^:\n]*[:&]?\s*([\d.]+)',
        'LDL': r'LDL[^:\n]*[:&]?\s*([\d.]+)',
        'Glucose': r'(?:Fasting\s*)?(?:Blood\s*Sugar|Glucose)[^:\n]*[:&]?\s*([\d.]+)',
        'Blood Pressure': r'(?:BP|Blood\s*Pressure)[^:\n]*[:&]?\s*(\d+\s*/\s*\d+)'
    }

    for metric, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            val = parse_value(match.group(1))
            if val is not None:
                metrics[metric] = val
                break
    return metrics

# ===== MISSING FUNCTIONS THAT APP.PY NEEDS =====

def display_metric_summary(metrics):
    """Display metrics in table and chart format"""
    if not metrics:
        st.warning("⚠️ No recognizable health metrics found.")
        return

    st.subheader("📊 Extracted Health Metrics")
    df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.table(df)

    # Create bar chart for numeric values only
    numeric_df = df[df['Value'].apply(lambda x: isinstance(x, (int, float)))]
    if not numeric_df.empty:
        st.bar_chart(numeric_df.set_index("Metric"))

def predict_conditions(metrics):
    """Generate AI-based health predictions"""
    st.subheader("🧠 AI-based Risk Assessment")
    
    ref_ranges = {
        'Hemoglobin': (13, 17),
        'WBC': (4000, 11000),
        'Platelets': (150000, 410000),
        'RBC': (4.5, 5.5)
    }

    if 'Hemoglobin' in metrics:
        if metrics['Hemoglobin'] < 13:
            st.error("🔴 Possible Anemia (Low Hemoglobin)")
        else:
            st.success("🟢 Hemoglobin looks normal")

    if 'WBC' in metrics:
        if metrics['WBC'] > 11000:
            st.warning("🟡 Elevated WBC - Possible infection")
        elif metrics['WBC'] < 4000:
            st.warning("🟡 Low WBC - Possible immune issue")
        else:
            st.success("🟢 WBC count is normal")

    if 'Platelets' in metrics:
        if metrics['Platelets'] < 150000:
            st.error("🔴 Low Platelets - Bleeding risk")
        elif metrics['Platelets'] > 410000:
            st.warning("🟡 High Platelets - Possible inflammation")
        else:
            st.success("🟢 Platelet count is normal")

def download_metrics(metrics):
    """Enable CSV download of extracted metrics"""
    if metrics:
        df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Report (CSV)", 
            csv, 
            "health_metrics.csv", 
            "text/csv"
        )
