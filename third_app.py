import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


st.title('Sales dashboard Company Name')

df1 = st.cache(pd.read_excel)("Sales Data.xlsx", sheet_name='Sales Data')
is_check = st.checkbox("Display Sales Data")
if is_check:
    st.write(df1)

df2 = st.cache(pd.read_excel)("Sales Data.xlsx", sheet_name='Product Master')
is_check = st.checkbox("Display Product Data")
if is_check:
    st.write(df2)

df3 = st.cache(pd.read_excel)("Sales Data.xlsx", sheet_name='Emp Master')
is_check = st.checkbox("Display Employee Data")
if is_check:
    st.write(df3)



def create_barplot(df6,rev_count2):
    st.header("Revenue in Barplot by products")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rev_count2=df6.groupby(['Product ID']).sum()['Revenue']

    if rev_count2.empty==0:
        ax.bar(
            rev_count2.nlargest(rev_count2.shape[0]).index, \
            rev_count2.nlargest(rev_count2.shape[0])
        )
        plt.xticks(rotation=90)
        st.write(fig)
    if rev_count2.empty==1:
        st.subheader('No revenue earned')



#create sidebar
st.sidebar.title("Filter data")

productid_list = st.sidebar.multiselect("Select Product ID", df1['Product ID'].unique())
empid_list = st.sidebar.multiselect("Select Employee ID", df3['EMP ID'].unique())
supervisor_list = st.sidebar.multiselect("Select Supervisor", df3['Supervisor'].unique())


df4 = pd.merge(df1,df2, on ='Product ID', how ='inner')
df4['Revenue']=df4['Unit Sold']*df4['Price per unit']
df5 = pd.merge(df4,df3, on ='EMP ID', how ='inner')

df5=df5.sort_values(by='Date')
df5=df5.reset_index(drop=True)
df5['Date'] = pd.to_datetime(df5['Date'], errors='coerce').dt.date

start_date=df5['Date'][0]
end_date=df5['Date'][len(df5['Date'])-1]
start_date = st.sidebar.date_input('Start date', start_date)
end_date = st.sidebar.date_input('End date', end_date)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')


df_filtered=df5
plot=1
if productid_list!=[]:
    df_filtered = df_filtered[(df_filtered['Product ID'].isin(productid_list))]
    df6=df_filtered
    rev_count2 = df6.groupby(['Product ID']).sum()['Revenue']
    create_barplot(df6, rev_count2)
    plot=0
if empid_list!=[]:
    df_filtered = df_filtered[(df_filtered['EMP ID'].isin(empid_list))]
    df6 = df_filtered
    rev_count2 = df6.groupby(['EMP ID']).sum()['Revenue']
    create_barplot(df6, rev_count2)
    plot=0
if supervisor_list!=[]:
    df_filtered = df_filtered[(df_filtered['Supervisor'].isin(supervisor_list))]
    df6 = df_filtered

if start_date!=[] and end_date!=[]:
    start_date=start_date
    end_date=end_date
    start_index = df_filtered[df_filtered['Date'] == start_date].index.tolist()[0]
    end_index = df_filtered[df_filtered['Date'] == end_date].index.tolist()[0]
    df_filtered=df_filtered[start_index:end_index]


df6=pd.DataFrame()
is_check = st.sidebar.checkbox("Apply Filter")
df6=df5
check=0
if is_check:
    check=1
    df6=df_filtered
    st.sidebar.subheader('Filter applied')

def create_barplot(df6,rev_count2):
    st.header("Revenue in Barplot by products")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rev_count2=df6.groupby(['Product ID']).sum()['Revenue']

    if rev_count2.empty==0:
        ax.bar(
            rev_count2.nlargest(rev_count2.shape[0]).index, \
            rev_count2.nlargest(rev_count2.shape[0])
        )
        plt.xticks(rotation=90)
        st.write(fig)
    if rev_count2.empty==1:
        st.subheader('No revenue earned')

def create_piechart(df6,rev_count1,check):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    rev_count1=df6.groupby(['Supervisor']).sum()['Revenue']

    # check
    if check == 0:
        labels = df3['Supervisor'].unique()
    if check == 1:
        labels = supervisor_list
        if supervisor_list==[]:
            labels=df3['Supervisor'].unique()

    st.header("Revenue in Piechart by supervisor")
    if rev_count1.empty==0:
        ax.pie(
            rev_count1,
            labels=labels,
            autopct='%1.1f%%',
            shadow=1,
            startangle=90
        )
        st.write(fig)
    if rev_count1.empty==1:
        st.subheader('No revenue earned')

def create_trend(df3,rev_count3):
    st.header("Revenue over Time")
    fig = plt.figure()
    rev_count3=df6.groupby(['Date']).sum()['Revenue']
    if rev_count3.empty==0:
        plt.plot(rev_count3.index,rev_count3)
        plt.xticks(rotation=90)
        st.write(fig)
    if rev_count3.empty==1:
        st.subheader('No revenue earned')


if plot==1:
    rev_count1=df6.groupby(['Supervisor']).sum()['Revenue']
    rev_count2=df6.groupby(['Product ID']).sum()['Revenue']
    rev_count3=df6.groupby(['Date']).sum()['Revenue']

    create_barplot(df6,rev_count2)
    create_piechart(df6,rev_count1,check)
    create_trend(df3,rev_count3)

st.subheader('Total Revenue = ')
rev = st.empty()
rev.text(df6['Revenue'].sum())









