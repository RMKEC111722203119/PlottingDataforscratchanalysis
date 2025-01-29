import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

# Configure page settings
st.set_page_config(
    page_title="Enhanced Data Visualization App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom color palette with high contrast
status_colors = {
    "Healthy": "#4CAF50",
    "1H": "#FF5722",
    "2H": "#FFC107",
    "3H": "#2196F3",
    "4H": "#9C27B0",
    "1 Scratch": "#673AB7",
    "2 Scratch": "#009688",
    "3 Scratch": "#F44336",
    "4 Scratch": "#795548"
}

# Sidebar - File Upload
st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader(
    "Upload your Excel/CSV file",
    type=["xlsx", "xls", "csv"]
)

# Main App Area
st.title("Data Visualization Dashboard")
st.write("Upload your data and customize visualizations")

# Read file if uploaded
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic data cleaning
        df = df.dropna()
        
        # Identify numerical and categorical columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if 'Status' in cat_cols:
            status_options = df['Status'].unique()
        else:
            st.warning("No 'Status' column found. Please upload a file with a 'Status' column.")
            st.stop()
        
        # Allow status filtering with checkboxes
        st.subheader("Select Status Categories")
        selected_statuses = []
        for status in status_options:
            if st.checkbox(status, key=status):
                selected_statuses.append(status)
        
        # Stop if no statuses are selected
        if not selected_statuses:
            st.warning("Please select at least one status category")
            st.stop()
        
        filtered_df = df[df['Status'].isin(selected_statuses)]
        
        # Sidebar - Chart Configuration
        st.sidebar.header("Visualization Configuration")
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["2D Scatter", "3D Scatter", "Boxplot", "Histogram", "Line Chart", "Bar Chart"]
        )
        
        show_grid = st.sidebar.checkbox("Show Gridlines", value=True)
        chart_title = st.sidebar.text_input("Enter chart title", "Default Title")
        
        # Chart creation based on user selection
        if chart_type == "2D Scatter":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols)
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            for status in selected_statuses:
                subset = filtered_df[filtered_df['Status'] == status]
                ax.scatter(
                    subset[x_var],
                    subset[y_var],
                    label=status,
                    color=status_colors.get(status, '#000000'),
                    alpha=0.7
                )
            ax.set_title(chart_title)
            ax.set_xlabel(x_var)
            ax.set_ylabel(y_var)
            ax.legend(title='Status')
            ax.grid(show_grid)
            
            st.pyplot(fig)
        
        elif chart_type == "3D Scatter":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols)
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
            z_var = st.sidebar.selectbox("Z-axis", numeric_cols)
            
            fig = px.scatter_3d(
                filtered_df,
                x=x_var,
                y=y_var,
                z=z_var,
                color='Status',
                title=chart_title,
                color_discrete_map=status_colors
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Boxplot":
            x_var = st.sidebar.selectbox("X-axis (Categorical)", cat_cols)
            y_var = st.sidebar.selectbox("Y-axis (Numerical)", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(
                x=x_var,
                y=y_var,
                data=filtered_df,
                palette=[status_colors.get(status, '#0000') for status in selected_statuses],
                ax=ax
            )
            ax.set_title(chart_title)
            ax.grid(show_grid)
            
            st.pyplot(fig)
        
        elif chart_type == "Histogram":
            x_var = st.sidebar.selectbox("Variable", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            for status in selected_statuses:
                subset = filtered_df[filtered_df['Status'] == status]
                sns.histplot(
                    subset[x_var],
                    label=status,
                    color=status_colors.get(status, '#0000'),
                    kde=True,
                    alpha=0.5,
                    ax=ax
                )
            ax.legend(title='Status')
            ax.set_title(chart_title)
            ax.grid(show_grid)
            
            st.pyplot(fig)
        
        elif chart_type == "Line Chart":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols)
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            for status in selected_statuses:
                subset = filtered_df[filtered_df['Status'] == status]
                ax.plot(
                    subset[x_var],
                    subset[y_var],
                    label=status,
                    color=status_colors.get(status, '#0000'),
                    marker='o'
                )
            ax.set_title(chart_title)
            ax.set_xlabel(x_var)
            ax.set_ylabel(y_var)
            ax.legend(title='Status')
            ax.grid(show_grid)
            
            st.pyplot(fig)
        
        elif chart_type == "Bar Chart":
            x_var = st.sidebar.selectbox("X-axis (Categorical)", cat_cols)
            y_var = st.sidebar.selectbox("Y-axis (Numerical)", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            for status in selected_statuses:
                subset = filtered_df[filtered_df['Status'] == status]
                sns.barplot(
                    x=x_var,
                    y=y_var,
                    data=subset,
                    label=status,
                    color=status_colors.get(status, '#0000'),
                    ax=ax
                )
            ax.legend(title='Status')
            ax.set_title(chart_title)
            ax.grid(show_grid)
            
            st.pyplot(fig)
        
        # Show filtered data
        if st.checkbox("Show data"):
            st.subheader("Filtered Data")
            st.dataframe(filtered_df)
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed")
