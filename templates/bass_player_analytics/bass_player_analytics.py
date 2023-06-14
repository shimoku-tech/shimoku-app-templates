from os import getenv
from typing import List, Dict, Tuple, Optional
import pandas as pd
from aux import get_data
from copy import deepcopy
import shimoku_api_python as shimoku


def page_header(s: shimoku.Client, menu_path: str, data: Dict):
    s.plt.html(
        menu_path=menu_path, order=0,
        rows_size=2, cols_size=8,
        html=s.html_components.box_with_button(
            title='BassPlayer Analytics Dashboard',
            line='Bass centric song analytics',
            background="https://gcdnb.pbrd.co/images/0aqp633hbl3X.jpg?o=1",
            href='https://shimoku.com',
            button_text='Visit Shimoku',
        ),
    )
    bentobox_data = {
        'bentoboxId': 'BassPlayerLinks',
        'bentoboxOrder': 1,
        'bentoboxSizeColumns': 4,
        'bentoboxSizeRows': 2,
    }
    s.plt.html(html=data['link_button_github'], menu_path=menu_path, padding='1,1,0,1',
               order=1, cols_size=6, rows_size=3, bentobox_data=bentobox_data)
    s.plt.html(html=data['link_button_youtube'], menu_path=menu_path, padding='1,1,0,1',
               order=2, cols_size=6, rows_size=3, bentobox_data=bentobox_data)
    s.plt.html(html=data['link_button_medium'], menu_path=menu_path, padding='1,1,0,1',
               order=3, cols_size=6, rows_size=3, bentobox_data=bentobox_data)

    s.plt.html(
        menu_path='BassPlayer', order=4, cols_size=24, rows_size=20, padding='0,1,0,1',
        html='The BassPlayer Analytics Dashboard is a powerful tool designed to provide bass players with valuable '
             'insights into their recordings and enhance their playing skills. It offers a visually appealing and '
             'intuitive interface that allows bass players to analyze their songs and explore their playing data '
             'in a comprehensive manner.',
        bentobox_data=bentobox_data,
    )

    # Crete the modal now because the explanation can be shared for all songs
    s.plt.html(menu_path=menu_path, order=0, modal_name='Chroma Heatmap', cols_size=12, rows_size=2,
               html=('<h3>Chroma Heatmap Visualization</h3>'
                     '<p> This visualization offers a unique perspective on the distribution of chroma '
                     'frequencies over time in your recordings. By analyzing the tonal content of your bass playing, '
                     'it allows you to gain valuable insights into the harmonic characteristics and '
                     'patterns of your performances.</p>')
               )

    s.plt.update_tabs_group_metadata(menu_path=menu_path, group_name='Songs', order=6)


def amplitude_chart(s: shimoku.Client, df: pd.DataFrame, x: str, y: List[str],
                    cols_size: int, rows_size: int, menu_path: str, order: int,
                    tabs_index: Optional[Tuple[str, str]] = None, bentobox_data: Optional[Dict] = None,
                    legend: bool = False, padding: str = '0,0,0,0'):
    v_cols = []
    for y_value in y:
        df[y_value] = abs(df[y_value])
        df[f'-{y_value}'] = -df[y_value]
        v_cols.extend([y_value, f'-{y_value}'])

    df['sort_values'] = range(len(df))
    df = df[[x, *v_cols, 'sort_values']]
    chart_options = {
        'legend': {
            'show': legend,
            'type': 'scroll',
            'itemGap': 16,
            'icon': 'circle'
        },
        'xAxis': {
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
                'smooth': True,
                'name': name,
                'color': f'var(--chart-C{i+1})',
                'symbol': 'none',
                'areaStyle': {'opacity': 0.25 if len(y) > 1 else 0.5},
                'emphasis': {
                    'lineStyle': {'color': f'var(--chart-C{i+1})'},
                    'areaStyle': {'opacity': 0.25 if len(y) > 1 else 0.5 , 'color': f'var(--chart-C{i+1})'},
                }
            }
            for i, o_name in enumerate(y)
            for name in [o_name, f'-{o_name}']]
    }
    s.plt.free_echarts(
        data=df, menu_path=menu_path, padding=padding,
        options=chart_options, order=order,
        tabs_index=tabs_index, bentobox_data=bentobox_data,
        rows_size=rows_size, cols_size=cols_size,
        sort={'field': 'sort_values', 'direction': 'asc'}
    )


def fft_bar(s: shimoku.Client, fft_data: pd.DataFrame, order: int,
            menu_path: str, tabs_index: Optional[Tuple[str, str]] = None):
    s.plt.infographics_text_bubble(
        menu_path=menu_path, order=order, title='Frequency Space', bubble_location='left',
        text='Gain a deeper understanding of the frequency distribution in your recordings. Identify dominant '
             'frequencies and detect tonal imbalances or excessive frequencies that may need adjustment, '
             'such as a high-pitched whine or a low rumble.',
        tabs_index=tabs_index,
        chart_function=s.plt.bar,
        chart_parameters={
            'data': fft_data, 'x': 'frequency', 'y': ['amplitude'],
            'padding': '1,0,0,1', 'cols_size': 20, 'rows_size': 34,
            'option_modifications': {
                'xAxis': {'nameLocation': 'middle', 'nameGap': 30, 'name': 'Frequency (Hz)'},
                'yAxis': {'nameLocation': 'middle', 'nameGap': 30, 'name': 'Amplitude'},
                'grid': {'left': '5%', 'right': '0%', 'bottom': '5%', 'top': '2%', 'containLabel': True},
                'toolbox': {'show': False},
            },
        }
    )


