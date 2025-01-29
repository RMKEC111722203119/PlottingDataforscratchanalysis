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

st.sidebar.header("Visualization Configuration")

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

        # Default axis columns
        default_x = "30.9" if "30.9" in df.columns else df.select_dtypes(include=['float64', 'int64']).columns[0]
        default_y = "89.6" if "89.6" in df.columns else df.select_dtypes(include=['float64', 'int64']).columns[0]

        # Move color configuration to a dedicated sidebar section
        st.sidebar.header("Color Customization")
        color_mapping = {}
        for status in df["Status"].unique():
            color = st.sidebar.color_picker(f"Color for {status}", PRO_COLOR_PALETTE.get(status, "#1f77b4"))
            color_mapping[status] = color

        # Main area configuration
        st.subheader("Select Statuses:")
        status_options = df["Status"].unique()
        selected_status = []
        for status in status_options:
            checkbox = st.checkbox(status, value=True, key=status)
            if checkbox:
                selected_status.append(status)

        # Filter data based on selected statuses
        filtered_df = df[df["Status"].isin(selected_status)]

        # Allow users to change X, Y, and Z axes
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        x_axis_column = st.sidebar.selectbox("Select X-axis Column", numeric_cols, index=numeric_cols.get_loc(default_x))
        y_axis_column = st.sidebar.selectbox("Select Y-axis Column", numeric_cols, index=numeric_cols.get_loc(default_y))
        z_axis_column = st.sidebar.selectbox("Select Z-axis Column (3D Only)", numeric_cols, index=numeric_cols.get_loc("RPM") if "RPM" in numeric_cols else 0)

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
                ax.set_xlim(-70, -20)  # Fixed X-axis range
                ax.set_ylim(-70, -20)  # Fixed Y-axis range
                ax.tick_params(axis='both', colors='#666')
                ax.legend(title="Status", loc='upper left', frameon=False)
                plt.grid(color='#eee', linestyle='--', linewidth=0.5)
                st.pyplot(fig)

            elif chart_type == "3D Scatter":
                fig = px.scatter_3d(
                    filtered_df,
                    x=x_axis_column,
                    y=y_axis_column,
                    z=z_axis_column,
                    color="Status",
                    color_discrete_map=color_mapping,
                    title="3D Performance Visualization",
                    labels={z_axis_column: "Revolutions per Minute"},
                    range_x=[-70, -20],  # Fixed X-axis range
                    range_y=[-70, -20],  # Fixed Y-axis range
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
                    y=[x_axis_column, y_axis_column, z_axis_column],
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
                                f"{z_axis_column}: %{y:.2f}",
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
