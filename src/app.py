import datetime

import hydralit_components as hc
import numpy as np
import streamlit as st

from data.dataset import load_data

if __name__ == "__main__":
    # make it look nice from the start
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # specify the primary menu definition
    menu_data = [
        {"icon": "far fa-copy", "label": "Left End"},
        {"id": "Copy", "icon": "🐙", "label": "Copy"},
        {
            "icon": "fa-solid fa-radar",
            "label": "Dropdown1",
            "submenu": [
                {"id": " subid11", "icon": "fa fa-paperclip", "label": "Sub-item 1"},
                {"id": "subid12", "icon": "💀", "label": "Sub-item 2"},
                {"id": "subid13", "icon": "fa fa-database", "label": "Sub-item 3"},
            ],
        },
        {"icon": "far fa-chart-bar", "label": "Chart"},  # no tooltip message
        {"id": " Crazy return value 💀", "icon": "💀", "label": "Calendar"},
        {
            "icon": "fas fa-tachometer-alt",
            "label": "Dashboard",
            "ttip": "I'm the Dashboard tooltip!",
        },  # can add a tooltip message
        {"icon": "far fa-copy", "label": "Right End"},
        {
            "icon": "fa-solid fa-radar",
            "label": "Dropdown2",
            "submenu": [
                {"label": "Sub-item 1", "icon": "fa fa-meh"},
                {"label": "Sub-item 2"},
                {
                    "icon": "🙉",
                    "label": "Sub-item 3",
                },
            ],
        },
    ]

    over_theme = {"txc_inactive": "#FFFFFF"}

    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name="Home",
        login_name="Logout",
        hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
        sticky_nav=True,  # at the top or not
        sticky_mode="pinned",  # jumpy or not-jumpy, but sticky or pinned
    )

    if menu_id == "Copy":
        DATE_COLUMN = "date/time"

        st.title("Uber pickups in NYC")
        data_load_state = st.text("Loading data...")
        data = load_data(10000)
        data_load_state.text("Done! (using st.cache)")

        if st.checkbox("Show raw data"):
            st.subheader("Raw data")
            st.write(data)

        st.subheader("Number of pickups by hour")
        hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
        st.bar_chart(hist_values)

        hour_to_filter = st.slider("hour", 0, 23, 17)
        filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

        st.subheader("Map of all pickups at %s:00" % hour_to_filter)
        st.map(filtered_data)
    if st.button("click me"):
        st.info("You clicked at: {}".format(datetime.datetime.now()))

    if st.sidebar.button("click me too"):
        st.info("You clicked at: {}".format(datetime.datetime.now()))

    # get the id of the menu item clicked
    st.info(f"{menu_id}")
