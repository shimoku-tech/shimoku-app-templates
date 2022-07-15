"""
"""

from os import getenv

import datetime as dt
import pandas as pd

import shimoku_api_python as shimoku
from shimoku_components_catalog.html_components import (
    create_h1_title, button_click_to_new_tab, beautiful_indicator,
    box_with_button, panel,
)

api_key: str = getenv('API_TOKEN')
universe_id: str = getenv('UNIVERSE_ID')
business_id: str = getenv('BUSINESS_ID')
environment: str = getenv('ENVIRONMENT')


s = shimoku.Client(
    config={'access_token': api_key},
    universe_id=universe_id,
    environment=environment,
)
s.plt.set_business(business_id=business_id)
menu_path: str = 'Portfolio'
create_rt_indicators: bool = True


html = create_h1_title(title='Real-time', subtitle='Users')
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=0, rows_size=1, cols_size=12,
)


if create_rt_indicators:
    data_ = [
        {
            'description': '27 / 05 / 2022 · 11:14:54',
            'title': 'Events',
            'value': '552,298',
            'color': '',
            'align': 'left'
        }
    ]
    s.plt.indicator(
        data=data_,
        menu_path=menu_path,
        order=1, rows_size=1, cols_size=6,
        value='value',
        color='color',
        header='title',
        footer='description',
        align='align'
    )


    data_ = [
        {
            'description': 'In minutes',
            'title': 'Time Sessions AVG',
            'value': '1,59',
            'color': '',
            'align': 'left'
        }
    ]
    s.plt.indicator(
        data=data_,
        menu_path=menu_path,
        order=2, rows_size=1, cols_size=6,
        value='value',
        color='color',
        header='title',
        footer='description',
        align='align'
    )


html = create_h1_title(title='Summary', subtitle='Results 28 days previous')
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=3, rows_size=1, cols_size=12,
)


data = [
    {'date': 1, 'Sessions': 360},
    {'date': 2, 'Sessions': 164},
    {'date': 3, 'Sessions': 132},
    {'date': 3, 'Sessions': 214},
    {'date': 4, 'Sessions': 301},
    {'date': 5, 'Sessions': 105},
    {'date': 6, 'Sessions': 156},
    {'date': 7, 'Sessions': 245},
    {'date': 8, 'Sessions': 321},
    {'date': 9, 'Sessions': 204},
    {'date': 10, 'Sessions': 262},
    {'date': 11, 'Sessions': 300},
    {'date': 12, 'Sessions': 324},
    {'date': 13, 'Sessions': 406},
    {'date': 14, 'Sessions': 239},
    {'date': 15, 'Sessions': 297},
    {'date': 16, 'Sessions': 424},
    {'date': 17, 'Sessions': 311},
    {'date': 18, 'Sessions': 237},
    {'date': 19, 'Sessions': 109},
    {'date': 20, 'Sessions': 70},
    {'date': 21, 'Sessions': 132},
    {'date': 22, 'Sessions': 320},
    {'date': 23, 'Sessions': 346},
    {'date': 24, 'Sessions': 479},
    {'date': 25, 'Sessions': 560},
]
s.plt.line(
    data=data,
    x='date', y=['Sessions'],
    menu_path=menu_path,
    order=4, rows_size=2, cols_size=7,
    title='Total Sessions x day',
    option_modifications={'dataZoom': False}
)

data_ = [
    {'name': 'Mobile', 'value': 12478},
    {'name': 'Tablet', 'value': 3217},
    {'name': 'Desktop', 'value': 9418},
]

s.plt.pie(
    data=data_,
    x='name', y='value',
    menu_path=menu_path,
    order=5, rows_size=2, cols_size=5,
    title='Devices',
)


html = beautiful_indicator(
    title='View Anomaly Suite',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6d9e984908a5aca6a1_shim-anomaly-bg-s.jpg',
    href='https://develop.shimoku.io/big-bang',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=6, rows_size=1, cols_size=4,
)


