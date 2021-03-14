import streamlit as st
import pandas as pd

from src.utils import generate_trajectory_chart

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
