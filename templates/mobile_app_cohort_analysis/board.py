from shimoku_api_python import Client
from utils.utils import get_data, compute_percent, cohort_analysis, generate_category, generate_life_time
import pandas as pd
import datetime as dt
import numpy as np

class Board:
    """
    A class used to represent a Dashboard for displaying various data visualizations.

    Attributes:
        board_name (str): Name of the dashboard.
        dfs (DFs): An instance of a DFs class for handling data frames.
        shimoku (Client): An instance of a Client class for Shimoku API interactions.
    """

    def __init__(self, shimoku: Client):
        """
        The constructor for the Dashboard class.

        Parameters:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        file_names = ["data/active_users.csv"]
        # Name of the dashboard
        self.board_name = "Mobile App Template"
        # Get data from CSV files
        self.dfs = get_data(file_names)
        # Shimoku client instance
        self.shimoku = shimoku
        # Setting up the board in Shimoku
        self.shimoku.set_board(name=self.board_name)
        # Make the board public
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)

    def transform(self) -> bool:
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df_active_users = self.dfs["active_users"]

        activity_weeks = df_active_users.apply(lambda row:
            row.unregister_date - row.register_date if pd.notna(row.unregister_date) else dt.datetime.now() - row.register_date,
            axis=1,
        ).dt.days / 7

        # Main KPIs
        main_kpis = [
            # Total users
            {
                "title": "Users",
                "description": "Total Users",
                "value": df_active_users["user_id"].unique().shape[0],
                "color": "default",
                "align": "center",
            },
            # Average Life Time
            {
                "title": "Average Life Time",
                "description": "",
                "value": "%d weeks"%(
                    sum(activity_weeks) / df_active_users.shape[0]
                ),
                "color": "default",
                "align": "center",
            },
            # Organic
            {
                "title": "Organic",
                "description": "Organic Users",
                "value": df_active_users[df_active_users["acquisition_source"] == "Organic"].shape[0],
                "color": "default",
                "align": "center",
            },
            # Google-Ads
            {
                "title": "Google-Ads",
                "description": "Users from Google-Ads",
                "value": df_active_users[df_active_users["acquisition_source"] == "Google-Ads"].shape[0],
                "color": "default",
                "align": "center",
            },
            # Facebook
            {
                "title": "Facebook",
                "description": "Users from Facebook",
                "value": df_active_users[df_active_users["acquisition_source"] == "Facebook"].shape[0],
                "color": "default",
                "align": "center",
            },
        ]


        week_range = 9
        reference_date = df_active_users["register_date"].min()


        # All section
        ## ALL section - Users Life Time
        all_life_time = generate_life_time(df_active_users, activity_weeks)

        ## ALL section - Cohort Analysis
        all_cohort = cohort_analysis(df_active_users, activity_weeks, week_range, reference_date)


        # Gender section
        ## Gender section - Gender Category
        gender_category = generate_category(df_active_users, "gender")

        ## Gender section - Users Life Time by Gender
        gender_life_time = generate_life_time(df_active_users, activity_weeks, True, "gender")

        ## Gender section - Cohort Analysis by Gender
        gender_cohort = {}
        for gender_name in df_active_users["gender"].unique():
            gender_cohort[gender_name] = cohort_analysis(df_active_users, activity_weeks, week_range, reference_date, True, "gender", gender_name)



        # Age section
        ## Age section - Age Category
        age_ranges = [
            {"name": "18 - 25", "min": 18, "max": 26},
            {"name": "26 - 40", "min": 26, "max": 41},
            {"name": "41 - 60", "min": 41, "max": 61},
            {"name": "Above 61", "min": 61, "max": 200},
        ]

        age_category = [
            {
                'name': age_range["name"],
                'value': df_active_users[
                    df_active_users["age"].isin(range(age_range["min"], age_range["max"]))
                ].shape[0],
            }
        for age_range in age_ranges]

        ## Age section - Users Life Time by Age
        age_life_time = [
            {
                "week":f"W{week}",
            } |
            {
                age_range["name"]: compute_percent(
                    sum(activity_weeks[df_active_users["age"].isin(range(age_range["min"], age_range["max"]))] >= week),
                    sum(df_active_users["age"].isin(range(age_range["min"], age_range["max"]))),
                )
            for age_range in age_ranges}
        for week in range(0,int(sum(activity_weeks) / df_active_users.shape[0]) + 3)]


        ## Age section - Cohort Analysis by Age
        age_cohort = {}
        for age_range in age_ranges:
            age_per_week = [
                {
                    "Week (Date)": reference_date + dt.timedelta(days=7*week),
                    "Users": sum(df_active_users["register_date"].between(
                            reference_date + dt.timedelta(days=7*week),
                            reference_date + dt.timedelta(days= 7*(week + 1)),
                        ) & (df_active_users["age"].isin(range(age_range["min"], age_range["max"]))),
                    ),
                }
            for week in range(week_range)]

            age_cohort[age_range["name"]] = [
                age_per_week[row_week] |
                {
                    f"W{columns_week}": compute_percent(
                        sum(activity_weeks[df_active_users["register_date"].between(
                                reference_date + dt.timedelta(days=7*row_week),
                                reference_date + dt.timedelta(days= 7*(row_week + 1))
                            ) & (df_active_users["age"].isin(range(age_range["min"], age_range["max"])))
                        ] >= columns_week),
                        age_per_week[row_week]["Users"],
                    ) if columns_week + row_week < week_range + 1 else 0
                for columns_week in range(week_range + 1)}
            for row_week in range(week_range)]


        # Adquisitions Source section
        ## Adquisitions Source section - Adquisitions Source Category
        source_category = generate_category(df_active_users, "acquisition_source")

        ## Adquisitions Source section - Line Chart
        source_life_time = generate_life_time(df_active_users, activity_weeks, True, "acquisition_source")

        ## Acquisition Source section - table
        source_cohort = {}
        for source_name in df_active_users["acquisition_source"].unique():
            source_cohort[source_name] = cohort_analysis(df_active_users, activity_weeks, week_range, reference_date, True, "acquisition_source", source_name)

        # Saved as Dataframe to plot
        self.df_app = {
            "main_kpis": pd.DataFrame(main_kpis),
            "all_life_time": pd.DataFrame(all_life_time),
            "all_cohort": pd.DataFrame(all_cohort),
            "gender_category": pd.DataFrame(gender_category),
            "gender_life_time": pd.DataFrame(gender_life_time),
            "age_category": pd.DataFrame(age_category),
            "age_life_time": pd.DataFrame(age_life_time),
            "source_category": pd.DataFrame(source_category),
            "source_life_time": pd.DataFrame(source_life_time),
        }

        self.df_app |= {
            f"gender_cohort_{gender_name}" : pd.DataFrame(gender_cohort[gender_name])
        for gender_name in df_active_users["gender"].unique()}

        self.df_app |= {
            f"age_cohort_{age_range['name']}" : pd.DataFrame(age_cohort[age_range["name"]])
        for age_range in age_ranges}

        self.df_app |= {
            f"source_cohort_{source_name}" : pd.DataFrame(source_cohort[source_name])
        for source_name in df_active_users["acquisition_source"].unique()}

        return True

    def plot(self):
        """
        A method to plot Cohort Analysis.

        This method utilizes the CohortAnalysis class from the paths.cohort_analysis
        module to create and display a plot related to the user. It assumes that
        CohortAnalysis requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the CohortAnalysis class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the CohortAnalysis class has access to all necessary data
          through the passed instance.
        """

        from paths.cohort_analysis import CohortAnalysis

        CA = CohortAnalysis(self)
        CA.plot()
