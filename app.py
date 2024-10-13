import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
df = pd.read_csv('Imports_Exports_Dataset.csv')

# Sample for performance
df_sample = df.sample(n=3001, random_state=055035)

# Sidebar filters
st.sidebar.title("Filters")

# Category Filter
categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Import/Export Filter
import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

# Year filter (based on the Date column)
df_sample['Date'] = pd.to_datetime(df_sample['Date'], format='%d-%m-%Y')
df_sample['Year'] = df_sample['Date'].dt.year
years = df_sample['Year'].unique()
selected_years = st.sidebar.multiselect("Select Years", options=years, default=years)

# Filter the data based on selections
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) & 
    (df_sample['Import_Export'].isin(selected_import_export)) & 
    (df_sample['Year'].isin(selected_years))
]

# Title
st.title("Imports and Exports Dashboard")

# Ensure data is not empty
if not filtered_df.empty:

    # 1. Scatter Plot: Quantity vs. Value
    st.subheader('1. Scatter Plot of Quantity vs. Value')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Quantity', y='Value', data=filtered_df, color='blue')
    plt.title('Scatter Plot of Quantity vs. Value')
    plt.xlabel('Quantity')
    plt.ylabel('Value')
    st.pyplot(plt)

    # 2. Pie chart for Percentage of High-Value Transactions
    high_value_transactions = filtered_df[filtered_df['Value'] >= filtered_df['Value'].quantile(0.90)]
    percentage_high_value = len(high_value_transactions) / len(filtered_df) * 100

    st.subheader('2. Percentage of High-Value Transactions')
    plt.figure(figsize=(6, 6))
    plt.pie([percentage_high_value, 100 - percentage_high_value],
            labels=['High Value', 'Others'], autopct='%1.1f%%', startangle=90,
            colors=['#800080', '#FFC0CB'])
    plt.title('Percentage of High-Value Transactions')
    plt.axis('equal')
    st.pyplot(plt)

    # 3. Bar Plot: Frequency of Shipping Methods
    st.subheader('3. Bar Plot of Shipping Methods')
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Shipping_Method', data=filtered_df, color='red')
    plt.title('Bar Plot of Shipping Methods')
    plt.xlabel('Shipping Method')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # 4. Histogram: Transaction Value Distribution
    st.subheader('4. Transaction Value Distribution')
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df['Value'], bins=30, kde=True, color='red', alpha=0.7)
    sns.histplot(filtered_df['Value'], bins=30, kde=True, color='lightblue', alpha=0.3)
    plt.title('Transaction Value Distribution')
    plt.xlabel('Transaction Value')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    # 5. Box-Whisker Plot: Weight Distribution per Product Category
    st.subheader('5. Weight Distribution per Product Category')
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Category', y='Weight', data=filtered_df, palette='pastel')
    plt.title('Weight Distribution per Product Category')
    plt.xlabel('Category')
    plt.ylabel('Weight')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # 6. Line Plot: Monthly Transaction Trends
    st.subheader('6. Monthly Transaction Trends')
    filtered_df['Month'] = filtered_df['Date'].dt.month
    monthly_transactions = filtered_df.groupby('Month')['Value'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Month', y='Value', data=monthly_transactions, color='pink', linewidth=2)
    plt.title('Monthly Transaction Trends')
    plt.xlabel('Month')
    plt.ylabel('Total Value')
    plt.xticks(rotation=0)
    st.pyplot(plt)

else:
    st.warning("No data available for the selected filters. Please adjust your filters.")
