import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

st.set_page_config(
    page_title="Professional Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Load data (replace with your file loading method)
@st.cache
def load_data(file):
    if file.name.lower().endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

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

        # Default chart boundaries
        fixed_x_range = (-70, -20)
        fixed_y_range = (-70, -20)
        fixed_z_range = (1700, 1800)

        # Status selection
        status_options = df["Status"].unique()
        selected_statuses = st.sidebar.multiselect(
            "Select Statuses to Include:",
            options=status_options,
            default=list(status_options),
            format_func=lambda x: x.replace(" ", " - ").title(),
            key="status_selector"
        )

        # Filter data based on selected statuses
        filtered_df = df[df["Status"].isin(selected_statuses)]

        # Visualization type selection
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["2D Scatter", "3D Scatter", "Bar Chart"],
            key="chart_type_selector"
        )

        # Plotting
        if not filtered_df.empty:
            if chart_type == "2D Scatter":
                fig, ax = plt.subplots(figsize=(10, 6))
                for status in selected_statuses:
                    subset = filtered_df[filtered_df["Status"] == status]
                    ax.scatter(
                        subset["30.9"],
                        subset["89.6"],
                        label=status,
                        color=PRO_COLOR_PALETTE.get(status, '#1f78b4'),
                        alpha=0.7,
                        edgecolor='white',
                        linewidth=0.5
                    )
                ax.set_title("30.9 vs 89.6 Performance", fontsize=16, weight='bold')
                ax.set_xlim(fixed_x_range)
                ax.set_ylim(fixed_y_range)
                ax.set_xlabel("30.9 Metric", fontsize=12, color='#444')
                ax.set_ylabel("89.6 Metric", fontsize=12, color='#444')
                ax.tick_params(axis='both', colors='#666')
                ax.legend(title="Status", loc='upper left', frameon=False)
                plt.grid(color='#eee', linestyle='--', linewidth=0.5)
                st.pyplot(fig)

            elif chart_type == "3D Scatter":
                fig = px.scatter_3d(
                    filtered_df,
                    x="30.9",
                    y="89.6",
                    z="RPM",
                    color="Status",
                    color_discrete_map=PRO_COLOR_PALETTE,
                    title="3D Performance Visualization",
                    labels={"RPM": "Revolutions per Minute"},
                    range_x=fixed_x_range,
                    range_y=fixed_y_range,
                    range_z=fixed_z_range
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
                    y=["30.9", "89.6", "RPM"],
                    color="Status",
                    color_discrete_map=PRO_COLOR_PALETTE,
                    title="Average Metrics by Status",
                    labels={"value": "Average Value"},
                    width=1000,
                    height=600
                )
                fig.update_traces(
                    opacity=0.8,
                    hovertemplate="<b>Status: %{x}</b><br><br>" +
                                "30.9: %{y:.2f}<br>" +
                                "89.6: %{y:.2f}<br>" +
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

            # Download processed data
            @st.cache
            def convert_df(data):
                return data.to_csv(index=False).encode('utf-8')

            csv = convert_df(filtered_df)
            st.download_button(
                label="Download Filtered Data",
                data=csv,
                file_name='filtered_data.csv',
                mime='text/csv',
            )

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
