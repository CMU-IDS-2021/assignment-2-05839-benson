import altair as alt
from vega_datasets import data
cars = data.cars()

highlight = alt.selection_single()
select = alt.selection_single(encodings=['x', 'y'])

chart = alt.Chart(cars).mark_rect().encode(
	x=alt.X('Miles_per_Gallon', bin=True),
	y=alt.X('Horsepower', bin=True),
	color=alt.condition(highlight, 'count()', alt.value('lightgray'))
).add_selection(
	highlight, select
)

hist = alt.Chart(cars).mark_bar().encode(
	y='count()',
	x='Origin'
).transform_filter(select)

chart | hist