html = beautiful_indicator(
    title='View Retention Suite',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6dca821c951f9554e4_shim-retention-bg-s.jpg',
    href='https://develop.shimoku.io/big-bang',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=7, rows_size=1, cols_size=4,
)


html = beautiful_indicator(
    title='View Stock Suite',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6d1dcb0d6fbb50159e_shim-stock-bg-s.jpg',
    href='https://develop.shimoku.io/big-bang',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=8, rows_size=1, cols_size=4,
)


html = create_h1_title(title='Cohort', subtitle='Results')
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=9, rows_size=1, cols_size=12,
)


data_ = [
        {
            "xAxis": "Monday",
            "yAxis": "12 a.m",
            "value": 9
        },
        {
            "xAxis": "Monday",
            "yAxis": "6 p.m",
            "value": 10
        },
        {
            "xAxis": "Monday",
            "yAxis": "12 p.m",
            "value": 9
        },
        {
            "xAxis": "Monday",
            "yAxis": "6 a.m",
            "value": 10
        },
        {
            "xAxis": "Tuesday",
            "yAxis": "12 a.m",
            "value": 9
        },
        {
            "xAxis": "Tuesday",
            "yAxis": "6 p.m",
            "value": 9
        },
        {
            "xAxis": "Tuesday",
            "yAxis": "12 p.m",
            "value": 8
        },
        {
            "xAxis": "Tuesday",
            "yAxis": "6 a.m",
            "value": 0
        },
        {
            "xAxis": "Wednesday",
            "yAxis": "12 a.m",
            "value": 2
        },
        {
            "xAxis": "Wednesday",
            "yAxis": "6 p.m",
            "value": 7
        },
        {
            "xAxis": "Wednesday",
            "yAxis": "12 p.m",
            "value": 0
        },
        {
            "xAxis": "Wednesday",
            "yAxis": "6 a.m",
            "value": 2
        },
        {
            "xAxis": "Thursday",
            "yAxis": "12 a.m",
            "value": 4
        },
        {
            "xAxis": "Thursday",
            "yAxis": "6 p.m",
            "value": 0
        },
        {
            "xAxis": "Thursday",
            "yAxis": "12 p.m",
            "value": 1
        },
        {
            "xAxis": "Thursday",
            "yAxis": "6 a.m",
            "value": 6
        }
    ]
s.plt.heatmap(
        data=data_,
        x='xAxis', y='yAxis',
        value='value',
        menu_path=menu_path,
        order=10, rows_size=2, cols_size=12,
)


html = create_h1_title(title='Creativity analysis', subtitle='New campaign 2022')
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=11, rows_size=1, cols_size=12,
)


html = button_click_to_new_tab(
    title='Pug',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080dbb92e78ae2b2cdbe2_pug.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080dbb92e78ae2b2cdbe2_pug.jpg'
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=12, rows_size=1, cols_size=3,
)


html = button_click_to_new_tab(
    title='Chupa-Chups',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db5f002762a688eae7_chup.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db5f002762a688eae7_chup.jpg',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=13, rows_size=1, cols_size=3,
)


html = button_click_to_new_tab(
    title='Orange',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db9e9849832eace72f_orange.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db9e9849832eace72f_orange.jpg',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=14, rows_size=1, cols_size=3,
)


html = button_click_to_new_tab(
    title='Voice',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db484a3c2ebeb21a0d_voice.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db484a3c2ebeb21a0d_voice.jpg',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=15, rows_size=1, cols_size=3,
)


html = create_h1_title(title='Revenue prediction', subtitle='Revenue in €')
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=16, rows_size=1, cols_size=12,
)
df = pd.read_csv('../../data/test/pred_data.csv')
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


html = box_with_button(
    href='https://www.shimoku.com',
    title='Shimoku is a White Label App',
    line='Share with your clients your own App,  not an Standard',
)
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=18, rows_size=2, cols_size=7,
)


html = panel(href='www.shimoku.com', text='Attention, this is a brief explanation about the information in this section')
s.plt.html(
    html=html,
    menu_path=menu_path,
    order=19, rows_size=1, cols_size=5,
)

s.plt.set_apps_orders({'overview': 1})
