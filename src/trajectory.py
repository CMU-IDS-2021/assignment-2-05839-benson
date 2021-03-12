import streamlit as st
import pandas as pd

from utils import generate_trajectory_chart

from gettext import NullTranslations


def trajectory_cases(data: pd.DataFrame, lang: NullTranslations) -> None:
	# language
	_ = lang.gettext

	# ti
	st.markdown(_("# YELP in US - Statistical data"))

	# states / city
	map_scale = st.radio(
		label=_("1) What resolution would you like to visualise?"),
		options=[_("state"), _("county")],
	)
	is_state = map_scale == _("state")

	# method
	method = st.selectbox(
		label=_("2) What method would you like to use to aggregate?"),
		options=["mean", "max", "min"],
		index=0
	)

	# indicator
	if method == "mean":
		feature = st.selectbox(
			label=_("3) What indicator would you like to visualise?"),
			options=["stars", "review_count", "is_open", "RestaurantsTableService", "BikeParking", "WiFi",
					 "BusinessAcceptsCreditCards", "RestaurantsReservations", "WheelchairAccessible",
					 "Caters", "OutdoorSeating", "RestaurantsGoodForGroups", "BusinessAcceptsBitcoin"],
			index=0
		)
	else:
		feature = st.selectbox(
			label=_("3) What indicator would you like to visualise?"),
			options=["stars", "review_count"],
			index=0
		)

	# altair
	choropleth1, choropleth2 = generate_trajectory_chart(
		feature, method, is_states=is_state
	)
	st.altair_chart(choropleth1)
	st.altair_chart(choropleth2)
