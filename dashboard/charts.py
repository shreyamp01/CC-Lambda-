import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

def show_function_metrics():
    response = requests.get("http://localhost:8000/metrics")
    metrics = response.json()
    df = pd.DataFrame(metrics)

    st.subheader("Function Execution Time")
    st.line_chart(df.set_index("function_name")["execution_time"])

    st.subheader("Error Rate")
    st.bar_chart(df.set_index("function_name")["error_count"])
