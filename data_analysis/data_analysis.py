import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from io import BytesIO

def extract_health_metrics(text):
    metrics = {}
    
    # First try to extract tabular data
    table_metrics = extract_tabular_data(text)
    metrics.update(table_metrics)
    
    # Then scan remaining text with enhanced regex
    text_metrics = extract_from_unstructured_text(text)
    metrics.update(text_metrics)
    
    return metrics

def extract_tabular_data(text):
    metrics = {}
    # Generic table pattern detection
    table_pattern = r'\\begin{tabular}.*?\\end{tabular}'
    tables = re.findall(table_pattern, text, re.DOTALL)
    
    for table in tables:
        # Extract all rows with data separators
        rows = re.findall(r'\\hline\s*(.*?)\s*\\\\', table, re.DOTALL)
        for row in rows:
            # Split columns by any common separator (&,|, etc)
            cols = re.split(r'[&|]', row)
            if len(cols) >= 2:
                metric_name = clean_metric_name(cols[0])
                metric_value = parse_value(cols[1])
                if metric_name and metric_value is not None:
                    metrics[metric_name] = metric_value
    return metrics

def clean_metric_name(name):
    # Standardize metric names across formats
    name = re.sub(r'\(.*?\)', '', name)  # Remove parentheses content
    name = re.sub(r'\b(Calculated|Count|Total)\b', '', name).strip()
    name = re.sub(r'\s+', ' ', name)
    return name

def parse_value(value):
    try:
        # Handle different number formats
        value = value.replace(',', '').replace(' ', '')
        if '/' in value:  # Blood pressure case
            return value
        return float(value) if '.' in value else int(value)
    except:
        return None

def extract_from_unstructured_text(text):
    metrics = {}
    # Enhanced regex patterns with multiple separators
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
                break  # Take first valid match
    
    return metrics

def generate_analysis(metrics):
    analysis = []
    ref_ranges = {
        'Hemoglobin': (13, 17),
        'WBC': (4000, 11000),
        'Platelets': (150000, 410000),
        'RBC': (4.5, 5.5)
    }

    for metric, value in metrics.items():
        if metric in ref_ranges:
            low, high = ref_ranges[metric]
            if value < low:
                analysis.append(f"Low {metric}: Possible deficiency")
            elif value > high:
                analysis.append(f"High {metric}: Potential condition")
    
    return analysis

def create_annotated_chart(metrics, analysis):
    fig, ax = plt.subplots(figsize=(10,6))
    items = [(k,v) for k,v in metrics.items() if isinstance(v, (int, float))]
    labels, values = zip(*items)
    
    ax.bar(labels, values, color='skyblue')
    ax.set_title('Medical Metrics Analysis')
    ax.set_ylabel('Value')
    plt.xticks(rotation=45, ha='right')
    
    # Add analysis annotations
    note = "Clinical Notes:\n" + "\n".join(analysis)
    plt.figtext(0.5, -0.25, note, 
                ha='center', fontsize=10, 
                bbox=dict(facecolor='lightyellow', alpha=0.5))
    
    return fig

def main():
    st.title("Medical Report Analyzer")
    
    uploaded_file = st.file_uploader("Upload medical report", type=["txt", "pdf"])
    if uploaded_file:
        text = uploaded_file.getvalue().decode()
        metrics = extract_health_metrics(text)
        
        if metrics:
            st.subheader("Extracted Metrics")
            st.write(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))
            
            analysis = generate_analysis(metrics)
            if analysis:
                st.subheader("Clinical Insights")
                st.write("\n".join(f"- {item}" for item in analysis))
            
            # Generate downloadable chart
            fig = create_annotated_chart(metrics, analysis)
            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            st.download_button(
                "Download Analysis Chart",
                buf.getvalue(),
                "medical_analysis.png",
                "image/png"
            )
        else:
            st.warning("No medical metrics found in document")

if __name__ == "__main__":
    main()
