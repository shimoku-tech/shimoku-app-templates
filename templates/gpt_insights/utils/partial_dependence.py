
from typing import Dict

import numpy as np
import pandas as pd


## Draw tools
def load_header_style1(s, order: int, settings: Dict) -> None:
    """
    Draw header

    :param settings: Specific settings for the function.
    Example: {
    "header_title": "Up-Selling", "header_subtitle": "Prediction of Upselling Probability"
    }
    """
    def _create_header_style1(header_title: str,
                              header_subtitle: str) -> str:
        """Generate header.
        """
        html = (
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
                "<h1>" + header_title + "</h1>"
                                        "<p class='base-white'>" +
                header_subtitle + "</p>"
                                  "</div>"
                                  "</div>"
        )
        return html

    s.plt.html(
        html=_create_header_style1(
            header_title=settings['header_title'],
            header_subtitle=settings['header_subtitle']),
        order=order, rows_size=2, cols_size=12,
    )
    order += 1

    return order


def load_header_style2(s, order: int, settings: Dict) -> None:
    """Draw header style2
    """
    def _create_header_style2(header_title: str,
                              header_subtitle: str,
                              padding_top: int = 50) -> str:
        """Generate header.
        """
        html = '<div style="width:100%; height:90px; padding-top: ' + str(padding_top) + 'px; "><h4>'
        html += header_title + '</h4><p>' + header_subtitle + '</p></div>'

        return html

    s.plt.html(
        html=_create_header_style2(
            header_title=settings['header_title'],
            header_subtitle=settings['header_subtitle']),
        order=order, rows_size=2, cols_size=12,
    )
    order += 1

    return order


def container(s, text: str, order: int, cols_size, rows_size, padding):

    table_explanaiton = (
        "<head>"
        "<style>.banner"
        "{height:100%; width:100%; border-radius:var(--border-radius-m); padding:24px;"
        "background-size: cover;"
        "background-image: url('https://ajgutierrezcommx.files.wordpress.com/2022/12/bg-info-predictions.png');"
        "color:var(--color-white);}"
        ".base-white" 
        "{font-size: 16px;}"
        "</style>"
        "</head>"
        "<div class='banner'>"
        "<div class='banner'>"
        "<p class='base-white'>" + text + "</p>"
        "</div>"
    )
    s.plt.html(
        html=table_explanaiton, order=order, cols_size=cols_size,
        rows_size=rows_size, padding=padding)

    order += 1

    return order


## Format
def format_data(list_df, output_target, output_class):

    # Filter
    for i in range(len(list_df)):
        list_df[i] = list_df[i][list_df[i]['column_target'] == output_target]
        list_df[i] = list_df[i][list_df[i]['class'].astype(str) == output_class]

    return list_df


def rename_columns(df_pd: pd.DataFrame):
    """
    Rename columns
    """
    df_pd = df_pd.rename(columns={'pd': 'partial dependence'})
    return df_pd


def force_numeric(df: pd.DataFrame):
    """
    Ensure that numeric colums appear as numeric. E.g., '4' -> 4.
    """
    try:
        df['value_feature'] = pd.to_numeric(df['value_feature'])
    except ValueError:
        pass

    return df


## Charts
def page_header(s, order):
    return load_header_style1(
        s=s, order=order,
        settings={'header_title': 'Partial Dependence',
                  'header_subtitle': 'Partial Dependence Plots with GPT Insights'})


def pd_tabs(s, order, df_pd, df_insights, input_features):
    """
    Draw Partial Dependence tabs
    """
    # Split into tabs
    s.plt.set_tabs_index(('tab_group', input_features[0]), order=order)
    order += 1

    for feature in input_features:

        # Get slice
        df_pd_feature = df_pd[df_pd['name_feature'] == feature]

        # Convert to numeric if possible
        df_pd_feature = force_numeric(df=df_pd_feature)

        # Split numerical and nominal/boolean
        input_values = df_pd_feature['value_feature'].unique()
        if all(isinstance(x, str) for x in input_values):
            feature_type = 'categorical'
        elif all(x in [0, 1] for x in input_values):
            feature_type = 'categorical'
        elif all(np.issubdtype(type(x), np.number) for x in input_values):
            feature_type = 'numerical'
        else:
            raise ValueError('The feature is not numerical or categorical')

        # Order in tab
        s.plt.change_current_tab(feature)

        # Name
        order = load_header_style2(
            s, order=order,
            settings={'header_title': feature, 'header_subtitle': ''})

        # Draw
        if feature_type == 'numerical':
            s.plt.line(
                data=df_pd[df_pd['name_feature'] == feature],
                x='value_feature',
                y='partial dependence',
                order=order,
                rows_size=2,
                cols_size=7,
                padding='0,0,0,0',
            )

        elif feature_type == 'categorical':
            s.plt.bar(
                data=df_pd[df_pd['name_feature'] == feature],
                x='value_feature',
                y='partial dependence',
                order=order,
                rows_size=2,
                cols_size=7,
                padding='0,0,0,0',
            )

        order += 1

        # Add insights
        order = container(
            s, text=df_insights[df_insights['name_feature'] == feature]['insight'].values[0],
            order=order, cols_size=4, rows_size=2, padding='0,0,0,1')

    s.plt.pop_out_of_tabs_group()

    return order
