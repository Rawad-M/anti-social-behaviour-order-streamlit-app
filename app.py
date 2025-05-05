import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

#################################
# Load dataset from /data folder
#################################
@st.cache_data
def load_data():
    data_asbo_issued = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-issued-0113.csv', encoding='ISO-8859-1')  
    data_asbo_breached = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-breaches-0113.csv', encoding='ISO-8859-1')  
    return data_asbo_issued, data_asbo_breached

data_asbo_issued, data_asbo_breached = load_data()

st.title("UK Government anti-social behaviour order (ASBO)")
st.write("This application will visualise & display ASBO data for analysis and deeper understanding of the dataset")

#################################
# Create tables overview
#################################
@st.cache_data
def display_head_info(data_asbo_issued, data_asbo_breached):
  st.subheader("Data Overview")
  st.write("Issued ASBOs dataset overview:")
  st.dataframe(data_asbo_issued.head())
  st.write("Breached ASBOs dataset overview:")
  st.dataframe(data_asbo_breached.head())
  st.divider()

display_head_info(data_asbo_issued, data_asbo_breached)

#################################
# Plot Overview
#################################
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

#####################################
# Add Gender Filter for ASBOs Issued
#####################################
@st.cache_data
def create_issued_gender_filter(data_asbo_issued):
  # Collect the required data
  st.subheader("Breaches by Gender with Court")
  court_gender_data = data_asbo_issued.groupby(['Court', 'Sex'])['ASBOs issued'].sum().unstack(fill_value=0)
  court_gender_data['Total'] = court_gender_data.sum(axis=1)  # Add a total for each court
  court_gender_data = court_gender_data.reset_index() # Make 'Court' a regular column
  return court_gender_data

court_gender_data = create_issued_gender_filter(data_asbo_issued)

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
st.divider()

#################################
# Add Search Filter
#################################
st.subheader("Search by Court")

@st.cache_data
def asbos_issued_by_court(data_asbo_issued):
  # Add a text input for filtering by Court
  court_data = data_asbo_issued.groupby('Court')['ASBOs issued'].sum().reset_index()
  return court_data

filtered_issued_asbos = asbos_issued_by_court(data_asbo_issued)

issued_search_term = st.text_input("Search ASBOs 'issued' by Court", "")
if issued_search_term: # Apply the case-insensitive search filter
    filtered_issued_asbos = filtered_issued_asbos[filtered_issued_asbos['Court'].str.contains(issued_search_term, case=False, na=False)]
    
    for index, row in filtered_issued_asbos.iterrows():
      with st.expander(f"{row['Court']} - {row['ASBOs issued']} ASBOs"):
          # Show all records for this court from original data
          court_details = data_asbo_issued[data_asbo_issued['Court'] == row['Court']]
          st.dataframe(court_details)

st.dataframe(filtered_issued_asbos)

#####
@st.cache_data
def asbos_breached_by_court(data_asbo_breached):
  # Add a text input for filtering by Court
  court_data = data_asbo_breached.groupby('Court_breach')['ASBOs_breached'].sum().reset_index()
  return court_data

filtered_breached_asbos = asbos_breached_by_court(data_asbo_breached)

breached_search_term = st.text_input("Search ASBOs 'breached' by Court", "")
if breached_search_term: # Apply the case-insensitive search filter
    filtered_breached_asbos = filtered_breached_asbos[filtered_breached_asbos['Court_breach'].str.contains(breached_search_term, case=False, na=False)]
    
    for index, row in filtered_breached_asbos.iterrows():
      with st.expander(f"{row['Court_breach']} - {row['ASBOs_breached']} ASBOs"):
          # Show all records for this court from original data
          court_details = data_asbo_breached[data_asbo_breached['Court_breach'] == row['Court_breach']]
          st.dataframe(court_details)

st.dataframe(filtered_breached_asbos)
st.divider()

#################################
# ASBOs Breached Data Explorer
#################################
st.title("ASBOs Breached Data Explorer")
df_breached = data_asbo_breached;

# Dropdowns
years = df_breached['Year of Breach'].dropna().unique()
age_groups = df_breached['Age group breach 2'].dropna().unique()

selected_year = st.selectbox("Select Year of Breach", sorted(years))
selected_age_group = st.selectbox("Select Age Group", sorted(age_groups))

# Radio for Sex with mapping
sex_choice = st.radio("Breached Select Sex", ['Male', 'Female', 'Both'])
sex_map = {
    'Male': [1],
    'Female': [2],
    'Both': [1, 2, 9]
}

# Slider for ASBOs_breached
min_breach = int(df_breached['ASBOs_breached'].min())
max_breach = int(df_breached['ASBOs_breached'].max())
selected_breach = st.slider("Select ASBOs Breached", min_breach, max_breach, (min_breach, max_breach))

# Filter data
filtered_df_breached = df_breached[
    (df_breached['Year of Breach'] == selected_year) &
    (df_breached['Age group breach 2'] == selected_age_group) &
    (df_breached['Sex'].isin(sex_map[sex_choice])) &
    (df_breached['ASBOs_breached'].between(*selected_breach))
]

st.write(f"Filtered Results ({len(filtered_df_breached)} rows):")
st.dataframe(filtered_df_breached)
st.divider()

#################################
# ASBOs Issued Data Explorer
#################################
st.title("ASBO Issued Data Explorer")
df = data_asbo_issued

# Dropdown for Year of Issue
issued_years = df['Year of Issue'].dropna().unique()
issued_selected_year = st.selectbox("Select Year of Issue", sorted(issued_years))

# Radio for Sex 
issued_sex_choice = st.radio("Select Sex", ['Male', 'Female', 'Both'])
issued_sex_map = {
    'Male': ['Male'],
    'Female': ['Female'],
    'Both': ['Male', 'Female']
}

# Radio for "Asbo on application or conviction"
asbo_type_options = df['Asbo on application or conviction'].dropna().unique()
selected_asbo_type = st.radio("ASBO on Application or Conviction", asbo_type_options)

# Radio for Age Group
age_group_options = df['Age_Group'].dropna().unique()
issued_selected_age_group = st.radio("Select Age Group", age_group_options)

# Slider for ASBOs issued
min_issued = int(df['ASBOs issued'].min())
max_issued = int(df['ASBOs issued'].max())
selected_issued = st.slider("Select ASBOs Issued", min_issued, max_issued, (min_issued, max_issued))

# Filter data
issued_filtered_df = df[
    (df['Year of Issue'] == issued_selected_year) &
    (df['Sex'].isin(issued_sex_map[issued_sex_choice])) &
    (df['Asbo on application or conviction'] == selected_asbo_type) &
    (df['Age_Group'] == issued_selected_age_group) &
    (df['ASBOs issued'].between(*selected_issued))
]

st.write(f"Filtered Results ({len(issued_filtered_df)} rows):")
st.dataframe(issued_filtered_df)