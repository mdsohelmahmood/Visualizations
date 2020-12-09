import streamlit as st
import pandas as pd

df = st.cache(pd.read_csv)("iris.csv")
is_check = st.checkbox("Display Data")
if is_check:
    st.write(df)


species = st.sidebar.multiselect("Enter Species", df['Species'].unique())
st.write("Your input Species", species)

variables = st.sidebar.multiselect("Enter the variables", df.columns)
st.write("You selected these variables", variables)

selected_species_data = df[(df['Species'].isin(species))]
Speciess_data = selected_species_data[variables]
Species_data_is_check = st.checkbox("Display the data of selected Speciess")
if Species_data_is_check:
    st.write(Speciess_data)
