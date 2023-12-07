from utils.utils import convert_dataframe_to_array, beautiful_indicator
from board import Board


class UserOverview(Board):
    """
    This path is responsible for rendering the user overview page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Users overview"  # Set the menu path for this page

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the user overview page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_kpi_indicators()
        self.plot_active_users()
        self.plot_active_users_weekly()
        self.plot_newsletter_subscribers()
        self.plot_new_users_weekly()

    def plot_header(self):
        title = "Users overview"
        href = "https://docs.shimoku.com/development/charts/charts/html/background-indicators"
        background_url = "https://st2.depositphotos.com/2001755/8564/i/450/depositphotos_85647140-stock-photo-beautiful-landscape-with-birds.jpg"


        indicator = beautiful_indicator(
            title=title, href=href, background_url=background_url
        )
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=12,
        )
        self.order += 1
        
        return True

    def plot_kpi_indicators(self):
        order = self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app["main_kpis"]),
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        return True

    def plot_active_users(self):
        df = self.df_app["main_kpis"]

        registered_users = df[df["title"] == "Registered Users"]["value"].iloc[0]
        active_users_24 = df[df["title"] == "Active Users 24h"]["value"].iloc[0]
        inactive_users_24 = registered_users - active_users_24

        wau = df[df["title"] == "WAU"]["value"].iloc[0]
        inactive_users_wau = registered_users - wau

        mau = df[df["title"] == "MAU"]["value"].iloc[0]
        inactive_users_mau = registered_users - mau

        # TABS: Create
        self.shimoku.plt.set_tabs_index(
            ("Active_Users_tabs", "Last 24h"),
            order=self.order,
            cols_size=4,
            padding="0,1,0,0",
        )

        # PIE CHART: Active Users (24)
        data = [
            {"name": "Active", "value": active_users_24},
            {"name": "Inactive", "value": inactive_users_24},
        ]
        self.shimoku.plt.pie(
            title="Active Users (24h)",
            data=data,
            order=self.order,
            names="name",
            values="value",
            rows_size=2,
            cols_size=4,
        )
        self.order += 1

        # TABS: Change tab
        self.shimoku.plt.change_current_tab("Last week")

        # PIE CHART: WAU
        data = [
            {"name": "Active", "value": wau},
            {"name": "Inactive", "value": inactive_users_wau},
        ]
        self.shimoku.plt.pie(
            title="Active Users (Week)",
            data=data,
            order=self.order,
            names="name",
            values="value",
            rows_size=2,
            cols_size=4,
        )
        self.order += 1

        # TABS: Change tab
        self.shimoku.plt.change_current_tab("Last month")

        # PIE CHART: MAU
        data = [
            {"name": "Active", "value": mau},
            {"name": "Inactive", "value": inactive_users_mau},
        ]
        self.shimoku.plt.pie(
            title="Active Users (Month)",
            data=data,
            order=self.order,
            names="name",
            values="value",
            rows_size=2,
            cols_size=4,
        )
        self.order += 1

        # TABS: End
        self.shimoku.plt.pop_out_of_tabs_group()

        return True

    def plot_active_users_weekly(self):
        df = self.dfs["active_users"]

        # Crear la columna "year_week"
        df["year_week"] = df["last_login_date"].dt.strftime("%Y-W%U")

        # Agrupar por "year_week" y contar usuarios activos
        result = df.groupby("year_week")["user_id"].count().reset_index()
        result.rename(columns={"user_id": "count_active_users"}, inplace=True)

        # BAR
        self.shimoku.plt.bar(
            title="Active Users weekly",
            data=result.sort_values("year_week", ascending=True),
            x="year_week",
            x_axis_name="Year-Week",
            y_axis_name="Active Users by week",
            order=self.order,
            rows_size=2,
            cols_size=7,
            padding="0,0,1,0",
        )
        self.order += 1

        return True

    def plot_newsletter_subscribers(self):
        df = self.df_app["main_kpis"]

        registered_users = df[df["title"] == "Registered Users"]["value"].iloc[0]
        subscribed_users = df[df["title"] == "Subscribers"]["value"].iloc[0]
        unsubscribed_users = registered_users - subscribed_users

        # PIE CHART: Active Users (24)
        data = [
            {"name": "Subscribers", "value": subscribed_users},
            {"name": "Non subscribers", "value": unsubscribed_users},
        ]
        self.shimoku.plt.pie(
            title="Newsletter Subscribers",
            data=data,
            order=self.order,
            names="name",
            values="value",
            rows_size=2,
            cols_size=4,
            padding="0,1,0,0",
        )
        self.order += 1

        return True

    def plot_new_users_weekly(self):
        df = self.dfs["active_users"]

        ### New users by year_week
        df["year_week"] = df["register_date"].dt.strftime("%Y-W%U")
        result_df = (
            df.groupby(["year_week", "account_type"])
            .size()
            .reset_index(name="count_new_users")
        )
        result_df = result_df.pivot(
            index="year_week", columns="account_type", values="count_new_users"
        ).reset_index()
        result_df.fillna(0, inplace=True)
        dict_result_df = result_df.to_dict(orient="records")

        account_type_list = (result_df.columns.tolist())
        account_type_list.remove("year_week")

        # LINE
        self.shimoku.plt.line(
            title="New Users weekly",
            data=dict_result_df,
            x="year_week",
            y=account_type_list,
            order=self.order,
            rows_size=2,
            cols_size=7,
        )
        self.order += 1

        return True
