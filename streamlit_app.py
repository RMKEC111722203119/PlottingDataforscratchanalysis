import streamlit as st
import pandas as pd
import plotly.express as px

# Configure app theme
st.set_page_config(
    page_title="Data Visualization Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define color scheme from the HEX codes
primary_color = "#1f77b4"
secondary_color = "#2ca02c"
bg_color = "#f5f5f5"

# Define visualization parameters
chart_size = (1000, 600)
mark_size = 10

# Initialize session state for file handling
if "data_uploaded" not in st.session_state:
    st.session_state.data_uploaded = False

# File upload section
st.sidebar.title("📊 Data Configuration")
uploaded_file = st.sidebar.file_uploader(
    "Upload your Excel/CSV file", 
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
    try:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Clean data
        df = df.dropna()
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        
        # Set session state
        st.session_state.data_uploaded = True
    except:
        st.sidebar.warning("Error loading file")
        st.session_state.data_uploaded = False

# Visualization section
if st.session_state.data_uploaded and 'Status' in df.columns:
    st.sidebar.title("📈 Visualization Settings")
    
    # Status selector
    st.sidebar.subheader("📊 Select Status Categories")
    status_options = sorted(df['Status'].unique())
    selected_statuses = st.sidebar.multiselect(
        "Select statuses", 
        options=status_options, 
        default=status_options
    )
    filtered_df = df[df['Status'].isin(selected_statuses)]
    
    # Chart type selector with emojis & labels
    chart_type = st.sidebar.radio(
        "📊 Choose Chart Type",
        [
            "2D Scatter Plot (📊)", 
            "3D Scatter Plot (📈)", 
            "Boxplot (📊)",
            "Histogram (📊)", 
            "Bar Chart (📊)",
            "Line Chart (📈)"
        ],
        labels=[
            "2D Scatter (X/Y)",
            "3D Scatter (X/Y/Z)",
            "Boxplot (Categories)",
            "Histogram (Distributions)",
            "Bar Chart (Categories)",
            "Line Chart (Trends)"
        ],
        horizontal=True
    )

    # Main visualization container
    container = st.container()
    container.title("📊 Interactive Data Visualization")
    container.markdown(
        """
        * **Steps**: Select data, choose chart type, customize settings
        * **Features**: Status filtering, color coding, hover info
        """
    )

    if chart_type == "2D Scatter Plot (📊)":
        x_var = st.sidebar.selectbox("X-axis", numeric_cols)
        y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
        color_var = st.sidebar.selectbox("Color Group", cat_cols)
        size_var = st.sidebar.selectbox("Size Scale", numeric_cols)

        fig = px.scatter(
            filtered_df,
            x=x_var,
            y=y_var,
            color=color_var,
            size=size_var,
            hover_name="Status",
            title=f"2D Scatter: {x_var} vs {y_var}",
            template="plotly_white",
            width=chart_size[0],
            height=chart_size[1]
        )
        container.plotly_chart(fig, use_container_width=True)

    elif chart_type == "3D Scatter Plot (📈)":
        x_var = st.sidebar.selectbox("X-axis (3D)", numeric_cols)
        y_var = st.sidebar.selectbox("Y-axis (3D)", numeric_cols)
        z_var = st.sidebar.selectbox("Z-axis (3D)", numeric_cols)
        color_var = st.sidebar.selectbox("Color Group (3D)", cat_cols)

        fig = px.scatter_3d(
            filtered_df,
            x=x_var,
            y=y_var,
            z=z_var,
            color=color_var,
            hover_name="Status",
            title=f"3D Scatter: {x_var}, {y_var}, {z_var}",
            template="plotly_dark"
        )
        container.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Boxplot (📊)":
        x_var = st.sidebar.selectbox("Boxplot X-axis (Categorical)", cat_cols)
        y_var = st.sidebar.selectbox("Boxplot Y-axis (Numerical)", numeric_cols)
        
        fig = px.box(
            filtered_df,
            x=x_var,
            y=y_var,
            color="Status",
            title=f"Boxplot: {y_var} by {x_var}",
            template="ggplot2"
        )
        container.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Histogram (📊)":
        x_var = st.sidebar.selectbox("Histogram Variable", numeric_cols)
        nbins = st.sidebar.slider("Number of Bins", 5, 50, 20)
        
        fig = px.histogram(
            filtered_df,
            x=x_var,
            nbins=nbins,
            color="Status",
            marginal="rug",
            title=f"Histogram: {x_var} Distribution",
            template="seaborn"
        )
        container.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart (📊)":
        x_var = st.sidebar.selectbox("Bar Chart X-axis (Categorical)", cat_cols)
        y_var = st.sidebar.selectbox("Bar Chart Y-axis (Numerical)", numeric_cols)
        
        fig = px.bar(
            filtered_df,
            x=x_var,
            y=y_var,
            color="Status",
            title=f"Bar Chart: {y_var} by {x_var}",
            template="simple_white"
        )
        container.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart (📈)":
        x_var = st.sidebar.selectbox("Line Chart X-axis", numeric_cols)
        y_var = st.sidebar.selectbox("Line Chart Y-axis", numeric_cols)
        color_var = st.sidebar.selectbox("Color Group (Line Chart)", cat_cols)
        
        fig = px.line(
            filtered_df,
            x=x_var,
            y=y_var,
            color=color_var,
            title=f"Line Chart: {y_var} over {x_var}",
            template="plotly_dark"
        )
        container.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Upload a file to start visualizing")

# Add footer style
st.markdown(
    """
    <style>
        footer {visibility: hidden;}
        .st-emotion-cache-1tom5gy {
            background-color: #f5f5f5;
            padding: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    ---
    Developed by ai_expert  
    [GitHub](https://github.com/ai-expert) | [LinkedIn](https://linkedin.com/ai_expert)
    """
)
