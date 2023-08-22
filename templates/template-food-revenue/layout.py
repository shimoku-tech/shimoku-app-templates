# Core python libraries
from typing import Any, Tuple
# Third party
import pandas as pd
import numpy as np
from shimoku_api_python import Client
# Local imports
from transform import filter_by_origin, human_format
from utils import origins, get_data

# --- Tabs Configuration ---
periodpath = "Food"
pt_tab_group = "ptgroup"
origin_tabs_map = {
    'all': {
        'tab_index': (pt_tab_group, "All")
    },
    'web': {
        'tab_index': (pt_tab_group, "Web")
    },
    'app_mobile': {
        'tab_index': (pt_tab_group,"App mobile")
    },
    'store': {
        'tab_index': (pt_tab_group, "Store")
    }
}
period_group = "period_group"
period_tabs = {
    'WoW': {
        'tab_index': (period_group, "Week over Week")
    },
    'MoM': {
        'tab_index': (period_group, "Month over Month")
    },
    'YoY': {
        'tab_index': (period_group, "Year over Year")
    },
}

stackbar_tab_group = "stackbar_tabs"
# wn: Week name map
wn = {
    "current_week": {
        "dfsname": "cw_data",
        "colname": "Current week",
    },
    "last_week": {
        "dfsname": "lw_data",
        "colname": "Last week",
    }
}
# --- End Tabs Configuration ---


def kpis(s: Client, order: int, dfs: dict[str, pd.DataFrame], origin=""):
    """
    Indicators
    """

    def calculate_kpis(df: pd.DataFrame):
        """
        Calculate values for indicators
        """

        data: pd.DataFrame = filter_by_origin(df, origin)

        # number of orders
        orders_kpi = data['order_id'].nunique()

        # revenue made
        revenue = data['prod_billing'].sum()

        # How many products were sold
        prod_sold = data['quantity'].sum()

        return {
            'orders': orders_kpi,
            'revenue': revenue,
            'products_sold': prod_sold,
        }

    # Calculate kpis for each week period
    cw_kpis = calculate_kpis(dfs['cw_data'])
    lw_kpis = calculate_kpis(dfs['lw_data'])

    def plot_indicator(data: dict[str, Any], kpi_name: str, order: int, options=None):
        """
        Plots the indicators to the dashboard
        """
        if options is None:
            options = {}

        cw_kpi = cw_kpis[kpi_name]
        lw_kpi = lw_kpis[kpi_name]

        kpi_diff = cw_kpi - lw_kpi

        # Put difference in the footer
        common_data = {
            'align': 'center',
            'value': human_format(cw_kpi),
            'icon': '',
            'bigIcon': '',
            'description': f"CW {human_format(cw_kpi)} - SPLW {human_format(lw_kpi)}"
        }

        if kpi_diff < 0:
            common_data['color'] = 'warning'
            common_data['icon'] = 'Line/arrow-down'
            common_data['value'] = f"{human_format((-1)*kpi_diff)}"
        else:
            common_data['color'] = 'success'
            common_data['icon'] = "Line/arrow-up"
            common_data['value'] = f"{human_format(kpi_diff)}"

        # Default indicator parameter, extend via the 'options'
        # parameter
        s.plt.indicator(
            data={**data, **common_data},
            order=order,
            cols_size=3,
            rows_size=1,
            **options
        )

    next_order = order

    # Current week
    title = "CW - Current Week status Vs SPLW - Same Period Last Week"

    s.plt.html(
        order=next_order, cols_size=12,
        html=s.html_components.panel(
            text=title,
            href="",
        ),
    )

    hash_tag = "(#)"
    next_order += 1
    plot_indicator(
        data={'title': f"Orders {hash_tag}"},
        kpi_name='orders',
        order=next_order,
        options={'padding': '0, 0, 0, 2'}
    )

    next_order += 1
    plot_indicator(
        data={'title': f"Revenue (€)"},
        kpi_name='revenue',
        order=next_order,
    )

    next_order += 1
    plot_indicator(
        data={'title': f"Products sold {hash_tag}"},
        kpi_name='products_sold',
        order=next_order,
        options={'padding': '0, 2, 0, 0'},
    )

    return next_order+1


