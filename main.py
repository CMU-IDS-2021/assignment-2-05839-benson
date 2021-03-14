import streamlit as st
import altair as alt
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import json 
from gettext import translation, NullTranslations
from typing import Dict, Callable
from src.trajectory import trajectory_cases
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
        
#part 1
st.header("Part 1: Yelp Businesses Across States")
st.write("We broke down the raw data from Yelp to understand the classification of each business based on the state.")
st.markdown("First, let's determine: what kind of business categories can we find in each state?")
states = list(yelp_dataset_df.groupby(["state"]).count().sort_values(by="categories", ascending=False).head(15).index)

state = st.selectbox("Choose a state from Yelp you would like to analyze:", states)

# get rows with selected state
state_categories = yelp_dataset_df.loc[yelp_dataset_df['state'] == state]

# get categories col specifically
state_categories = state_categories['categories']

# get count of categories in cat col
state_categories_counts = state_categories.value_counts().to_dict()

# Trim array to 10 instances to not break altair
categories = [*state_categories]
categories = categories[0:10]

# Get array of counts associated with categories in categories array
categories_counts = [state_categories_counts[x] for x in categories]

# Plot using altair
source = pd.DataFrame({
    'Categories': categories,
    'Count': categories_counts
})

stateBarChart = alt.Chart(source).mark_bar().encode(
    x='Count',
    y='Categories'
)
st.write(stateBarChart) 

# Page choice
st.sidebar.title("Page")
page = st.sidebar.selectbox(
    label="Page",
    options=[
		"Statistical data",
        "Geographical data",
    ],
)
page_function_mapping: Dict[str, Callable[[pd.DataFrame], None]] = {
	"Statistical data": trajectory_cases,
    "Geographical data": choropleth_maps,
}
page_function_mapping[page](None)

# other mark downs
st.sidebar.markdown(
        """
    **Please note**:

    Many of the plots are interactive, you can zoom with scrolling and hover on data points for additional information.
    """
)