def chroma_heatmap(s: shimoku.Client, chroma_data: List[List], chroma_heatmap_options: Dict, order: int,
                   menu_path: str, tabs_index: Optional[Tuple[str, str]] = None):

    chart_options = deepcopy(chroma_heatmap_options)
    chart_options['series'][0]['data'] = chroma_data

    s.plt.chart_and_modal_button(
        menu_path=menu_path,
        order=order, tabs_index=tabs_index,
        button_label='Info',
        button_modal='Chroma Heatmap',
        button_side_text='Heatmap visualization of the chroma frequencies',
        chart_function=s.plt.free_echarts,
        chart_parameters=dict(
            rows_size=23,
            cols_size=24,
            padding='2,0,0,0',
            data=[{'dummy': 0}],
            options=chart_options,
        )
    )


def separated_instruments_charts(
        s: shimoku.Client, song_name: str, order: int, data: Dict, menu_path: str,
        tabs_index: Optional[Tuple[str, str]] = None
):
    bentobox_data = {
        'bentoboxId': 'Separated Instruments',
        'bentoboxOrder': order,
        'bentoboxSizeColumns': 12,
        'bentoboxSizeRows': 3,
    }

    s.plt.html(html=f'<h3>Separated Instruments and tracks</h3>'
                    f'<p>Using a machine learning model, we separate the song into 3 tracks: drums, bass and other. '
                    f'This allows us to see more fine grained information about the song and the individual '
                    f'instruments.</p>',
               order=order,
               menu_path=menu_path, tabs_index=tabs_index, bentobox_data=bentobox_data,
               cols_size=22, rows_size=5, padding='1,1,1,1')
    tracks_to_get = ['bass', 'other', 'drums']
    amplitude_chart(
        s=s,
        df=pd.concat(
            [data[song_name]['bass']['amplitude']['time']] +
            [data[song_name][track]['amplitude'][['amplitude']].rename({'amplitude': track}, axis=1)
             for track in tracks_to_get], axis=1),
        x='time', y=tracks_to_get, order=order+1, cols_size=11, padding='0,1,0,0',
        rows_size=21, menu_path=menu_path, tabs_index=tabs_index, bentobox_data=bentobox_data, legend=True
    )

    tabs_group_name = f'{song_name} - Tracks'
    for track in tracks_to_get:
        tracks_tabs_index = (tabs_group_name, track)
        chart_options = deepcopy(data['chroma_heatmap_options'])
        chart_options['series'][0]['data'] = data[song_name][track]['chroma']
        chart_options['xAxis']['name'] = ''
        chart_options['yAxis']['name'] = ''
        s.plt.free_echarts(
            rows_size=2,
            cols_size=12,
            data=[{'dummy': 0}],
            options=chart_options,
            menu_path=menu_path,
            order=0, tabs_index=tracks_tabs_index,
        )

    s.plt.insert_tabs_group_in_tab(
        menu_path=menu_path, parent_tab_index=tabs_index,
        child_tabs_group=tabs_group_name,
    )
    s.plt.update_tabs_group_metadata(
        menu_path=menu_path, group_name=tabs_group_name,
        bentobox_data=bentobox_data, just_labels=True,
        order=order + 2, cols_size=11, rows_size=2,
    )


def song_tab(s: shimoku.Client, menu_path: str, name: str, url: str, data: Dict):
    tabs_index = ('Songs', name)
    s.plt.html(
        menu_path=menu_path, order=0, cols_size=12, rows_size=2,
        html=s.html_components.create_h1_title_with_modal(
        title='Song Overview',
        subtitle='General song visualization',
        background_color='var(--color-base-icon)',
        modal_title='Processing Songs',
        modal_text='The songs provided from the YouTube codes are converted to an array of numbers '
                   'representing the amplitude of the songs at each point in time. This way, we can '
                   'visualize and analyze them in a variety of ways. Any public YouTube video can be '
                   'used.'),
        tabs_index=tabs_index)
    bentobox_data = {
        'bentoboxId': name,
        'bentoboxOrder': 1,
        'bentoboxSizeColumns': 24,
        'bentoboxSizeRows': 2,
    }
    amplitude_chart(s, df=data[name]['amplitude'], x='time', y=['amplitude'], cols_size=16, rows_size=22,
                    menu_path=menu_path, order=1, tabs_index=tabs_index, bentobox_data=bentobox_data)

    s.plt.iframe(menu_path=menu_path, order=2, cols_size=8, rows_size=2, height=352,
                 url=url, tabs_index=tabs_index, bentobox_data=bentobox_data)

    fft_bar(s, fft_data=data[name]['fft'], order=4, menu_path=menu_path, tabs_index=tabs_index)
    chroma_heatmap(s, chroma_data=data[name]['chroma'], chroma_heatmap_options=data['chroma_heatmap_options'],
                   order=6, menu_path=menu_path, tabs_index=tabs_index)

    # Make sure to have the necessary files in the separated songs folder
    # separated_instruments_charts(s, song_name=name, order=9, menu_path=menu_path,
    #                              tabs_index=tabs_index, data=data)


def main():
    s = shimoku.Client(
        access_token=getenv('API_TOKEN'),
        universe_id=getenv('UNIVERSE_ID'),
        environment=getenv('ENVIRONMENT'),
        business_id=getenv('BUSINESS_ID'),
        async_execution=True,
        verbosity='INFO',
    )
    menu_path = 'BassPlayer'
    s.plt.delete_path(menu_path)

    n_samples = 100
    data = get_data(n_samples)

    page_header(s, menu_path, data)
    for name, url in data['song_tuples']:
        song_tab(s, menu_path, name, url, data)

    s.run()


if __name__ == '__main__':
    main()
