import streamlit as st
import pandas as pd
from gettext import translation, NullTranslations
from typing import Dict, Callable
from src.trajectory import trajectory_cases
from src.maps import choropleth_maps


# Translate dataframe to given language
# Features are derived directly from dataframe columns, following the tidy format of dataframes
# data.loc[:, :] = dataframe_translator(data, lang)

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

    All line plots are interactive, you can zoom with scrolling and hover on data points for additional information.
    """
)




