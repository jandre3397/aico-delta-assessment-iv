import streamlit as st
import requests

st.title("Internal ML Platform Dashboard")

services = {
    "Fraud Detection": "http://localhost:8001/health",
    "Recommendations": "http://localhost:8002/health",
    "Forecasting": "http://localhost:8003/health",
}

for name, url in services.items():
    st.subheader(name)
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            st.success("Healthy")
            st.json(r.json())
        else:
            st.error(f"Error: {r.status_code}")
    except Exception as e:
        st.warning(f"Currently unreachable: {e}")