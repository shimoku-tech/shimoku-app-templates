from os import getenv

import shimoku_api_python as shimoku

import numpy as np

from data.lead_scoring_data import (
    prediction_indicators_data, prediction_header, prediction_table_header,
    binary_prediction_table, table_explanaiton, distribution_header, doughnut_chart_options,
    feature_importance, next_best_product_header, product_recommendation_indicators, product_recommendation_table
)

api_key: str = getenv('API_TOKEN')
universe_id: str = getenv('UNIVERSE_ID')
business_id: str = getenv('BUSINESS_ID')
environment: str = getenv('ENVIRONMENT')

#---------------- CLIENT INITIALIZATION ----------------#
s = shimoku.Client(
    access_token=api_key,
    universe_id=universe_id,
    environment=environment,
    business_id=business_id,
    async_execution=True,
    verbosity='INFO',
)

menu_path = 'Lead Scoring'

#-------------------- PAGE HEADER --------------------#
s.plt.html(html=prediction_header, menu_path=menu_path, order=0)

#----------------- GENERAL INDICATORS -----------------#
for i in range(3):
    order = s.plt.indicator(
        data=prediction_indicators_data[i * 2:i * 2 + 2],
        menu_path=menu_path, order=1, rows_size=1, cols_size=12,
        value="value", header='title',
        footer='description', color='color', variant='variant'
    )

#------------------ PREDICTION TABLE ------------------#
s.plt.html(html=prediction_table_header, menu_path=menu_path, order=7)

low_threshold = binary_prediction_table["Probability"][binary_prediction_table["Lead Scoring"] == "Low"].max() + 1e-10
mid_threshold = binary_prediction_table["Probability"][binary_prediction_table["Lead Scoring"] == "Medium"].max() + 1e-10
label_columns = {
    'Positive Impact Factors': ('#20C69E', 'filled', 'rounded'),
    'Negative Impact Factors': ('#ED5627', 'filled', 'rounded'),
    'Lead Scoring': {
        'Low': ('#F86C7D', 'rounded', 'filled'),
        'High': ('#001E50', 'rounded', 'filled'),
        'Medium': ('#F2BB67', 'rounded', 'filled'),
    },
    'Probability': {
        (0, low_threshold): ('#F86C7D', 'rounded', 'outlined'),
        (low_threshold, mid_threshold): ('#F2BB67', 'rounded', 'outlined'),
        (mid_threshold, np.inf): ('#001E50', 'rounded', 'outlined'),
    },
}

s.plt.table(
    menu_path=menu_path, order=8, data=binary_prediction_table[:200],
    label_columns=label_columns, filter_columns=['Lead Scoring'],
    search_columns=['Lead ID', 'Negative Impact Factors', 'Positive Impact Factors'],
    value_suffixes={'Probability': '%'}
)

s.plt.html(html=table_explanaiton, menu_path=menu_path, order=9)


#--------- DOUGHNUT CHART AND FEATURE IMPORTANCE ---------#
s.plt.html(html=distribution_header, menu_path=menu_path, order=10)

s.plt.free_echarts(
    raw_options=doughnut_chart_options,
    menu_path=menu_path, order=11, cols_size=5, rows_size=2
)

s.plt.bar(
    data=feature_importance.sort_values('Importance (%)', ascending=False)[:10],
    x='Feature', y=['Importance (%)'],
    menu_path=menu_path, order=12, rows_size=2, cols_size=7,
)

#-------------- NEXT BEST PRODUCT INDICATORS --------------#
s.plt.html(html=next_best_product_header, menu_path=menu_path, order=13)

s.plt.indicator(
    data=product_recommendation_indicators, menu_path=menu_path, order=14,
    value='value', header='title', align='align', color='color',
    variant='variant', background_image='backgroundImage',
)

#----------------- NEXT BEST PRODUCT TABLE -----------------#
s.plt.table(
    data=product_recommendation_table[:200], menu_path=menu_path, order=17,
    filter_columns=['Lead Scoring'], search_columns=['Lead ID', 'Next Best Product'],
    label_columns=label_columns,
)

#-------------------- EXECUTE ALL TASKS --------------------#
s.run()
