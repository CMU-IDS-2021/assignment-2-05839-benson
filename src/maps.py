import datetime
from gettext import NullTranslations

import pandas as pd
import streamlit as st

from src.utils import (
	generate_regions_choropleth,
)


def choropleth_maps(data: pd.DataFrame) -> None:
	# title
	st.header("Part 3: Yelp Data by Geographical distribution")

	st.markdown("In this analysis, we will break down the data with a national visualization of the user's selected category. Select from the slider on the left to switch between views")

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
	choropleth = generate_regions_choropleth(
		feature, method, is_states=is_state
	)
	st.altair_chart(choropleth)
