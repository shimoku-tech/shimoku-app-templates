
from typing import Dict


## Format
def format_data(df_predicted, list_df, nrows, id_columns, output_target, output_class):

    # Filter
    df_predicted = df_predicted[df_predicted['column_target'] == output_target]
    df_predicted = df_predicted[df_predicted['class'].astype(str) == output_class]
    for i in range(len(list_df)):
        list_df[i] = list_df[i][list_df[i]['column_target'] == output_target]
        list_df[i] = list_df[i][list_df[i]['class'].astype(str) == output_class]

    # Get top nrows rows
    df_predicted = df_predicted.nlargest(nrows, 'probability')[id_columns]
    for i in range(len(list_df)):
        list_df[i] = df_predicted.merge(list_df[i], on=id_columns, how='inner')

    return df_predicted, list_df


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


## Charts
def page_header(s, order):
    return load_header_style1(
        s=s, order=order,
        settings={'header_title': 'Drivers & Barriers',
                  'header_subtitle': 'Drivers & Barriers Plots with GPT Insights'})


def table_header(s, order, output_target, nrows):
    return load_header_style2(
        s, order=order,
        settings={'header_title': f"Users prone to {output_target.lower()}" , 'header_subtitle': f"Top {str(nrows)}"})


def table(s, order, df_db, menu_path, id_columns):
    s.plt.table(
        data=df_db.drop(columns=['column_target', 'class', '_base_values']),
        menu_path=menu_path,
        order=order,
        search_columns=id_columns,
    )
    order += 1
    return order


def users_insights(s, order, df_top, df_shap, df_insights, id_columns):

    for index, row in df_top[id_columns].iterrows():

        # Format
        df_shap_row = df_shap[df_shap[id_columns].eq(row.values, axis=1).all(axis=1)]
        df_shap_row = df_shap_row.filter(like='shap_').melt(var_name='feature', value_name='feature contributions')
        df_shap_row['feature'] = df_shap_row['feature'].str.replace('shap_', '')
        df_shap_row = df_shap_row.sort_values(by='feature contributions', ascending=True)

        df_insights_row = df_insights[df_insights[id_columns].eq(row.values, axis=1).all(axis=1)]

        # Name
        order = load_header_style2(
            s, order=order,
            settings={'header_title': row.values[0], 'header_subtitle': ''})

        s.plt.horizontal_bar(
            data=df_shap_row,
            x='feature',
            rows_size=3,
            cols_size=7,
            order=order,
            # padding='0,0,0,0'
        )
        order += 1

        order = container(
            s=s, text=df_insights_row['insight'].values[0],
            order=order, cols_size=3, rows_size=3, padding='0,0,0,1')

    return order
