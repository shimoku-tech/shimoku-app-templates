import shimoku_api_python as shimoku
import numpy as np
import pandas as pd

from typing import List, Dict, Union
from os import getenv
from aux import get_data


#--------------------AUXILIARY FUNCTIONS--------------------#
def get_label_columns(table_data: pd.DataFrame) -> Dict:
    low_threshold = table_data["Probability"][table_data["Lead Scoring"] == "Low"].max() + 1e-10
    mid_threshold = table_data["Probability"][table_data["Lead Scoring"] == "Medium"].max() + 1e-10
    return {
        ('Positive Impact Factors', 'outlined'): '#20C69E',
        ('Negative Impact Factors', 'outlined'): '#ED5627',
        'Lead Scoring': {
            'Low': '#F86C7D',
            'High': '#001E50',
            'Medium': '#F2BB67',
        },
        'Probability': {
            (0, low_threshold): '#F86C7D',
            (low_threshold, mid_threshold): '#F2BB67',
            (mid_threshold, np.inf): '#001E50',
        },
    }


#--------------------DASHBOARD FUNCTIONS--------------------#
def page_header(shimoku_client: shimoku.Client, order: int):
    prediction_header = (
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
        "<h1>Predictions</h1>"
        "<p class='base-white'>"
        "Lead scoring prediction</p>"
        "</div>"
        "</div>"
    )
    shimoku_client.plt.html(html=prediction_header, order=order)


def general_indicators(shimoku_client: shimoku.Client, order: int, prediction_indicators: List[Dict]):
    for i in range(3):
        shimoku_client.plt.indicator(
            data=prediction_indicators[i * 2:i * 2 + 2], order=i*2+order, rows_size=1, cols_size=12,
        )


def prediction_table(shimoku_client: shimoku.Client, order: int, binary_prediction_table: pd.DataFrame):
    prediction_table_header = (
        '<div style="width:100%; height:90px; "><h4>Lead predicton & factors</h4>'
        '<p>Affectation values for each lead</p></div>'
    )
    shimoku_client.plt.html(html=prediction_table_header, order=order)

    label_columns = get_label_columns(binary_prediction_table)

    shimoku_client.plt.table(
        order=order+1, data=binary_prediction_table[:200],
        label_columns=label_columns, categorical_columns=['Lead Scoring'],
        columns_options={
            'Lead ID': {'width': 100},
            'Lead Scoring': {'width': 120},
            'Probability': {'width': 120},
            'Positive Impact Factors': {'width': 590},
            'Negative Impact Factors': {'width': 590}
        }
    )

    table_explanaiton = (
        "<head>"
        "<style>.banner"
        "{height:100%; width:100%; border-radius:var(--border-radius-m); padding:24px;"
        "background-size: cover;"
        "background-image: url('https://ajgutierrezcommx.files.wordpress.com/2022/12/bg-info-predictions.png');"
        "color:var(--color-white);}"
        "</style>"
        "</head>"
        "<a href='https://shimoku.webflow.io/product/churn-prediction' target='_blank'>"  # link
        "<div class='banner'>"
        "<p class='base-white'>"
        "This table shows the impact values that effect each prediction of each policy. "
        "With it you can make the best decisions. <br>"
        "By filtering the data, by the values that interest you the most or by the probability of "
        "conversion that you want to improve, you will be able to take the necessary actions "
        "to obtain the maximum benefit or reduce the losses to a minimum."
        "</p>"
        "<div class='button'>Know more</div>"  # Text button
        "</div>"
        "</a>"
    )
    shimoku_client.plt.html(html=table_explanaiton, order=order+2)


def distribution_header(shimoku_client: shimoku.Client, order: int):
    distribution_header_html = (
        '<div style="width:100%; height:90px; "><h4>Lead distribution according to % scoring prediction</h4>'
        '<p>Total and disaggregated distribution and porcentage</p></div>'
    )
    shimoku_client.plt.html(html=distribution_header_html, order=order)


def distribution_chart(shimoku_client: shimoku.Client, order: int, doughnut_chart_data: Dict):
    shimoku_client.plt.free_echarts(raw_options=doughnut_chart_data, order=order, cols_size=5, rows_size=2)


def feature_importance_chart(shimoku_client: shimoku.Client, order: int, feature_importance: pd.DataFrame):
    shimoku_client.plt.bar(
        data=feature_importance.sort_values('Importance (%)', ascending=False)[:10],
        x='Feature', y=['Importance (%)'], order=order, rows_size=2, cols_size=7,
    )


def next_best_product_header(shimoku_client: shimoku.Client, order: int):
    next_best_product_header_html = (
        '<div style="width:100%; height:90px; "><h4>Next best product prediction</h4>'
        '<p>Products with a high probability of conversion for each lead</p></div>'
    )
    shimoku_client.plt.html(html=next_best_product_header_html, order=order)


def next_best_product_indicators(
    shimoku_client: shimoku.Client,  order: int, product_recommendation_indicators: pd.DataFrame
):
    shimoku_client.plt.indicator(
        data=product_recommendation_indicators, order=order,
        value='value', header='title', align='align', color='color',
        variant='variant', background_image='backgroundImage',
    )


def next_best_product_table(
    shimoku_client: shimoku.Client, order: int, product_recommendation_table: pd.DataFrame
):
    label_columns = get_label_columns(product_recommendation_table)
    shimoku_client.plt.table(
        data=product_recommendation_table[:200], order=order,
        categorical_columns=['Lead Scoring'], label_columns=label_columns,
        columns_options={
            'Lead ID': {'width': 360},
            'Lead Scoring': {'width': 360},
            'Probability': {'width': 360},
            'Next Best Product': {'width': 360},
        }
    )


def main():
    #--------------- GET THE DATA DICTIONARY ----------------#
    data = get_data('data/Leads.csv')

    #----------------- CLIENT INITIALIZATION ----------------#
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
    s.set_workspace(workspace_id)
    s.set_menu_path('Lead Scoring')

    #--------------- CREATE DASHBOARD TASKS ----------------#
    page_header(                 s, 0)
    general_indicators(          s, 1, data['prediction_indicators'])
    prediction_table(            s, 7, data['binary_prediction_table'])
    distribution_header(         s, 10)
    distribution_chart(          s, 11, data['doughnut_chart_data'])
    feature_importance_chart(    s, 12, data['feature_importance'])
    next_best_product_header(    s, 13)
    next_best_product_indicators(s, 14, data['product_recommendation_indicators'])
    next_best_product_table(     s, 17, data['product_recommendation_table'])

    #------------------ EXECUTE ALL TASKS -----------------#
    s.run()


if __name__ == '__main__':
    main()
