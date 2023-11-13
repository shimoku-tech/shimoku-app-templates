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
    Función que genera el encabezado de la page
    page_name: variable que define el nombre de la pagina para el  encabezado
    devuelve el html para plotear.
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


def craft_html(css: str, html: str):
    """
    Combines the given CSS and HTML strings into a single HTML string
    with the CSS included in a <style> tag in the <head> section.

    Args:
        css (str): The CSS string to include in the <style> tag.
        html (str): The HTML string to include in the <body> section.

    Returns:
        str: The combined HTML string.
    """
    html = f"""
        <head>
            <style>
                {css}
            </style>
        </head>
        {html}
    """

    return html


def info_modal_predicted():
    """
    Modal content for the Predicted Opportunities page
    """
    html = """
    <article class="modal-article">
        <h4>Probability</h4>
        <p>The probability of recommending a product for each user is defined as follows: <code>Probability = Drivers + Barriers + Base value</code></p>

        <h4 class="h-top-space">Drivers & Barriers</h4>
        <p>
        It is the influence of each predictive variable with respect to each user and recommended product. This influence can be positive (Driver) or negative (Barrier). In the table, only a limited number of factors are shown and those whose influence is less than 1% are not shown.
        </p>

        <h4 class="h-top-space">Base Value</h4>
        <p>The average purchase probability of a product. It gives us a general idea about the popularity or purchase rate of the product in question. If the value is high, it could indicate that the product is generally popular or has a high probability of being purchased by an average user. If it is low, it could indicate the opposite.

This value acts as a starting point or reference value, and the drivers and barriers tell us how the prediction deviates from that starting point due to the presence (or absence) of certain user characteristics.</p>
    </article>
    """
    return craft_html(modals_css, html)
