import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UK Government anti-social behaviour order (ASBO)")
st.write("This application will visualise & display ASBO data for analysis and deeper understanding of the dataset")

# Load dataset from /data folder
data_asbo_issued = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-issued-0113.csv', encoding='ISO-8859-1')  
data_asbo_breached = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-breaches-0113.csv', encoding='ISO-8859-1')  

# Create table overview
st.subheader("Data Overview")
st.write("Issued ASBOs dataset overview:")
st.dataframe(data_asbo_issued.head())
st.write("Breached ASBOs dataset overview:")
st.dataframe(data_asbo_breached.head())
st.divider()

# Plot Overview
st.subheader("ASBOs Issued Over Years")
fig, ax = plt.subplots()
ax.bar(data_asbo_issued['Year of Issue'], data_asbo_issued['ASBOs issued'], color='skyblue')
ax.set_xlabel("Year of Issue")
ax.set_ylabel("ASBOs Issued")
ax.set_title("ASBOs Issued Over Years")
st.pyplot(fig)

st.subheader("ASBOs Breached Over Years")
fig, ax = plt.subplots()
ax.bar(data_asbo_breached['Year of Breach'], data_asbo_breached['ASBOs_breached'], color='skyblue')
ax.set_xlabel("Year of Breach")
ax.set_ylabel("ASBOs Breach")
ax.set_title("ASBOs Breached Over Years")
st.pyplot(fig)
st.divider()

# Collect the required data
st.subheader("Breaches by Gender with Court")
court_gender_data = data_asbo_issued.groupby(['Court', 'Sex'])['ASBOs issued'].sum().unstack(fill_value=0)
court_gender_data['Total'] = court_gender_data.sum(axis=1)  # Add a total for each court
court_gender_data = court_gender_data.reset_index() # Make 'Court' a regular column

# Create the radio button
st.subheader("Filter by Gender")
gender_filter = st.radio(
    "Select Gender",
    options=["Both", "Male", "Female"],
    horizontal=True,
)

# Apply the radio button gender filter on the dataset 
if gender_filter == "Male":
    filtered_data = court_gender_data[['Court', 'Male']]  # Only show 'Court' and 'Male'
elif gender_filter == "Female":
    filtered_data = court_gender_data[['Court', 'Female']] # Only show 'Court' and 'Female'
else:
    filtered_data = court_gender_data # Show all

# Show the filtered data table.
st.write("Data used for the court representation (aggregated by Gender):")
st.dataframe(filtered_data)