def stacked_bar_sales(
    s: Client, order: int, dfs: dict[str, pd.DataFrame],
    origins: list[str], parent_tabs_index: tuple[str, str]
):
    """
    Plots a stacked bar chart that compare revenues of the week by origin
    """

    def get_stack_data(origin: str, period: str):
        """
        Get the grouped data needed for the stack chart

        Filters:
        - period: current_week, last_week
        - origin: web, app_mobile, store, all
        """

        dfsname = wn[period]['dfsname']

        data = filter_by_origin(dfs[dfsname], origin)

        grouped_data = data.groupby('date', as_index=False)['prod_billing'].sum()

        # Rename columns
        grouped_data.rename(
            columns={'prod_billing': wn[period]['colname']},
            inplace=True
        )

        return grouped_data

    def plot_stacked(week: str):
        """
        Plots the stacked bar chart
        """

        # Build data
        basedfs = pd.DataFrame(data={
            'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        })

        week_colname = wn[week]['colname']
        for origin in origins:
            revenue = get_stack_data(
                origin,
                week,
            )
            # Add revenue by origin
            pt_colname = origin_tabs_map[origin]['tab_index'][1]
            basedfs[pt_colname] = revenue[week_colname]

        # Fill in with 0 NAN values
        basedfs.fillna(0, inplace=True)

        # Format numbers to two decimals
        basedfs.loc[:, 'Web'] = basedfs['Web'].map('{:.2f}'.format)
        basedfs.loc[:, 'App mobile'] = basedfs['App mobile'].map('{:.2f}'.format)
        basedfs.loc[:, 'Store'] = basedfs['Store'].map('{:.2f}'.format)

        s.plt.stacked_bar(
            title=week_colname,
            data=basedfs,
            x='Day',
            order=0,
            cols_size=12,
        )

    s.plt.set_tabs_index(
        tabs_index=(stackbar_tab_group, list(wn.keys())[0]), just_labels=True,
        sticky=False, order=order, parent_tabs_index=parent_tabs_index
    )
    for week in wn.keys():
        s.plt.change_current_tab(week)
        plot_stacked(week)

    s.plt.set_tabs_index(tabs_index=parent_tabs_index)
    return order + 1


def product_type_table(s: Client, order: int, dfs: dict[str, pd.DataFrame], origin: str) -> int:
    """
    The table shows the revenue
    """
    def get_products_data(column: str, rn_cols: dict[str, str]):
        """
        """
        aggregations = {
            'revenue': ('prod_billing', 'sum'),
            'quantity': ('quantity', "sum"),
            'origin': ('origin','first'),
        }

        filter_by_origin(dfs['cw_data'], origin)
        cw_revenue = filter_by_origin(dfs['cw_data'], origin).groupby(column, as_index=False).agg(
            **aggregations,
        )
        lw_revenue = filter_by_origin(dfs['lw_data'], origin).groupby(column, as_index=False).agg(
            **aggregations
        )
        pt_table_plan = pd.merge(cw_revenue,lw_revenue, on=[column, 'origin'], how="outer")

        pt_table_plan.fillna(0, inplace=True)

        # -- Calculate growth rate, based on current week vs last week

        # Revenue
        replace_vals = ((np.inf, -np.inf, np.NAN, -100), (0, 0, 0, 0))
        pt_table_plan['Rev Growth'] = (
            ((pt_table_plan['revenue_x'] - pt_table_plan['revenue_y']) / pt_table_plan['revenue_y']) * 100
        ).replace(
            replace_vals[0], replace_vals[1]
        )
        # Quantity
        pt_table_plan['Qty Growth'] = (
            ((pt_table_plan['quantity_x'] - pt_table_plan['quantity_y']) / pt_table_plan['quantity_y']) * 100
        ).replace(
            replace_vals[0], replace_vals[1]
        )
        # --

        def get_percent_cat(percentage: float):
            if percentage > 0:
                return 'Up'
            if percentage < 0:
                return 'Down'
            if percentage == 0:
                return 'No change'

        # Add a category to the percentage ranges
        pt_table_plan['Qty Change'] = pt_table_plan['Qty Growth'].apply(get_percent_cat)
        pt_table_plan['Rev Change'] = pt_table_plan['Rev Growth'].apply(get_percent_cat)

        # Format numbers in table before plotting
        pt_table_plan.loc[:,'revenue_x'] = pt_table_plan['revenue_x'].map('{:.0f}'.format)
        pt_table_plan.loc[:,'revenue_y'] = pt_table_plan['revenue_y'].map('{:.0f}'.format)
        pt_table_plan.loc[:,'Rev Growth'] = pt_table_plan['Rev Growth'].map('{:.1f}'.format)
        pt_table_plan.loc[:,'Qty Growth'] = pt_table_plan['Qty Growth'].map('{:.1f}'.format)

        # Make columns names more readable for plotting
        pt_table_plan.rename(
            columns={
                'revenue_x':'Revenue CW (€)',
                'quantity_x': 'Quantity CW',
                'revenue_y': 'Revenue SPLW (€)',
                'quantity_y': 'Quantity SPLW',
                'origin': 'Origin',
                 **rn_cols,
            },
            inplace=True)
        return pt_table_plan

    # Products
    table = get_products_data(
        column='product_name', rn_cols={'product_name': 'Product'}
    )

    # Reorder columns
    table = table[['Product', 'Revenue SPLW (€)', 'Revenue CW (€)', 'Rev Growth', 'Rev Change', 'Quantity SPLW', 'Quantity CW', 'Qty Growth', 'Qty Change', 'Origin']]

    s.plt.html(
        order=order,
        html=s.html_components.panel(
            text="Compare the last two weeks, see which products grew in revenue",
            href=""
        )
    )

    color_dict = {
        'Up': 'active',
        'Down': 'error',
        'No change': 'neutral',
    }

    base_filters = ['Rev Change']
    s.plt.table(
        data=table,
        categorical_columns=base_filters + ['Origin'] if origin == "all" else base_filters,
        menu_path=periodpath,
        order=order+1,
        label_columns={
            'Qty Change': color_dict,
            'Rev Change': color_dict,
        },
    )

    return order+2


def top_ten_winners(
    s: Client, order: int, dfs: dict[str, pd.DataFrame],
    origin: str
) -> int:
    """
    Top 10 Product Winners WoW & Top 10 Product Losers WoW

    This chart is useful to see wich products gained and lost more revenue
    compared to last week
    """

    top_ten_tabgroup = f"top_ten_tabgroup_{origin}"
    tabs_index = origin_tabs_map[origin]['tab_index']
    menupath = periodpath

    def plot_chart(agg_col: str, tab: str, order: int):
        def group_rev(df: pd.DataFrame):
            """
            Filters data by origin, then groups and sums the products by revenue or quantity
            """
            return filter_by_origin(df, origin).groupby('product_name', as_index=False).agg({agg_col: "sum"})

        cw_rev = group_rev(dfs['cw_data'])
        lw_rev = group_rev(dfs['lw_data'])

        # Join tables, to compare revenues over cw & lw
        df = pd.merge(cw_rev, lw_rev, on='product_name', how='outer')

        # Rename columns

        df.rename(
            columns={
                f"{agg_col}_x": 'cw_rev',
                f"{agg_col}_y": 'lw_rev',
                f"product_name": 'Product name',
            }, inplace= True,
        )

        df.fillna(0, inplace=True)

        # Calculate difference
        df['Diff'] = df['cw_rev'] - df['lw_rev']

        # Round values to two decimal places
        df = df.round(1)

        # Order by diff
        df.sort_values(['Diff'], ascending=False, inplace=True)

        # Skip those products that had the same revenue in
        df.query(f"Diff != 0", inplace=True)

        qty = 10
        df_winners = df.query(f"Diff > 0").head(n=qty)  # Top 10 best revenue

        # Top 10 worst revenue
        df_loosers = df.query(f" Diff < 0 & cw_rev > 0").tail(n=qty)
        df_loosers.sort_values(["Diff"], ascending=True, inplace=True)

        # Invert order because the bar chart inverts it
        df_winners.sort_values(['Diff'], ascending=True, inplace=True)

        next_order = order

        positiveDataOps = {
            'label': {
                'position': 'right',
            },
            'itemStyle': {
                'color': 'var(--chart-C2)',
                'borderRadius': [0, 9, 9, 0],
            },
            'emphasis': {
                'itemStyle': {
                    'color': 'var(--chart-C2)',
                    'borderColor': 'var(--chart-C2)',
                }
            },
        }

        negDataOps = {
            'label': {
                'position': 'left',
            },
            'itemStyle': {
                'color': 'var(--complementary-red-light)',
                'borderRadius': [9, 0, 0, 9],
            },
            'emphasis': {
                'itemStyle': {
                    'color': 'var(--complementary-red-light)',
                    'borderColor': 'var(--complementary-red-light)',
                }
            },
        }

        # Assign neg and positive values
        series_data_neg = [{
            'value': val,
            **negDataOps,
        } for val in list(df_loosers['Diff'])]

        series_data_pos = [{
            'value': val,
            **positiveDataOps,
        } for val in list(df_winners['Diff'])]

        # Join neg and positive options together
        series_data = series_data_neg + series_data_pos

        y_data = list(df_loosers['Product name']) + list(df_winners['Product name'])

        # Set general echarts options
        options = {
            'title': {
                'text': f"Top 10 Winners and Losers"
            },
            'toolbox': {
                'right': 10,
                'feature': {
                    'saveAsImage': {},
                    'dataView': {},
                }
            },
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'shadow'
                }
            },
            'grid': {
                'top': 80,
                'bottom': 30
            },
            'xAxis': {
                'type': 'value',
                'axisLine': {'show': False},
                'position': 'top',
                'axisLabel': {'show': False},
                'splitLine': {
                    'show': False,
                }
            },
            'yAxis': {
                'type': 'category',
                'axisLine': {'show': True},
                'axisLabel': {'show': False},
                'axisTick': {'show': False},
                'splitLine': {'show': False},
                'data': y_data,
            },
            'series': [
                {
                    'name': 'Revenue',
                    'type': 'bar',
                    'stack': 'Total',
                    'smooth': True,
                    'label': {
                        'show': True,
                        'width': 270,
                        'overflow': 'truncate',
                        # 'formatter': '{b}, {c} €',
                        'formatter': '{b}\n{c} €' if tab == "Revenue (€)" else '{b}\n{c}',
                    },
                    'data': series_data,
                }
            ]
        }

        next_order = order
        s.plt.free_echarts(
            data=[{}],
            options=options,
            order=next_order,
            cols_size=12,
            rows_size=5,
        )

        return next_order

    s.plt.set_tabs_index(tabs_index)
    s.plt.html(
        html=s.html_components.panel(
            text="Products that didn't sold this current week, are not shown.",
            symbol_name="info",
            href="",
        ), order=order,
    )

    # Plot charts
    s.plt.set_tabs_index((top_ten_tabgroup, "Revenue (€)"), order=order+1,
                         just_labels=True, sticky=False, parent_tabs_index=tabs_index)
    plot_chart(agg_col="prod_billing", tab="Revenue (€)", order=0)
    s.plt.change_current_tab("Units Sold")
    plot_chart(agg_col="quantity", tab="Units Sold", order=0)

    s.plt.set_tabs_index(tabs_index)
    return order+2


