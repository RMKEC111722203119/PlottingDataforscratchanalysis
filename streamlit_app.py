import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import plotly.figure_factory as ff

# Load custom CSS
st.markdown(
    """
<style>
body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
.reportview-container .main .block-container {
    max-width: 1200px;
    padding: 2rem;
}
.sidebar .sidebar-content {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.st-bd {
    background-color: #ffffff;
    border-radius: 10px;
}
header {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

# Application title with gradient header
st.title("Advanced Data Diagnosis Center")
st.markdown(
    '<h2 style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);'
    '-webkit-background-clip: text;'
    '-webkit-text-fill-color: transparent;'
    'font-weight: bold;'
    'margin-bottom: 2rem;">Health Intelligence Dashboard</h2>',
    unsafe_allow_html=True,
)

# Sidebar configuration
st.sidebar.header("Health Analysis Engine")
file_options = st.sidebar.radio(
    "Data Ingestion Path",
    ["Sample Heart Rate Dataset", "Upload Custom File"]
)

# Load dataset based on selection
if file_options == "Sample Heart Rate Dataset":
    df = pd.read_csv("https://raw.githubusercontent.com/johnsnow00/healthdata/master/sample.csv")
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel/CSV", type=["xlsx", "xls", "csv"]
    )
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except:
            df = pd.read_excel(uploaded_file)

# Basic data cleaning
df = df.dropna()

# Feature extraction
df['Status'] = df['Status'].str.strip()
status = st.sidebar.multiselect(
    "Filter by Health Status",
    df['Status'].unique(),
    default=list(df['Status'].unique())
)

if not status:
    st.warning("Please select at least one status.")
    st.stop()

filtered_df = df[df['Status'].isin(status)]

# Advanced analytics section
st.header("Health Pulse Metrics")
cols = st.columns(4)
with cols[0]:
    st.metric("Average RPM", round(filtered_df['RPM'].mean(), 2))
with cols[1]:
    st.metric("Max 30.9 Reading", filtered_df['30.9'].max())
with cols[2]:
    st.metric("Min 89.6 Reading", filtered_df['89.6'].min())
with cols[3]:
    st.metric("Status Distribution", len(filtered_df) / len(df))

# Gradient background plots
st.header("Advanced Diagnostics Visualization Suite")

# 1. Interactive 3D Heart Pulse Waveform
fig = px.scatter_3d(
    filtered_df,
    x='30.9',
    y='89.6',
    z='RPM',
    color='Status',
    size=np.abs(filtered_df['30.9'] - filtered_df['89.6']),
    hover_name='Status',
    title="3D Cardiac Pulse Waveform Analysis"
)
fig.update_layout(
    scene=dict(
        xaxis=dict(title='30.9 Pulse (μV)'),
        yaxis=dict(title='89.6 Pulse (μV)'),
        zaxis=dict(title='RPM'),
        bgcolor="rgba(240, 240, 240, 0.5)"
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial"),
)

st.plotly_chart(fig, use_container_width=True)

# 2. Density Heatmap with Gradient Pitch
x = filtered_df['30.9']
y = filtered_df['89.6']
counts, xedges, yedges = np.histogram2d(x, y, bins=20)
xmid = (xedges[:-1] + xedges[1:]) / 2
ymid = (yedges[:-1] + yedges[1:]) / 2
X, Y = np.meshgrid(xmid, ymid)
Z = np.log1p(counts.T)
fig = px.imshow(
    Z,
    labels=dict(color="Log Density"),
    x=xmid,
    y=ymid,
    origin="lower",
    title="Heat Density Mapping (Gradient Pitch Analysis)"
)
fig.update_layout(
    coloraxis=dict(
        colorscale=[
            [0, "rgba(38, 50, 56, 0.3)"],
            [0.5, "rgba(255, 82, 82, 0.7)"],
            [1, "rgba(255, 235, 59, 0.9)"],
        ]
    )
)
st.plotly_chart(fig, use_container_width=True)

# 3. Dynamic Interactive Pulse Chart
fig = px.area(
    filtered_df,
    x='RPM',
    y='30.9',
    color='Status',
    title="Pulse Profiling with RPM Modulation"
)
fig.update_layout(
    xaxis_title="Rotational Pulse Modulation (RPM)",
    yaxis_title="Electrocardiogram Amplitude (30.9 μV)",
    legend_title="Health Status",
    paper_bgcolor='rgba(240, 240, 240, 0.5)'
)
fig.update_traces(hovertemplate="RPM: %{x}<br>30.9 μV: %{y}")
st.plotly_chart(fig, use_container_width=True)

# 4. Gaussian Distribution Overlay
fig = go.Figure()
for status_name in status:
    subset = filtered_df[filtered_df['Status'] == status_name]
    kde = gaussian_kde(subset['30.9'])
    x = np.linspace(subset['30.9'].min(), subset['30.9'].max(), 500)
    y = kde(x)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=status_name,
            fill='tozeroy',
            fillcolor=f'rgba({np.random.randint(0,255)}, {np.random.randint(100,255)}, {np.random.randint(0,255)}, 0.3)'
        )
    )
fig.update_layout(
    title="Gaussian Mixture Model (GMM) Analysis",
    xaxis_title="30.9 μV Amplitude",
    yaxis_title="Probability Density",
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)

# 5. Status Correlation Matrix
corr = filtered_df.corr()
fig = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Pearson Coefficient")
    )
)
fig.update_layout(
    title="Health Parameter Correlation Matrix",
    template="seaborn"
)
st.plotly_chart(fig, use_container_width=True)

# 6. Time Series Micro-Current Analysis (Simulated Time)
filtered_df['timestamp'] = pd.date_range('2024-01-01', periods=len(filtered_df), freq='s')
fig = px.line(
    filtered_df,
    x='timestamp',
    y=['30.9', '89.6'],
    title="Real-Time Micro-Current Waveform"
)
fig.update_traces(
    mode='lines+markers',
    marker=dict(size=4, opacity=0.6),
    line=dict(width=1.5)
)
fig.update_layout(
    xaxis_title="Biometric Timestamp",
    yaxis_title="Current (μV)",
    legend_title="Electrode Contact",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Advanced data summary panel
st.header("Health Data Audit Log")
st.dataframe(
    filtered_df.drop(['timestamp'], axis=1, errors='ignore').describe().style
    .background_gradient(cmap='RdYlBu')
    .set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#007bff'), ('color', 'white')]
    }])
)

st.sidebar.markdown(
    '<h3 style="text-align: center; color: #0056b3;">'
    'HealthTech R&D - LifeGuard Systems ©2024</h3>',
    unsafe_allow_html=True
)
