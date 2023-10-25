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
        "<h1>"+title+"</h1>"
        "<p class='base-white'>"
        f"{subtitle}</p>"
        "</div>"
        "</div>"
    )
    return html

def download_button(button_url: str):
    css="""
    .download_btn{
        display: flex;
        justify-content: flex-end;
    }

    .download_btn button {
        background-color: var(--color-primary);
        color: white;
        padding: 1rem;
        border: 0px;
        border-radius: 10px;
    }
    """

    html = f"""
    <head>
        <style>
            {css}
        </style>
    </head>

    <!-- link button -->
    <div class="download_btn">
        <button>
            <a href='{button_url}'>
                Descargar todos los datos
            </a>
        </button>
    </div>
    """
    return html

def craft_html(css: str, html: str):
    html=f"""
        <head>
            <style>
                {css}
            </style>
        </head>
        {html}
    """

    return html

modals_css="""
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

def info_modal_predicted():
    """
    Modal content for page Predicted opportunities
    """
    html="""
    <article class="modal-article">
        <h4>Probability</h4>
        <p>La probabilidad de recomendación de un producto para cada usuario se define de la siguiente manera: <code>Probability = Drivers + Barriers + Base value</code></p>

        <h4 class="h-top-space">Drivers & Barriers</h4>
        <p>
        Es la influencia de cada variable predictiva respecto de cada usuario y producto recomendado. Esta influencia puede ser positiva (Driver) o negativa (Barrier). En la tabla, solo se muestra un número limitado de factores y no se muestran aquellos cuya influencia es menor del 1%
        </p>

        <h4 class="h-top-space">Base Value</h4>
        <p>Es la probabilidad media de compra de un producto. Nos da una idea general sobre la popularidad o tasa de compra del producto en cuestión. Si el valor es alto, podría indicar que el producto es generalmente popular o tiene una alta probabilidad de ser comprado por un usuario promedio. Si es bajo, podría indicar lo contrario.

Este valor actúa como un punto de partida o valor de referencia y los drivers and barriers nos dicen cómo se aleja la predicción de ese punto de partida debido a la presencia (o ausencia) de ciertas características de usuario.</p>
    </article>
    """
    return craft_html(modals_css,html)

def info_modal_ai_insights():
    """
    Modal content for pages 'AI insights'
    """
    html = """
    <article class="modal-article">
        <h4>Importance</h4>
        <p>Es la influencia que tiene cada ‘feature’ (variable predictiva) en la predicción de compra de un producto determinado. No se determina si la influencia es positiva o negativa. La suma de todos los valores da un total de 100, ya que los estos han sido normalizados.</p>

        <h4 class="h-top-space">Partial Dependence</h4>
        <p>
        Nos permite entender, por cada feature y de manera independiente de las demás, cómo aumenta o disminuye la probabilidad de compra de un producto. Aún así, hay que recordar que el patrón de conducta respecto a compra/no compra de un producto se forma por más de una variable (ingresos, lugar de residencia, edad…) y no solo por una. Por ejemplo: Podríamos observar que tener 35 años aumente la probabilidad de compra de un producto en un 50%, pero, la interacción de esta feature con las demás (ingresos, lugar de residencia…) podría hacer que disminuya la probabilidad de que el cliente compre un producto.
        </p>
    </article>
    """
    return craft_html(modals_css,html)

def modal_partial_dependence():

    html = """
    <article class="modal-article">
        <h4>Definición de categorías en features</h4>
        <p><b>idSex</b>: 0 = 1 Mutua; 1 = 2 Mutua</p>
    </article>
    """
    return craft_html(modals_css,html)
