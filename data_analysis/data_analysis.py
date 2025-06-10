import streamlit as st
import pandas as pd
import json
import re

def parse_llm_summary(summary_text):
    """Robust JSON extraction from LLM output"""
    try:
        # Remove markdown code blocks
        clean_summary = re.sub(r'``````', '', summary_text)
        
        # Extract JSON array using regex
        json_match = re.search(r'\[.*\]', clean_summary, re.DOTALL)
        if not json_match:
            return []
            
        json_str = json_match.group(0)
        
        # Fix common JSON issues
        json_str = json_str.replace("'", '"')  # Replace single quotes
        json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas
        
        data = json.loads(json_str)
        
        # Add missing fields and clean data
        required_fields = ['metric', 'value', 'reference_range', 'unit', 'status']
        for item in data:
            for field in required_fields:
                if field not in item:
                    item[field] = 'N/A'
            item['metric'] = item['metric'].strip().title()
            
        return data
        
    except Exception as e:
        st.error(f"Parsing error: {str(e)}")
        return []

def display_metric_summary(metrics_data):
    """Display metrics with interactive components"""
    if not metrics_data:
        st.warning("⚠️ No health metrics found")
        return
    
    df = pd.DataFrame(metrics_data)
    
    # Convert numeric values
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Create styled dataframe
    st.subheader("📊 Health Metrics Analysis")
    st.dataframe(
        df[['metric', 'value', 'unit', 'reference_range', 'status']],
        use_container_width=True,
        hide_index=True
    )
    
    # Visualize numeric metrics
    if not df.empty and 'value' in df:
        st.bar_chart(df.set_index('metric')['value'])

def predict_conditions(metrics_data):
    """Generate clinical insights"""
    st.subheader("🧠 Clinical Risk Assessment")
    
    if not isinstance(metrics_data, list):
        st.error("Invalid data format")
        return
    
    for test in metrics_data:
        metric = test.get('metric', 'Unknown')
        value = test.get('value', '')
        ref_range = test.get('reference_range', 'N/A')
        status = test.get('status', '').lower()
        
        if status == 'low':
            st.warning(f"🟡 Low {metric}: {value} (Ref: {ref_range})")
        elif status == 'high':
            st.error(f"🔴 High {metric}: {value} (Ref: {ref_range})")

def download_metrics(metrics_data):
    """Generate downloadable CSV report"""
    if metrics_data:
        df = pd.DataFrame(metrics_data)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Full Report",
            csv,
            "medical_analysis.csv",
            "text/csv",
            help="Contains complete analysis of all medical metrics"
        )
