import pandas as pd
import os
from re import sub
import datetime as dt
from shimoku_api_python import ShimokuPalette


def get_data(file_names: list):
    """Returns a dictionary of dataframes, one item for each file of file_names array parameter.
    Example:
    file_names = ['data/active_users.csv', 'data/shop_events.csv', ...]
    dict_dfs ['active_users'] = A dataframe with 'data/active_users.csv' CSV file
    dict_dfs ['shop_events'] = A dataframe with 'data/shop_events.csv' CSV file

    Args:
        dict_dfs (dict): A dictionary of dataframes.
    """

    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)

        # Finds the columns containing "_date" in their name
        columnas_fecha = [col for col in df.columns if "_date" in col]

        # Convert columns identified with "_date" to datetime
        df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime)

        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs


def convert_dataframe_to_array(df: pd.DataFrame):
    """Return a list, convert a dataframe to a list.

    Args:
        df (pd.DataFrame): A dataFrame to convert.

    Returns:
        new_data (List): A List with the dataframe information.
    """
    # Get list of column names
    columns_to_include = df.columns.tolist()
    new_data = []

    for index, row in df.iterrows():
        new_dict = {column: row[column] for column in columns_to_include}
        new_data.append(new_dict)

    return new_data

def beautiful_header(title: str) -> str:
    """Return a HTML structure to plot the header on the menu path.

    Args:
        title (str): title of the header in the menu path.

    Returns:
        str: HTML structure to plot the header.
    """
    return (
        "<head>"
        "<style>"  # Styles title
        ".component-title{height:auto; width:100%; "
        "border-radius:16px; padding:16px;"
        "display:flex; align-items:center;"
        "background-color:var(--chart-C1); color:var(--color-white);}"
        "</style>"
        # Start icons style
        "<style>.big-icon-banner"
        "{width:48px; height: 48px; display: flex;"
        "margin-right: 16px;"
        "justify-content: center;"
        "align-items: center;"
        "background-size: contain;"
        "background-position: center;"
        "background-repeat: no-repeat;"
        "background-image: url('https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63594ccf3f311a98d72faff7_suite-customer-b.svg');}"
        "</style>"
        # End icons style
        "<style>.base-white{color:var(--color-white);}</style>"
        "</head>"  # Styles subtitle
        "<div class='component-title'>"
        "<div class='big-icon-banner'></div>"
        "<div class='text-block'>"
        "<h1>" + title + "</h1>"
        "</div>"
    )

def categories(df: pd.DataFrame) -> str:
    """Return a string of the HTML structure with the differents categories used on the
    Category section for each tab.

    Args:
        df (pd.DataFrame): dataframe which contains the categories and the users count.

    Returns:
        str: string of the HTML structure with the differents categories.
    """
    total = df["value"].apply('sum')

    sections = [
        ("<div style='display: flex; justify-content: center; flex-wrap: wrap;column-gap: 5%;'>"
        f"<div "
        f"style='display: flex;"
        f"justify-content: center;"
        f"background-color: {ShimokuPalette['CHART_C%d'%(1 + index%10)].value};"
        f"width: 40%;"
        f"border-radius: 10px;'>"
        f"{row['name']}"
        f"</div>"
        f"<div>{compute_percent(row['value'], total):05.2f}% ({row['value']:03d})</div>"
        "</div>")
    for index, row in df.iterrows()]
    return "".join(sections)

def compute_percent(value: float, total: float) -> float:
    """Compute the percentage value.

    Args:
        value (float): fraction of the total value.
        total (float): total value.

    Returns:
        float: percentage value.
    """
    return value * 100 / total if total != 0 else 0

def cohort_colors() -> dict:
    """Return a dictionary which contains the range for each percentage as key and
    the color to each range as value.

    Returns:
        dict: dictionary with a range and colors.
    """
    return {
        (0, 10): "#eaffed",
        (10, 20): "#d0fdd7",
        (20, 30): "#9bfab0",
        (30, 50): "#64c27b",
        (50, 100): "#2a8c4a",
    }

