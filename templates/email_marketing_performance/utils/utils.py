import pandas as pd
import os


def get_data(file_names: list) -> dict:
    """Returns a dictionary of dataframes, one item for each file of file_names array parameter.
    Example:
    file_names = ['data/active_users.csv', 'data/shop_events.csv', ...]
    dict_dfs ['active_users'] = A dataframe with 'data/active_users.csv' CSV file
    dict_dfs ['shop_events'] = A dataframe with 'data/shop_events.csv' CSV file

    Args:
        dict_dfs (dict): A dictionary of dataframes.
    """

    dict_dfs = dict()
    for file_name in file_names:
        df = pd.read_csv(file_name)

        # Finds the columns containing "_date" in their name
        columnas_fecha = [col for col in df.columns if "_date" in col]

        # Convert columns identified with "_date" to datetime
        df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime)

        dict_dfs[os.path.splitext(os.path.basename(file_name))[0]] = df

    return dict_dfs


def convert_dataframe_to_array(df: pd.DataFrame) -> list:
    """Return a list, convert a dataframe to a list.

    Args:
        df (pd.DataFrame): A dataFrame to convert.

    Returns:
        new_data (List): A List with the dataframe information.
    """
    # Get list of column names
    columns_to_include = df.columns.tolist()
    new_data = []

    for index, row in df.iterrows():
        new_dict = {column: row[column] for column in columns_to_include}
        new_data.append(new_dict)

    return new_data

def beautiful_header(title: str) -> str:
    """Return a HTML structure to plot the header on the menu path.

    Args:
        title (str): title of the header in the menu path.

    Returns:
        str: HTML structure to plot the header.
    """
    return (
        "<head>"
            # Styles title
            "<style>"
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
        "</head>"
        "<div class='component-title'>"
            "<div class='big-icon-banner'></div>"
            "<div class='text-block'>"
                "<h1>" + title + "</h1>"
            "</div>"
        "</div>"
    )

def beautiful_section(title: str) -> str:
    """Return a HTML structure to plot the title section.

    Args:
        title (str): title of the header in the menu path.

    Returns:
        str: HTML structure to plot the header.
    """
    return (
        "<head>"
            # Styles title
            "<style>"
                ".component-title{height:auto; width:100%; "
                "border-radius:16px; padding:16px;"
                "display:flex; align-items:center;"
                "background-color:var(--chart-C1); color:var(--color-white);}"
            "</style>"
            "<style>.base-white{color:var(--color-white);}</style>"
        "</head>"  # Styles subtitle
        "<div class='text-block'>"
            "<h1>" + title + "</h1>"
        "</div>"
    )

def compute_percent(value: float, total: float) -> float:
    """Compute the percentage value.

    Args:
        value (float): fraction of the total value.
        total (float): total value.

    Returns:
        float: percentage value.
    """
    return round(value * 100 / total if total != 0 else 0, 1)

def html_overview(name: str, value: float) -> str:
    """_summary_

    Args:
        name (str): _description_
        value (float): _description_

    Returns:
        str: _description_
    """
    return (
        "<div class='overview__row'>"
            f"<div class='row__description'>- Emails {name}</div>"
            f"<div class='row__value'>{value:d}</div>"
        "</div>"
    )

def beautiful_email_subject(subject: str) -> str:
    return (
        "<style>"
            ".email_subject{display:flex; justify-content: center;"
                "font-weight: bold; font-size: 1.5rem; text-align: center;}"
        "</style>"
        "<div class='email_subject'>"
            f'"{subject}"'
        "</div>"
    )


def overview_section(df: pd.DataFrame) -> str:
    """Return a string of the HTML structure with the differents categories used on the
    Category section for each tab.

    Args:
        df (pd.DataFrame): dataframe which contains the categories and the users count.

    Returns:
        str: string of the HTML structure with the differents categories.
    """
    total = df["value"].apply('sum')

    css_style = (
        "<style>"
            ".container{display:grid; align-content: space-between; width: 100%; min-height: 25rem; margin-top: 3rem;}"
            ".overview__header{display: flex; align-items: center; font-size: 2rem;"
                "min-height: 2rem; padding: 1rem 0 0 0.5rem ; border-bottom: 5px solid #000;}"
            ".overview__content{display: grid; grid-template-columns: 1fr; row-gap: 2rem; padding: 0 1rem;}"
            ".overview__row{display: grid; grid-template-columns: 3fr 1fr; grid-template-rows: 1fr; width: 100%;}"
            ".row__value{display: flex; justify-content: right;}"
            ".overview__total{display: grid; grid-template-columns: 1fr 1fr; align-items: center;"
                "min-height: 2rem; border: 1px solid #000;}"
            ".overview__total-description, .overview__total-value{"
                "display: flex; align-items: center; height: 100%; padding: 0 0.5rem;}"
            ".overview__total-description{background-color: var(--chart-C1);}"
            ".overview__total-value{justify-content: right; border-left: 1px solid #000; background-color: var(--color-grey-300)}"
        "</style>"
    )

    sections = [css_style]
    sections += ["<div class='container'>"]
    sections += ["<div class='overview__header'>Contacts Achieved</div>"]
    sections += ["<div class='overview__content'>"]
    sections += [html_overview("Sent", total)]
    sections += [html_overview(row["name"], row["value"]) for _, row in df.iterrows()]
    sections += ["</div>"]
    sections += [
        (
            "<div class='overview__total'>"
                "<div class='overview__total-description'>Total</div>"
                f"<div class='overview__total-value'>{total:d}</div>"
            "</div>"
        )
    ]
    sections += ["</div>"]

    return "".join(sections)


