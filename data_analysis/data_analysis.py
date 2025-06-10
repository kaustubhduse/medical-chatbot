import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO

# ------------------ METRIC EXTRACTION ------------------

def extract_health_metrics(text):
    metrics = {}
    metrics.update(extract_tabular_data(text))
    metrics.update(extract_from_unstructured_text(text))
    return normalize_percentages(metrics)

def extract_tabular_data(text):
    metrics = {}

    # LaTeX tables
    latex_tables = re.findall(r'\\begin{tabular}.*?\\end{tabular}', text, re.DOTALL)
    for table in latex_tables:
        rows = re.findall(r'\\hline\s*(.*?)\s*\\\\', table, re.DOTALL)
        for row in rows:
            cols = [c.strip() for c in re.split(r'(?<!\\)&', row)]
            if len(cols) >= 2:
                name = clean_metric_name(cols[0])
                val = parse_table_value(cols[1])
                if name and val is not None:
                    metrics[name] = val

    # Markdown-style tables
    markdown_rows = re.findall(r'^\|(.+?)\|$', text, re.MULTILINE)
    for row in markdown_rows:
        cols = [c.strip() for c in row.split('|')]
        if len(cols) >= 2:
            name = clean_metric_name(cols[0])
            val = parse_table_value(cols[1])
            if name and val is not None:
                metrics[name] = val

    return metrics

def extract_from_unstructured_text(text):
    metrics = {}
    patterns = {
        'Hemoglobin': r'(?:Hemoglobin|Hb|HGB)[^\d:]*[:\-]?\s*([\d.]+)\s*(?:g/dL|g\%|gm\%|g)?',
        'WBC': r'(?:White\s*Blood\s*Cell|WBC|TLC)[^\d:]*[:\-]?\s*([\d,]+)',
        'Platelets': r'(?:Platelets|Platelet\s*Count)[^\d:]*[:\-]?\s*([\d,]+)',
        'RBC': r'(?:RBC|Red\s*Blood\s*Cell)[^\d:]*[:\-]?\s*([\d.]+)',
        'Hematocrit': r'(?:Packed\s*Cell\s*Volume|PCV|Hematocrit)[^\d:]*[:\-]?\s*([\d.]+)',
        'Neutrophils': r'Neutrophils[^\d:]*[:\-]?\s*([\d.]+)',
        'Lymphocytes': r'Lymphocytes[^\d:]*[:\-]?\s*([\d.]+)',
        'Eosinophils': r'Eosinophils[^\d:]*[:\-]?\s*([\d.]+)',
        'Blood Pressure': r'(?:BP|Blood\s*Pressure)[^\d:]*[:\-]?\s*(\d+\s*/\s*\d+)',
    }

    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = parse_text_value(match.group(1), metric)
            if value is not None:
                metrics[metric] = value

    return metrics

def clean_metric_name(name):
    name = re.sub(r'\\(?:textbf|textit)\{([^}]*)\}', r'\1', name)
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    name_map = {
        'PCV': 'Hematocrit',
        'Hb': 'Hemoglobin',
        'TLC': 'WBC',
        'DLC': 'Differential Count'
    }
    return name_map.get(name, name)

def parse_table_value(value):
    try:
        clean_val = re.sub(r'[^\d./]', '', value.replace(',', ''))
        if '/' in clean_val:
            return clean_val.strip()
        return float(clean_val) if '.' in clean_val else int(clean_val)
    except:
        return None

def parse_text_value(value, metric):
    try:
        clean_val = re.sub(r'[^\d./]', '', value.replace(',', ''))
        if '/' in clean_val:
            return clean_val.strip()
        return float(clean_val)
    except:
        return None

def normalize_percentages(metrics):
    percent_metrics = ['Hematocrit', 'Neutrophils', 'Lymphocytes', 'Eosinophils']
    return {
        k: (v / 100 if k in percent_metrics and isinstance(v, (int, float)) else v)
        for k, v in metrics.items()
    }

# ------------------ ANALYSIS & DISPLAY ------------------

REFERENCE_RANGES = {
    'Hemoglobin': (13.0, 17.0),
    'WBC': (4000, 11000),
    'Platelets': (150000, 410000),
    'RBC': (4.5, 5.5),
    'Hematocrit': (0.40, 0.50),
    'Neutrophils': (0.50, 0.62),
    'Lymphocytes': (0.20, 0.40),
}

