import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO

# ------------------ METRIC EXTRACTION ------------------
def extract_health_metrics(text):
    """Extract metrics from both tabular and unstructured text"""
    metrics = {}
    
    # 1. Priority: Extract from structured tables
    table_metrics = extract_tabular_data(text)
    metrics.update(table_metrics)
    
    # 2. Fallback: Extract from unstructured text
    text_metrics = extract_from_unstructured_text(text)
    metrics.update(text_metrics)
    
    # Convert percentage values to floats
    return normalize_percentages(metrics)

def extract_tabular_data(text):
    """Handle LaTeX and markdown-style tables"""
    metrics = {}
    
    # Improved table detection with escaped characters
    table_pattern = r'\\begin{tabular}.*?\\end{tabular}'
    tables = re.findall(table_pattern, text, re.DOTALL)
    
    for table in tables:
        # Extract rows between horizontal lines
        rows = re.findall(r'\\hline\s*(.*?)\s*\\\\', table, re.DOTALL)
        for row in rows:
            # Split columns considering escaped ampersands
            cols = re.split(r'(?<!\\)&', row)
            cols = [c.strip() for c in cols]
            
            if len(cols) >= 2:
                metric_name = clean_metric_name(cols[0])
                metric_value = parse_table_value(cols[1])
                
                if metric_name and metric_value is not None:
                    metrics[metric_name] = metric_value
    return metrics

def clean_metric_name(name):
    """Standardize metric names across formats"""
    # Remove LaTeX formatting
    name = re.sub(r'\\(?:textbf|textit)\{([^}]*)\}', r'\1', name)
    # Remove special characters and parentheticals
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Standardization map
    name_map = {
        'PCV': 'Hematocrit',
        'Hb': 'Hemoglobin',
        'TLC': 'WBC',
        'DLC': 'Differential Count'
    }
    return name_map.get(name, name)

def parse_table_value(value):
    """Parse values from table cells with units"""
    try:
        # Remove units and special characters
        clean_val = re.sub(r'[^0-9./]', '', value)
        
        # Handle different value types
        if '/' in clean_val:  # Blood pressure
            return clean_val
        if '%' in value:
            return float(clean_val) / 100 if clean_val else None
        if '.' in clean_val:
            return float(clean_val)
        return int(clean_val)
    except:
        return None

def extract_from_unstructured_text(text):
    """Extract metrics from free text"""
    metrics = {}
    
    patterns = {
        'Hemoglobin': r'(?:Hemoglobin|Hb)[^:\n]*[:&]?\s*([\d.]+)\s*(?:g/dL|g\%|gm\%|g)',
        'WBC': r'(?:White\s*Blood\s*Cell|WBC|TLC)[^:\n]*[:&]?\s*([\d,]+)\s*(?:cells?/c?mm3|cmm|/mm3)?',
        'Platelets': r'Platelet[^:\n]*[:&]?\s*([\d,]+)\s*(?:cells?/c?mm3|cmm|/mm3)?',
        'RBC': r'(?:RBC|Red\s*Blood\s*Cell)[^:\n]*[:&]?\s*([\d.]+)\s*(?:mill?/c?mm3)?',
        'Hematocrit': r'(?:Packed\s*Cell\s*Volume|PCV|Hematocrit)[^:\n]*[:&]?\s*([\d.]+)\s*\%?',
        'Neutrophils': r'Neutrophils[^:\n]*[:&]?\s*([\d.]+)\s*\%?',
        'Lymphocytes': r'Lymphocytes[^:\n]*[:&]?\s*([\d.]+)\s*\%?',
        'Eosinophils': r'Eosinophils[^:\n]*[:&]?\s*([\d.]+)\s*\%?',
        'Blood Pressure': r'(?:BP|Blood\s*Pressure)[^:\n]*[:&]?\s*(\d+\s*/\s*\d+)'
    }

    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = parse_text_value(match.group(1), metric)
            if value is not None:
                metrics[metric] = value
    return metrics

def parse_text_value(value, metric):
    """Parse values from unstructured text"""
    try:
        clean_val = re.sub(r'[^0-9./]', '', value)
        if 'Blood Pressure' in metric:
            return clean_val
        if '%' in value or metric in ['Neutrophils', 'Lymphocytes', 'Eosinophils']:
            return float(clean_val)
        return float(clean_val) if '.' in clean_val else int(clean_val)
    except:
        return None

def normalize_percentages(metrics):
    """Convert percentage values to decimal floats"""
    percent_metrics = ['Hematocrit', 'Neutrophils', 'Lymphocytes', 'Eosinophils']
    return {
        k: (v/100 if k in percent_metrics and isinstance(v, (int, float)) else v)
        for k, v in metrics.items()
    }

