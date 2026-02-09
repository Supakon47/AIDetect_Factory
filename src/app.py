import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="PPE Compliance Dashboard", layout="wide")

log_path = os.path.join("logs", "events.csv")

st.title("PPE Compliance Dashboard")

if not os.path.exists(log_path):
    st.warning("No log file found yet. Run `python src/main.py` first to generate logs.")
    st.stop()

df = pd.read_csv(log_path)

st.subheader("Latest Events")
st.dataframe(df.tail(50), use_container_width=True)

st.subheader("Today Summary")
df["date"] = df["timestamp"].str.slice(0, 10)
today = df["date"].max()
df_today = df[df["date"] == today].copy()

pass_rate = (df_today["compliant"] == True).mean() if len(df_today) > 0 else 0.0
fail_count = (df_today["compliant"] == False).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Date", today)
col2.metric("Pass Rate", f"{pass_rate*100:.1f}%")
col3.metric("Fail Count", int(fail_count))

st.subheader("Most Missing Items (Today)")
# Count missing items
missing_series = df_today[df_today["missing"] != "-"]["missing"].str.split(",").explode()
missing_counts = missing_series.value_counts()
st.bar_chart(missing_counts)