def display_metric_summary(metrics):
    if not metrics:
        st.warning("⚠️ No recognizable health metrics found.")
        return

    data = []
    for metric, val in metrics.items():
        ref = REFERENCE_RANGES.get(metric, (None, None))
        data.append({
            'Metric': metric,
            'Value': val,
            'Reference Low': ref[0],
            'Reference High': ref[1],
            'Status': get_status_indicator(val, ref)
        })

    df = pd.DataFrame(data)
    st.subheader("📊 Health Metrics Analysis")
    st.dataframe(df.style.apply(color_status, axis=1), use_container_width=True)
    plot_metric_comparison(df)

def get_status_indicator(val, ref):
    if None in ref:
        return '➖ Reference unknown'
    if isinstance(val, str):
        return '⚠️ Needs manual check'
    if val < ref[0]:
        return '🔴 Low'
    if val > ref[1]:
        return '🟡 High'
    return '🟢 Normal'

def color_status(row):
    colors = {
        '🔴 Low': '#ffcccc',
        '🟡 High': '#fff3cd',
        '🟢 Normal': '#d4edda'
    }
    return ['background-color: {}'.format(colors.get(row.Status, 'white'))] * len(row)

def plot_metric_comparison(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df_plot = df[df['Status'].isin(['🔴 Low', '🟡 High', '🟢 Normal'])]

    for _, row in df_plot.iterrows():
        val = row['Value']
        low = row['Reference Low']
        high = row['Reference High']
        ax.bar(row['Metric'], val, color=get_bar_color(row['Status']))
        if low is not None and high is not None:
            ax.hlines([low, high], -0.4, 0.4, color='gray', linestyle='--')
            ax.text(0, high * 1.02, 'Ref Range', ha='center', color='gray')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

def get_bar_color(status):
    return {
        '🔴 Low': '#dc3545',
        '🟡 High': '#ffc107',
        '🟢 Normal': '#28a745'
    }.get(status, '#007bff')

def predict_conditions(metrics):
    st.subheader("🧠 Clinical Risk Assessment")
    if 'Hemoglobin' in metrics:
        hb = metrics['Hemoglobin']
        if hb < 13:
            st.error(f"**Anemia Risk:** Low hemoglobin ({hb} g/dL)")
        elif hb > 17:
            st.warning(f"**Polycythemia Risk:** High hemoglobin ({hb} g/dL)")

    if 'Hematocrit' in metrics:
        hct = metrics['Hematocrit']
        if hct > 0.50:
            st.error(f"**Hemoconcentration:** High hematocrit ({hct * 100:.1f}%)")

    if 'WBC' in metrics:
        wbc = metrics['WBC']
        if wbc < 4000:
            st.warning(f"**Leukopenia:** Low WBC ({wbc})")
        elif wbc > 11000:
            st.warning(f"**Leukocytosis:** High WBC ({wbc})")

    if 'Platelets' in metrics:
        p = metrics['Platelets']
        if p < 150000:
            st.error(f"**Thrombocytopenia:** Low Platelets ({p})")
        elif p > 410000:
            st.warning(f"**Thrombocytosis:** High Platelets ({p})")

def download_metrics(metrics):
    if metrics:
        df = pd.DataFrame({'Metric': metrics.keys(), 'Value': metrics.values()})
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Metrics (CSV)", csv, "metrics.csv", "text/csv"
        )

# ------------------ STREAMLIT UI ------------------

st.set_page_config(page_title="Medical Report Analyzer", layout="wide")

st.title("🩺 Medical Report Analyzer")
st.write("Paste medical report content (text, PDF content, LaTeX, etc.):")

user_input = st.text_area("📄 Paste Report Content", height=300)

if st.button("🔍 Analyze"):
    if user_input.strip():
        metrics = extract_health_metrics(user_input)
        if st.checkbox("🧪 Show Extracted Metrics JSON"):
            st.json(metrics)
        display_metric_summary(metrics)
        predict_conditions(metrics)
        download_metrics(metrics)
    else:
        st.error("Please paste some text to analyze.")
