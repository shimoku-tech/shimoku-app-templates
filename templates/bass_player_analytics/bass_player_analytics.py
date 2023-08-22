from os import getenv
from typing import List, Dict, Tuple
import pandas as pd
from aux import get_data
from copy import deepcopy
import shimoku_api_python as shimoku


def page_header(s: shimoku.Client, data: Dict):
    s.plt.html(
        order=0, rows_size=2, cols_size=8,
        html=s.html_components.box_with_button(
            title='BassPlayer Analytics Dashboard',
            line='Bass centric song analytics',
            background="https://gcdnb.pbrd.co/images/0aqp633hbl3X.jpg?o=1",
            href='https://shimoku.com',
            button_text='Visit Shimoku',
        ),
    )
    s.plt.set_bentobox(cols_size=4, rows_size=2)
    s.plt.html(html=data['link_button_github'], padding='1,1,0,1',
               order=1, cols_size=6, rows_size=3)
    s.plt.html(html=data['link_button_youtube'], padding='1,1,0,1',
               order=2, cols_size=6, rows_size=3)
    s.plt.html(html=data['link_button_medium'], padding='1,1,0,1',
               order=3, cols_size=6, rows_size=3)

    s.plt.html(
        order=4, cols_size=24, rows_size=20, padding='0,1,0,1',
        html='The BassPlayer Analytics Dashboard is a powerful tool designed to provide bass players with valuable '
             'insights into their recordings and enhance their playing skills. It offers a visually appealing and '
             'intuitive interface that allows bass players to analyze their songs and explore their playing data '
             'in a comprehensive manner.'
    )
    s.plt.pop_out_of_bentobox()

    # Crete the modal now because the explanation can be shared for all songs
    s.plt.set_modal('Chroma Heatmap')
    s.plt.html(order=0, cols_size=12, rows_size=2,
               html=('<h3>Chroma Heatmap Visualization</h3>'
                     '<p> This visualization offers a unique perspective on the distribution of chroma '
                     'frequencies over time in your recordings. By analyzing the tonal content of your bass playing, '
                     'it allows you to gain valuable insights into the harmonic characteristics and '
                     'patterns of your performances.</p>')
               )
    s.plt.pop_out_of_modal()


def amplitude_chart(
    s: shimoku.Client, df: pd.DataFrame, x: str, y: List[str],
    cols_size: int, rows_size: int, order: int, legend: bool = False, padding: str = '0,0,0,0'
):
    v_cols = []
    for y_value in y:
        df[y_value] = abs(df[y_value])
        df[f'-{y_value}'] = -df[y_value]
        v_cols.extend([y_value, f'-{y_value}'])

    df = df[[x, *v_cols]]
    chart_options = {
        'legend': {
            'show': legend,
            'type': 'scroll',
            'itemGap': 16,
            'icon': 'circle'
        },
        'xAxis': {
            'data': '#set_data#',
            'fontFamily': 'Rubik',
            'type': 'category',
            'nameLocation': 'middle',
            'nameGap': 30,
        },
        'yAxis': {
            'show': False,
            'fontFamily': 'Rubik',
            'type': 'value',
        },
        'grid': {
            'left': '0%',
            'right': '2%',
            'bottom': '8%',
            'top': '2%',
            'containLabel': True
        },
        'series': [
            {
                'type': 'line',
                'data': '#set_data#',
                'smooth': True,
                'name': name,
                'color': f'var(--chart-C{i+1})',
                'symbol': 'none',
                'areaStyle': {'opacity': 0.25 if len(y) > 1 else 0.5},
                'emphasis': {
                    'lineStyle': {'color': f'var(--chart-C{i+1})'},
                    'areaStyle': {'opacity': 0.25 if len(y) > 1 else 0.5, 'color': f'var(--chart-C{i+1})'},
                }
            }
            for i, o_name in enumerate(y)
            for name in [o_name, f'-{o_name}']]
    }
    s.plt.free_echarts(
        data=df, padding=padding,
        options=chart_options, order=order,
        rows_size=rows_size, cols_size=cols_size,
        fields=[x, *v_cols]
    )


def fft_bar(s: shimoku.Client, fft_data: pd.DataFrame, order: int):
    s.plt.infographics_text_bubble(
        order=order, title='Frequency Space', bubble_location='left',
        text='Gain a deeper understanding of the frequency distribution in your recordings. Identify dominant '
             'frequencies and detect tonal imbalances or excessive frequencies that may need adjustment, '
             'such as a high-pitched whine or a low rumble.',
        chart_function=s.plt.bar,
        chart_parameters={
            'data': fft_data, 'x': 'frequency', 'y': ['amplitude'],
            'padding': '1,0,0,1', 'cols_size': 20, 'rows_size': 32,
            'x_axis_name': 'Frequency (Hz)', 'y_axis_name': 'Amplitude',
            'option_modifications': {
                'grid': {'left': '5%', 'right': '0%', 'bottom': '5%', 'top': '2%', 'containLabel': True},
                'toolbox': {'show': False},
            },
        }
    )


