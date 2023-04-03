"""
"""

from shimoku_components_catalog.html_components import (
    create_h1_title, button_click_to_new_tab, beautiful_indicator,
    box_with_button, panel,
)


data_html_real_time = create_h1_title(title='Real-time', subtitle='Users')

data_indicator_real_time_events = [
    {
        'description': '27 / 05 / 2022 · 11:14:54',
        'title': 'Events',
        'value': '552,298',
        'color': '',
        'align': 'left'
    }
]

data_indicator_real_time_time_session = [
    {
        'description': 'In minutes',
        'title': 'Time Sessions AVG',
        'value': '1,59',
        'color': '',
        'align': 'left'
    }
]

data_html_summary = create_h1_title(title='Summary', subtitle='Results 28 days previous')

data_line_sessions_date = [
    {'date': 0, 'Sessions': 360},
    {'date': 1, 'Sessions': 164},
    {'date': 2, 'Sessions': 132},
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

data_pie = [
    {'name': 'Mobile', 'value': 12478},
    {'name': 'Tablet', 'value': 3217},
    {'name': 'Desktop', 'value': 9418},
]

data_html_beautiful_indicator_anomaly_suite = beautiful_indicator(
    title='View Anomaly Suite',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6d9e984908a5aca6a1_shim-anomaly-bg-s.jpg',
    href='https://develop.shimoku.io/big-bang',
)

data_html_beautiful_indicator_retention_suite = beautiful_indicator(
    title='View Retention Suite',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6dca821c951f9554e4_shim-retention-bg-s.jpg',
    href='https://develop.shimoku.io/big-bang',
)

data_html_beautiful_indicator_stock_suite = beautiful_indicator(
    title='View Stock Suite',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a07a6d1dcb0d6fbb50159e_shim-stock-bg-s.jpg',
    href='https://develop.shimoku.io/big-bang',
)

data_html_title_cohort = create_h1_title(title='Cohort', subtitle='Results')

data_heatmap = [
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

data_html_creativity = create_h1_title(title='Creativity analysis', subtitle='New campaign 2022')

data_html_pug = button_click_to_new_tab(
    title='Pug',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080dbb92e78ae2b2cdbe2_pug.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080dbb92e78ae2b2cdbe2_pug.jpg'
)

data_html_chupa_chups = button_click_to_new_tab(
    title='Chupa-Chups',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db5f002762a688eae7_chup.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db5f002762a688eae7_chup.jpg',
)

data_html_orange = button_click_to_new_tab(
    title='Orange',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db9e9849832eace72f_orange.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db9e9849832eace72f_orange.jpg',
)

data_html_voice = button_click_to_new_tab(
    title='Voice',
    background_url='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db484a3c2ebeb21a0d_voice.jpg',
    href='https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/62a080db484a3c2ebeb21a0d_voice.jpg',
)

data_html_revenue_prediction = create_h1_title(title='Revenue prediction', subtitle='Revenue in €')

data_html_boxbutton = box_with_button(
    href='https://www.shimoku.com',
    title='Shimoku is a White Label App',
    line='Share with your clients your own App,  not an Standard',
)

data_html_panel = panel(
    href='www.shimoku.com',
    text='Attention, this is a brief explanation about the information in this section',
)
