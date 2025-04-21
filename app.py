import streamlit as st
import pandas as pd

st.title("UK Government anti-social behaviour order (ASBO)")
st.write("This application will visualise & display ASBO data for analysis and deeper understanding of the dataset")


# Load dataset from /data folder
data_asbo_issued = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-issued-0113.csv', encoding='ISO-8859-1')  
data_asbo_breached = pd.read_csv('data/anti-social-behaviour-order-statistics-court-level-breaches-0113.csv', encoding='ISO-8859-1')  


data_asbo_issued.info()
data_asbo_breached.info()