def html_results(info: dict) -> str:
    """Return a HTML structure of the results row sections

    Args:
        info (dict): Results row information

    Returns:
        str: HTML structure of the results row sections
    """

    return (
        "<div class='row'>"
            "<div class='section'>"
                f"<div class='title'>{info['title']}</div>"
                f"<div class='description'>{info['description']}</div>"
            "</div>"
            "<div class='stats'>"
                f"<div class='stats__description value'>Total {info['title'].replace(' Rate', 's')}</div>"
                f"<div class='stats__description percentage'>{info['title']} (%)</div>"
                f"<div class='stats__value-primary value'>{info['value']}</div>"
                f"<div class='stats__value-primary percentage'>{info['percentage']}%</div>"
                "<div class='stats__value-secondary'></div>"
                f"<div class='stats__value-secondary'>{100 - info['percentage']}%</div>"
            "</div>"
        "</div>"
    )

def results_section(
        df_open: pd.DataFrame, df_click: pd.DataFrame,
        df_answer: pd.DataFrame, df_rebound: pd.DataFrame
) -> str:
    """Return a HTML structure of Results section

    Args:
        df_open (pd.DataFrame): dataframe with the open
        df_click (pd.DataFrame): dataframe with the click
        df_answer (pd.DataFrame): dataframe with the answer
        df_rebound (pd.DataFrame): dataframe with the rebound

    Returns:
        str: HTML structure of Results section
    """
    information = {
        "open": {
            "title": "Open Rate",
            "description": "Emails open rate",
            "value": df_open[df_open["name"] == "Opened"].value.values[0],
            "percentage": df_open[df_open["name"] == "Opened"].percentage.values[0],
        },
        "click": {
            "title": "Click Rate",
            "description": "They have clicked on any of the links contained in the email",
            "value": df_click[df_click["name"] == "Clicked"].value.values[0],
            "percentage": df_click[df_click["name"] == "Clicked"].percentage.values[0],
        },
        "answer": {
            "title": "Answer Rate",
            "description": "Response rate of the delivery achieved",
            "value": df_answer[df_answer["name"] == "Answered"].value.values[0],
            "percentage": df_answer[df_answer["name"] == "Answered"].percentage.values[0],
        },
        "rebound": {
            "title": "Rebound Rate",
            "description": "Number of mails that have not reached the addressee",
            "value": df_rebound[df_rebound["name"] == "Rebound"].value.values[0],
            "percentage": df_rebound[df_rebound["name"] == "Rebound"].percentage.values[0],
        },
    }

    css_style = (
        "<style>"
            ".result-header{display: grid;"
                "grid-template-columns: 3fr 2fr; padding: 0 1.6rem;"
                "height: 2rem; width: 100%; column-gap: 3rem;}"
            ".result-header__container {display: grid;"
                "grid-template-columns: 4fr 1fr;}"
            ".result-header__title {display: flex;"
                "justify-content: center; border-bottom: 6px solid #000;}"
            ".row{display: grid; grid-template-columns: 3fr 2fr; padding: 1.6rem;"
                "width: 100%; column-gap: 3rem;}"
            ".section {display: grid; grid-auto-flow: column;"
                "grid-template-columns: 1fr; grid-template-rows: 1fr 1fr}"
            ".title, .description, .stats__description, .stats__value-primary, .stats__value-secondary{"
                "display: flex; align-items: center;}"
            ".section .title {border-bottom: 3px solid #000; width: 100%;}"
            ".section .description {border-top: 3px solid #000;}"
            ".stats {display: grid; grid-auto-flow: column;"
                "grid-template-columns: 3fr 1fr 1fr; grid-template-rows: 1fr 1fr;}"
            ".stats__description, .stats__value-primary{"
                "border-bottom: 1px solid #000; border-left: 1px solid #000;}"
            ".stats__description {padding-left: 0.5rem; background-color: var(--chart-C1);}"
            ".value {border-top: 1px solid #000;}"
            ".stats__value-primary{justify-content: right; padding-right: 0.5rem;"
                "background-color: var(--color-grey-300); border-right: 1px solid #000;}"
            ".stats__value-secondary {justify-content: rightleft; padding-left: 0.5rem;}"
        "</style>"
    )
    result_header = (
        "<div class='result-header'>"
            "<div></div>"
            "<div class='result-header__container'>"
                "<div class='result-header__title'>Mail Rate</div>"
                "<div></div>"
            "</div>"
        "</div>"
    )

    sections = [css_style, result_header]
    sections += [html_results(information[key]) for key in information]

    return "".join(sections)


