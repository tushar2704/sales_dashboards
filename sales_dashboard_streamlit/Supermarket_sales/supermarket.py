# By Tushar Aggarwal

import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl as op




# Application title and body
st.set_page_config(page_title="Supermarket Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide')



df = pd.read_excel(io="sales_dashboard_streamlit\supermarket_sales\supermarkt_sales.xlsx",
                   engine="openpyxl",
                   sheet_name='Sales',
                   skiprows=3,
                   usecols="B:R",
                   nrows=1000)

#-----Sidebar-----

st.sidebar.header("Please select :")
city= st.sidebar.multiselect(
    "Selected City:",
    options=df['City'].unique(),
    default=df['City'].unique()
)
customer_type= st.sidebar.multiselect(
    "Selected Customer Type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)
gender= st.sidebar.multiselect(
    "Selected Gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City ==@city & Customer_type == @customer_type & Gender == @gender"
)
#-----Mainpage-----
st.title(":bar_chart: Supermarket Sales Dashboard")
st.markdown("### By Tushar Aggarwal")