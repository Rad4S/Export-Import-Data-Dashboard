import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use('Agg')  # Ensure compatibility with Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
df = pd.read_csv('Imports_Exports_Dataset.csv')

# Sample for performance
df_sample = df.sample(n=3001, random_state=55035)

# Sidebar filters
st.sidebar.title("Filters")

# Category Filter
categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect(
    "Select Categories", options=categories, default=categories
)

# Import/Export Filter
import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect(
    "Select Import/Export", options=import_export_options, default=import_export_options
)

# Year Filter
df_sample['Date'] = pd.to_datetime(df_sample['Date'], format='%d-%m-%Y', errors='coerce')
df_sample['Year'] = df_sample['Date'].dt.year
years = df_sample['Year'].dropna().unique()
selected_years = st.sidebar.multiselect(
    "Select Years", options=sorted(years), default=sorted(years)
)

# Filter the data based on selections
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) &
    (df_sample['Import_Export'].isin(selected_import_export)) &
    (df_sample['Year'].isin(selected_years))
]

# Dashboard Title
st.title("Imports and Exports Dashboard")

# Check if data exists after filtering
if not filtered_df.empty:

    # 1. Scatter Plot: Quantity vs. Value
    st.subheader('1. Scatter Plot of Quantity vs. Value')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Quantity', y='Value', data=filtered_df, color='blue', ax=ax)
    ax.set_title('Scatter Plot of Quantity vs. Value')
    ax.set_xlabel('Quantity')
    ax.set_ylabel('Value')
    st.pyplot(fig)
    plt.close(fig)

    # 2. Pie Chart: High-Value Transactions Percentage
    high_value_transactions = filtered_df[filtered_df['Value'] >= filtered_df['Value'].quantile(0.90)]
    percentage_high_value = len(high_value_transactions) / len(filtered_df) * 100

    st.subheader('2. Percentage of High-Value Transactions')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        [percentage_high_value, 100 - percentage_high_value],
        labels=['High Value', 'Others'], autopct='%1.1f%%', startangle=90,
        colors=['#800080', '#FFC0CB']
    )
    ax.set_title('Percentage of High-Value Transactions')
    ax.axis('equal')
    st.pyplot(fig)
    plt.close(fig)

    # 3. Bar Plot: Frequency of Shipping Methods
    st.subheader('3. Bar Plot of Shipping Methods')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x='Shipping_Method', data=filtered_df, color='red', ax=ax)
    ax.set_title('Bar Plot of Shipping Methods')
    ax.set_xlabel('Shipping Method')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

    # 4. Histogram: Transaction Value Distribution
    st.subheader('4. Transaction Value Distribution')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['Value'], bins=30, kde=True, color='red', alpha=0.7, ax=ax)
    sns.histplot(filtered_df['Value'], bins=30, kde=True, color='lightblue', alpha=0.3, ax=ax)
    ax.set_title('Transaction Value Distribution')
    ax.set_xlabel('Transaction Value')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    plt.close(fig)

    # 5. Box-Whisker Plot: Weight Distribution per Product Category
    st.subheader('5. Weight Distribution per Product Category')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Category', y='Weight', data=filtered_df, palette='pastel', ax=ax)
    ax.set_title('Weight Distribution per Product Category')
    ax.set_xlabel('Category')
    ax.set_ylabel('Weight')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

    # 6. Line Plot: Monthly Transaction Trends
    st.subheader('6. Monthly Transaction Trends')
    filtered_df['Month'] = filtered_df['Date'].dt.month
    monthly_transactions = filtered_df.groupby('Month')['Value'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Month', y='Value', data=monthly_transactions, color='pink', linewidth=2, ax=ax)
    ax.set_title('Monthly Transaction Trends')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Value')
    plt.xticks(rotation=0)
    st.pyplot(fig)
    plt.close(fig)

else:
    st.warning("No data available for the selected filters. Please adjust your filters.")
