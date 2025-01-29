import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO

# Custom CSS styling
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
        padding: 2rem;
    }
    .stTitle {
        color: #1a73e8;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
    }
    .stSidebar {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton {
        background-color: #4285f4;
        color: white;
        border-radius: 5px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton:hover {
        background-color: #2b5297;
    }
    .stCheckbox {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Main application
st.title("Advanced Data Visualization Dashboard")

# Sidebar configuration
with st.sidebar:
    st.header("Data Configuration")
    uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=["xlsx", "csv"])
    
    st.header("Visualization Settings")
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Interactive Dashboard", "3D Scatter", "Heatmap", "Violin Plot", "Parallel Coordinates"]
    )
    
    color_scheme = st.selectbox(
        "Choose Color Scheme",
        ["Plotly", "Viridis", "Plasma", "Inferno", "Magma", "Cividis"]
    )
    
    show_grid = st.checkbox("Show Gridlines")
    show_legend = st.checkbox("Show Legend")
    export_chart = st.checkbox("Enable Export")

# Main content area
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # Data preprocessing
        if 'Status' not in df.columns:
            st.error("Status column not found. Please ensure your data contains a 'Status' column.")
            st.stop()
        
        # Interactive Dashboard
        if chart_type == "Interactive Dashboard":
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                specs=[[{"type": "scatter"}, {"type": "histogram"}],
                       [{"type": "box"}, {"type": "bar"}]],
                subplot_titles=("2D Scatter", "Histogram", "Boxplot", "Status Distribution")
            )
            
            # 2D Scatter
            scatter = px.scatter(
                df, x='30.9', y='89.6', color='Status',
                title="2D Scatter Plot",
                color_continuous_scale=color_scheme
            )
            fig.add_traces(scatter.data, rows=[1]*len(scatter.data), cols=[1]*len(scatter.data))
            
            # Histogram
            hist = px.histogram(
                df, x='RPM', color='Status',
                title="RPM Distribution",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.add_traces(hist.data, rows=[1]*len(hist.data), cols=[2]*len(hist.data))
            
            # Boxplot
            box = px.box(
                df, x='Status', y='30.9',
                title="30.9 Distribution by Status",
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.add_traces(box.data, rows=[2]*len(box.data), cols=[1]*len(box.data))
            
            # Bar Chart
            bar = px.bar(
                df['Status'].value_counts(),
                title="Status Distribution",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.add_traces(bar.data, rows=[2]*len(bar.data), cols=[2]*len(bar.data))
            
            fig.update_layout(
                height=800,
                showlegend=show_legend,
                hovermode="closest"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "3D Scatter":
            fig = px.scatter_3d(
                df, x='30.9', y='89.6', z='RPM',
                color='Status',
                title="3D Scatter Plot",
                color_continuous_scale=color_scheme
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Heatmap":
            fig = px.density_heatmap(
                df, x='30.9', y='89.6',
                marginal_x='rug', marginal_y='rug',
                title="Density Heatmap",
                color_continuous_scale=color_scheme
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Violin Plot":
            fig = px.violin(
                df, x='Status', y='RPM',
                title="RPM Distribution by Status",
                color='Status',
                box=True,
                points='all',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Parallel Coordinates":
            fig = px.parallel_coordinates(
                df, color='Status',
                dimensions=['30.9', '89.6', 'RPM'],
                title="Parallel Coordinates Plot",
                color_continuous_scale=color_scheme
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Export functionality
        if export_chart:
            buf = BytesIO()
            fig.write_image(buf, format="png")
            st.download_button(
                label="Download Visualization",
                data=buf.getvalue(),
                file_name="visualization.png",
                mime="image/png"
            )
        
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
else:
    st.info("Please upload a dataset to get started.")
