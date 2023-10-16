import pandas as pd
from functools import cached_property

from utils.settings import data_file, data_folder

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


def format_number(number):
    """
    Format a number with thousands separator used in SPAIN.

    Args:
        number: The number to format.

    Returns:
        str: The formatted number as a string.
    """
    return "{0:,}".format(number).replace(",", ".")


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    """
    Read a CSV file and return its content as a DataFrame.

    Args:
        name (str): The name of the CSV file to read.
        **kwargs: Additional keyword arguments to pass to pd.read_csv().

    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    """
    return pd.read_csv(f"utils/{data_folder}/{name}.csv", **kwargs)


class DFs:
    """
    Collection of DataFrames.

    This class represents a collection of DataFrames used for data analysis.
    """

    @cached_property
    def df(self) -> pd.DataFrame:
        """
        Get the primary DataFrame.

        Returns:
            pd.DataFrame: The primary DataFrame containing data.
        """
        x = read_csv(data_file)
        return x
