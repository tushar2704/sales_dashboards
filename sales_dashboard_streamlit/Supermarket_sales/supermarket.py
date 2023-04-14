# By Tushar Aggarwal

import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl as op




# Application title and body
st.set_page_config(page_title="Supermarket Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide')


@st.cache_data
def get_df():

    df = pd.read_excel(io="sales_dashboard_streamlit\supermarket_sales\supermarkt_sales.xlsx",
                   engine="openpyxl",
                   sheet_name='Sales',
                   skiprows=3,
                   usecols="B:R",
                   nrows=1000)
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
# Adding "hour" column
    

df = get_df()
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

# Top KPI's
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(),1)
star_rating =":star:"* int(round(average_rating,0))
average_sale_by_transaction = round(df_selection['Total'].mean(),2)

left, middle, right =st.columns(3)

with left:
    st.subheader("Total Sales: ")
    st.subheader(f"US $ {total_sales:,}")

with middle:
    st.subheader("Average Rating: ")
    st.subheader(f"{average_rating} {star_rating}")

with right:
    st.subheader("Average Slaes Per Transaction: ")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

# Sales by Product Line(bar chart)
sales_by_product_line =(
    df_selection.groupby(by=['Product line']).sum()[["Total"]].sort_values(by="Total")

)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b> Sales by Product Line</b>",
    color_discrete_sequence=['#0083B8']*len(sales_by_product_line),
    template="plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0)",
    xaxis =(dict(showgrid=False))
)


# Sales by hour bar chart

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left1, right1 = st.columns(2)

left1.plotly_chart(fig_hourly_sales, use_container_width=True)
right1.plotly_chart(fig_product_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)










