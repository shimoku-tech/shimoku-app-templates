"""
"""

from os import getenv

import datetime as dt
import pandas as pd

import shimoku_api_python as shimoku

from data.portfolio_data import (
    data_html_real_time, data_indicator_real_time_events,
    data_indicator_real_time_time_session,
    data_html_summary, data_line_sessions_date,
    data_pie, data_html_beautiful_indicator_retention_suite,
    data_html_beautiful_indicator_anomaly_suite,
    data_html_title_cohort, data_heatmap,
    data_html_creativity, data_html_pug,
    data_html_orange, data_html_chupa_chups, data_html_voice,
    data_html_boxbutton, data_html_revenue_prediction,
    data_html_panel, data_html_beautiful_indicator_stock_suite,
)

api_key: str = getenv('API_TOKEN')
universe_id: str = getenv('UNIVERSE_ID')
business_id: str = getenv('BUSINESS_ID')
environment: str = getenv('ENVIRONMENT')


s = shimoku.Client(
    access_token=api_key,
    universe_id=universe_id,
    environment=environment,
    business_id=business_id,
    async_execution=True,
    verbosity='INFO',
)

menu_path: str = 'Portfolio'
create_rt_indicators: bool = True


s.plt.html(
    html=data_html_real_time,
    menu_path=menu_path,
    order=0, rows_size=1, cols_size=12,
)


if create_rt_indicators:
    s.plt.indicator(
        data=data_indicator_real_time_events,
        menu_path=menu_path,
        order=1, rows_size=1, cols_size=6,
        value='value',
        color='color',
        header='title',
        footer='description',
        align='align'
    )

    s.plt.indicator(
        data=data_indicator_real_time_time_session,
        menu_path=menu_path,
        order=2, rows_size=1, cols_size=6,
        value='value',
        color='color',
        header='title',
        footer='description',
        align='align'
    )


s.plt.html(
    html=data_html_summary,
    menu_path=menu_path,
    order=3, rows_size=1, cols_size=12,
)


s.plt.line(
    data=data_line_sessions_date,
    x='date', y=['Sessions'],
    menu_path=menu_path,
    order=4, rows_size=2, cols_size=7,
    title='Total Sessions x day',
    option_modifications={'dataZoom': False}
)

s.plt.pie(
    data=data_pie,
    x='name', y='value',
    menu_path=menu_path,
    order=5, rows_size=2, cols_size=5,
    title='Devices',
)


s.plt.html(
    html=data_html_beautiful_indicator_anomaly_suite,
    menu_path=menu_path,
    order=6, rows_size=1, cols_size=4,
)

s.plt.html(
    html=data_html_beautiful_indicator_retention_suite,
    menu_path=menu_path,
    order=7, rows_size=1, cols_size=4,
)

s.plt.html(
    html=data_html_beautiful_indicator_stock_suite,
    menu_path=menu_path,
    order=8, rows_size=1, cols_size=4,
)

s.plt.html(
    html=data_html_title_cohort,
    menu_path=menu_path,
    order=9, rows_size=1, cols_size=12,
)

s.plt.heatmap(
        data=data_heatmap,
        x='xAxis', y='yAxis',
        value='value',
        menu_path=menu_path,
        order=10, rows_size=2, cols_size=12,
)

s.plt.html(
    html=data_html_creativity,
    menu_path=menu_path,
    order=11, rows_size=1, cols_size=12,
)

s.plt.html(
    html=data_html_pug,
    menu_path=menu_path,
    order=12, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_chupa_chups,
    menu_path=menu_path,
    order=13, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_orange,
    menu_path=menu_path,
    order=14, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_voice,
    menu_path=menu_path,
    order=15, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_revenue_prediction,
    menu_path=menu_path,
    order=16, rows_size=1, cols_size=12,
)

df = pd.read_csv('../data/portfolio_predictive_line.csv')
df['date'] = pd.to_datetime(df['date']).dt.date
min_date: str = '2022-06-12'
s.plt.predictive_line(
    # title='Revenue prediction',
    data=df.to_dict(orient='records'), x='date', y=['billing'],
    min_value_mark=min_date,
    max_value_mark=df['date'].max().isoformat(),
    menu_path=menu_path,
    order=17, rows_size=2, cols_size=12,
)

s.plt.html(
    html=data_html_boxbutton,
    menu_path=menu_path,
    order=18, rows_size=2, cols_size=7,
)

s.plt.html(
    html=data_html_panel,
    menu_path=menu_path,
    order=19, rows_size=1, cols_size=5,
)

s.plt.set_apps_orders({'overview': 1})
