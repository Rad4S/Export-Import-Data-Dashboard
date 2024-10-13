import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Cache the dataset loading to avoid reloading every time
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Imports_Exports_Dataset.csv')
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
        df['Year'] = df['Date'].dt.year
        return df.dropna(subset=['Date', 'Year'])
    except FileNotFoundError:
        st.error("Dataset not found. Please upload the 'Imports_Exports_Dataset.csv' file.")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.stop()  # Stop execution if the dataset is empty or not loaded

# Sample data for performance
df_sample = df.sample(n=min(3000, len(df)), random_state=42)

# Sidebar filters
st.sidebar.title("Filters")

categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", import_export_options, default=import_export_options)

years = sorted(df_sample['Year'].unique())
selected_years = st.sidebar.multiselect("Select Years", years, default=years)

# Filter the data based on selections
filtered_df = df_sample[
    df_sample['Category'].isin(selected_categories) &
    df_sample['Import_Export'].isin(selected_import_export) &
    df_sample['Year'].isin(selected_years)
]

# Main dashboard title
st.title("Imports and Exports Dashboard")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your filters.")
    st.stop()  # Stop execution if filtered data is empty

# 1. Scatter Plot: Quantity vs. Value
st.subheader('1. Scatter Plot of Quantity vs. Value')
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_df, x='Quantity', y='Value', ax=ax, color='blue')
ax.set_title('Scatter Plot of Quantity vs. Value')
st.pyplot(fig)
plt.close(fig)

# 2. Pie Chart: Percentage of High-Value Transactions
high_value = filtered_df['Value'] >= filtered_df['Value'].quantile(0.90)
percentage_high_value = high_value.mean() * 100

st.subheader('2. Percentage of High-Value Transactions')
fig, ax = plt.subplots()
ax.pie(
    [percentage_high_value, 100 - percentage_high_value],
    labels=['High Value', 'Others'], autopct='%1.1f%%', startangle=90,
    colors=['#800080', '#FFC0CB']
)
ax.set_title('Percentage of High-Value Transactions')
st.pyplot(fig)
plt.close(fig)

# 3. Bar Plot: Frequency of Shipping Methods
if 'Shipping_Method' in filtered_df.columns:
    st.subheader('3. Bar Plot of Shipping Methods')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=filtered_df, x='Shipping_Method', ax=ax, color='red')
    ax.set_title('Bar Plot of Shipping Methods')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

# 4. Histogram: Transaction Value Distribution
st.subheader('4. Transaction Value Distribution')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_df['Value'], bins=30, kde=True, ax=ax, color='red', alpha=0.7)
sns.histplot(filtered_df['Value'], bins=30, kde=True, ax=ax, color='lightblue', alpha=0.3)
ax.set_title('Transaction Value Distribution')
st.pyplot(fig)
plt.close(fig)

# 5. Box Plot: Weight Distribution per Product Category
st.subheader('5. Weight Distribution per Product Category')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=filtered_df, x='Category', y='Weight', ax=ax, palette='pastel')
ax.set_title('Weight Distribution per Product Category')
plt.xticks(rotation=45)
st.pyplot(fig)
plt.close(fig)

# 6. Line Plot: Monthly Transaction Trends
filtered_df = filtered_df.assign(Month=filtered_df['Date'].dt.month)
monthly_transactions = filtered_df.groupby('Month')['Value'].sum().reset_index()

st.subheader('6. Monthly Transaction Trends')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_transactions, x='Month', y='Value', ax=ax, color='pink', linewidth=2)
ax.set_title('Monthly Transaction Trends')
st.pyplot(fig)
plt.close(fig)
