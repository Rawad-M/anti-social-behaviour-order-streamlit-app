import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset from /data folder
@st.cache_data
def load_data():
    data_asbo_issued = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-issued-0113.csv', encoding='ISO-8859-1')  
    data_asbo_breached = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-breaches-0113.csv', encoding='ISO-8859-1')  
    return data_asbo_issued, data_asbo_breached

data_asbo_issued, data_asbo_breached = load_data()

st.title("UK Government anti-social behaviour order (ASBO)")
st.write("This application will visualise & display ASBO data for analysis and deeper understanding of the dataset")


# Create table overview
@st.cache_data
def display_head_info(data_asbo_issued, data_asbo_breached):
  st.subheader("Data Overview")
  st.write("Issued ASBOs dataset overview:")
  st.dataframe(data_asbo_issued.head())
  st.write("Breached ASBOs dataset overview:")
  st.dataframe(data_asbo_breached.head())
  st.divider()

display_head_info(data_asbo_issued, data_asbo_breached)

# Plot Overview
@st.cache_data
def plot_asbos_issued(data_asbo_issued):
  st.subheader("ASBOs Issued Over Years")
  fig, ax = plt.subplots()
  ax.bar(data_asbo_issued['Year of Issue'], data_asbo_issued['ASBOs issued'], color='skyblue')
  ax.set_xlabel("Year of Issue")
  ax.set_ylabel("ASBOs Issued")
  ax.set_title("ASBOs Issued Over Years")
  st.pyplot(fig)

plot_asbos_issued(data_asbo_issued)

@st.cache_data
def plot_asbos_breached(data_asbo_breached):
  st.subheader("ASBOs Breached Over Years")
  fig, ax = plt.subplots()
  ax.bar(data_asbo_breached['Year of Breach'], data_asbo_breached['ASBOs_breached'], color='skyblue')
  ax.set_xlabel("Year of Breach")
  ax.set_ylabel("ASBOs Breach")
  ax.set_title("ASBOs Breached Over Years")
  st.pyplot(fig)
  st.divider()
  
plot_asbos_breached(data_asbo_breached)

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


# Add a text input for filtering by Court
court_data = data_asbo_issued.groupby('Court')['ASBOs issued'].sum().reset_index()
filtered_data = court_data
search_term = st.text_input("Search by Court", "")
if search_term: # Apply the search filter:  case-insensitive search
    filtered_data = filtered_data[filtered_data['Court'].str.contains(search_term, case=False, na=False)]
st.write("Data used for the geographic representation (aggregated by Court):")
st.dataframe(filtered_data)