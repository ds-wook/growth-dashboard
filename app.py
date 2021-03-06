import hydralit_components as hc
import pandas as pd
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
        {"id": "Cohort Analysis", "icon": "π", "label": "Cohort Analysis"},
        {"id": "User acquisition", "icon": "π¨βπ»", "label": "User acquisition"},
        {"id": "Funnel Analysis", "icon": "π", "label": "Funnel Analysis"},
        {"id": "User journey diagram", "icon": "πββοΈ", "label": "User journey diagram"},
        {"id": "AB-Test", "icon": "π­", "label": "AB-Test"},
        {"id": "Notepad", "icon": "π", "label": "Notepad"},  # no tooltip message
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
        `pyuba`λ κ·Έλ‘μ€ ν΄νΉ ν΄ λΌμ΄λΈλ¬λ¦¬ μλλ€.  
        κ·Έλ‘μ€ ν΄νΉμ΄λ μ±μ₯μ λ»νλ κ·Έλ‘μ€(growth)+ν΄νΉ(hacking)μ ν©μ±μ΄λ‘  
        μ νλ°μ΄ν°λ‘ μλΉμ€ κ°μ νλ©°, λ§μΌνν¨κ³Όλ₯Ό μμΉμν€λ λ§μΌν λ°©λ²λ‘ μλλ€.  
        """
        )

        st.subheader("Installation")
        st.markdown(
            """
        `pyuba`λ PyPIμμ λ€μ΄ λ°μΌμ€μ μμ΅λλ€.
        ν°λ―Έλμ
        ```
        pip install pyuba
        ```
        λΌκ³  μλ ₯νμΈμ.
        """
        )

    if menu_id == "Cohort Analysis":
        st.title("Load Cohort Dataset")
        st.markdown(
            """
            μ½νΈνΈ λΆμν λ μ°μ΄λ μ½λλ₯Ό λΆλ¬ μ¬ μ μμ΅λλ€.  
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
            Retention Plotμ κ·Έλ €λ³΄λ μ½λμλλ€.  
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

        st.header("Calulate Revenue")
        st.subheader("Example Payment DataFrame")
        st.markdown(
            """
            Revenueλ κ³μ° ν  μ μμ΅λλ€.  
            κ° νμν μ§νλ₯Ό λ½μ μ μμ΅λλ€.  
            """
        )
        st.markdown(
            """
            ```python
            payment = pd.read_excel("input/data1.xlsx", sheet_name="payment")
            payment.head()
            ```
            |payment_id|item|payment|buy_date|user_id|
            |-----|--|------|-------|--------|-------|
            |1|itemE|20000|2019-12-01|70|
            |2|itemB|5000|2019-12-01|1153|
            |3|itemA|3000|2019-12-01|1210|
            |4|itemA|3000|2019-12-01|1242|
            |5|itemE|20000|2019-12-01|975|
            """
        )

        payment = pd.read_excel("./input/data1.xlsx", sheet_name="payment")
        sign_up = pd.read_excel("./input/data1.xlsx", sheet_name="signup")
        st.subheader("Example Sign Up DataFrame")
        st.markdown(
            """
            ```python
            sign_up = pd.read_excel("input/data1.xlsx", sheet_name="signup")
            sign_up.head()
            ```
            |user_id|item|payment|
            |-----|--|------|-------|
            |1|2019-01-01|2019-06-03|
            |2|2019-01-01|2019-11-02|
            |3|2019-01-01|2019-01-23|
            |4|2019-01-01|2019-04-19|
            |5|2019-01-01|2019-06-25|
            """
        )

        st.subheader("Show Revenue DataFrame")
        st.markdown(
            """
            μ€νμΌλ§μ μΆκ°νμ¬ ν λμ μκ°ν νκΈ° νΈν¨  
            λ°μ΄ν°νλ μμΌλ‘ λ³νμ λ³μλͺ.dataλ‘ λ³ν κ°λ₯  
            ```python
            retention = uba.split_revenue(sign_up, payment)
            retention.head()
            ```
            """
        )

        retention = uba.split_revenue(sign_up, payment)
        st.write(retention)

    if menu_id == "User acquisition":
        st.title("Load User acquisition Dataset")
        st.markdown(
            """
            μ μ μ μΌ μ λ λ³λ‘ μ¬μ©λ λ° μ¬μ© μκ°μ λΆμν λ°μ΄ν° μλλ€.  
            λΌμ΄λΈλ¬λ¦¬μ μ μ¬ν λ°μ΄ν° νλ μμμλ λμ κ°λ₯ ν©λλ€.  
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
            μ μ μ μΌ μ λ λ³λ‘ μ¬μ©λ λ° μ¬μ© μκ°μ μκ°νν λ°μ΄ν° μλλ€.  
            ν΄λΉ μ»¬λΌκ³Ό μ΄λ¦μ΄ λ§λ κ²½μ° ν΄λΉ μ½λλ₯Ό μ¬μ©ν  μ μμ΅λλ€.  
            ```python
            import pyuba as uba
            from plotly.offline import iplot

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
            νΌλ λ°μ΄ν°μ μ°μ΄λ λ°μ΄ν°μλλ€.  
            ν΄λΉ λ°μ΄ν°μ μ μ¬ν λ°μ΄ν° νλ μμ λμ ν©λλ€.  
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
            Funnel λ°μ΄ν°λ₯Ό μκ°νν μ½λ μλλ€.  
            μ λ°μ΄ν°μ μ μ¬ν λ°μ΄ν° νλ μμ μκ°νκ° κ°λ₯ν©λλ€.  
            ```python
            import pyuba as uba
            from plotly.offline import iplot

            events = uba.load_dataset(10000)
            fig = uba.plot_stacked_funnel(events, steps, col="user_source")
            iplot(fig)
            ```
            """
        )
        fig = uba.plot_stacked_funnel(events, steps, col="user_source")
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "User journey diagram":
        st.title("Draw User journey diagram Dataset")
        events = uba.load_dataset(10000)
        st.markdown(
            """
            μ μ μ μ¬μ©μ μ¬μ μ κ·Έλ¦° μκ°ν μ½λμλλ€.  
            μ΄λ²€νΈ λ°μ΄ν° νλ μμ λμ ν©λλ€.  
            ```python
            import pyuba as uba
            from plotly.offline import iplot

            events = uba.load_dataset(10000)
            fig = uba.plot_user_flow(events, "Click Product", n_steps=5)
            iplot(fig)
            ```
            """
        )
        fig = uba.plot_user_flow(events, "Click Product", n_steps=5)
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
