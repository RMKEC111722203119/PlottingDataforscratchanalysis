import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

st.set_page_config(
    page_title="Flexible Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional color palette
PRO_COLOR_PALETTE = {
    "Healthy": "#4CAF50",
    "1H": "#2196F3",
    "2H": "#FF9800",
    "3H": "#9C27B0",
    "4H": "#795548",
    "1 Scratch": "#E91E63",
    "2 Scratch": "#607D8B",
    "3 Scratch": "#FF5722",
    "4 Scratch": "#009688"
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

st.sidebar.header("Customization Options")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["2D Scatter", "3D Scatter", "Bar Chart"],
    key="chart_type_selector"
)

# Main App Area
st.title("Data Visualization Dashboard")
st.markdown(
    "<h3 style='text-align: center; color: #333;'>Upload your data and explore visualizations</h3>",
    unsafe_allow_html=True
)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        df = df.dropna()

        status_options = df["Status"].unique()
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

        # Status selection with color picker
        status_col, color_col = st.columns([3, 1])
        selected_statuses = []
        color_mapping = {}
        
        for status in status_options:
            status_col.checkbox(
                status,
                value=True,
                key=status,
                help=f"Toggle {status} visibility"
            )
            color = color_col.color_picker(
                f"Color for {status}",
                value=PRO_COLOR_PALETTE.get(status, '#1f78b4'),
                key=f"color_{status}"
            )
            color_mapping[status] = color

        # Get selected statuses
        selected_statuses = [status for status in status_options if status_col.checkbox.status]

        filtered_df = df[df["Status"].isin(selected_statuses)]

        # Chart configuration
        x_var = st.sidebar.selectbox("X-axis", numeric_cols, index=0, key="x_axis")
        y_var = st.sidebar.selectbox("Y-axis", numeric_cols, index=1, key="y_axis")
        z_var = st.sidebar.selectbox("Z-axis (3D Only)", numeric_cols, index=2, key="z_axis")

        x_range = st.sidebar.slider("X-axis Range", float(df[x_var].min()), float(df[x_var].max()), (float(df[x_var].min()), float(df[x_var].max())))
        y_range = st.sidebar.slider("Y-axis Range", float(df[y_var].min()), float(df[y_var].max()), (float(df[y_var].min()), float(df[y_var].max())))

        chart_title = st.sidebar.text_input("Chart Title", "Default Chart Title")

        # Plotting
        if not filtered_df.empty:
            if chart_type == "2D Scatter":
                fig, ax = plt.subplots(figsize=(10, 6))
                for status in selected_statuses:
                    subset = filtered_df[filtered_df["Status"] == status]
                    ax.scatter(
                        subset[x_var],
                        subset[y_var],
                        label=status,
                        color=color_mapping[status],
                        alpha=0.7,
                        edgecolor='white',
                        linewidth=0.5
                    )
                ax.set_title(chart_title, fontsize=16, weight='bold')
                ax.set_xlim(x_range)
                ax.set_ylim(y_range)
                ax.set_xlabel(x_var, fontsize=12, color='#444')
                ax.set_ylabel(y_var, fontsize=12, color='#444')
                ax.tick_params(axis='both', colors='#666')
                ax.legend(title="Status", loc='upper left', frameon=False)
                plt.grid(color='#eee', linestyle='--', linewidth=0.5)
                st.pyplot(fig)

            elif chart_type == "3D Scatter":
                fig = px.scatter_3d(
                    filtered_df,
                    x=x_var,
                    y=y_var,
                    z=z_var,
                    color="Status",
                    color_discrete_map=color_mapping,
                    title=chart_title,
                    range_x=x_range,
                    range_y=y_range,
                    range_z=[float(df[z_var].min()), float(df[z_var].max())]
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
                    y=[x_var, y_var],
                    color="Status",
                    color_discrete_map=color_mapping,
                    title=chart_title,
                    labels={"value": "Average Value"},
                    barmode="group"
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
            st.dataframe(filtered_df.style.set_properties(**{
                'background-color': '#f9f9f9',
                'color': '#333'
            }))
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed")
