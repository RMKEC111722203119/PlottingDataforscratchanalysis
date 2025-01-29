import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

# Define professional color palette
PRO_COLOR_PALETTE = {
    "Healthy": "#4CAF50",   # Green
    "1H": "#2196F3",        # Blue
    "2H": "#FF9800",        # Orange
    "3H": "#9C27B0",        # Purple
    "4H": "#795548",        # Brown
    "1 Scratch": "#E91E63", # Pink
    "2 Scratch": "#607D8B", # Grey
    "3 Scratch": "#FF5722", # Red
    "4 Scratch": "#009688"  # Teal
}

# Load data with Streamlit's new caching mechanism
@st.cache_data
def load_data(file):
    if file.name.lower().endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

st.set_page_config(
    page_title="Professional Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader("Upload your Excel/CSV file", type=["xlsx", "xls", "csv"])

st.title("Data Visualization Dashboard")
st.markdown(
    "<h3 style='text-align: center; color: #333;'>Upload your data and explore visualizations</h3>",
    unsafe_allow_html=True
)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        df = df.dropna()  # Basic data cleaning

        # Move color configuration to a dedicated sidebar section
        st.sidebar.header("Color Customization")
        color_mapping = {}
        for status in df["Status"].unique():
            color = st.sidebar.color_picker(f"Color for {status}", PRO_COLOR_PALETTE.get(status, "#1f77b4"))
            color_mapping[status] = color

        # Main sidebar configuration
        st.sidebar.header("Visualization Configuration")
        selected_status = st.sidebar.multiselect(
            "Select Statuses:",
            options=df["Status"].unique(),
            default=list(df["Status"].unique()),
            key="status_selector"
        )

        # Allow users to change X and Y axes
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        x_axis_column = st.sidebar.selectbox("Select X-axis Column", numeric_cols, key="x_axis")
        y_axis_column = st.sidebar.selectbox("Select Y-axis Column", numeric_cols, key="y_axis")

        # Filter data based on selected statuses
        filtered_df = df[df["Status"].isin(selected_status)]

        # Visualization type selection
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["2D Scatter", "3D Scatter", "Bar Chart"],
            key="chart_type"
        )

        # Plotting
        if not filtered_df.empty:
            if chart_type == "2D Scatter":
                fig, ax = plt.subplots(figsize=(10, 6))
                for status in selected_status:
                    subset = filtered_df[filtered_df["Status"] == status]
                    ax.scatter(
                        subset[x_axis_column],
                        subset[y_axis_column],
                        label=status,
                        color=color_mapping[status],
                        alpha=0.7,
                        edgecolor='white',
                        linewidth=0.5
                    )
                ax.set_title("Custom Scatter Plot", fontsize=16, weight='bold')
                ax.set_xlabel(x_axis_column, fontsize=12, color='#444')
                ax.set_ylabel(y_axis_column, fontsize=12, color='#444')
                ax.tick_params(axis='both', colors='#666')
                ax.legend(title="Status", loc='upper left', frameon=False)
                plt.grid(color='#eee', linestyle='--', linewidth=0.5)
                st.pyplot(fig)

            elif chart_type == "3D Scatter":
                fig = px.scatter_3d(
                    filtered_df,
                    x=x_axis_column,
                    y=y_axis_column,
                    z="RPM",
                    color="Status",
                    color_discrete_map=color_mapping,
                    title="3D Performance Visualization",
                    labels={"RPM": "Revolutions per Minute"}
                )
                fig.update_layout(
                    scene=dict(
                        xaxis=dict(backgroundcolor="#f0f0f0"),
                        yaxis=dict(backgroundcolor="#f0f0f0"),
                        zaxis=dict(backgroundcolor="#f0f0f0"),
                    ),
                    title_font=dict(size=16, color='#333'),
                    legend_font=dict(color='#444'),
                    paper_bgcolor='#f9f9f9',
                    plot_bgcolor='#f9f9f9'
                )
                st.plotly_chart(fig)

            elif chart_type == "Bar Chart":
                fig = px.bar(
                    filtered_df.groupby("Status", as_index=False).mean(),
                    x="Status",
                    y=[x_axis_column, y_axis_column, "RPM"],
                    color="Status",
                    color_discrete_map=color_mapping,
                    title="Average Metrics by Status",
                    labels={"value": "Average Value"},
                    width=1000,
                    height=600
                )
                fig.update_traces(
                    opacity=0.8,
                    hovertemplate="<b>Status: %{x}</b><br><br>" +
                                f"{x_axis_column}: %{y:.2f}<br>" +
                                f"{y_axis_column}: %{y:.2f}<br>" +
                                "RPM: %{y:.2f}",
                )
                fig.update_layout(
                    title_font=dict(size=16, color='#333'),
                    xaxis_title_font=dict(color='#444'),
                    yaxis_title_font=dict(color='#444'),
                    legend_font=dict(color='#444'),
                    paper_bgcolor='#f9f9f9',
                    plot_bgcolor='#f9f9f9',
                    xaxis_gridcolor='#eee',
                    yaxis_gridcolor='#eee'
                )
                st.plotly_chart(fig)

        else:
            st.warning("No data available for the selected statuses")

        # Show raw data
        if st.checkbox("Show Raw Data", key="data_toggle"):
            st.subheader("Raw Data")
            st.write(filtered_df.style.set_properties(**{
                'background-color': '#f9f9f9',
                'color': '#333'
            }))
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed")
