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

# Load data (replace with your file loading method)
@st.cache
def load_data(file):
    if file.name.lower().endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader(
    "Upload your Excel/CSV file", 
    type=["xlsx", "xls", "csv"], 
    help="Upload your data file to begin visualization"
)

st.sidebar.header("Chart Configuration")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["2D Scatter", "3D Scatter", "Bar Chart (Mean)"],
    help="Choose the type of visualization"
)

color_palette = st.sidebar.selectbox(
    "Select Color Palette",
    ["Set1", "Set2", "Dark2"],
    help="Choose a professional color palette"
)

chart_title = st.sidebar.text_input(
    "Chart Title",
    "Professional Data Visualization",
    help="Enter a custom title for your chart"
)

st.sidebar.markdown("---")
st.sidebar.markdown("© 2024, Your Professional Data Team")

st.title("Professional Data Visualization Dashboard")
st.write("A polished interface for data exploration and analysis")

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        df = df.dropna()
    
        status_options = df["Status"].unique()
        
        # Advanced status selection
        st.sidebar.subheader("Status Selection")
        selected_statuses = st.sidebar.multiselect(
            "Select Statuses to Compare:",
            status_options,
            default=status_options.tolist(),
            help="Choose statuses to include in the visualization"
        )
        
        # Color customization
        st.sidebar.subheader("Color Customization")
        color_mapping = {}
        for status in status_options:
            default_color = f"C{status_options.tolist().index(status)}"
            color = st.sidebar.color_picker(
                f"Status {status}:",
                value=sns.color_palette(color_palette)[status_options.tolist().index(status)],
                help="Select a color for each status"
            )
            color_mapping[status] = color
        
        filtered_df = df[df["Status"].isin(selected_statuses)]
        
        # Chart customization
        if chart_type == "2D Scatter":
            fig, ax = plt.subplots(figsize=(10, 6))
            for status in selected_statuses:
                subset = filtered_df[filtered_df["Status"] == status]
                ax.scatter(
                    subset["30.9"],
                    subset["89.6"],
                    label=status,
                    color=color_mapping.get(status, sns.color_palette(color_palette)[status_options.tolist().index(status)]),
                    alpha=0.7
                )
            ax.set_title(chart_title, fontsize=16, fontweight="bold")
            ax.set_xlabel("30.9 Sensor Value", fontsize=12)
            ax.set_ylabel("89.6 Sensor Value", fontsize=12)
            ax.set_xlim(-70, -20)
            ax.set_ylim(-70, -20)
            ax.legend(title="Status", loc="upper right")
            plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            st.pyplot(fig)
        
        elif chart_type == "3D Scatter":
            fig = px.scatter_3d(
                filtered_df,
                x="30.9",
                y="89.6",
                z="RPM",
                color="Status",
                color_discrete_map=color_mapping,
                title=chart_title,
                labels={"30.9": "30.9 Sensor Value", "89.6": "89.6 Sensor Value", "RPM": "RPM Value"}
            )
            fig.update_layout(
                scene=dict(
                    xaxis=dict(range=[-70, -20], title="30.9 Sensor Value"),
                    yaxis=dict(range=[-70, -20], title="89.6 Sensor Value"),
                ),
                margin=dict(l=40, r=40, b=40, t=40),
                font=dict(size=12, color="black"),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            st.plotly_chart(fig)
        
        elif chart_type == "Bar Chart (Mean)":
            fig = px.bar(
                filtered_df.groupby("Status", as_index=False).mean(),
                x="Status",
                y=["30.9", "89.6", "RPM"],
                color="Status",
                color_discrete_map=color_mapping,
                title=chart_title,
                labels={"Status": "Status", "value": "Mean Value", "variable": "Metric"},
            )
            fig.update_layout(
                margin=dict(l=40, r=40, b=40, t=40),
                font=dict(size=12, color="black"),
                paper_bgcolor='white',
                plot_bgcolor='white',
                legend=dict(title="Status", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig)
        
        # Show data table
        if st.checkbox("Show Raw Data"):
            st.subheader("Raw Data")
            st.dataframe(filtered_df.style.highlight_max(axis=0))
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to get started")
