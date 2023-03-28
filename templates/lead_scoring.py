import shimoku_api_python as shimoku
import numpy as np
import pandas as pd

from typing import List, Dict, Union
from os import getenv
from data.lead_scoring_data import get_data


#--------------------AUXILIARY FUNCTIONS--------------------#
def get_label_columns(table_data: pd.DataFrame) -> Dict:
    low_threshold = table_data["Probability"][table_data["Lead Scoring"] == "Low"].max() + 1e-10
    mid_threshold = table_data["Probability"][table_data["Lead Scoring"] == "Medium"].max() + 1e-10
    return {
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


#--------------------DASHBOARD FUNCTIONS--------------------#
def page_header(shimoku_client: shimoku.Client, menu_path: str, order: int):
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
    shimoku_client.plt.html(html=prediction_header, menu_path=menu_path, order=order)


def general_indicators(shimoku_client: shimoku.Client, menu_path: str, order: int,
                       prediction_indicators: List[Dict]):
    for i in range(3):
        shimoku_client.plt.indicator(
            data=prediction_indicators[i * 2:i * 2 + 2],
            menu_path=menu_path, order=i*2+order, rows_size=1, cols_size=12,
            value="value", header='title',
            footer='description', color='color', variant='variant'
        )


def prediction_table(shimoku_client: shimoku.Client, menu_path: str, order: int, binary_prediction_table: pd.DataFrame):
    prediction_table_header = (
        '<div style="width:100%; height:90px; "><h4>Lead predicton & factors</h4>'
        '<p>Affectation values for each lead</p></div>'
    )
    shimoku_client.plt.html(html=prediction_table_header, menu_path=menu_path, order=order)

    label_columns = get_label_columns(binary_prediction_table)

    shimoku_client.plt.table(
        menu_path=menu_path, order=order+1, data=binary_prediction_table[:200],
        label_columns=label_columns, filter_columns=['Lead Scoring'],
        search_columns=['Lead ID', 'Negative Impact Factors', 'Positive Impact Factors'],
        value_suffixes={'Probability': '%'}
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
    shimoku_client.plt.html(html=table_explanaiton, menu_path=menu_path, order=order+2)


def distribution_header(shimoku_client: shimoku.Client, menu_path: str, order: int):
    distribution_header_html = (
        '<div style="width:100%; height:90px; "><h4>Lead distribution according to % scoring prediction</h4>'
        '<p>Total and disaggregated distribution and porcentage</p></div>'
    )
    shimoku_client.plt.html(html=distribution_header_html, menu_path=menu_path, order=order)


def distribution_chart(shimoku_client: shimoku.Client, menu_path: str, order: int,
                       high_conversion_occurrences: int, moderate_conversion_occurrences: int,
                       low_conversion_occurrences: int):
    doughnut_chart_options = f"""
            {{
                tooltip: {{
                trigger: 'item'
            }},
            legend: {{
                top: '5%',
                left: 'center'
            }},
            series: [
            {{
                name: 'Access From',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {{
                    borderRadius: 0,
                    borderColor: '#fff',
                    borderWidth: 0
                }},
                label: {{
                    show: false,
                    position: 'center'
                }},
                emphasis: {{
                    label: {{
                    show: false,
                    fontSize: '40',
                    fontWeight: 'bold'
                }}
              }},
              labelLine: {{
                show: false
              }},
              data: [
                {{ value: {high_conversion_occurrences}, name: 'High > 75%' }},
                {{ value: {moderate_conversion_occurrences}, name: 'Medium [50% - 75%]' }},
                {{ value: {low_conversion_occurrences}, name: 'Low < 50%' }}
              ]
            }}
          ]
        }};      
        """
    shimoku_client.plt.free_echarts(
        raw_options=doughnut_chart_options,
        menu_path=menu_path, order=order, cols_size=5, rows_size=2
    )


def feature_importance_chart(shimoku_client: shimoku.Client, menu_path: str, order: int,
                             feature_importance: pd.DataFrame):
    shimoku_client.plt.bar(
        data=feature_importance.sort_values('Importance (%)', ascending=False)[:10],
        x='Feature', y=['Importance (%)'],
        menu_path=menu_path, order=order, rows_size=2, cols_size=7,
    )


def next_best_product_header(shimoku_client: shimoku.Client, menu_path: str, order: int):
    next_best_product_header_html = (
        '<div style="width:100%; height:90px; "><h4>Next best product prediction</h4>'
        '<p>Products with a high probability of conversion for each lead</p></div>'
    )
    shimoku_client.plt.html(html=next_best_product_header_html, menu_path=menu_path, order=order)


def next_best_product_indicators(shimoku_client: shimoku.Client, menu_path: str, order: int,
                                 product_recommendation_indicators: pd.DataFrame):
    shimoku_client.plt.indicator(
        data=product_recommendation_indicators, menu_path=menu_path, order=order,
        value='value', header='title', align='align', color='color',
        variant='variant', background_image='backgroundImage',
    )


def next_best_product_table(shimoku_client: shimoku.Client, menu_path: str, order: int,
                            product_recommendation_table: pd.DataFrame):
    label_columns = get_label_columns(product_recommendation_table)
    shimoku_client.plt.table(
        data=product_recommendation_table[:200], menu_path=menu_path, order=order,
        filter_columns=['Lead Scoring'], search_columns=['Lead ID', 'Next Best Product'],
        label_columns=label_columns, value_suffixes={'Probability': '%'}
    )


def main():
    #--------------- GET THE DATA DICTIONARY ----------------#
    data = get_data('../data/Leads.csv')

    #----------------- CLIENT INITIALIZATION ----------------#
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
    menu_path = 'Lead Scoring'

    #--------------- CREATE DASHBOARD TASKS ----------------#
    page_header(                 s, menu_path, 0)
    general_indicators(          s, menu_path, 1, data['prediction_indicators'])
    prediction_table(            s, menu_path, 7, data['binary_prediction_table'])
    distribution_header(         s, menu_path, 10)
    distribution_chart(          s, menu_path, 11,
                                 data['high_conversion_occurrences'],
                                 data['moderate_conversion_occurrences'],
                                 data['low_conversion_occurrences'])
    feature_importance_chart(    s, menu_path, 12, data['feature_importance'])
    next_best_product_header(    s, menu_path, 13)
    next_best_product_indicators(s, menu_path, 14, data['product_recommendation_indicators'])
    next_best_product_table(     s, menu_path, 17, data['product_recommendation_table'])

    #------------------ EXECUTE ALL TASKS -----------------#
    s.run()


if __name__ == '__main__':
    main()
