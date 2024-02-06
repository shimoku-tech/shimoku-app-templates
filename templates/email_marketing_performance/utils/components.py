from utils.utils import (
    beautiful_header,
    beautiful_section,
    overview_section,
    results_section,
)

class Components:
    def plot_header(self, title: str) -> bool:
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        self.shimoku.plt.html(
            beautiful_header(title=title),
            order = self.order,
            rows_size = 1,
            cols_size = 12,
        )
        self.order += 1

        return True

    def plot_title_section(self, title: str) -> bool:
        self.shimoku.plt.html(
            beautiful_section(title),
            order = self.order,
            cols_size = 10,
            rows_size = 1,
            padding = "0,1,0,1",
        )
        self.order += 1

        return True

    def plot_description_section(self, model: str) -> bool:
        self.shimoku.plt.html(
            "Hola",
            order = self.order,
            cols_size = 10,
            rows_size = 1,
            padding = "0,1,0,1",
        )
        self.order += 1

    def plot_dates_secuence(self) -> bool:
        data_ = [{
            "color": "success",
            "variant": "contained",
            "description": "This indicator has a Link",
            "targetPath": "/indicators/indicator/1",
            "title": "Target Indicator",
            "align": "left",
            "value": "500€"
        }, {
            "color": "warning",
            "backgroundImage": "https://images.unsplash.com/photo-1535957998253-26ae1ef29506?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=736&q=80",
            "variant": "outlined",
            "description": "This has a background",
            "title": "Super cool indicator",
            "align": "left",
            "value": "Value"
        }, {
            "color": "error",
            "variant": "outlined",
            "description": "This hasn't got any icons",
            "title": "Error indicator",
            "align": "left",
            "value": "Value",
        }, {
            "color": "caution",
            "variant": "contained",
            "description": "Aligned to right and full of icons",
            "title": "Multiple cases",
            "align": "right",
            "value": "Value",
        }]

        self.shimoku.plt.indicator(
            data=data_, order=self.order, rows_size=2, cols_size=12,
        )
        self.order += len(data_) + 1
        return True

    def plot_resumen(self, dataframe_name: str):
        # Html
        self.shimoku.plt.html(
            order = self.order,
            cols_size = 4,
            rows_size = 2,
            padding = "0,1,0,1",
            html = overview_section(self.df_app[dataframe_name])
        )
        self.order += 1
        return True

    def plot_pie(self, title: str, dataframe_name: str) -> bool:
        self.shimoku.plt.pie(
            data=self.df_app[dataframe_name],
            order=self.order,
            title=title,
            cols_size=4,
            rows_size=2,
            padding = "0,1,0,1",
            names='name',
            values='percentage',
        )
        self.order += 1

        return True

    def plot_results(self):
        # Html
        self.shimoku.plt.html(
            order = self.order,
            cols_size = 7,
            rows_size = 4,
            padding="0,2,0,2",
            html = results_section()
        )
        self.order += 1
        return True