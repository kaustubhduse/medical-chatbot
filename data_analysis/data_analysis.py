import re
import streamlit as st
import pandas as pd

# ========== METRIC EXTRACTION ==========

def extract_health_metrics(text):
    """
    Generalized extraction of medical metrics from any report format.
    Returns a dict with metric names and numeric values.
    """
    metrics = {}
    patterns = {
        'Hemoglobin': r'(?i)(?:hemoglobin|hb)[^\d]*(\d+\.?\d*)\s*(?:g/dL|g%|gm%)?',
        'WBC': r'(?i)(?:white\s*blood\s*cell|wbc|tlc)[^\d]*(\d{3,6})\s*(?:cells?/mm3|/mm3|cumm)?',
        'Platelets': r'(?i)(?:platelet\s*count|platelets|plt)[^\d]*(\d{3,6})\s*(?:cells?/mm3|/mm3|cumm)?',
        'RBC': r'(?i)(?:rbc|red\s*blood\s*cell)[^\d]*(\d+\.?\d*)\s*(?:mill?/mm3)?',
        'Hematocrit': r'(?i)(?:hematocrit|pcv|packed\s*cell\s*volume)[^\d]*(\d+\.?\d*)\s*%?',
        'MCV': r'(?i)mcv[^\d]*(\d+\.?\d*)\s*fL?',
        'MCH': r'(?i)mch[^\d]*(\d+\.?\d*)\s*pg?',
        'MCHC': r'(?i)mchc[^\d]*(\d+\.?\d*)\s*g/dL?',
        'RDW': r'(?i)rdw[^\d]*(\d+\.?\d*)\s*%?',
        'Neutrophils': r'(?i)neutrophils[^\d]*(\d+\.?\d*)\s*%?',
        'Lymphocytes': r'(?i)lymphocytes[^\d]*(\d+\.?\d*)\s*%?',
        'Eosinophils': r'(?i)eosinophils[^\d]*(\d+\.?\d*)\s*%?',
        'Monocytes': r'(?i)monocytes[^\d]*(\d+\.?\d*)\s*%?',
        'Basophils': r'(?i)basophils[^\d]*(\d+\.?\d*)\s*%?',
        'Blood Pressure': r'(?i)(?:blood\s*pressure|bp)[^\d]*(\d+\s*/\s*\d+)'
    }
    for metric, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            value = clean_numeric(matches[-1])
            if value is not None:
                metrics[metric] = value

    # Handle percentage normalization
    percent_metrics = ['Hematocrit', 'Neutrophils', 'Lymphocytes', 
                       'Eosinophils', 'Monocytes', 'Basophils', 'RDW']
    for metric in percent_metrics:
        if metric in metrics:
            value = metrics[metric]
            if 0 < value < 1:
                metrics[metric] = value * 100

    return metrics

def clean_numeric(value):
    """Convert string numbers to float/int, handle BP as string."""
    try:
        cleaned = str(value).replace(',', '').replace(' ', '')
        if '/' in cleaned:  # Blood pressure
            return cleaned
        if '.' in cleaned:
            return float(cleaned)
        return int(cleaned)
    except:
        return None

# ========== DISPLAY AND ANALYSIS ==========

REFERENCE_RANGES = {
    'Hemoglobin': (13, 17),
    'WBC': (4000, 11000),
    'Platelets': (150000, 410000),
    'RBC': (4.5, 5.5),
    'Hematocrit': (40, 50),
    'MCV': (83, 101),
    'MCH': (27, 32),
    'MCHC': (32.5, 34.5),
    'RDW': (11.6, 14.0),
    'Neutrophils': (50, 62),
    'Lymphocytes': (20, 40),
    'Eosinophils': (0, 6),
    'Monocytes': (0, 10),
    'Basophils': (0, 2)
}

def display_metric_summary(metrics):
    if not metrics:
        st.warning("⚠️ No recognizable health metrics found.")
        return
    rows = []
    for metric, value in metrics.items():
        ref = REFERENCE_RANGES.get(metric, ("N/A", "N/A"))
        status = get_status(value, ref)
        rows.append({
            "Metric": metric,
            "Value": value,
            "Reference Range": f"{ref[0]} - {ref[1]}" if ref[0] != "N/A" else "N/A",
            "Status": status
        })
    df = pd.DataFrame(rows)
    st.subheader("📊 Extracted Health Metrics")
    st.dataframe(df, use_container_width=True)
    # Bar chart for numeric metrics
    numeric_df = df[df['Value'].apply(lambda x: isinstance(x, (int, float)))]
    if not numeric_df.empty:
        st.bar_chart(numeric_df.set_index("Metric")["Value"])

def get_status(value, ref):
    if ref == ("N/A", "N/A") or value is None or isinstance(value, str):
        return "Unknown"
    try:
        low, high = ref
        if value < low:
            return "Low"
        elif value > high:
            return "High"
        else:
            return "Normal"
    except:
        return "Unknown"

def predict_conditions(metrics):
    st.subheader("🧠 AI-based Risk Assessment")
    if 'Hemoglobin' in metrics and metrics['Hemoglobin'] < 13:
        st.error(f"🔴 Anemia: Low hemoglobin ({metrics['Hemoglobin']} g/dL)")
    if 'Hematocrit' in metrics and metrics['Hematocrit'] > 50:
        st.warning(f"🟡 High PCV/Hematocrit ({metrics['Hematocrit']}%)")
    if 'WBC' in metrics:
        wbc = metrics['WBC']
        if wbc > 11000:
            st.warning(f"🟡 High WBC ({wbc}) - Possible infection")
        elif wbc < 4000:
            st.warning(f"🟡 Low WBC ({wbc}) - Possible immune issue")
    if 'Platelets' in metrics:
        plt = metrics['Platelets']
        if plt < 150000:
            st.error(f"🔴 Low platelets ({plt}) - Bleeding risk")
        elif plt > 410000:
            st.warning(f"🟡 High platelets ({plt}) - Possible inflammation")

def download_metrics(metrics):
    if metrics:
        df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Metrics (CSV)", 
            csv, 
            "medical_metrics.csv", 
            "text/csv"
        )