# ------------------ VISUALIZATION & ANALYSIS ------------------
REFERENCE_RANGES = {
    'Hemoglobin': (13.0, 17.0),    # g/dL
    'WBC': (4000, 11000),          # cells/mm3
    'Platelets': (150000, 410000), # cells/mm3
    'RBC': (4.5, 5.5),             # million/mm3
    'Hematocrit': (0.40, 0.50),    # fraction
    'Neutrophils': (0.50, 0.62),   # fraction
    'Lymphocytes': (0.20, 0.40)    # fraction
}

def display_metric_summary(metrics):
    """Display metrics with reference ranges"""
    if not metrics:
        st.warning("⚠️ No recognizable health metrics found.")
        return

    # Create analysis dataframe
    analysis_data = []
    for metric, value in metrics.items():
        ref_range = REFERENCE_RANGES.get(metric, (None, None))
        analysis_data.append({
            'Metric': metric,
            'Value': value,
            'Reference Low': ref_range[0],
            'Reference High': ref_range[1],
            'Status': get_status_indicator(value, ref_range)
        })
    
    df = pd.DataFrame(analysis_data)
    
    # Display formatted table
    st.subheader("📊 Health Metrics Analysis")
    st.dataframe(
        df.style.apply(color_status, axis=1),
        use_container_width=True
    )
    
    # Display interactive chart
    plot_metric_comparison(df)

def get_status_indicator(value, ref_range):
    """Determine status indicator for metrics"""
    if None in ref_range:
        return '➖ Reference unknown'
    if isinstance(value, str):  # Handle blood pressure
        return '⚠️ Needs manual check'
    if value < ref_range[0]:
        return '🔴 Low'
    if value > ref_range[1]:
        return '🟡 High'
    return '🟢 Normal'

def color_status(row):
    """Color coding for dataframe"""
    colors = {
        '🔴 Low': '#ffcccc',
        '🟡 High': '#fff3cd',
        '🟢 Normal': '#d4edda'
    }
    return ['background-color: {}'.format(colors.get(row.Status, 'white'))]*len(row)

def plot_metric_comparison(df):
    """Create annotated bar chart"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filter plottable metrics
    plot_df = df[df['Status'].isin(['🔴 Low', '🟡 High', '🟢 Normal'])]
    
    # Create bars with reference lines
    for _, row in plot_df.iterrows():
        value = row['Value']
        ref_low = row['Reference Low']
        ref_high = row['Reference High']
        
        # Plot value
        bar = ax.bar(row['Metric'], value, color=get_bar_color(row['Status']))
        
        # Add reference range
        ax.hlines(ref_low, -0.4, 0.4, color='gray', linestyle='--')
        ax.hlines(ref_high, -0.4, 0.4, color='gray', linestyle='--')
        ax.text(0, ref_high*1.02, 'Ref Range', ha='center', color='gray')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

def get_bar_color(status):
    """Get color based on status"""
    return {
        '🔴 Low': '#dc3545',
        '🟡 High': '#ffc107',
        '🟢 Normal': '#28a745'
    }.get(status, '#007bff')

def predict_conditions(metrics):
    """Generate AI-based health predictions"""
    st.subheader("🧠 Clinical Risk Assessment")
    
    # Hematological analysis
    if 'Hemoglobin' in metrics:
        hb = metrics['Hemoglobin']
        if hb < 13:
            st.error(f"**Anemia Risk:** Low hemoglobin ({hb} g/dL) - Recommend iron studies and nutritional assessment")
        elif hb > 17:
            st.warning(f"**Polycythemia:** Elevated hemoglobin ({hb} g/dL) - Check for dehydration or hematological disorders")

    if 'Hematocrit' in metrics:
        hct = metrics['Hematocrit']
        if hct > 0.50:
            st.error(f"**Hemoconcentration:** High hematocrit ({hct*100:.1f}%) - Evaluate for dehydration or polycythemia vera")
    
    # Inflammatory markers
    if 'WBC' in metrics:
        wbc = metrics['WBC']
        if wbc > 11000:
            st.warning(f"**Leukocytosis:** Elevated WBC ({wbc}) - Possible infection or inflammation")
        elif wbc < 4000:
            st.warning(f"**Leukopenia:** Low WBC ({wbc}) - Consider viral infections or bone marrow disorders")

    # Platelet analysis
    if 'Platelets' in metrics:
        plt = metrics['Platelets']
        if plt < 150000:
            st.error(f"**Thrombocytopenia:** Low platelets ({plt}) - Increased bleeding risk")
        elif plt > 410000:
            st.warning(f"**Thrombocytosis:** High platelets ({plt}) - Possible reactive process or myeloproliferative disorder")

def download_metrics(metrics):
    """Enable CSV download of extracted metrics"""
    if metrics:
        df = pd.DataFrame({
            'Metric': metrics.keys(),
            'Value': metrics.values()
        })
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Metrics (CSV)", 
            csv, 
            "medical_metrics.csv", 
            "text/csv",
            help="Download extracted metrics in CSV format"
        )
