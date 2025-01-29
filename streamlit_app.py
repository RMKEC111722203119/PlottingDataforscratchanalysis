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
    "Select Default Palette",
    ["viridis", "plasma", "inferno", "magma", "cividis", "tab10", "Set1", "Set2"]
)

min_value = -70
max_value = -20
st.sidebar.info(f"Data range fixed between {min_value} and {max_value}")

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

        # Column layout for status checkboxes
        col1, col2, col3 = st.columns(3)
        selected_statuses = []
        status_colors = {}
        
        for i, status in enumerate(status_options):
            with st.columns(3)[i % 3]:
                selected = st.checkbox(status, value=True, key=f"{status}_check")
                if selected:
                    selected_statuses.append(status)
                    color = st.color_picker(f"Color for {status}", value="#ffff00", key=f"{status}_color")
                    status_colors[status] = color
        
        filtered_df = df[df['Status'].isin(selected_statuses)]
        
        # Assign custom colors first, then default palette
        custom_colors = [status_colors.get(s, color_palette) for s in filtered_df['Status']]
        
        if chart_type == "2D Scatter":
            x_var = st.sidebar.selectbox("X-axis", numeric_cols, index=list(numeric_cols).index(default_x))
            y_var = st.sidebar.selectbox("Y-axis", numeric_cols, index=list(numeric_cols).index(default_y))
            
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = sns.scatterplot(
                x=x_var, 
                y=y_var, 
                hue='Status', 
                data=filtered_df,
                palette=custom_colors,
                ax=ax
            )
            
            # Assign custom colors
            for label, color in status_colors.items():
                scatter.legend_.get_texts()[list(status_colors.keys()).index(label)].set_color(color)
            
            # Set fixed data limits
            ax.set_xlim(min_value, max_value)
            ax.set_ylim(min_value, max_value)
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
                color_discrete_sequence=list(status_colors.values()) or px.colors.qualitative.Set1
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Add more chart types here if needed...
        
        if st.checkbox("Show data"):
            st.subheader("Filtered Data")
            st.dataframe(filtered_df)
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a file to proceed")
