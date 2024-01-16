"""
"""

from os import getenv

import datetime as dt
import pandas as pd

import shimoku_api_python as shimoku

from utils import (
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
workspace_id: str = getenv('WORKSPACE_ID')
environment: str = getenv('ENVIRONMENT')


s = shimoku.Client(
    access_token=api_key,
    universe_id=universe_id,
    environment=environment,
    async_execution=True,
    verbosity='INFO',
)
s.reuse_data_sets()
s.set_workspace(workspace_id)

s.set_menu_path('Portfolio')

create_rt_indicators: bool = True


s.plt.html(
    html=data_html_real_time,
    order=0, rows_size=1, cols_size=12,
)


if create_rt_indicators:
    s.plt.indicator(
        data=data_indicator_real_time_events,
        order=1, rows_size=1, cols_size=6,
    )

    s.plt.indicator(
        data=data_indicator_real_time_time_session,
        order=2, rows_size=1, cols_size=6,
    )


s.plt.html(
    html=data_html_summary,
    order=3, rows_size=1, cols_size=12,
)


s.plt.line(
    data=data_line_sessions_date,
    x='date', y=['Sessions'],
    order=4, rows_size=2, cols_size=7,
    title='Total Sessions x day',
)

s.plt.pie(
    data=data_pie,
    names='name', values='value',
    order=5, rows_size=2, cols_size=5,
    title='Devices',
)


s.plt.html(
    html=data_html_beautiful_indicator_anomaly_suite,
    order=6, rows_size=1, cols_size=4,
)

s.plt.html(
    html=data_html_beautiful_indicator_retention_suite,
    order=7, rows_size=1, cols_size=4,
)

s.plt.html(
    html=data_html_beautiful_indicator_stock_suite,
    order=8, rows_size=1, cols_size=4,
)

s.plt.html(
    html=data_html_title_cohort,
    order=9, rows_size=1, cols_size=12,
)

s.plt.heatmap(
    data=data_heatmap,
    x='xAxis', y='yAxis', values='value',
    order=10, rows_size=2, cols_size=12,
)

s.plt.html(
    html=data_html_creativity,
    order=11, rows_size=1, cols_size=12,
)

s.plt.html(
    html=data_html_pug,
    order=12, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_chupa_chups,
    order=13, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_orange,
    order=14, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_voice,
    order=15, rows_size=1, cols_size=3,
)

s.plt.html(
    html=data_html_revenue_prediction,
    order=16, rows_size=1, cols_size=12,
)

df = pd.read_csv('data/portfolio_predictive_line.csv')
df['date'] = pd.to_datetime(df['date']).dt.date
min_date: str = '2022-06-12'
s.plt.predictive_line(
    # title='Revenue prediction',
    data=df.to_dict(orient='records'), x='date', y=['billing'],
    min_value_mark=min_date,
    max_value_mark=df['date'].max().isoformat(),
    order=17, rows_size=2, cols_size=12,
)

s.plt.html(
    html=data_html_boxbutton,
    order=18, rows_size=2, cols_size=7,
)

s.plt.html(
    html=data_html_panel,
    order=19, rows_size=1, cols_size=5,
)

s.workspaces.change_menu_order(uuid=workspace_id, menu_order=['Portfolio'])
