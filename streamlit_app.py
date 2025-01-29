import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Sample data generation (replace with your actual data loading logic)
# Assuming the structure: '30.9', '89.6', 'RPM', 'Status'
np.random.seed(42)
data = {
    '30.9': np.random.uniform(-60, -30, 200),
    '89.6': np.random.uniform(-60, -30, 200),
    'RPM': np.random.choice([1765, 1770, 1775, 1780], 200),
    'Status': np.random.choice(['Healthy', '1H', '2H', '3H', '4H'], 200)
}
df = pd.DataFrame(data)

# Streamlit App
st.title("Dynamic Data Visualization Dashboard")

# Sidebar with interactive controls
st.sidebar.header("Data Filters")
status_options = df['Status'].unique()
default_status = status_options.tolist()

# Select all checkbox to toggle selections
select_all = st.sidebar.checkbox("Select All Statuses", value=True)
if select_all:
    selected_status = status_options.tolist()
else:
    selected_status = st.sidebar.multiselect(
        "Select Statuses to Include:",
        options=status_options,
        default=default_status
    )

# Additional plot controls
var_to_plot = st.sidebar.selectbox("Select Variable for Y-Axis:", ['30.9', '89.6', 'RPM'])

# Filter dataframe based on selections
filtered_df = df[df['Status'].isin(selected_status)]

# Main visualization section
st.header("Data Visualization")
plot_type = st.selectbox(
    "Select Plot Type:",
    [
        "2D Scatter (30.9 vs 89.6)",
        "3D Scatter (30.9, 89.6, RPM)",
        "Boxplot",
        "Histogram",
        "Violin Plot",
        "Status Count"
    ]
)

# Custom plots based on selection
if plot_type == "2D Scatter (30.9 vs 89.6)":
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        x='30.9', y='89.6', hue='Status', 
        data=filtered_df, palette='viridis', ax=ax
    )
    ax.set_title("2D Scatter Plot (30.9 vs 89.6)")
    st.pyplot(fig)

elif plot_type == "3D Scatter (30.9, 89.6, RPM)":
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for status in filtered_df.Status.unique():
        subset = filtered_df[filtered_df.Status == status]
        ax.scatter(
            subset['30.9'], subset['89.6'], subset['RPM'],
            label=status, alpha=0.7
        )
    ax.set_xlabel('30.9')
    ax.set_ylabel('89.6')
    ax.set_zlabel('RPM')
    ax.legend(title='Status')
    st.pyplot(fig)

elif plot_type == "Boxplot":
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.boxplot(
        x='Status', y=var_to_plot, data=filtered_df, 
        palette='viridis', ax=ax
    )
    ax.set_title(f"Boxplot of {var_to_plot} by Status")
    st.pyplot(fig)

elif plot_type == "Histogram":
    bins = st.sidebar.slider("Number of bins:", min_value=5, max_value=50, value=20)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(
        filtered_df[var_to_plot], bins=bins, 
        kde=True, ax=ax, color='skyblue'
    )
    ax.set_title(f"Histogram of {var_to_plot}")
    st.pyplot(fig)

elif plot_type == "Violin Plot":
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.violinplot(
        x='Status', y=var_to_plot, data=filtered_df, 
        palette='viridis', ax=ax
    )
    ax.set_title(f"Violin Plot of {var_to_plot} by Status")
    st.pyplot(fig)

elif plot_type == "Status Count":
    status_counts = filtered_df['Status'].value_counts()
    st.bar_chart(status_counts)

# Show filtered data
st.subheader("Filtered Data")
st.write(filtered_df)
