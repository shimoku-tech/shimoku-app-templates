import json

modals_css = """
.modal-article .h-top-space {
    margin-top: 30px;
}
.modal-article .ordered-list {
    margin-top: 5px;
}
.modal-article .ordered-list li {
    margin-top: 5px;
}
"""


def create_title_name_head(title: str, subtitle: str) -> str:
    """
    Function that generates the page header.

    Args:
        title (str): The main title for the page header.
        subtitle (str): The subtitle or additional text for the header.

    Returns:
        str: The HTML content to be plotted as the header.
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
        "<h1>" + title + "</h1>"
        "<p class='base-white'>"
        f"{subtitle}</p>"
        "</div>"
        "</div>"
    )
    return html


def format_raw_options(sales_by_store):
    """
    Formats the raw options for the ECharts configuration.

    Args:
        sales_by_store (DataFrame): DataFrame containing store sales data with columns 'store_id', 'Number of Users', and 'Sales Amount'.

    Returns:
        str: A string formatted for the ECharts JavaScript configuration.
    """
    # Extract data from the DataFrame
    store_ids = sales_by_store["store_id"].tolist()
    number_of_users = sales_by_store["Number of Users"].tolist()
    sales_amount = sales_by_store["Sales Amount"].tolist()

    # Convert lists to JSON strings
    store_ids_json = json.dumps(store_ids)
    number_of_users_json = json.dumps(number_of_users)
    sales_amount_json = json.dumps(sales_amount)

    # Construct the ECharts options string
    raw_options = f"""
    {{
        xAxis: {{
            type: 'category',
            data: {store_ids_json},
            fontFamily: 'Rubik',
            nameLocation: 'middle',
        }},
        'legend': {{
            data: ['Number of Users', 'Sales Amount'],
            show: true,
            type: 'scroll',
            icon: 'circle',
            padding: [5, 5, 5, 5],
        }},
        'tooltip': {{
            trigger: 'item',
            axisPointer: {{
                type: 'cross'
            }},
        }},
        'grid': {{
            left: '2%',
            right: '1%',
            bottom: 48,
            containLabel: true,
        }},
        'toolbox': {{
            'show': true,
            'orient': 'horizontal',
            'itemSize': 20,
            'itemGap': 24,
            'showTitle': true,
            'zlevel': 100,
            'bottom': 0,
            'right': '24px',
            'feature': {{
                'dataView': {{
                    'title': 'data',
                    'readOnly': false,
                    'icon': 'image://https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/6398a555461a3684b16d544e_database.svg',
                    'emphasis': {{
                        'iconStyle': {{
                            'textBackgroundColor': 'var(--chart-C1)',
                            'textBorderRadius': [50, 50, 50, 50],
                            'textPadding': [8, 8, 8, 8],
                            'textFill': 'var(--color-white)'
                        }}
                    }}
                }},
                'magicType': {{
                    'type': ['line', 'bar'],
                    'title': {{
                        'line': 'Switch to Line Chart',
                        'bar': 'Switch to Bar Chart'
                    }},
                    'icon': {{
                        'line': 'image://https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/6398a55564d52c1ba4d9884d_linechart.svg',
                        'bar': 'image://https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/6398a5553cc6580f8e0edea4_barchart.svg'
                    }},
                    'emphasis': {{
                        'iconStyle': {{
                            'textBackgroundColor': 'var(--chart-C1)',
                            'textBorderRadius': [50, 50, 50, 50],
                            'textPadding': [8, 8, 8, 8],
                            'textFill': 'var(--color-white)'
                        }}
                    }}
                }},
                'saveAsImage': {{
                    'show': true,
                    'title': 'Save as image',
                    'icon': 'image://https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/6398a555662e1af339154c64_download.svg',
                    'emphasis': {{
                        'iconStyle': {{
                            'textBackgroundColor': 'var(--chart-C1)',
                            'textBorderRadius': [50, 50, 50, 50],
                            'textPadding': [8, 8, 8, 8],
                            'textFill': 'var(--color-white)'
                        }}
                    }}
                }}
            }}
        }},
        yAxis: [
            {{
                type: 'value',
                position: 'right',
                alignTicks: true,
                'fontFamily': 'Rubik',
                axisLine: {{
                    show: true,
                    lineStyle: {{
                        color: '#4c73f8'
                    }},
                }},
            }},
            {{
                type: 'value',
                position: 'left',
                alignTicks: true,
                'fontFamily': 'Rubik',
                axisLine: {{
                    show: true,
                    lineStyle: {{
                        color: '#74d890'
                    }},
                }},
            }},
        ],
        series: [
            {{
                name: 'Number of Users',
                type: 'bar',
                data: {number_of_users_json},
                'itemStyle': {{
                    'borderRadius': [9, 9, 0, 0]
                }},
                'smooth': true,
                'emphasis': {{
                    focus: 'series'
                }},
            }},
            {{
                name: 'Sales Amount',
                type: 'bar',
                yAxisIndex: 1,
                data: {sales_amount_json},
                'itemStyle': {{
                    'borderRadius': [9, 9, 0, 0]
                }},
                'smooth': true,
                'emphasis': {{
                    'focus': 'series'
                }},
            }},
        ]
    }};
    """

    return raw_options