def generate_category(
    df_users:pd.DataFrame,
    column_name: str,
) -> list:
    """Generate a list of dictiorany with the category and its respective users number

    Args:
        df_users (pd.DataFrame): Dataframe with the data users
        column_name (str): Column name to filter the data

    Returns:
        list: List of dictionary with the category and users number
    """
    return [
        {
            'name': category,
            'value': df_users[df_users[column_name] == category].shape[0],
        }
    for category in df_users[column_name].unique()]

def generate_life_time(
    df_users: pd.DataFrame,
    activity_weeks: pd.DataFrame,
    filter_flag: bool=False,
    column_name: str="",
) -> list:
    """Return the Users Life Time by category if the filter_flag is True.

    Args:
        df_users (pd.DataFrame): Dataframe with the data users
        column_name (str): Column name to filter the data
        activity_weeks (pd.DataFrame): Dataframe with the users activity in weeks
        filter_flag (bool, optional): Flag to filter the data. Defaults to False.

    Returns:
        list: List of dictionary with users life time by category
    """
    if filter_flag:
        return [
            {
                "week":f"W{week}",
            } |
            {
                category: compute_percent(
                    sum(activity_weeks[df_users[column_name] == category] >= week),
                    df_users[df_users[column_name] == category].shape[0],
                )
            for category in df_users[column_name].unique()}
        for week in range(0,int(sum(activity_weeks) / df_users.shape[0]) + 3)]
    else:
        return [
            {
                "week":f"W{week}",
                'users': compute_percent(sum(activity_weeks >= week), df_users.shape[0]),
            }
        for week in range(0,int(sum(activity_weeks) / df_users.shape[0]) + 3)]

def cohort_analysis(
    df_users: pd.DataFrame,
    activity_weeks: pd.DataFrame,
    week_range: int,
    reference_date: dt.datetime,
    filter_flag: bool=False,
    column_name: str="",
    column_option: str=""
) -> list:
    """Return the Cohort Analysis consider all the data or grouping by category

    Args:
        df_users (pd.DataFrame): Dataframe with the data users.
        activity_weeks (pd.DataFrame): Dataframe with the users activity in weeks.
        week_range (int): week range to consider in the filter.
        reference_date (dt.datetime): reference data to filter the data.
        filter_flag (bool, optional): Flag to filter the data. Defaults to False.
        column_name (str): Column name to filter the data. Defaults to ""-
        column_option (str, optional): Category option to filter the data. Defaults to "".

    Returns:
        list: List of dictionary of the cohort analysis
    """
    user_per_week = [
        {
            "Week (Date)": reference_date + dt.timedelta(days=7*week),
            "Users": sum(users_by_weeks_by_category(df_users,reference_date,week,filter_flag, column_name, column_option)),
        }
    for week in range(week_range)]

    return [user_per_week[row_week] |
        {
            f"W{columns_week}": compute_percent(
                sum(activity_weeks[
                    users_by_weeks_by_category(df_users, reference_date,row_week, filter_flag, column_name, column_option)
                ] >= columns_week),
                user_per_week[row_week]["Users"],
            ) if columns_week + row_week < week_range + 1 else 0
        for columns_week in range(week_range + 1)}
    for row_week in range(week_range)]

def users_by_weeks_by_category(
    df_users: pd.DataFrame,
    reference_date: dt.datetime,
    week: int,
    filter_flag: bool=False,
    column_name: str="",
    column_option: str="",
) -> pd.DataFrame:
    """Return a Dataframe with the boolean value if a users will be considering in the filter.

    Args:
        df_users (pd.DataFrame): Dataframe with the data users.
        reference_date (dt.datetime): reference data to filter the data.
        week (int): number week to consider in the filter.
        filter_flag (bool, optional): Flag to filter the data. Defaults to False.
        column_name (str): Column name to filter the data. Defaults to ""-
        column_option (str, optional): Category option to filter the data. Defaults to "".

    Returns:
        pd.DataFrame: Boolean series if a users will be considering in the filter
    """
    filter_date = df_users["register_date"].between(
        reference_date + dt.timedelta(days=7*week),
        reference_date + dt.timedelta(days= 7*(week + 1)),
    )
    return filter_date & (df_users[column_name] == column_option) if filter_flag else filter_date