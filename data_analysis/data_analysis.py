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

def clean_metric_name(name):
    """Standardize metric names for matching."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    mapping = {
        'hb': 'hemoglobin',
        'packedcellvolume': 'hematocrit',
        'pcv': 'hematocrit',
        'tlc': 'wbc',
        'plt': 'platelets',
        'plateletcount': 'platelets',
        'redbloodcell': 'rbc'
    }
    return mapping.get(name, name)

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

# ========== REFERENCE RANGE EXTRACTION ==========

def extract_reference_ranges(text):
    """
    Extract reference ranges for each metric from the report text.
    Returns a dict: {metric_name: (low, high)}
    """
    ref_ranges = {}

    # Table row pattern: Metric | Value | ... | Reference Range | Unit
    table_row_pattern = re.compile(
        r'([A-Za-z \(\)%]+)[\s|:&]+[\d.,/]+[\s|:&]+[A-Za-z]*[\s|:&]+([\d.]+)\s*-\s*([\d.]+)', re.IGNORECASE
    )
    for match in table_row_pattern.finditer(text):
        metric = clean_metric_name(match.group(1))
        low = float(match.group(2))
        high = float(match.group(3))
        ref_ranges[metric] = (low, high)

    # Inline pattern: Metric ... reference range ... low - high
    inline_pattern = re.compile(
        r'([A-Za-z \(\)%]+)[^\n]*reference\s*range[^\d]*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', re.IGNORECASE
    )
    for match in inline_pattern.finditer(text):
        metric = clean_metric_name(match.group(1))
        low = float(match.group(2))
        high = float(match.group(3))
        ref_ranges[metric] = (low, high)

    return ref_ranges

# ========== DISPLAY AND ANALYSIS ==========

def display_metric_summary(metrics, ref_ranges=None):
    if not metrics:
        st.warning("⚠️ No recognizable health metrics found.")
        return
    rows = []
    for metric, value in metrics.items():
        # Try to match metric name using cleaned version
        metric_key = clean_metric_name(metric)
        ref = ref_ranges.get(metric_key, ("N/A", "N/A")) if ref_ranges else ("N/A", "N/A")
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

def predict_conditions(metrics, ref_ranges=None):
    st.subheader("🧠 AI-based Risk Assessment")
    # You can enhance this logic as needed
    if 'Hemoglobin' in metrics and ref_ranges:
        hb = metrics['Hemoglobin']
        ref = ref_ranges.get('hemoglobin', (13, 17))
        if hb < ref[0]:
            st.error(f"🔴 Anemia: Low hemoglobin ({hb})")
        elif hb > ref[1]:
            st.warning(f"🟡 High hemoglobin ({hb})")
    # Add more conditions as needed...

def download_metrics(metrics, ref_ranges=None):
    if metrics:
        rows = []
        for metric, value in metrics.items():
            metric_key = clean_metric_name(metric)
            ref = ref_ranges.get(metric_key, ("N/A", "N/A")) if ref_ranges else ("N/A", "N/A")
            rows.append({
                "Metric": metric,
                "Value": value,
                "Reference Range": f"{ref[0]} - {ref[1]}" if ref[0] != "N/A" else "N/A"
            })
        df = pd.DataFrame(rows)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Metrics (CSV)", 
            csv, 
            "medical_metrics.csv", 
            "text/csv"
        )
