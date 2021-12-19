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
        {"id": "Cohort Analysis", "icon": "📈", "label": "Cohort Analysis"},
        {"id": "User acquisition", "icon": "👨‍💻", "label": "User acquisition"},
        {"id": "Funnel Analysis", "icon": "📊", "label": "Funnel Analysis"},
        {"id": "User journey diagram", "icon": "🏃‍♂️", "label": "User journey diagram"},
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
        터미널에
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
            코호트 분석할때 쓰이는 코드를 불러 올 수 있습니다.  
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
            Retention Plot을 그려보는 코드입니다.  
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
            Revenue도 계산 할 수 있습니다.  
            각 필요한 지표를 뽑을 수 있습니다.  
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
            스타일링을 추가하여 한 눈에 시각화 하기 편함  
            데이터프레임으로 변환시 변수명.data로 변환 가능  
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
            유저의 일 월 년 별로 사용량 및 사용 시간을 분석한 데이터 입니다.  
            라이브러리와 유사한 데이터 프레임에서도 동작 가능 합니다.  
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
            유저의 일 월 년 별로 사용량 및 사용 시간을 시각화한 데이터 입니다.  
            해당 컬럼과 이름이 맞는 경우 해당 코드를 사용할 수 있습니다.  
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
            퍼널 데이터에 쓰이는 데이터입니다.  
            해당 데이터와 유사한 데이터 프레임에 동작 합니다.  
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
            Funnel 데이터를 시각화한 코드 입니다.  
            위 데이터와 유사한 데이터 프레임에 시각화가 가능합니다.  
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
            유저의 사용자 여정을 그린 시각화 코드입니다.  
            이벤트 데이터 프레임에 동작 합니다.  
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
