import streamlit as st
import pandas as pd
from gettext import translation, NullTranslations
from typing import Dict, Callable
from trajectory import trajectory_cases
from maps import choropleth_maps



# language == "English" is the default
lang = translation("messages", localedir="locale", languages=["en_GB"])
lang.install()
_ = lang.gettext

# Translate dataframe to given language
# Features are derived directly from dataframe columns, following the tidy format of dataframes
# data.loc[:, :] = dataframe_translator(data, lang)

# Page choice
st.sidebar.title(_("Page"))
page = st.sidebar.selectbox(
    label=_("Page"),
    options=[
		_("Statistical data"),
        _("Geographical data"),
    ],
)
page_function_mapping: Dict[str, Callable[[pd.DataFrame, NullTranslations], None]] = {
	_("Statistical data"): trajectory_cases,
    _("Geographical data"): choropleth_maps,
}
page_function_mapping[page](None, lang)

# other mark downs
st.sidebar.markdown(
    _(
        """
    **Please note**:

    All line plots are interactive, you can zoom with scrolling and hover on data points for additional information.
    """
    )
)