def generate_pie_plot_dict_two_option(names_list: list, value: float, total: float):
    """Return a data structure with two option

    Args:
        names_list (list): option list names
        value (float): principal value
        total (float): total value

    Returns:
        list: data structure with to option
    """

    return [
        {
            "name": names_list[0],
            "value" : value,
            "percentage": compute_percent(value, total),
        },
        {
            "name": names_list[1],
            "value" : total - value,
            "percentage": compute_percent(total - value, total),
        }
    ]


def generate_indicators_delivery_days(delivery_days: str) -> list:
    """Return a data structure for a indicators charts

    Args:
        delivery_days (str): string with the delivery days

    Returns:
        list: Data structure for a indicators charts
    """
    days_values = [
        f"{pd.to_datetime(day).day_name()} {pd.to_datetime(day).day}"
    for day in delivery_days.split(" ")]

    data = [
        {
            "title": "Mail 1",
            "description": "Sequence Start",
            "value": days_values[0],
            "color": "success",
            "align": "center",
            "variant": "contained",
        },
        {
            "title": "Mail 2",
            "description": "",
            "value": days_values[1],
            "color": "neutral",
            "align": "center",
            "variant": "outlined",
        },
        {
            "title": "Mail 3",
            "description": "",
            "value": days_values[2],
            "color": "neutral",
            "align": "center",
            "variant": "outlined",
        },
        {
            "title": "Mail 4",
            "description": "Sequence End ",
            "value": days_values[3],
            "align": "center",
            "color": "caution",
            "variant": "contained",
        }
    ]

    return data

def get_campaign_model(campaign_id: str, model: pd.DataFrame, campaign_model: pd.DataFrame) -> pd.DataFrame:
    """Return a filter model and campaign_model dataframe by campaign_id

    Args:
        campaign_id (str): campaign id
        model (pd.DataFrame): dataframe of model
        campaign_model (pd.DataFrame): dataframe of campaign_model

    Returns:
        pd.DataFrame: filter dataframe by campaign_id
    """
    campaign_model = campaign_model[campaign_model["id_campaign"] == campaign_id]
    model = model[model["id"].isin(campaign_model.id_model)]

    return campaign_model, model

def genenerate_data_by_campaign(df_email):

    total_email_send = df_email[df_email["rebound_flag"] == False].shape[0]

    return {
        "overview" : generate_pie_plot_dict_two_option(
            ["Delivered", "Rebounded"],
            df_email[df_email["rebound_flag"] == False].shape[0],
            df_email.shape[0]
        ),
        "open" : generate_pie_plot_dict_two_option(
            ["Opened", "Not Opened"],
            df_email[df_email["open_flag"] == True].shape[0],
            total_email_send,
        ),
        "click" : generate_pie_plot_dict_two_option(
            ["Clicked", "Not Clicked"],
            df_email[df_email["click_number"] > 0].shape[0],
            total_email_send,
        ),
        "answer" : generate_pie_plot_dict_two_option(
            ["Answered", "Not Answered"],
            df_email[df_email["answer_flag"] == True].shape[0],
            total_email_send,
        ),
        "rebound" : generate_pie_plot_dict_two_option(
            ["Rebound", "Not Rebound"],
            df_email[df_email["rebound_flag"] == True].shape[0],
            df_email.shape[0],
        ),
    }

def generate_tables_by_campaign(df_client: pd.DataFrame, df_email: pd.DataFrame):
    """Return a data structure of client information with a emails openend and click numbers counts

    Args:
        df_client (pd.DataFrame): client dataframe
        df_email (pd.DataFrame): email dataframe

    Returns:
        pd.DataFrame: data structure of client information
    """
    df_open = pd.DataFrame(columns=["Contact Name", "Last Name", "Company"])

    df_open[["Contact Name", "Last Name", "Company"]] = df_client[["first_name", "last_name", "company_name"]]

    df_click = df_open.copy()

    open_values = []
    click_values = []
    for id in df_client.id:
        df = df_email[df_email["id_client"] == id]
        open_values.append(sum([val for val in df["open_flag"] if pd.notnull(val)]))
        click_values.append(sum([val for val in df["click_number"] if pd.notnull(val)]))

    df_open["Nº of Opens"] = open_values
    df_click["Nº of Clicks"] = click_values

    return drop_values(df_open, "Opens"), drop_values(df_click, "Clicks")

def drop_values(df: pd.DataFrame, table: str):
    """Drop rows with null and zero values

    Args:
        df (pd.DataFrame): dataframe to clean
        table (str): columns name

    Returns:
        pd.DataFrame: dataframe cleaned
    """
    return df[df[f"Nº of {table}"].notnull() & (df[f"Nº of {table}"]!=0)]