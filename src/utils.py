import pandas as pd
import altair as alt
import streamlit as st

states_mapping = {
	'AK': 'Alaska',
	'AL': 'Alabama',
	'AR': 'Arkansas',
	'AS': 'American Samoa',
	'AZ': 'Arizona',
	'CA': 'California',
	'CO': 'Colorado',
	'CT': 'Connecticut',
	'DC': 'District of Columbia',
	'DE': 'Delaware',
	'FL': 'Florida',
	'GA': 'Georgia',
	'GU': 'Guam',
	'HI': 'Hawaii',
	'IA': 'Iowa',
	'ID': 'Idaho',
	'IL': 'Illinois',
	'IN': 'Indiana',
	'KS': 'Kansas',
	'KY': 'Kentucky',
	'LA': 'Louisiana',
	'MA': 'Massachusetts',
	'MD': 'Maryland',
	'ME': 'Maine',
	'MI': 'Michigan',
	'MN': 'Minnesota',
	'MO': 'Missouri',
	'MP': 'Northern Mariana Islands',
	'MS': 'Mississippi',
	'MT': 'Montana',
	'NA': 'National',
	'NC': 'North Carolina',
	'ND': 'North Dakota',
	'NE': 'Nebraska',
	'NH': 'New Hampshire',
	'NJ': 'New Jersey',
	'NM': 'New Mexico',
	'NV': 'Nevada',
	'NY': 'New York',
	'OH': 'Ohio',
	'OK': 'Oklahoma',
	'OR': 'Oregon',
	'PA': 'Pennsylvania',
	'PR': 'Puerto Rico',
	'RI': 'Rhode Island',
	'SC': 'South Carolina',
	'SD': 'South Dakota',
	'TN': 'Tennessee',
	'TX': 'Texas',
	'UT': 'Utah',
	'VA': 'Virginia',
	'VI': 'Virgin Islands',
	'VT': 'Vermont',
	'WA': 'Washington',
	'WI': 'Wisconsin',
	'WV': 'West Virginia',
	'WY': 'Wyoming'
}

