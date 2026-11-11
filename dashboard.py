
import streamlit as st
import subprocess
import platform
import re
import time 

st.set_page_config(page_title="Network Security Dashboard", layout="wide")


st.title("🔐 Network Security Dashboard")
st.write("Monitor network devices and check their response times.")

devices = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]

def check_device(ip):
    system = platform.system().lower()
    option = "-n" if system == "windows" else "-c"

    try:
        result = subprocess.run(
            ["ping", option, "1", ip],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            match = re.search(r"time[=<]\s*(\d+)", result.stdout, re.IGNORECASE)
            response = int(match.group(1)) if match else None
            return "Online", response

        return "Offline", None

    except (subprocess.TimeoutExpired, OSError):
        return "Error", None

@st.fragment(run_every="30s")
def monitor_dashboard():
    results = []

    for ip in devices:
        status, response = check_device(ip)

        results.append({
            "IP Address": ip,
            "Status": status,
            "Response Time (ms)": response
        })

    st.subheader("Network Monitoring Results")
    st.dataframe(results, use_container_width=True)

    online = sum(1 for r in results if r["Status"] == "Online")
    offline = len(results) - online

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Devices", len(devices))
    col2.metric("Online", online)
    col3.metric("Offline / Error", offline)

monitor_dashboard()
