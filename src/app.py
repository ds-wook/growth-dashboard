import datetime

import hydralit_components as hc
import plotly.express as px
import streamlit as st

from calc.bayesian import Bayesian
from calc.frequentist import Frequentist
from calc.functions import create_plotly_table, local_css
from data.dataset import load_cohorts, load_user_retention
from graph.graph import draw_user_retention

if __name__ == "__main__":
    # make it look nice from the start
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # specify the primary menu definition
    menu_data = [
        {"id": "Cohort Analysis", "icon": "📈", "label": "Cohort Analysis"},
        {"id": "AB-Test", "icon": "fa-solid fa-radar", "label": "AB-Test"},
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

    if menu_id == "Cohort Analysis":
        st.title("Load Cohort Dataset")
        data_load_state = st.text("Loading data...")
        chorts = load_cohorts("../input/relay-foods.xlsx")
        user_retention = load_user_retention(chorts)
        data_load_state.text("Done! (using st.cache)")

        if st.checkbox("Show raw data"):
            st.subheader("Raw data")
            st.write(chorts)

        st.header("Draw Polt Chart")
        fig = px.line(user_retention)
        st.plotly_chart(fig)

        st.header("Draw Cohorts: User Retention")
        fig = draw_user_retention(user_retention.T)
        st.plotly_chart(fig, height=800, width=500)

    if menu_id == "AB-Test":
        roboto = {"size": "12"}
        roboto_title = {"size": "14", "weight": "bold"}
        roboto_bold = {"size": "12", "weight": "bold"}
        roboto_small = {"size": "10"}

        local_css("../style/style.css")

        """
        # AB test calculator
        _Enter your test data into the sidebar and choose either a Bayesian or
        Frequentist testing approach. Below is Bayesian by default._
        ---
        """

        # Sidebar
        st.sidebar.markdown(
            """
        ## Approach
        """
        )

        method = st.sidebar.radio(
            "Bayesian vs. Frequentist", ["Bayesian", "Frequentist"]
        )

        st.sidebar.markdown(
            """
        ## Test data
        """
        )

        visitors_A = st.sidebar.number_input("Visitors A", value=50000, step=100)
        conversions_A = st.sidebar.number_input("Conversions A", value=1500, step=10)
        visitors_B = st.sidebar.number_input("Visitors B", value=50000, step=100)
        conversions_B = st.sidebar.number_input("Conversions B", value=1560, step=10)

        st.sidebar.markdown(
            """
        ## Frequentist settings
        """
        )

        alpha_input = 1 - st.sidebar.slider(
            "Significance level", value=0.95, min_value=0.5, max_value=0.99
        )
        tails_input = st.sidebar.selectbox(
            "One vs. two tail", ["One-tail", "Two-tail"], index=1
        )

        if tails_input == "One-tail":
            two_tails_bool = False
        else:
            two_tails_bool = True

        b = Bayesian(visitors_A, conversions_A, visitors_B, conversions_B)

        # Bayesian Method
        if method == "Bayesian":

            try:
                b.generate_posterior_samples()
                b.calculate_probabilities()
                b.plot_bayesian_probabilities()

                st.text("")

                bayesian_data = {
                    "<b>Variant</b>": ["A", "B"],
                    "<b>Visitors</b>": [f"{b.visitors_A:,}", f"{b.visitors_B:,}"],
                    "<b>Conversions</b>": [b.conversions_A, b.conversions_B],
                    "<b>Conversion rate</b>": [
                        f"{b.control_cr:.2%}",
                        f"{b.variant_cr:.2%}",
                    ],
                    "<b>Uplift</b>": ["", f"{b.relative_difference:.2%}"],
                    "<b>Likelihood of being better</b>": [
                        f"{b.prob_A:.2%}",
                        f"{b.prob_B:.2%}",
                    ],
                }

                create_plotly_table(bayesian_data)

                """
                The below graph plots the simulated difference between the two
                posterior distributions for the variants. It highlights the potential
                range of difference between the two variants. More data will reduce
                the range.
                """

                st.text("")

                b.plot_simulation_of_difference()

                """
                ---
                ### Recommended Reading
                * [Bayesian Methods for Hackers by Cameron Davidson-Pilon]\
                    (https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)
                * [Bayesian AB test calculator by AB Testguide]\
                    (https://abtestguide.com/bayesian/)
                * [Beta distribution Wikipedia]\
                    (https://en.wikipedia.org/wiki/Beta_distribution)
                """

            except ValueError:

                t = """
                <img class='error'
                    src='https://www.flaticon.com/svg/static/icons/svg/595/595067.svg'>
                """
                st.markdown(t, unsafe_allow_html=True)

                """
                An error occured, please check the test data input and try again.
                For Bayesian calculations, the conversion rate must be between 0 and
                1.
                """

        else:  # Frequentist

            f = Frequentist(
                visitors_A,
                conversions_A,
                visitors_B,
                conversions_B,
                alpha=alpha_input,
                two_tails=two_tails_bool,
            )

            z_score, p_value = f.z_test()

            power = f.get_power()

            if p_value < alpha_input:
                t = """
                <h3 class='frequentist_title'>Significant</h3>
                <img class='frequentist_icon'
                    src='https://www.flaticon.com/svg/static/icons/svg/1533/1533913.svg'>
                """
                st.markdown(t, unsafe_allow_html=True)

                if f.relative_difference < 0:
                    t = (
                        """
                    <p>B's conversion rate is <span class='lower'>"""
                        + "{:.2%}".format(abs(f.relative_difference))
                        + """ lower</span> than A's CR."""
                    )
                    st.markdown(t, unsafe_allow_html=True)
                else:
                    t = (
                        """
                    <p>B's conversion rate is <span class='higher'>"""
                        + "{:.2%}".format(abs(f.relative_difference))
                        + """ higher</span> than A's CR."""
                    )
                    st.markdown(t, unsafe_allow_html=True)

                f"""
                You can be {1-alpha_input:.0%} confident that the result is true and
                due to the changes made. There is a {alpha_input:.0%} chance that the result
                is a false positive or type I error meaning the result is due to
                random chance.
                """

            else:
                t = """
                <h3 class='frequentist_title'>Not significant</h3>
                <img class='frequentist_icon'
                    src='https://www.flaticon.com/svg/static/icons/svg/1533/1533919.svg'>
                """
                st.markdown(t, unsafe_allow_html=True)

                f"""
                There is not enough evidence to prove that there is a
                {f.relative_difference:.2%} difference in the conversion rates between
                variants A and B.
                """

                """
                Either collect more data to achieve greater precision in your test,
                or conclude the test as inconclusive.
                """

            frequentist_data = {
                "<b>Variant</b>": ["A", "B"],
                "<b>Visitors</b>": [f"{f.visitors_A:,}", f"{f.visitors_B:,}"],
                "<b>Conversions</b>": [f.conversions_A, f.conversions_B],
                "<b>Conversion rate</b>": [
                    f"{f.control_cr:.2%}",
                    f"{f.variant_cr:.2%}",
                ],
                "<b>Uplift</b>": ["", f"{f.relative_difference:.2%}"],
                "<b>Power</b>": ["", f"{power:.4f}"],
                "<b>Z-score</b>": ["", f"{z_score:.4f}"],
                "<b>P-value</b>": ["", f"{p_value:.4f}"],
            }

            create_plotly_table(frequentist_data)

            z = f.get_z_value()

            """
            According to the null hypothesis, there is no difference between the means.
            The plot below shows the distribution of the difference of the means that
            we would expect under the null hypothesis.
            """

            f.plot_test_visualisation()

            if p_value < alpha_input:
                f"""
                The shaded areas cover {alpha_input:.0%} of the distribution. It is
                because the observed mean of the variant falls into this area that we
                can reject the null hypothesis with {1-alpha_input:.0%} confidence.
                """
            else:
                f"""
                The shaded areas cover {alpha_input:.0%} of the distribution. It is
                because the observed mean of the variant does not fall into this area that
                we are unable to reject the null hypothesis and get a significant
                result. A difference of greater than
                {f.se_difference*z/f.control_cr:.2%} is needed.
                """

            """
            #### Statistical Power
            """

            f"""
            Power is a measure of how likely we are to detect a difference when there
            is one with 80% being the generally accepted threshold for statistical
            validity. **The power for your test is {power:.2%}**
            """

            f"""
            An alternative way of defining power is that it is our likelihood of
            avoiding a Type II error or a false negative. Therefore the inverse of
            power is 1 - {power:.2%} = {1-power:.2%} which is our likelihood of a
            type II error.
            """

            f.plot_power()

            """
            ---
            ### Recommended reading
            * [Z-test Wikipedia](https://en.wikipedia.org/wiki/Z-test)
            * [The Math Behind AB Testing by Nguyen Ngo]\
                (https://towardsdatascience.com/the-math-behind-a-b-testing-with-example-code-part-1-of-2-7be752e1d06f)
            * [AB test calculator by AB Testguide](https://www.abtestguide.com/calc/)
            """

        """
        ### See also
        * [Sample size calculator](https://abtestsamplesize.herokuapp.com/)
        * [Github Repository](https://github.com/rjjfox/ab-test-calculator)
        """
    if st.button("click me"):
        st.info("You clicked at: {}".format(datetime.datetime.now()))

    if st.sidebar.button("click me too"):
        st.info("You clicked at: {}".format(datetime.datetime.now()))

    # get the id of the menu item clicked
    st.info(f"{menu_id}")
