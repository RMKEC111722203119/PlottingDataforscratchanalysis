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

st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader(
    "Upload your Excel/CSV file",
    type=["xlsx", "xls", "csv"]
)

st.sidebar.header("Visualization Configuration")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["2D Scatter", "3D Scatter", "Boxplot", "Histogram", "Line Chart", "Bar Chart"]
)

color_palette = st.sidebar.selectbox(
    "Select Color Palette",
    ["Set1", "Set2", "tab10", "Dark2", "Paired"]
)

show_grid = st.sidebar.checkbox("Show Gridlines", value=True)
chart_title = st.sidebar.text_input("Enter chart title", "Default Title")

st.title("Data Visualization Dashboard")
st.write("Upload your data and customize visualizations")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        df = df.dropna()
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if 'Status' in cat_cols:
            status_options = df['Status'].unique()
        else:
            st.warning("No 'Status' column found. Please upload a file with a 'Status' column.")
            st.stop()
        
        # Set default axis values if columns exist
        default_x = '30.9' if '30.9' in numeric_cols else numeric_cols[0]
        default_y = '89.6' if '89.6' in numeric_cols else numeric_cols[0]
        default_z = 'RPM' if 'RPM' in numeric_cols else None

        st.subheader("Select Status Categories")
        selected_statuses = []
        for status in status_options:
            checkbox = st.checkbox(status, value=True, key=status)
            if checkbox:
                selected_statuses.append(status)
        
        filtered_df = df[df['Status'].isin(selected_statuses)]
        
        if chart_type == "2D Scatter":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols, index=list(numeric_cols).index(default_x))
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols, index=list(numeric_cols).index(default_y))
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(
                x=x_var, 
                y=y_var, 
                hue='Status', 
                data=filtered_df,
                palette=color_palette,
                ax=ax
            )
            ax.set_title(chart_title)
            ax.grid(show_grid)
            st.pyplot(fig)
        
        elif chart_type == "3D Scatter":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols, index=list(numeric_cols).index(default_x))
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols, index=list(numeric_cols).index(default_y))
            z_var = st.sidebar.selectbox("Z-axis", numeric_cols, index=list(numeric_cols).index(default_z))
            
            fig = px.scatter_3d(
                filtered_df, 
                x=x_var, 
                y=y_var, 
                z=z_var, 
                color='Status',
                title=chart_title,
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Boxplot":
            x_var = st.sidebar.selectbox("X-axis", cat_cols)
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(
                x=x_var,
                y=y_var,
                data=filtered_df,
                palette=color_palette,
                ax=ax
            )
            ax.set_title(chart_title)
            ax.grid(show_grid)
            st.pyplot(fig)
        
        elif chart_type == "Histogram":
            x_var = st.sidebar.selectbox("Variable", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(
                filtered_df[x_var],
                kde=True,
                color=color_palette,
                ax=ax
            )
            ax.set_title(chart_title)
            ax.grid(show_grid)
            st.pyplot(fig)
        
        elif chart_type == "Line Chart":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols)
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(
                x=x_var, 
                y=y_var, 
                hue='Status',
                data=filtered_df,
                palette=color_palette,
                ax=ax
            )
            ax.set_title(chart_title)
            ax.grid(show_grid)
            st.pyplot(fig)
        
        elif chart_type == "Bar Chart":
            x_var = st.sidebar.selectbox("X-axis", cat_cols)
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x=x_var,
                y=y_var,
                hue='Status',
                data=filtered_df,
                palette=color_palette,
                ax=ax
            )
            ax.set_title(chart_title)
            ax.grid(show_grid)
            st.pyplot(fig)
        
        if st.checkbox("Show data"):
            st.subheader("Filtered Data")
            st.dataframe(filtered_df)
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed")
