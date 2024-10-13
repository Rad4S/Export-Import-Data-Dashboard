import pandas as pd
import streamlit as st
import matplotlib as plt
import seaborn as sns
import plotly.express as px

# Set the Streamlit page configuration
st.set_page_config(
    page_title="Imports and Exports Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title of the dashboard
st.title("Imports and Exports Dashboard")

@st.cache_data
def load_data(filepath):
    """
    Load the dataset from a CSV file and perform initial preprocessing.
    """
    try:
        df = pd.read_csv(filepath)
        # Ensure 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
        # Drop rows with invalid dates
        df = df.dropna(subset=['Date'])
        return df
    except FileNotFoundError:
        st.error(f"File '{filepath}' not found. Please ensure the CSV file is in the correct directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

# Load dataset
df = load_data('Imports_Exports_Dataset.csv')

if df.empty:
    st.stop()  # Stop execution if data is not loaded

# Random Sample from the dataset
df_sample = df.sample(n=3001, random_state=55011)

# Sidebar for filters
st.sidebar.title("Filters")

# Category filter
categories = sorted(df_sample['Category'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories", options=categories, default=categories
)

# Import/Export filter
import_export_options = sorted(df_sample['Import_Export'].dropna().unique())
selected_import_export = st.sidebar.multiselect(
    "Select Import/Export", options=import_export_options, default=import_export_options
)

# Payment Terms filter
payment_terms = sorted(df_sample['Payment_Terms'].dropna().unique())
selected_payment_terms = st.sidebar.multiselect(
    "Select Payment Terms", options=payment_terms, default=payment_terms
)

# Filter the dataframe based on selections
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) &
    (df_sample['Import_Export'].isin(selected_import_export)) &
    (df_sample['Payment_Terms'].isin(selected_payment_terms))
]

# Check if filtered_df is not empty
if not filtered_df.empty:
    # Layout with multiple columns for better visualization
    col1, col2 = st.columns(2)

    with col1:
        # Scatter plot for Quantity vs. Value
        st.markdown('### Scatter Plot: Quantity vs. Value')
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(
            x='Quantity',
            y='Value',
            data=filtered_df,
            hue='Category',
            palette='viridis',
            alpha=0.7,
            edgecolor=None,
            ax=ax1
        )
        ax1.set_title('Quantity vs. Value')
        ax1.set_xlabel('Quantity')
        ax1.set_ylabel('Value')
        ax1.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig1)

    with col2:
        # Pie chart for percentage of high-value transactions
        st.markdown('### Pie Chart: Percentage of High-Value Transactions')
        high_value_threshold = filtered_df['Value'].quantile(0.75)
        high_value_transactions = filtered_df[filtered_df['Value'] >= high_value_threshold]
        high_value_pct = (len(high_value_transactions) / len(filtered_df)) * 100
        low_value_pct = 100 - high_value_pct
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(
            [high_value_pct, low_value_pct],
            labels=['High Value', 'Low Value'],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#66b3ff', '#ff9999']
        )
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig2)

    # Bar plot for frequency of shipping methods
    st.markdown('### Bar Plot: Frequency of Shipping Methods')
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.countplot(
        x='Shipping_Method',
        data=filtered_df,
        order=filtered_df['Shipping_Method'].value_counts().index,
        palette='magma',
        ax=ax3
    )
    ax3.set_title('Frequency of Shipping Methods')
    ax3.set_xlabel('Shipping Method')
    ax3.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Box plot for weight distribution per product category
    st.markdown('### Box Plot: Weight Distribution per Product Category')
    fig4, ax4 = plt.subplots(figsize=(14, 7))
    sns.boxplot(
        x='Category',
        y='Weight',
        data=filtered_df,
        palette='Set2',
        ax=ax4
    )
    ax4.set_title('Weight Distribution per Product Category')
    ax4.set_xlabel('Product Category')
    ax4.set_ylabel('Weight')
    plt.xticks(rotation=45)
    st.pyplot(fig4)

    # Line plot for monthly transaction trends
    st.markdown('### Line Plot: Monthly Transaction Trends')
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').dt.to_timestamp()
    monthly_avg_value = filtered_df.groupby(['Month', 'Import_Export'])['Value'].mean().reset_index()

    fig5, ax5 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x='Month',
        y='Value',
        hue='Import_Export',
        data=monthly_avg_value,
        marker='o',
        ax=ax5
    )
    ax5.set_title('Average Value of Transactions by Month')
    ax5.set_xlabel('Month')
    ax5.set_ylabel('Average Transaction Value')
    plt.xticks(rotation=45)
    ax5.legend(title='Import/Export', loc='upper left')
    st.pyplot(fig5)

    # Optional: Interactive Plotly Chart
    st.markdown('### Interactive Bar Chart: Frequency of Shipping Methods')
    shipping_counts = filtered_df['Shipping_Method'].value_counts().reset_index()
    shipping_counts.columns = ['Shipping_Method', 'Count']
    fig6 = px.bar(
        shipping_counts,
        x='Shipping_Method',
        y='Count',
        title='Frequency of Shipping Methods',
        labels={'Shipping_Method': 'Shipping Method', 'Count': 'Count'},
        color='Shipping_Method',
        template='plotly_dark'
    )
    st.plotly_chart(fig6, use_container_width=True)

else:
    st.warning("No data available for the selected filters. Please select at least 1 item from each filter.")
