from shimoku_api_python import Client
from utils.utils import get_data, compute_percent
import pandas as pd
import datetime as dt

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
        activity_days = df_active_users.apply(lambda row: row.last_login_date - row.register_date, axis=1).dt.days
        activity_weeks = activity_days / 7

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

        # Gender
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

        # Age
        ## Age - Pie Chart
        age_ranges = [
            {"min": 18, "max": 26},
            {"min": 26, "max": 41},
            {"min": 41, "max": 61},
            {"min": 61, "max": 200},
        ]

        age_pie_chart = [
            {
                'name': f"{age_range['min']} - {age_range['max']}" if age_range["min"] != 61 else f"Above {age_range['min']}",
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
                f"{age_range['min']} - {age_range['max']}" if age_range["min"] != 61 else f"Above {age_range['min']}": compute_percent(
                    sum(activity_weeks[df_active_users["age"].isin(range(age_range["min"], age_range["max"]))] >= week),
                    sum(df_active_users["age"].isin(range(age_range["min"], age_range["max"]))),
                )
            for age_range in age_ranges}
        for week in range(0,int(sum(activity_weeks) / df_active_users.shape[0]) + 3)]

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
        reference_date = df_active_users["register_date"].min()

        user_per_day = [
            {
                "Day (Date)": reference_date + dt.timedelta(days=day),
                "Users": df_active_users[
                    df_active_users["register_date"] == reference_date + dt.timedelta(days=day)
                ].shape[0]
            }
        for day in range(7)]

        source_table_chart = [
            user_per_day[row_day] |
            {
                f"{columns_day}D": compute_percent(sum(activity_days[
                    df_active_users["register_date"] == user_per_day[row_day]["Day (Date)"]
                ] >= columns_day), user_per_day[row_day]["Users"])
            for columns_day in range(1, 8)}
        for row_day in range(7)]



        self.df_app = {
            "main_kpis": pd.DataFrame(main_kpis),
            "gender_pie_chart": pd.DataFrame(gender_pie_chart),
            "gender_line_chart": pd.DataFrame(gender_line_chart),
            "age_pie_chart": pd.DataFrame(age_pie_chart),
            "age_line_chart": pd.DataFrame(age_line_chart),
            "source_pie_chart": pd.DataFrame(source_pie_chart),
            "source_line_chart": pd.DataFrame(source_line_chart),
            "source_table_chart": pd.DataFrame(source_table_chart),
        }

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
