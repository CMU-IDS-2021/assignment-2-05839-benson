import streamlit as st
import pandas as pd

from src.utils import generate_trajectory_chart
import altair as alt
from gettext import NullTranslations


def trajectory_cases(data: pd.DataFrame) -> None:
	# ti
	st.header("Part 2: Yelp Statistical Data by Region")

	st.markdown("Next, we took a state and national view to the data to understand the breakdown segmentations of data in Yelp. Select from the slider on the left to switch between views.")

	# states / city
	map_scale = st.radio(
		label="1) What resolution would you like to visualise?",
		options=["state", "county"],
	)
	is_state = map_scale == "state"

	# method
	method = st.selectbox(
		label="2) What method would you like to use to aggregate?",
		options=["mean", "max", "min"],
		index=0
	)

	# indicator
	if method == "mean":
		feature = st.selectbox(
			label="3) What indicator would you like to visualise?",
			options=["stars", "review_count", "is_open", "RestaurantsTableService", "BikeParking", "WiFi",
					 "BusinessAcceptsCreditCards", "RestaurantsReservations", "WheelchairAccessible",
					 "Caters", "OutdoorSeating", "RestaurantsGoodForGroups", "BusinessAcceptsBitcoin"],
			index=0
		)
	else:
		feature = st.selectbox(
			label="3) What indicator would you like to visualise?",
			options=["stars", "review_count"],
			index=0
		)

	# altair
	choropleth1 = generate_trajectory_chart(
		feature, method, is_states=is_state
	)
	st.altair_chart(choropleth1)


def business_by_states(yelp_dataset_df: pd.DataFrame):
	#part 1
	st.header("Part 1: Yelp Businesses Across States")

	st.write("We broke down the raw data from Yelp to understand the classification of each business based on the state.")

	st.markdown("First, let's determine: what kind of business categories can we find in each state?")

	states = list(yelp_dataset_df.groupby(["state"]).count().sort_values(by="categories", ascending=False).head(25).index)

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
