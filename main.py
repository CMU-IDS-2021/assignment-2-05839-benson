import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from gettext import translation, NullTranslations
from typing import Dict, Callable
from src.trajectory import trajectory_cases, business_by_states
from src.maps import choropleth_maps

st.title("Yelp Data Analysis 📊")
st.markdown("By Shicheng Huang and Jennifer Park")

st.markdown("In this project, we will take you through an exploration of Yelp's business data to help visualize the landscape of businesses throughout the United States. We evaluate regional to national data in order to understand the current business landscape across the United States for listed businesses on Yelp.")

#loading the data
yelp_dataset_df = pd.read_csv("./data/yelp-academic-business.zip")

#breaking down the data
st.header("Understanding the Business Yelp Database")

st.markdown("There are multiple unique columns in the Business Yelp dataset including business id, name, categories, reviews, address and latitude / longitude that we used for the analysis.")

st.markdown("We began digging into the types of data available to understand how users may identify the distribution of the types of food across different regions and domains.")
if st.checkbox("Show Raw Dataset", False):
        st.dataframe(yelp_dataset_df.head())

# Page choice
st.sidebar.title("Page")
page = st.sidebar.selectbox(
    label="Page",
    options=[
		"Business Across States",
		"Statistical data Across Region",
        "Geographical data Across Region",
    ],
)
page_function_mapping: Dict[str, Callable[[pd.DataFrame], None]] = {
	"Business Across States": business_by_states,
	"Statistical data Across Region": trajectory_cases,
    "Geographical data Across Region": choropleth_maps,
}
page_function_mapping[page](yelp_dataset_df)

# other mark downs
st.sidebar.markdown(
        """
    **Please note**:

    Many of the plots are interactive, you can zoom with scrolling and hover on data points for additional information.
    """
)
