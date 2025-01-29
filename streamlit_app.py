import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

st.set_page_config(
    page_title="Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
st.write("Upload your data and customize visualizations")

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        df = df.dropna()  # Basic data cleaning

        # Default chart boundaries
        fixed_x_range = (-70, -20)
        fixed_y_range = (-70, -20)

        # Column configuration
        status_col, color_col = st.columns(2)

        # Status selection
        status_options = df["Status"].unique()
        selected_statuses = st.sidebar.multiselect(
            "Select Statuses to Include:",
            options=status_options,
            default=list(status_options)
        )

        # Color picker for each status
        color_mapping = {}
        for status in status_options:
            color = st.sidebar.color_picker(
                f"Select color for {status}",
                value="#{:06x}".format(hash(status) % 0xFFFFFF)  # Random default color
            )
            color_mapping[status] = color if color else None

        # Filter data based on selected statuses
        filtered_df = df[df["Status"].isin(selected_statuses)]

        # Chart title input
        chart_title = st.sidebar.text_input("Chart Title", "Default Chart Title")

        # Visualization type selection
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["2D Scatter", "3D Scatter", "Bar Chart"]
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
                        color=color_mapping.get(status, '#1f78b4'),
                        alpha=0.7
                    )
                ax.set_title(chart_title)
                ax.set_xlim(fixed_x_range)
                ax.set_ylim(fixed_y_range)
                ax.set_xlabel("30.9")
                ax.set_ylabel("89.6")
                ax.legend(title="Status")
                st.pyplot(fig)

            elif chart_type == "3D Scatter":
                fig = px.scatter_3d(
                    filtered_df,
                    x="30.9",
                    y="89.6",
                    z="RPM",
                    color="Status",
                    color_discrete_map=color_mapping,
                    title=chart_title
                )
                st.plotly_chart(fig)

            elif chart_type == "Bar Chart":
                fig = px.bar(
                    filtered_df.groupby("Status", as_index=False).mean(),
                    x="Status",
                    y=["30.9", "89.6", "RPM"],
                    title=chart_title,
                    color_discrete_map=color_mapping
                )
                st.plotly_chart(fig)

            # Show raw data
            if st.checkbox("Show Raw Data"):
                st.subheader("Raw Data")
                st.write(filtered_df)

        else:
            st.warning("No data available for the selected statuses")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed")
