import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Load the data
data = pd.read_csv("Imports_Exports_Dataset.csv")

# Set the title of the Streamlit app
st.title('Imports and Exports Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
shipping_methods = st.sidebar.multiselect(
    'Select Shipping Method',
    options=data['Shipping_Method'].unique(),
    default=data['Shipping_Method'].unique()
)

# Filter the data based on the selected shipping methods
filtered_data = data[data['Shipping_Method'].isin(shipping_methods)]

# Scatter plot for Quantity vs. Value
st.subheader('1. Scatter Plot of Quantity vs. Value')
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Quantity', y='Value', data=filtered_data, color='blue')
plt.title('Scatter Plot of Quantity vs. Value')
plt.xlabel('Quantity')
plt.ylabel('Value')
st.pyplot(plt)

# Percentage of High-Value Transactions
high_value_transactions = filtered_data[filtered_data['Value'] >= filtered_data['Value'].quantile(0.90)]
percentage_high_value = len(high_value_transactions) / len(filtered_data) * 100

# Plotting the Pie Chart
st.subheader('2. Percentage of High-Value Transactions')
plt.figure(figsize=(6, 6))
plt.pie(
    [percentage_high_value, 100 - percentage_high_value],
    labels=['High Value', 'Others'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#800080', '#FFC0CB']
)
plt.title('Percentage of High-Value Transactions')
plt.axis('equal')
st.pyplot(plt)

# Bar plot for Frequency of Shipping Methods
st.subheader('3. Bar Plot of Shipping Methods')
plt.figure(figsize=(8, 6))
sns.countplot(x='Shipping_Method', data=filtered_data, color='red')
plt.title('Bar Plot of Shipping Methods')
plt.xlabel('Shipping Method')
plt.ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(plt)

# Transaction Value Distribution (Histogram)
st.subheader('4. Transaction Value Distribution')
plt.figure(figsize=(10, 6))
sns.histplot(filtered_data['Value'], bins=30, kde=True, color='green', alpha=0.7)
sns.histplot(filtered_data['Value'], bins=30, kde=True, color='lightblue', alpha=0.3)
plt.title('Transaction Value Distribution')
plt.xlabel('Transaction Value')
plt.ylabel('Frequency')
st.pyplot(plt)

# Weight Distribution per Product Category (Box-Whisker)
st.subheader('5. Weight Distribution per Product Category')
plt.figure(figsize=(12, 6))
sns.boxplot(x='Category', y='Weight', data=filtered_data, palette='pastel')
plt.title('Weight Distribution per Product Category')
plt.xlabel('Category')
plt.ylabel('Weight')
plt.xticks(rotation=45)
st.pyplot(plt)

# Monthly Transaction Trends (Line)
st.subheader('6. Monthly Transaction Trends')
filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], format='%d-%m-%Y', dayfirst=True)
filtered_data['Month'] = filtered_data['Date'].dt.month
monthly_transactions = filtered_data.groupby('Month')['Value'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x='Month', y='Value', data=monthly_transactions, color='pink', linewidth=2)
plt.title('Monthly Transaction Trends')
plt.xlabel('Month')
plt.ylabel('Total Value')
plt.xticks(rotation=0)
st.pyplot(plt)
