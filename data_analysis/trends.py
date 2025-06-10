# trends.py
import pandas as pd
import plotly.express as px
import streamlit as st

def plot_metric_trend(historical_df, metric, date_col='date'):
    """
    Plot the time series trend for a given metric.
    Args:
        historical_df: DataFrame with at least [date_col, metric]
        metric: str, the metric/column to plot
        date_col: str, the column representing time (default: 'date')
    """
    if metric not in historical_df.columns or date_col not in historical_df.columns:
        st.warning(f"Metric '{metric}' or date column '{date_col}' not found in data.")
        return

    df = historical_df[[date_col, metric]].dropna()
    df = df.sort_values(date_col)
    fig = px.line(df, x=date_col, y=metric, markers=True,
                  title=f"{metric} Trend Over Time",
                  labels={metric: metric, date_col: "Date"})
    st.plotly_chart(fig, use_container_width=True)

def plot_all_metric_trends(historical_df, metrics, date_col='date'):
    """
    Plot trends for multiple metrics.
    Args:
        historical_df: DataFrame with at least [date_col, metric1, metric2, ...]
        metrics: list of str, the metrics/columns to plot
        date_col: str, the column representing time (default: 'date')
    """
    for metric in metrics:
        plot_metric_trend(historical_df, metric, date_col)

def detect_anomalies(historical_df, metric, date_col='date', threshold=2.0):
    """
    Simple anomaly detection using z-score.
    Returns list of (date, value) where anomaly detected.
    """
    if metric not in historical_df.columns or date_col not in historical_df.columns:
        return []

    df = historical_df[[date_col, metric]].dropna()
    values = df[metric]
    mean, std = values.mean(), values.std()
    anomalies = df[(abs(values - mean) > threshold * std)]
    return list(anomalies[[date_col, metric]].itertuples(index=False, name=None))

def show_trend_analysis(historical_df, metrics, date_col='date'):
    """
    Streamlit dashboard for trends and anomaly alerts.
    """
    st.subheader("📈 Time Series Trend Analysis")
    for metric in metrics:
        plot_metric_trend(historical_df, metric, date_col)
        anomalies = detect_anomalies(historical_df, metric, date_col)
        if anomalies:
            st.warning(f"Anomalies detected in {metric}: {anomalies}")
