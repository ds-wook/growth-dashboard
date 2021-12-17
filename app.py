import hydralit_components as hc
import pyuba as uba
import streamlit as st

from home import draw_abtest

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

    if menu_id == "Home":
        st.header("PyUBA: Python User Behavior Analysis User Guide")
        st.subheader("What is it?")
        st.markdown(
            """
        `pyuba`는 그로스 해킹 툴 라이브러리 입니다.
        """
        )

        st.subheader("Installation")
        st.markdown(
            """
        `pyuba`는 PyPI에서 다운 받으실수 있습니다.
        ```
        $ pip install pyuba
        ```
        라고 입력하세요.
        """
        )

    if menu_id == "Cohort Analysis":
        st.title("Load Cohort Dataset")
        st.markdown(
            """
            ```python
            import pyuba as uba

            events = uba.load_dataset(10000)
            cohorts = uba.load_cohorts(events)
            user_retention = uba.load_user_retention(cohorts)
            display(user_retention)
            ```
            """
        )
        events = uba.load_dataset(10000)
        cohorts = uba.load_cohorts(events)
        user_retention = uba.load_user_retention(cohorts)
        st.write(events)

        st.header("Draw Cohorts: User Retention")
        st.markdown(
            """
            ```python
            import pyuba as uba
            from plotly.plotly import iplot

            fig = uba.draw_user_retention(user_retention.T)
            iplot(fig)
            ```
            """
        )
        fig = uba.draw_user_retention(user_retention.T)
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "User acquisition":
        st.title("Load User acquisition Dataset")
        st.markdown(
            """
            ```python
            import pyuba as uba

            events = uba.load_dataset(10000)
            per_period = uba.users_per_period(
                events=events,
                acquisition_event_name="Install",
                user_source_col="user_source",
                period="m",
            )

            display(per_period)
            ```
            """
        )
        events = uba.load_dataset(10000)
        st.write(
            uba.users_per_period(
                events=events,
                acquisition_event_name="Install",
                user_source_col="user_source",
                period="m",
            )
        )

        st.header("Draw User acquisition")
        st.markdown(
            """
            ```python
            import pyuba as uba
            from plotly.plotly import iplot

            events = uba.load_dataset(10000)
            fig = uba.plot_users_per_period(
                events=events,
                acquisition_event_name="Install",
                user_source_col="user_source",
                period="m",
            )
            iplot(fig)
            ```
            """
        )
        fig = uba.plot_users_per_period(
            events=events,
            acquisition_event_name="Install",
            user_source_col="user_source",
            period="m",
        )
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "Funnel Analysis":
        st.title("Load Funnel Dataset")
        st.markdown(
            """
            ```python
            import pyuba as uba

            steps = ["Install", "SignUp", "Click Product", "Purchase"]
            funnel_df = uba.create_funnel_df(events, steps)
            display(funnel_df)
            ```
            """
        )
        events = uba.load_dataset(10000)

        steps = ["Install", "SignUp", "Click Product", "Purchase"]
        funnel_df = uba.create_funnel_df(events, steps)
        st.write(funnel_df)

        st.header("Draw Funnel Analysis")
        st.markdown(
            """
            ```python
            import pyuba as uba
            from plotly.plotly import iplot

            events = uba.load_dataset(10000)
            fig = uba.plot_stacked_funnel(events, steps, col="user_source")
            iplot(fig)
            ```
            """
        )
        fig = uba.plot_stacked_funnel(events, steps, col="user_source")
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