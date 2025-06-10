import streamlit as st
import pandas as pd
import json
import re

def parse_llm_summary(summary_text):
    """Extract structured data from LLM's JSON summary"""
    try:
        # Clean potential markdown code blocks
        clean_summary = re.sub(r'``````', '', summary_text)
        data = json.loads(clean_summary)
        return data
    except json.JSONDecodeError:
        st.error("Failed to parse LLM summary")
        return []

def display_metric_summary(metrics_data):
    """Display metrics from parsed JSON data"""
    if not metrics_data:
        st.warning("⚠️ No health metrics found in summary")
        return
    
    # Create DataFrame with consistent columns
    df = pd.DataFrame(metrics_data)
    
    # Ensure required columns exist
    for col in ['metric', 'value', 'reference_range', 'status']:
        if col not in df.columns:
            df[col] = 'N/A'
    
    st.subheader("📊 Health Metrics Analysis")
    st.dataframe(
        df[['metric', 'value', 'reference_range', 'status']],
        use_container_width=True
    )
    
    # Display interactive chart
    if 'value' in df:
        numeric_df = df[pd.to_numeric(df['value'], errors='coerce').notnull()]
        if not numeric_df.empty:
            st.bar_chart(numeric_df.set_index('metric')['value'])

def predict_conditions(metrics_data):
    """Generate insights from parsed JSON data"""
    st.subheader("🧠 AI Clinical Insights")
    
    # Simple validation check
    if not isinstance(metrics_data, list):
        st.error("Invalid data format")
        return
    
    # Create analysis from LLM's status indications
    for item in metrics_data:
        if item.get('status', '').lower() == 'low':
            st.warning(f"🟡 Low {item['metric']}: {item['value']} (Ref: {item.get('reference_range', 'N/A')})")
        elif item.get('status', '').lower() == 'high':
            st.error(f"🔴 High {item['metric']}: {item['value']} (Ref: {item.get('reference_range', 'N/A')})")

def download_metrics(metrics_data):
    """Create downloadable report from JSON data"""
    if metrics_data:
        df = pd.DataFrame(metrics_data)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Full Report", 
            csv, 
            "medical_analysis.csv", 
            "text/csv",
            help="Contains all extracted metrics and reference ranges"
        )