def get_data():
	# get data
	yelpb_url = "https://media.githubusercontent.com/media/SteinsGate9/05-839-a2/main/data/business.json"
	business = pd.read_json(yelpb_url, lines=True)

	# get other attributes
	from collections import defaultdict
	q_attributes = ["stars", "review_count"]
	attributes = ["RestaurantsTableService", "BikeParking", "WiFi",
				  "BusinessAcceptsCreditCards", "RestaurantsReservations", "WheelchairAccessible",
				  "Caters", "OutdoorSeating", "RestaurantsGoodForGroups", "BusinessAcceptsBitcoin"]

	after_attributes = [ "mean_stars", "mean_review_count", "mean_is_open",
						 "mean_RestaurantsTableService", "mean_BikeParking", "mean_WiFi",
						 "mean_BusinessAcceptsCreditCards", "mean_RestaurantsReservations",
						 "mean_WheelchairAccessible", "mean_Caters", "mean_OutdoorSeating",
						 "mean_RestaurantsGoodForGroups", "mean_BusinessAcceptsBitcoin",
						 "max_stars", "max_review_count",
						 "min_stars", "min_review_count"]

	def collect(groupbys):
		# all methods
		attri_whole = defaultdict(int)
		methods = ["max", "min"]
		for m in methods:
			for a in q_attributes:
				if m == "max":
					attri_whole[f"{m}_{a}"] = -1
				else:
					attri_whole[f"{m}_{a}"] = 1e9

		# mean(stars), mean(review count), mean(is_open), means(other attributes
		for index, row in groupbys.iterrows():
			# simple attributes
			attri_whole["mean_stars"] += row['stars']
			attri_whole["mean_review_count"] += row['review_count']
			attri_whole["mean_is_open"] += row['is_open']

			attri_whole["max_stars"] = row["stars"] if row["stars"] > attri_whole["max_stars"] else attri_whole["max_stars"]
			attri_whole["max_review_count"] = row["review_count"] if row["review_count"] > attri_whole["max_review_count"] else attri_whole["max_review_count"]

			attri_whole["min_stars"] = row['stars'] if row["stars"] < attri_whole["min_stars"] else attri_whole["min_stars"]
			attri_whole["min_review_count"] = row['review_count'] if row["review_count"] < attri_whole["min_review_count"] else attri_whole["min_review_count"]


			# other attributes
			attri = row['attributes']
			if attri:
				for k, v in attri.items():
					if k in attributes:
						if k == "WiFi":
							if not (v == "'no'" or v == "u'no'"):
								attri_whole[f"mean_{k}"] += 1
						else:
							if v == 'True':
								attri_whole[f"mean_{k}"] += 1


		count = groupbys.shape[0]
		dic = dict(attri_whole)
		lis = []
		for a in after_attributes:
			if a in dic.keys():
				if a.startswith("mean"):
					lis.append(dic[a] / count)
				else:
					lis.append(dic[a])
			else:
				lis.append(0)

		return pd.Series(lis)

	# change state ABBR -> state full name
	def to_full(abbr):
		if abbr in states_mapping:
			return states_mapping[abbr]
		else:
			return None
	business.state = business.state.apply(to_full)
	business = business[business.state.notnull()]

	# get county from zipcode
	from uszipcode import SearchEngine
	search = SearchEngine() # set simple_zipcode=False to use rich info database
	def EOQ(idd):
		zipcode = search.by_zipcode(str(idd))
		if zipcode:
			return zipcode.to_dict()["county"]
		else:
			return None
	business['county'] = business.apply(lambda row: EOQ(row["postal_code"]), axis=1)

	# change state ABBR -> state full name
	def to_abbr(abbr):
		if abbr:
			return abbr.split(" County")[0]
		else:
			return None
	business.county = business.county.apply(to_abbr)
	business = business[business.county.notnull()]

	# get state average
	business_state = business.groupby("state").apply(collect)
	business_state.columns = after_attributes
	business_state["state"] = business_state.index

	# get county average
	business_county = business.groupby("county").apply(collect)
	business_county.columns = after_attributes
	business_county["county"] = business_county.index


	# review data
	yelpr_url = "../data/review.csv"
	review = pd.read_csv(yelpr_url)

	# get view joined data
	def collect(groupbys):
		return groupbys.iloc[:10]
	business_state_forshow = business.groupby("state").apply(collect)
	business_state_forshow = business_state_forshow.reset_index(level=0, drop=True)
	business_state_forshow = business_state_forshow.merge(review, on="business_id", how='left' )

	def collect(groupbys):
		return groupbys.iloc[:10]
	business_county_forshow = business.groupby("county").apply(collect)
	business_county_forshow = business_county_forshow.reset_index(level=0, drop=True)
	business_county_forshow = business_county_forshow.merge(review, on="business_id", how='left' )

	return business_state, business_county, business_state_forshow, business_county_forshow

@st.cache
def get_data_precalculated():
	business_state = pd.read_csv("https://media.githubusercontent.com/media/SteinsGate9/assignemnt2/master/data/business_state.csv")
	business_county = pd.read_csv("https://media.githubusercontent.com/media/SteinsGate9/assignemnt2/master/data/business_county.csv")
	business_state_forshow = pd.read_csv("https://media.githubusercontent.com/media/SteinsGate9/assignemnt2/master/data/business_state_forshow.csv")
	business_county_forshow = pd.read_csv("https://media.githubusercontent.com/media/SteinsGate9/assignemnt2/master/data/business_county_forshow.csv")

	return business_state, business_county, business_state_forshow, business_county_forshow

business_state, business_county, business_state_forshow, business_county_forshow = get_data_precalculated()



