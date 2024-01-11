from utils.utils import convert_dataframe_to_array, beautiful_header
from board import Board


class SocialMediaSharesPerformance(Board):
    """
    This path is responsible for rendering the social media shares performance page.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Social Media Shares Performance"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self):
        """
        Plots the Social Media Shares Performance page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_posts()
        self.plot_kpi_indicators()
        self.plot_posts_source()

    def plot_header(self):
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        title = "Social Media Shares Performance"

        indicator = beautiful_header(title=title)
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=12,
        )
        self.order += 1

        return True

    def plot_posts(self) -> bool:
        """Bar plot of Social Media Posts

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.bar(
            data=self.df_app["social_media_posts"],
            order=self.order,
            cols_size=4,
            rows_size=3,
            title='Social Media Posts',
            x='Month',
            x_axis_name='Month',
        )
        self.order += 1

        return True

    def plot_kpi_indicators(self) -> bool:
        """Indicatos plot of Main KPIs

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app["main_kpis"]),
            order=self.order,
            cols_size=8,
            rows_size=1,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        return True

    def plot_posts_source(self) -> bool:
        """Line plot of Shares by social Media

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.line(
            data=self.df_app["share_by_social_media"],
            order=self.order,
            cols_size=8,
            rows_size=2,
            title='Shares by Social Media',
            x='Month',
            x_axis_name='Month',
        )
        self.order += 1

        return True