def chroma_heatmap(
    s: shimoku.Client, chroma_data: List[List], chroma_heatmap_options: Dict, order: int
):
    s.plt.chart_and_modal_button(
        order=order,
        button_label='Info',
        button_modal='Chroma Heatmap',
        button_side_text='Heatmap visualization of the chroma frequencies',
        chart_function=s.plt.free_echarts,
        chart_parameters=dict(
            rows_size=23,
            cols_size=24,
            padding='2,0,0,0',
            data=chroma_data,
            options=chroma_heatmap_options,
            fields=[('time', 'pitch', 'amplitude')]
        )
    )


def separated_instruments_charts(s: shimoku.Client, song_name: str, order: int, data: Dict, parent_tabs_index: Tuple):
    s.plt.set_bentobox(cols_size=12, rows_size=3)
    s.plt.html(html=f'<h3>Separated Instruments and tracks</h3>'
                    f'<p>Using a machine learning model, we separate the song into 3 tracks: drums, bass and other. '
                    f'This allows us to see more fine grained information about the song and the individual '
                    f'instruments.</p>',
               order=order, cols_size=22, rows_size=5, padding='1,1,1,1')

    tracks_to_get = ['bass', 'other', 'drums']
    amplitude_chart(
        s=s,
        df=pd.concat(
            [data[song_name]['bass']['amplitude']['time']] +
            [data[song_name][track]['amplitude'][['amplitude']].rename({'amplitude': track}, axis=1)
             for track in tracks_to_get], axis=1),
        x='time', y=tracks_to_get, order=order+1, cols_size=11, padding='0,1,0,0',
        rows_size=21, legend=True
    )

    s.plt.set_tabs_index(tabs_index=(f'{song_name} - Tracks', tracks_to_get[0]),
                         order=order+2, cols_size=11, rows_size=2, parent_tabs_index=parent_tabs_index)
    for track in tracks_to_get:
        s.plt.change_current_tab(track)
        chart_options = deepcopy(data['chroma_heatmap_options'])
        chart_options['xAxis']['name'] = ''
        chart_options['yAxis']['name'] = ''
        s.plt.free_echarts(
            rows_size=2, cols_size=12, order=0,
            data=data[song_name][track]['chroma'],
            options=chart_options, fields=[('time', 'pitch', 'amplitude')]
        )
    s.plt.pop_out_of_bentobox()
    s.plt.set_tabs_index(tabs_index=parent_tabs_index)


def song_tab(s: shimoku.Client, name: str, url: str, data: Dict):
    s.plt.set_tabs_index(tabs_index=('Songs', name), order=6)
    s.plt.html(
        order=0, cols_size=12, rows_size=2,
        html=s.html_components.create_h1_title_with_modal(
            title='Song Overview',
            subtitle='General song visualization',
            background_color='var(--color-base-icon)',
            modal_title='Processing Songs',
            modal_text='The songs provided from the YouTube codes are converted to an array of numbers '
                       'representing the amplitude of the songs at each point in time. This way, we can '
                       'visualize and analyze them in a variety of ways. Any public YouTube video can be '
                       'used.'
        )
    )
    s.plt.set_bentobox(cols_size=12, rows_size=2)
    amplitude_chart(s, df=data[name]['amplitude'], x='time', y=['amplitude'], cols_size=16, rows_size=22, order=1)

    s.plt.iframe(order=2, cols_size=8, height=352, url=url)
    s.plt.pop_out_of_bentobox()

    fft_bar(s, fft_data=data[name]['fft'], order=4)
    chroma_heatmap(s, chroma_data=data[name]['chroma'], chroma_heatmap_options=data['chroma_heatmap_options'], order=6)

    # Make sure to have the necessary files in the separated songs folder
    # separated_instruments_charts(s, song_name=name, order=9, data=data, parent_tabs_index=('Songs', name))


def main():
    s = shimoku.Client(
        access_token=getenv('API_TOKEN'),
        universe_id=getenv('UNIVERSE_ID'),
        async_execution=True,
        verbosity='INFO',
    )
    s.reuse_data_sets()
    s.set_workspace(getenv('WORKSPACE_ID'))
    s.set_menu_path('BassPlayer')
    # s.plt.clear_menu_path()

    n_samples = 100
    data = get_data(n_samples)

    page_header(s, data)
    for name, url in data['song_tuples']:
        song_tab(s, name, url, data)

    s.run()


if __name__ == '__main__':
    main()