def plot_dashboard(s: Client):
    """
    Main function, plots the dashboard
    """
    # Get the two dataframes we will be working
    # cw_data, lw_data
    dfs = get_data()

    # Get origins including the special 'all'
    all_origins = ['all'] + origins

    s.set_menu_path(periodpath)
    s.plt.clear_menu_path()
    for period in period_tabs.keys():
        period_tab_index = period_tabs[period]['tab_index']
        s.plt.set_tabs_index(period_tabs[period]['tab_index'], order=0)

        if period != "WoW":
            # dummy stuff, so the other tabs are visible
            s.plt.html(
                order=1,
                html=s.html_components.panel(
                    text=f"{period_tab_index[1]}",
                    href="",
                )
            )
        if period == "WoW":
            for origin in all_origins:
                tabs_index = origin_tabs_map[origin]['tab_index']
                s.plt.set_tabs_index(tabs_index, order=2, parent_tabs_index=period_tabs[period]['tab_index'],
                                     sticky=False, just_labels=True)
                order = kpis(s, 1, dfs, origin)
                # Only plot the stacked bar chart in all tab
                if origin == "all":
                    s.plt.html(
                        order=order,
                        html=s.html_components.panel(
                            text="Revenue Week Over Week",
                            href="",
                        )
                    )
                    stacked_bar_sales(s, order+1, dfs, origins, tabs_index)

                order = top_ten_winners(s, order+2, dfs, origin)

                product_type_table(s, order, dfs, origin)
