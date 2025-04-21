import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("UK Government anti-social behaviour order (ASBO)")
st.write("This application will visualise & display ASBO data for analysis and deeper understanding of the dataset")

# Load dataset from /data folder
data_asbo_issued = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-issued-0113.csv', encoding='ISO-8859-1')  
data_asbo_breached = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-breaches-0113.csv', encoding='ISO-8859-1')  

#data_asbo_issued.info()
#data_asbo_breached.info()


# Plot
fig, ax = plt.subplots()
ax.bar(data_asbo_issued['Year of Issue'], data_asbo_issued['ASBOs issued'], color='skyblue')
ax.set_xlabel("Year of Issue")
ax.set_ylabel("ASBOs Issued")
ax.set_title("ASBOs Issued Over Years")
st.pyplot(fig)