import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Call Centre Complaints Dashboard", layout="wide")

# Load the Excel file
file_path = 'Call Centre Data.xlsx'  # Update the path if necessary

# Load data from each sheet
call_centre_data = pd.read_excel(file_path, sheet_name='Call Centre')
districts_complaints_data = pd.read_excel(file_path, sheet_name='Districts Complaints ')
regions_districts_data = pd.read_excel(file_path, sheet_name='Regions & Districts')

# Clean and prepare the Call Centre data
call_centre_data_cleaned = call_centre_data[['Date', 'Region', 'Complaint Type', 'number']].dropna()
call_centre_data_cleaned['Date'] = pd.to_datetime(call_centre_data_cleaned['Date'])

# Clean and prepare the Districts Complaints data
districts_complaints_data_cleaned = districts_complaints_data[['Date', 'District', 'Complaint Type', 'Number']].dropna()
districts_complaints_data_cleaned['Date'] = pd.to_datetime(districts_complaints_data_cleaned['Date'])

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Region Analysis", "Complaint Types", "District Analysis", "User Engagement"])

if page == "Home":
    # Title of the dashboard
    st.title("📞 Call Centre Complaints Dashboard")

    # Complaint Trends Over Time
    st.header("📅 Complaint Trends Over Time")
    complaint_trends = call_centre_data_cleaned.groupby('Date')['number'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(complaint_trends['Date'], complaint_trends['number'], marker='o', linestyle='-')
    ax.set_title('Total Complaints Over Time', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Complaints')
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

elif page == "Region Analysis":
    # Complaint Distribution by Region
    st.title("📍 Region Analysis")
    st.header("📍 Complaint Distribution by Region")
    complaints_by_region = call_centre_data_cleaned.groupby('Region')['number'].sum().reset_index().sort_values('number', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(complaints_by_region['Region'], complaints_by_region['number'], color='skyblue')
    ax.set_title('Total Complaints by Region', fontsize=16)
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Complaints')
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # Heatmap of complaints by Region and Date
    st.header("📅 Heatmap of Complaints by Region and Date")
    region_date_pivot = call_centre_data_cleaned.pivot_table(values='number', index='Region', columns='Date', aggfunc='sum', fill_value=0)
    st.dataframe(region_date_pivot)

elif page == "Complaint Types":
    # Top Complaint Types
    st.title("📊 Complaint Types")
    st.header("📊 Top Complaint Types")
    complaints_by_type = call_centre_data_cleaned.groupby('Complaint Type')['number'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(complaints_by_type['number'], labels=complaints_by_type['Complaint Type'], autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Complaint Types', fontsize=16)
    st.pyplot(fig)

    # Bar chart of Complaint Types
    st.header("📈 Bar Chart of Complaint Types")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(complaints_by_type['Complaint Type'], complaints_by_type['number'], color='orange')
    ax.set_title('Complaint Types Count', fontsize=16)
    ax.set_xlabel('Complaint Type')
    ax.set_ylabel('Number of Complaints')
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

elif page == "District Analysis":
    # District-Level Complaints
    st.title("📋 District Analysis")
    st.header("📋 District-Level Complaints")
    st.dataframe(districts_complaints_data_cleaned)  # Display interactive table of district complaints

    # Complaint Trends by District
    st.header("📅 Complaint Trends by District")
    district_trends = districts_complaints_data_cleaned.groupby(['Date', 'District'])['Number'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    for district in district_trends['District'].unique():
        district_data = district_trends[district_trends['District'] == district]
        ax.plot(district_data['Date'], district_data['Number'], marker='o', linestyle='-', label=district)
    ax.set_title('Complaint Trends by District', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Complaints')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

elif page == "User Engagement":
    # User Engagement Analysis
    st.title("📈 User Engagement Trends")

    # Engagement over Time
    st.header("📅 Engagement Over Time")
    user_engagement_trends = call_centre_data_cleaned.groupby('Date')['number'].count().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(user_engagement_trends['Date'], user_engagement_trends['number'], marker='o', linestyle='-')
    ax.set_title('User Engagement Over Time', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Interactions')
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

    # Engagement by Region
    st.header("📍 Engagement by Region")
    engagement_by_region = call_centre_data_cleaned.groupby('Region')['number'].count().reset_index().sort_values('number', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(engagement_by_region['Region'], engagement_by_region['number'], color='purple')
    ax.set_title('User Engagement by Region', fontsize=16)
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Interactions')
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

# End of Streamlit app
