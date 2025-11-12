import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="lte_db",
        user="lte_user",
        password="Ch@it@ny@gammaedge123"
    )

# --- Load data ---
@st.cache_data(ttl=300)
def load_data():
    conn = get_connection()
    query = "SELECT * FROM lte_spike_detection;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="LTE Spike Dashboard", layout="wide")
st.title("LTE Spike Detection Dashboard")

df = load_data()

# --- Filters ---
col1, col2 = st.columns(2)
with col1:
    cell_filter = st.multiselect("Select Cell", df["cell_name"].unique())
with col2:
    severity_filter = st.multiselect("Select Severity", df["severity_level"].dropna().unique())

filtered_df = df.copy()
if cell_filter:
    filtered_df = filtered_df[filtered_df["cell_name"].isin(cell_filter)]
if severity_filter:
    filtered_df = filtered_df[filtered_df["severity_level"].isin(severity_filter)]

st.markdown(f"Showing {len(filtered_df)} records")

# --- Charts ---
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        filtered_df.groupby("severity_level").size().reset_index(name="count"),
        x="severity_level", y="count", color="severity_level",
        title="Spike Severity Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(
        filtered_df,
        x="time",
        y="metric_value",
        color="cell_name",
        title="Traffic / Metric Value over Time"
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Table view ---
st.markdown("Detailed Records")
st.dataframe(filtered_df.sort_values(by="time", ascending=False).head(1000))
