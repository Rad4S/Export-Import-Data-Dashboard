import pandas as pd
import streamlit as st
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
    try:
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
        df = df.dropna(subset=['Date'])
        return df
    except FileNotFoundError:
        st.error(f"File '{filepath}' not found. Please ensure the CSV file is in the correct directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

df = load_data('Imports_Exports_Dataset.csv')

if df.empty:
    st.stop()

df_sample = df.sample(n=3001, random_state=55011)

st.sidebar.title("Filters")

categories = sorted(df_sample['Category'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Categories", options=categories, default=categories
)

import_export_options = sorted(df_sample['Import_Export'].dropna().unique())
selected_import_export = st.sidebar.multiselect(
    "Select Import/Export", options=import_export_options, default=import_export_options
)

payment_terms = sorted(df_sample['Payment_Terms'].dropna().unique())
selected_payment_terms = st.sidebar.multiselect(
    "Select Payment Terms", options=payment_terms, default=payment_terms
)

filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) &
    (df_sample['Import_Export'].isin(selected_import_export)) &
    (df_sample['Payment_Terms'].isin(selected_payment_terms))
]

if not filtered_df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Scatter Plot: Quantity vs. Value')
        fig1 = px.scatter(
            filtered_df,
            x='Quantity',
            y='Value',
            color='Category',
            title='Quantity vs. Value',
            labels={'Quantity': 'Quantity', 'Value': 'Value'}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown('### Pie Chart: Percentage of High-Value Transactions')
        high_value_threshold = filtered_df['Value'].quantile(0.75)
        high_value_transactions = filtered_df[filtered_df['Value'] >= high_value_threshold]
        high_value_pct = (len(high_value_transactions) / len(filtered_df)) * 100
        low_value_pct = 100 - high_value_pct
        fig2 = px.pie(
            names=['High Value', 'Low Value'],
            values=[high_value_pct, low_value_pct],
            title='Percentage of High-Value Transactions',
            color_discrete_sequence=['lightgreen', 'skyblue']
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('### Bar Plot: Frequency of Shipping Methods')
    shipping_counts = filtered_df['Shipping_Method'].value_counts().reset_index()
    shipping_counts.columns = ['Shipping_Method', 'Count']
    fig3 = px.bar(
        shipping_counts,
        x='Shipping_Method',
        y='Count',
        title='Frequency of Shipping Methods',
        labels={'Shipping_Method': 'Shipping Method', 'Count': 'Count'},
        color='Shipping_Method',
        template='plotly_dark'
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('### Box Plot: Weight Distribution per Product Category')
    fig4 = px.box(
        filtered_df,
        x='Category',
        y='Weight',
        title='Weight Distribution per Product Category',
        labels={'Weight': 'Weight', 'Category': 'Product Category'},
        points='all',
        color='Category'
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('### Line Plot: Monthly Transaction Trends')
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').dt.to_timestamp()
    monthly_avg_value = filtered_df.groupby(['Month', 'Import_Export'])['Value'].mean().reset_index()
    fig5 = px.line(
        monthly_avg_value,
        x='Month',
        y='Value',
        color='Import_Export',
        title='Average Value of Transactions by Month',
        markers=True,
        labels={'Value': 'Average Transaction Value', 'Month': 'Month'}
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown('### Interactive Bar Chart: Frequency of Shipping Methods')
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
