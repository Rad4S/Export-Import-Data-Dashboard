import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Import dataset
df = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Random Sample from the dataset
df_sample = df.sample(n=3001, random_state=55011)

# Sidebar for filters
st.sidebar.title("Filters")

# Category filter
categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Import/Export filter
import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

# Payment Terms filter
payment_terms = df_sample['Payment_Terms'].unique()
selected_payment_terms = st.sidebar.multiselect("Select Payment Terms", options=payment_terms, default=payment_terms)

# Filter the dataframe based on selections
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) &
    (df_sample['Import_Export'].isin(selected_import_export)) &
    (df_sample['Payment_Terms'].isin(selected_payment_terms))
]

# Title of the dashboard
st.title("Imports and Exports Dashboard")

# Check if filtered_df is not empty
if not filtered_df.empty:
    
    # Scatter plot for Quantity vs. Value
    st.markdown('### Scatter Plot: Quantity vs. Value')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Quantity', y='Value', data=filtered_df, hue='Category', ax=ax1)
    ax1.set_title('Quantity vs. Value')
    st.pyplot(fig1)

    # Pie chart for percentage of high-value transactions
    st.markdown('### Pie Chart: Percentage of High-Value Transactions')
    high_value_threshold = filtered_df['Value'].quantile(0.75)
    high_value_transactions = filtered_df[filtered_df['Value'] >= high_value_threshold]
    high_value_pct = (len(high_value_transactions) / len(filtered_df)) * 100
    low_value_pct = 100 - high_value_pct
    fig2, ax2 = plt.subplots()
    ax2.pie([high_value_pct, low_value_pct], labels=['High Value', 'Low Value'], autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'skyblue'])
    ax2.axis('equal')
    st.pyplot(fig2)

    # Bar plot for frequency of shipping methods
    st.markdown('### Bar Plot: Frequency of Shipping Methods')
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.countplot(x='Shipping_Method', data=filtered_df, ax=ax3)
    ax3.set_title('Frequency of Shipping Methods')
    st.pyplot(fig3)

    # Box plot for weight distribution per product category
    st.markdown('### Box Plot: Weight Distribution per Product Category')
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Category', y='Weight', data=filtered_df, ax=ax4)
    ax4.set_title('Weight Distribution per Product Category')
    st.pyplot(fig4)

    # Line plot for monthly transaction trends
    st.markdown('### Line Plot: Monthly Transaction Trends')
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%m-%Y')
    filtered_df['Month'] = filtered_df['Date'].dt.month
    monthly_avg_value = filtered_df.groupby(['Month', 'Import_Export'])['Value'].mean().unstack()
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    monthly_avg_value.plot(ax=ax5, marker='o')
    ax5.set_title('Average Value of Transactions by Month')
    ax5.set_xlabel('Month')
    ax5.set_ylabel('Average Transaction Value')
    st.pyplot(fig5)

else:
    st.warning("No data available for the selected filters. Please select at least 1 item from each filter.")
