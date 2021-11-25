import datetime

import hydralit_components as hc
import pandas as pd

# import plotly.express as px
import streamlit as st

from data.acquisition import users_per_period
from data.funnel import create_funnel_df
from data.retention import load_cohorts, load_user_retention
from home import draw_abtest
from visualizations.funnel_plots import plot_stacked_funnel
from visualizations.growth import plot_users_per_period
from visualizations.retention_plots import draw_user_retention

if __name__ == "__main__":
    # make it look nice from the start
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # specify the primary menu definition
    menu_data = [
        {"id": "Cohort Analysis", "icon": "📈", "label": "Cohort Analysis"},
        {"id": "User acquisition", "icon": "👨‍💻", "label": "User acquisition"},
        {"id": "Funnel Analysis", "icon": "📊", "label": "Funnel Analysis"},
        {"id": "AB-Test", "icon": "🎭", "label": "AB-Test"},
        {"id": "Notepad", "icon": "📑", "label": "Notepad"},  # no tooltip message
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

    if menu_id == "Cohort Analysis":
        st.title("Load Cohort Dataset")
        data_load_state = st.text("Loading data...")
        events = pd.read_csv("../input/events.csv")
        events["time"] = pd.to_datetime(events["time"], errors="coerce")
        cohorts = load_cohorts(events)
        user_retention = load_user_retention(cohorts)

        st.subheader("Raw data")
        st.write(events)

        st.header("Draw Cohorts: User Retention")
        fig = draw_user_retention(user_retention.T)
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "User acquisition":
        st.title("Load User acquisition Dataset")
        data_load_state = st.text("Loading data...")
        events = pd.read_csv("../input/events.csv")
        events["time"] = pd.to_datetime(events["time"], errors="coerce")

        st.subheader("activity stats per period")
        st.write(
            users_per_period(
                events=events,
                acquisition_event_name="Install",
                user_source_col="user_source",
                period="m",
            )
        )

        st.header("Draw User acquisition")
        fig = plot_users_per_period(
            events=events,
            acquisition_event_name="Install",
            user_source_col="user_source",
            period="m",
        )
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "Funnel Analysis":
        st.title("Load Funnel Dataset")
        data_load_state = st.text("Loading data...")
        events = pd.read_csv("../input/events.csv")
        events["time"] = pd.to_datetime(events["time"], errors="coerce")
        steps = ["Install", "SignUp", "Click Product", "Purchase"]
        funnel_df = create_funnel_df(events, steps)
        st.write(funnel_df)
        st.header("Draw Funnel Analysis")
        fig = plot_stacked_funnel(events, steps, col="user_source")
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "AB-Test":
        draw_abtest()

    if menu_id == "Notepad":
        st.subheader("Notepad")
        input_pa = st.text_area(
            "Use the example below or input your own text in Korean (maximum 1000 characters)",
            max_chars=1000,
            height=160,
        )
        if st.button("Submit", key="message"):
            st.info(input_pa)

    # if st.button("click me"):
    #     st.info("You clicked at: {}".format(datetime.datetime.now()))

    if st.sidebar.button("click me too"):
        st.info("You clicked at: {}".format(datetime.datetime.now()))

    # get the id of the menu item clicked
    st.info(f"{menu_id}")
