from board import Board
import pandas as pd
from shimoku_components_catalog.html_components import beautiful_indicator
import locale
from utils import super_admin_title
from datetime import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EcomerceAnalysis(Board):
    """
    This path is responsible for rendering the Ecommerce Analysis path.
    """

    def __init__(self, self_board: Board):
        """
        Initializes the HiddenIndicatorsPage with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        super().__init__(self_board.shimoku)
        
        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Sales and users"  # Set the menu path for this page
        
        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)
        
        self.shimoku.set_menu_path(name=self.menu_path)  # Set the menu path in Shimoku


    def plot(self):
        """
        Plots the user overview page.
        Each method is responsible for plotting a specific section of the page.
        """

        df = pd.read_csv("data/data.csv")

        df["Fecha_Compra"] = pd.to_datetime(df["Fecha_Compra"], format="%Y-%m-%d")
        df["Month"] = df["Fecha_Compra"].dt.month
        df["month_year"] = df["Fecha_Compra"].dt.strftime("%Y-%m")
        try:
            precio_has_comma = df["Precio"].str.contains(",", regex=False).any()
            cost_has_comma = df["Costo"].str.contains(",", regex=False).any()
        except AttributeError:
            precio_has_comma, cost_has_comma = False, False
            pass
        if precio_has_comma or cost_has_comma:
            df["Precio"] = df["Precio"].str.replace(",", ".", regex=True).astype(float)
            df["Costo"] = df["Costo"].str.replace(",", ".", regex=True).astype(float)
        else:
            df["Precio"] = df["Precio"].astype(float)
            df["Costo"] = df["Costo"].astype(float)

        self.df = df

        self.plot_header()
        self.plot_indicators()
        self.plot_sales_by_weekday()
        self.plot_bar_chart_prods()
        self.plot_table_users()
        self.plot_pie_chart()
        self.plot_stacked_bar()

    def plot_header(self):
        indicator = beautiful_indicator(
            title="Analysis of sales and ecommerce users",
            href="https://shimoku.io/9698715a-a9d3-4253-851e-30640dce743e/drag-and-drop",
            background_url="https://images.unsplash.com/photo-1516414447565-b14be0adf13e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1973&q=80",
        )
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=3,
            cols_size=12,
        )
        self.order += 1
        return True

    def plot_indicators(self):
        self.df = self.df.copy()

        # for formatting numbers with point
        locale.setlocale(locale.LC_NUMERIC, "")


        month_year_data = self.df["month_year"]
        one_month_before = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")
        df_last_month = self.df[month_year_data == one_month_before]
        last_month = df_last_month["month_year"].iloc[0]

        # get gross sales from last month
        gross_sales_last_month = round(df_last_month["Precio"].sum())
        gross_sales_last_month = locale.format_string(
            "%d", gross_sales_last_month, grouping=True
        )
        gross_sales_last_month = gross_sales_last_month.replace(",", ".")

        # get revenue from last month
        df_last_month["revenue"] = df_last_month["Precio"] - df_last_month["Costo"]
        revenue_last_month = round(df_last_month["revenue"].sum())
        revenue_last_month = locale.format_string(
            "%d", revenue_last_month, grouping=True
        )
        revenue_last_month = revenue_last_month.replace(",", ".")

        # get gross sales from current month
        df_current_month = self.df[month_year_data == datetime.today().strftime("%Y-%m")]

        if not df_current_month.empty:
            df_current_month["month_year"].iloc[0]
        else:
            # Handle the case where df_current_month is empty
            current_month = None  # or some appropriate default value

        current_month = df_current_month["month_year"].iloc[0]
        gross_sales_current_month = round(df_current_month["Precio"].sum())
        gross_sales_current_month = locale.format_string(
            "%d", gross_sales_current_month, grouping=True
        )
        gross_sales_current_month = gross_sales_current_month.replace(",", ".")

        data = [
            {
                "description": f"{last_month}",
                "title": "Gross sales last month",
                "value": f"€ {gross_sales_last_month}",
                "color": "default",
                "align": "center",
            },
            {
                "description": f"{last_month}",
                "title": "Net sales last month",
                "value": f"€ {revenue_last_month}",
                "color": "default",
                "align": "center",
            },
            {
                "description": f"{current_month}",
                "title": "Gross sales current month",
                "value": f"€ {gross_sales_current_month}",
                "color": "default",
                "align": "center",
            },
        ]

        self.shimoku.plt.indicator(
            data=data,
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
        )
        self.order += len(data)

        return True

    def plot_sales_by_weekday(self):
       
        self.shimoku.plt.html(
            html=super_admin_title(title="Accumulated daily revenue"),
            order=self.order,
        )

        self.order += 1

        df = self.df.copy()
        
        current_date = pd.Timestamp(datetime.now().date())
        end_of_last_week = current_date - pd.DateOffset(days=current_date.dayofweek + 1)

        # Calculate the start of last week (Monday)
        start_of_last_week = end_of_last_week - pd.DateOffset(days=6)

        # Filter data for the current week
        df_last_week = df[
            (df["Fecha_Compra"] >= start_of_last_week)
            & (df["Fecha_Compra"] <= end_of_last_week)
        ]

        df_last_week["day_of_week"] = df_last_week["Fecha_Compra"].dt.dayofweek
        df_last_week["day_of_week"] = df_last_week["day_of_week"].map(
            {
                0: "Lunes",
                1: "Martes",
                2: "Miércoles",
                3: "Jueves",
                4: "Viernes",
                5: "Sábado",
                6: "Domingo",
            }
        )
        cats = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ]
        df_last_week["revenue"] = round(df_last_week["Precio"] - df_last_week["Costo"])
        revenue_by_day = (
            df_last_week.groupby("day_of_week")["revenue"]
            .sum()
            .reindex(cats)
            .reset_index()
        )
        revenue_by_day.columns = ["Día de la semana", "revenue"]
        revenue_by_day = revenue_by_day.fillna(0)

        # print(revenue_by_day)
        revenue_by_day["Semana pasada"] = revenue_by_day["revenue"].cumsum()

        # print(revenue_by_day)
        current_date = pd.Timestamp(datetime.now().date())
        start_of_week = current_date - pd.DateOffset(days=current_date.dayofweek)
        end_of_week = start_of_week + pd.DateOffset(days=6)

        # Filter data for the current week
        df_this_week_data = df[
            (df["Fecha_Compra"] >= start_of_week) & (df["Fecha_Compra"] <= end_of_week)
        ]

        df_this_week_data["day_of_week"] = df_this_week_data[
            "Fecha_Compra"
        ].dt.dayofweek

        df_this_week_data["day_of_week"] = df_this_week_data["day_of_week"].map(
            {
                0: "Lunes",
                1: "Martes",
                2: "Miércoles",
                3: "Jueves",
                4: "Viernes",
                5: "Sábado",
                6: "Domingo",
            }
        )
        cats = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ]
        df_this_week_data["revenue"] = round(
            df_this_week_data["Precio"] - df_this_week_data["Costo"]
        )
        revenue_by_day_this_week = (
            df_this_week_data.groupby("day_of_week")["revenue"]
            .sum()
            .reindex(cats)
            .reset_index()
        )
        revenue_by_day_this_week.columns = ["Día de la semana", "revenue"]
        revenue_by_day_this_week = revenue_by_day_this_week.fillna(0)
        revenue_by_day["Semana actual"] = revenue_by_day_this_week["revenue"].cumsum()

        dict_revenue_by_day = revenue_by_day.to_dict(orient="records")

        self.shimoku.plt.line(
            data=dict_revenue_by_day,
            x="Día de la semana",
            y=["Semana pasada", "Semana actual"],
            order=self.order,
            rows_size=3,
            cols_size=12,
        )
        self.order += 1

        return True

    def plot_bar_chart_prods(self):
        df = self.df.copy()
        # get 5 most sold products from last month
        month_year_data = df["month_year"]
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        one_month_before = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")

        df_last_month = df[month_year_data == one_month_before]
        grouped_df = (
            df_last_month.groupby("Producto")
            .agg({"Precio": "sum", "Fecha_Compra": "count"})
            .sort_values(by="Precio", ascending=False)
            .reset_index()
        )
        grouped_df.columns = ["Producto", "Total(€)", "Unidades"]
        grouped_df["Total(€)"] = round(grouped_df["Total(€)"])
        first_five_products = grouped_df.loc[:4]
        first_five_products.sort_values(by="Total(€)", inplace=True)

        self.shimoku.plt.html(
            html=super_admin_title(
                title=f"Top 5 best-selling products and most frequent customers of the previous month ({one_month_before})",
            ),
            order=self.order,
        )
        self.order += 1

        print(first_five_products)

        self.shimoku.plt.horizontal_bar(
            data=first_five_products,
            x="Producto",
            y=["Total(€)"],
            order=self.order,
            rows_size=3,
            cols_size=6,
        )

        self.order += 1
        return True

    def plot_table_users(self):
        df = self.df.copy()
        month_year_data = df["month_year"]
        one_month_before = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")

        df_last_month = df[month_year_data == one_month_before]
        grouped_df = (
            df_last_month.groupby(["ClientID"])
            .agg({"Email": "first", "Precio": "sum", "Producto": "count"})
            .sort_values(by="Precio", ascending=False)
            .reset_index()
        )
        grouped_df.drop(columns=["ClientID"], inplace=True)
        grouped_df.columns = ["Email", "Total(€)", "Unidades"]
        grouped_df["Total(€)"] = round(grouped_df["Total(€)"])
        first_five_clients = grouped_df.loc[:4]

        print(first_five_clients)
        print(type(first_five_clients))

        self.shimoku.plt.table(
            data=first_five_clients,
            order=self.order,
            cols_size=5,
            rows_size=3,
            sort_descending=True,
            initial_sort_column="Total(€)",
        )

        self.order += 1
        return True

    def plot_pie_chart(self):
        self.shimoku.plt.html(
            html=super_admin_title(
                title="Active users in total and in the last semester"
            ),
            order=self.order,
        )
        self.order += 1

        self.order += 1
        df = self.df.copy()
        # Count the occurrences of each gender
        df["Genero"] = df["Genero"].replace("Male", "Hombres")
        df["Genero"] = df["Genero"].replace("Female", "Mujeres")
        df["Genero"] = df["Genero"].replace("na", "NA")
        gender_counts = df["Genero"].value_counts()
        gender_df = pd.DataFrame(gender_counts.reset_index())
        gender_df.columns = ["Gender", "Count"]
        self.shimoku.plt.doughnut(
            data=gender_df,
            names="Gender",
            values="Count",
            order=self.order,
            rows_size=3,
            cols_size=6,
            padding="0, 0, 0, 0",
        )
        self.order += 1
        return True

    def plot_stacked_bar(self):
        list_for_dict = list()
        for n_month in range(1, 7):
            month_year_data = self.df["month_year"]
            from datetime import datetime
            from dateutil.relativedelta import relativedelta

            # Assuming n_month is already defined as an integer representing the number of months
            n_month_before = (datetime.now() - relativedelta(months=n_month)).strftime("%Y-%m")

            df_mask = self.df[month_year_data == n_month_before]
            new_dict = dict()
            new_dict["Hombres"] = (df_mask["Genero"] == "Male").sum()
            new_dict["Mujeres"] = (df_mask["Genero"] == "Female").sum()
            new_dict["NA"] = (df_mask["Genero"] == "na").sum()
            new_dict["Total"] = len(df_mask["ClientID"])
            new_dict["Mes"] = n_month_before
            list_for_dict.append(new_dict)

        df_active_users = pd.DataFrame(list_for_dict)
        df_active_users.sort_values("Mes", inplace=True)

        self.shimoku.plt.stacked_bar(
            data=df_active_users,
            x="Mes",
            y=["Total", "Hombres", "Mujeres", "NA"],
            cols_size=5,
            order=self.order,
        )
        self.order += 1
        return True