def generate_regions_choropleth(
	feature: str,
	method: str,
	width: int = 700,
	height: int = 500,
	is_states: bool = True,
) -> alt.Chart:

	# shape of states
	if is_states:
		property_title = "state"
		property_name = "name"
		lookup_from = "state"

		states = alt.topo_feature(
			"https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json",
			"states",
		)
		data = business_state
	else:
		property_title = "county"
		property_name = "name"
		lookup_from = "county"

		states = alt.topo_feature(
			"https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json",
			"counties",
		)
		data = business_county

	# display method
	display_method = "%" if feature not in ["stars", "review_count"] else ""

	# selection & charts
	hover = alt.selection_single(on='mouseover', fields=['id'], empty='none')
	base_chart = (
		alt.Chart(states)
			.mark_geoshape(stroke="black", strokeWidth=0.5, color="white")
			.encode(tooltip=[alt.Tooltip(f"properties.name:N", title="asd")])
	)

	new_chart = (
		alt.Chart(states
				  ).mark_geoshape(stroke="black", strokeWidth=0.5
								  ).encode(
			color=alt.condition(hover, alt.value('red'),
								alt.Color(
									f"{method}_{feature}:Q",
									title=f"{method} of {feature}{display_method}",
									legend=alt.Legend(labelLimit=50),
								)),
			tooltip=[
				alt.Tooltip(f"properties.{property_name}:N", title=f"{property_title}"),
				alt.Tooltip(f"{method}_{feature}:Q", title=f"{method} of {feature}{display_method}", format=".2~f"),
			],
		).transform_lookup(
			lookup=f"properties.{property_name}",
			from_=alt.LookupData(data, f"{lookup_from}", [f"{method}_{feature}"])
		).project('albersUsa'
				  ).add_selection(hover
		)
	)

	# final
	final_chart = (
		(base_chart + new_chart)
			.configure_view(strokeWidth=0)
			.properties(width=width, height=height)
	)

	return final_chart


def generate_trajectory_chart(
	feature: str,
	method: str,
	is_states: bool,
	padding: int = 5,
	width: int = 500,
	height: int = 500,
):
	# shape of states
	if is_states:
		property_title = "state"
		property_name = "name"
		data = business_state
		data_forshow = business_state_forshow
	else:
		property_title = "county"
		property_name = "name"
		data = business_county
		data_forshow = business_county_forshow

	# display method
	display_method = "%" if feature not in ["stars", "review_count"] else ""

	# bar chart
	hover = alt.selection_single(on='mouseover', fields=[f'{property_title}'], nearest=True)
	highlight = alt.selection_single()
	click = alt.selection_single(on='mousedown', fields=[f'{property_title}'])

	bar_chart = alt.Chart(data).mark_bar().encode(
		x=f'{method}_{feature}:Q',
		y=alt.Y(f'{property_title}:N', sort='-x'),
		color=alt.condition(highlight, alt.value('red'), alt.value('lightgray')),
		opacity=alt.condition(hover, alt.value(1.0), alt.value(0.3)),
		tooltip=[
			alt.Tooltip(f"{property_title}:N", title=f"{property_title}"),
			alt.Tooltip(f"{method}_{feature}:Q", title=f"{method} of {feature}{display_method}", format=".2~f"),
		],
	).properties(
		height=height,
		width=width - 250
	).add_selection(hover, click, highlight
					).interactive()


	hist_chart = alt.Chart(business_state_forshow).mark_point().encode(
		y='stars_x:Q',
		x='name:N',
		tooltip=[
			alt.Tooltip(f"name:N", title=f"name"),
			alt.Tooltip(f"text:N", title=f"review"),
			alt.Tooltip(f"date:N", title=f"date"),
		],
	).properties(
		height=height,
		width=250
	).transform_filter(click).interactive()

	# review chart
	final_chart = (
		(bar_chart | hist_chart)
	)

	return final_chart
