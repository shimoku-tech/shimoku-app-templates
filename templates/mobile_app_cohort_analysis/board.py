from shimoku_api_python import Client
from utils.utils import get_data, compute_percent
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

        # Main KPIs
        week_range = 9
        activity_weeks = df_active_users.apply(lambda row:
            row.unregister_date - row.register_date if pd.notna(row.unregister_date) else dt.datetime.now() - row.register_date,
            axis=1,
        ).dt.days / 7
        reference_date = df_active_users["register_date"].min()

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

        # All
        ## ALL - Line Chart
        all_line_chart = [
            {
                "week":f"W{week}",
                'users': compute_percent(
                    sum(activity_weeks >= week),
                    df_active_users.shape[0],
                )
            }
        for week in range(0,int(sum(activity_weeks) / df_active_users.shape[0]) + 3)]

        ## ALL - table
        user_per_week = [
            {
                "Week (Date)": reference_date + dt.timedelta(days=7*week),
                "Users": sum(df_active_users["register_date"].between(
                    reference_date + dt.timedelta(days=7*week),
                    reference_date + dt.timedelta(days= 7*(week + 1)),
                )),
            }
        for week in range(week_range)]

        all_table_chart = [
            user_per_week[row_week] |
            {
                f"W{columns_week}": "%.2f"%(compute_percent(
                    sum(activity_weeks[
                        df_active_users["register_date"].between(
                        reference_date + dt.timedelta(days=7*row_week),
                        reference_date + dt.timedelta(days= 7*(row_week + 1))
                    )] >= columns_week),
                    user_per_week[row_week]["Users"],
                )) + "%" if columns_week + row_week < week_range + 1 else "--"
            for columns_week in range(week_range + 1)}
        for row_week in range(week_range)]


        # Gender
        ## Gender - Pie Chart
        gender_pie_chart = [
            {
                'name': gender_name,
                'value': df_active_users[
                    df_active_users["gender"] == gender_name
                ].shape[0],
            }
        for gender_name in df_active_users["gender"].unique()]

        ## Gender - Line Chart
        gender_line_chart = [
            {
                "week":f"W{week}",
            } |
            {
                gender_name: compute_percent(
                    sum(activity_weeks[df_active_users["gender"] == gender_name] >= week),
                    df_active_users[df_active_users["gender"] == gender_name].shape[0],
                )
            for gender_name in df_active_users["gender"].unique()}
        for week in range(0,int(sum(activity_weeks) / df_active_users.shape[0]) + 3)]


        ## Gender - table
        gender_per_week = {
            gender: [
                {
                    "Week (Date)": reference_date + dt.timedelta(days=7*week),
                    "Users": sum(
                        df_active_users["register_date"].between(
                            reference_date + dt.timedelta(days=7*week),
                            reference_date + dt.timedelta(days= 7*(week + 1)),
                        ) & (df_active_users["gender"] == gender),
                    ),
                }
            for week in range(week_range)]
        for gender in df_active_users["gender"].unique()}

        gender_table_chart = {
            gender : [
                gender_per_week[gender][row_week] |
                {
                    f"W{columns_week}": "%.2f"%(compute_percent(
                        sum(activity_weeks[
                            df_active_users["register_date"].between(
                                reference_date + dt.timedelta(days=7*row_week),
                                reference_date + dt.timedelta(days= 7*(row_week + 1))
                            ) & (df_active_users["gender"] == gender)
                        ] >= columns_week),
                        gender_per_week[gender][row_week]["Users"],
                    )) + "%" if columns_week + row_week < week_range + 1 else "--"
                for columns_week in range(week_range + 1)}
            for row_week in range(week_range)]
        for gender in df_active_users["gender"].unique()}

        # Age
        ## Age - Pie Chart
        age_ranges = [
            {"name": "18 - 25", "min": 18, "max": 26},
            {"name": "26 - 40", "min": 26, "max": 41},
            {"name": "41 - 60", "min": 41, "max": 61},
            {"name": "Above 61", "min": 61, "max": 200},
        ]

        age_pie_chart = [
            {
                'name': age_range["name"],
                'value': df_active_users[
                    df_active_users["age"].isin(range(age_range["min"], age_range["max"]))
                ].shape[0],
            }
        for age_range in age_ranges]

        ## Age - Line Chart
        age_line_chart = [
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


        ## Age - table
        age_per_week = {
            age_range["name"]: [
                {
                    "Week (Date)": reference_date + dt.timedelta(days=7*week),
                    "Users": sum(
                        df_active_users["register_date"].between(
                            reference_date + dt.timedelta(days=7*week),
                            reference_date + dt.timedelta(days= 7*(week + 1)),
                        ) & (df_active_users["age"].isin(range(age_range["min"], age_range["max"]))),
                    ),
                }
            for week in range(week_range)]
        for age_range in age_ranges}

        age_table_chart = {
            age_range["name"] : [
                age_per_week[age_range["name"]][row_week] |
                {
                    f"W{columns_week}": "%.2f"%(compute_percent(
                        sum(activity_weeks[
                            df_active_users["register_date"].between(
                                reference_date + dt.timedelta(days=7*row_week),
                                reference_date + dt.timedelta(days= 7*(row_week + 1))
                            ) & (df_active_users["age"].isin(range(age_range["min"], age_range["max"])))
                        ] >= columns_week),
                        age_per_week[age_range["name"]][row_week]["Users"],
                    )) + "%" if columns_week + row_week < week_range + 1 else "--"
                for columns_week in range(week_range + 1)}
            for row_week in range(week_range)]
        for age_range in age_ranges}


        # Adquisitions source
        ## Adquisitions source - Pier Chart
        source_pie_chart = [
            {
                'name': source_name,
                'value': df_active_users[
                    df_active_users["acquisition_source"] == source_name
                ].shape[0],
            }
        for source_name in df_active_users["acquisition_source"].unique()]


        ## Adquisitions source - Line Chart
        source_line_chart = [
            {
                "week":f"W{week}",
            } |
            {
                source_name: compute_percent(
                    sum(activity_weeks[df_active_users["acquisition_source"] == source_name] >= week),
                    df_active_users[df_active_users["acquisition_source"] == source_name].shape[0],
                )
            for source_name in df_active_users["acquisition_source"].unique()}
        for week in range(0,int(sum(activity_weeks) / df_active_users.shape[0]) + 3)]

        ## Acquisition source - table
        source_per_week = {
            source_name: [
                {
                    "Week (Date)": reference_date + dt.timedelta(days=7*week),
                    "Users": sum(
                        df_active_users["register_date"].between(
                            reference_date + dt.timedelta(days=7*week),
                            reference_date + dt.timedelta(days= 7*(week + 1)),
                        ) & (df_active_users["acquisition_source"] == source_name),
                    ),
                }
            for week in range(week_range)]
        for source_name in df_active_users["acquisition_source"].unique()}

        source_table_chart = {
            source_name : [
                source_per_week[source_name][row_week] |
                {
                    f"W{columns_week}": "%.2f"%(compute_percent(
                        sum(activity_weeks[
                            df_active_users["register_date"].between(
                                reference_date + dt.timedelta(days=7*row_week),
                                reference_date + dt.timedelta(days= 7*(row_week + 1))
                            ) & (df_active_users["acquisition_source"] == source_name)
                        ] >= columns_week),
                        source_per_week[source_name][row_week]["Users"],
                    )) + "%" if columns_week + row_week < week_range + 1 else "--"
                for columns_week in range(week_range + 1)}
            for row_week in range(week_range)]
        for source_name in df_active_users["acquisition_source"].unique()}



        self.df_app = {
            "main_kpis": pd.DataFrame(main_kpis),
            "all_line_chart": pd.DataFrame(all_line_chart),
            "all_table_chart": pd.DataFrame(all_table_chart),
            "gender_pie_chart": pd.DataFrame(gender_pie_chart),
            "gender_line_chart": pd.DataFrame(gender_line_chart),
            "age_pie_chart": pd.DataFrame(age_pie_chart),
            "age_line_chart": pd.DataFrame(age_line_chart),
            "source_pie_chart": pd.DataFrame(source_pie_chart),
            "source_line_chart": pd.DataFrame(source_line_chart),
        }
        self.df_app |= {
            f"gender_table_chart_{gender_name}" : pd.DataFrame(gender_table_chart[gender_name])
        for gender_name in df_active_users["gender"].unique()}
        self.df_app |= {
            f"age_table_chart_{age_range['name']}" : pd.DataFrame(age_table_chart[age_range["name"]])
        for age_range in age_ranges}
        self.df_app |= {
            f"source_table_chart_{source_name}" : pd.DataFrame(source_table_chart[source_name])
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

        UO = CohortAnalysis(self)
        UO.plot()
