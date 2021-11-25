import warnings

import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


# Label the CohortPeriod for each CohortGroup
def cohort_period(df):

    df["CohortPeriod"] = np.arange(len(df)) + 1
    return df


@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


@st.cache(allow_output_mutation=True)
def load_cohorts(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=1)
    df["OrderPeriod"] = df["OrderDate"].apply(lambda x: x.strftime("%Y-%m"))

    df.set_index("UserId", inplace=True)

    df["CohortGroup"] = (
        df.groupby(level=0)["OrderDate"].min().apply(lambda x: x.strftime("%Y-%m"))
    )
    df.reset_index(inplace=True)

    grouped = df.groupby(["CohortGroup", "OrderPeriod"])

    cohorts = grouped.agg(
        {
            "UserId": pd.Series.nunique,
            "OrderId": pd.Series.nunique,
            "TotalCharges": np.sum,
        }
    )

    cohorts.rename(
        columns={"UserId": "TotalUsers", "OrderId": "TotalOrders"}, inplace=True
    )
    cohorts = cohorts.groupby(level=0).apply(cohort_period)

    return cohorts


@st.cache(allow_output_mutation=True)
def load_user_retention(cohorts: pd.DataFrame) -> pd.DataFrame:
    # reindex the DataFrame
    cohorts.reset_index(inplace=True)
    cohorts.set_index(["CohortGroup", "CohortPeriod"], inplace=True)

    # create a Series holding the total size of each CohortGroup
    cohort_group_size = cohorts["TotalUsers"].groupby(level=0).first()

    user_retention = cohorts["TotalUsers"].unstack(0).divide(cohort_group_size, axis=1)

    return user_retention
