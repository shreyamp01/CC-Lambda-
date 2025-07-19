import streamlit as st
from charts import show_function_metrics
from api_client import list_functions

st.title("CCLambda Monitoring Dashboard")
st.sidebar.selectbox("View", ["Functions", "Metrics"])

page = st.sidebar.radio("Navigate", ["Deploy", "Execute", "Metrics"])
if page == "Metrics":
    show_function_metrics()
