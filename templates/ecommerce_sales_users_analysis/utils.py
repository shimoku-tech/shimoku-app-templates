import pandas as pd
from typing import Tuple
import locale
from datetime import datetime
from dateutil.relativedelta import relativedelta


def super_admin_title(title: str) -> str:
    css = """
        .title-section {
            --border-radius: 10px;
            display: flex;
            background: linear-gradient(90deg,  #345DA7 0%, #2e2d88 100%);
            border-radius: var(--border-radius);
            height: 46px;
        }

        .title-section-text {
            color: white;
            display: flex;
            align-items: center;
        }

        .title-section-icon {
            --secondary-accent-500-GW: #FB8500;
            display: flex;
            align-items: center;
            background: linear-gradient(135deg,#FB8500 70px,#0000 0);
            padding: 10px;
            border-top-left-radius: var(--border-radius);
            border-bottom-left-radius: var(--border-radius);
            width: 100px;
        }

        .title-section-icon svg {
            margin-left: 10px;
        }
    """

    html = f"""
        <section class="title-section">
            <div class="title-section-icon">
                <svg width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M18 7V18C18 19.1046 17.1046 20 16 20H6C4.89543 20 4 19.1046 4 18V7" stroke="white" stroke-width="2" stroke-linejoin="round"/>
                  <path d="M1 10L9.66207 2.20414C10.4227 1.51959 11.5773 1.51959 12.3379 2.20414L21 10" stroke="white" stroke-width="2" stroke-linecap="round"/>
                  <path d="M8 15C8 13.8954 8.89543 13 10 13H12C13.1046 13 14 13.8954 14 15V20H8V15Z" stroke="white" stroke-width="2"/>
                </svg>
            </div>
            <p class="title-section-text">
                {title}
            </p>

        </section>
    """

    return craft_html(css, html)


def craft_html(css: str, html: str) -> str:
    html = f"""
        <head>
            <style>
                {css}
            </style>
        </head>
        {html}
    """

    return html


def filter_data_by_week(df:pd.DataFrame, current_date:pd.Timestamp) -> pd.DataFrame:
    # Calculate the start and end of last week
    end_of_last_week = current_date - pd.DateOffset(days=current_date.dayofweek + 1)
    start_of_last_week = end_of_last_week - pd.DateOffset(days=6)

    # Filter data for the last week
    df_last_week = df[
        (df["Purchase_Date"] >= start_of_last_week)
        & (df["Purchase_Date"] <= end_of_last_week)
    ]

    return df_last_week


def process_revenue_by_day(df_week:pd.DataFrame, current_week=False) -> pd.DataFrame:
    # Map day of week to Spanish
    df_week["day_of_week"] = df_week["Purchase_Date"].dt.dayofweek
    df_week["day_of_week"] = df_week["day_of_week"].map(
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

    # Aggregate revenue by day
    cats = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    ]
    df_week["revenue"] = round(df_week["Price"] - df_week["Cost"])
    revenue_by_day = (
        df_week.groupby("day_of_week")["revenue"].sum().reindex(cats).reset_index()
    )
    revenue_by_day.columns = ["Día de la semana", "revenue"]
    revenue_by_day = revenue_by_day.fillna(0)

    # Add cumulative revenue column
    if current_week:
        revenue_by_day["Semana actual"] = revenue_by_day["revenue"].cumsum()
    else:
        revenue_by_day["Semana pasada"] = revenue_by_day["revenue"].cumsum()

    return revenue_by_day


def format_number(number:int) -> str:
    # Format numbers with point
    locale.setlocale(locale.LC_NUMERIC, "")
    formatted_number = locale.format_string("%d", number, grouping=True)
    return formatted_number.replace(",", ".")


def get_last_month_data(df:pd.DataFrame) -> Tuple[str, str, str]:
    # Get data for last month
    month_year_data = df["month_year"]
    one_month_before = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")
    df_last_month = df[month_year_data == one_month_before]
    last_month = df_last_month["month_year"].iloc[0]

    gross_sales_last_month = round(df_last_month["Price"].sum())
    gross_sales_last_month = format_number(gross_sales_last_month)

    df_last_month["revenue"] = df_last_month["Price"] - df_last_month["Cost"]
    revenue_last_month = round(df_last_month["revenue"].sum())
    revenue_last_month = format_number(revenue_last_month)

    return last_month, gross_sales_last_month, revenue_last_month


def get_current_month_data(df:pd.DataFrame) -> Tuple[str, str]:
    # Get data for current month
    month_year_data = df["month_year"]
    df_current_month = df[month_year_data == datetime.today().strftime("%Y-%m")]

    if not df_current_month.empty:
        current_month = df_current_month["month_year"].iloc[0]
        gross_sales_current_month = round(df_current_month["Price"].sum())
        gross_sales_current_month = format_number(gross_sales_current_month)
    else:
        current_month = None
        gross_sales_current_month = "N/A"

    return current_month, gross_sales_current_month
