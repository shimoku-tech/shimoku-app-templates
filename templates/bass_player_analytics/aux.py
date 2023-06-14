from os import listdir
from typing import List, Dict, Tuple
import librosa
import numpy as np
import pandas as pd
from pytube import YouTube


def retrieve_songs_data(yt_codes) -> List[Tuple[str, Tuple[np.ndarray, float], str]]:
    """ Retrieves the songs data from youtube and saves them in the songs folder """
    names = []
    yt_urls = [f'https://www.youtube.com/embed/{yt_code}' for yt_code in yt_codes]
    for url in yt_urls:
        yt = YouTube(url)

        video = yt.streams.filter(only_audio=True).first()
        names += [video.title]
        if video.title+'.mp4' not in listdir('songs'):
            video.download(output_path='songs')
            print(f'File {video.title+".mp4"} downloaded successfully')

    songs_data = []

    for name in names:
        songs_data.append(librosa.load(f'songs/{name}.mp4'))  # needs ffmpeg to be installed

    return list(zip(names, songs_data, yt_urls))


def calculate_amplitude_df(song_data: Tuple[np.ndarray, float], n_samples: int) -> pd.DataFrame:
    """  Calculates the amplitude of a song in n_samples parts """
    song, sr = song_data
    abs_song = np.abs(song)
    grouped_song = np.array_split(abs_song, n_samples)
    resized_song = np.array([np.mean(group) for group in grouped_song])
    song_length_s = librosa.get_duration(y=song, sr=sr)
    times = [f'{int(t // 60)}:{int(t % 60)}.{int((t % 1) * 1000)}'
             for t in [song_length_s / n_samples * i for i in range(n_samples)]]

    return pd.DataFrame({'time': times, 'amplitude': resized_song})


def calculate_fft_df(song_data: Tuple[np.ndarray, float], n_samples: int) -> pd.DataFrame:
    """  Calculates the FFT of a song in n_samples parts """
    song, sr = song_data
    # Perform FFT on the data
    fft_values = np.fft.fft(song)

    # Calculate the frequencies corresponding to the FFT values
    freq = np.fft.fftfreq(len(fft_values), 1 / sr)

    # Keep only the positive frequencies
    positive_freq = freq[:len(freq) // 2]

    # Keep only the corresponding FFT values for the positive frequencies
    positive_fft_values = 2.0 / len(song) * np.abs(fft_values[:len(fft_values) // 2])

    # Select a specific number of values for the plot
    freq_ranges = [f'{int(freq_range[0])} - {int(freq_range[-1])}'
                   for freq_range in np.array_split(positive_freq, n_samples)]
    mean_fft_values = np.array([np.mean(group) for group in np.array_split(positive_fft_values, n_samples)])
    return pd.DataFrame({'amplitude': mean_fft_values, 'frequency': freq_ranges})


def calculate_chroma_df(song_data: Tuple[np.ndarray, float], n_samples: int) -> List[List]:
    """  Calculates the chroma of a song in n_samples parts"""
    song, sr = song_data
    song_length_s = librosa.get_duration(y=song, sr=sr)
    times = [f'{int(t // 60)}:{int(t % 60)}.{int((t % 1) * n_samples)}'
             for t in [song_length_s / n_samples * i for i in range(n_samples)]]
    chroma = librosa.feature.chroma_stft(y=song, sr=sr)
    chroma_data = []
    pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
    for pitch, row in zip(pitches, chroma):
        grouped_row = np.array_split(row, n_samples)
        chroma_data.extend([[t, pitch, round(float(np.mean(group)), 2)] for t, group in zip(times, grouped_row)])

    return chroma_data


def get_data(n_samples: int) -> Dict:

    result = {}
    #-------------- BUTTON DEFINITIONS --------------#
    result['link_button_github'] = (
        "<head>"
        # Start styles button
        "<style>"
        ".vertical-block"
        "{display: contents; position: relative; width: 100%; height: 100%;}"
        #
        ".button-github"
        "{display: flex; width: 100%; height: auto; background-color: var(--color-grey-400);"  # Change bg color
        "padding: 5% 5%; border-radius: var(--border-radius-xl);"  # Change padding to increase width and height
        "font-size: 14px; color: var(--color-black); box-shadow: var(--box-shadow-m); transition-duration: 0.3s;}"
        ".button-github:hover{background-color: var(--color-grey-700); color: var(--color-white);}"
        # Change bg and text hover colors
        "</style>"
        # End styles button
        "</head>"
        "<div class='vertical-block'>"
        "<a href='https://github.com/shimoku-tech/shimoku-api-python' target='_blank'>"  # link button
        "<div class='button-github'>"
        "<img src='https://asset.brandfetch.io/idZAyF9rlg/id6a3YYV60.svg' alt='Github Logo' "
        "style='width: 32px; height: 32px; margin: auto; color: var(--color-white)'>"  # logo button
        "</div>"
        "</a>"
    )

    result['link_button_youtube'] = (
        "<head>"
        # Start styles button
        "<style>"
        ".vertical-block"
        "{display: contents; position: relative; width: 100%; height: 100%;}"
        #
        ".button-youtube"
        "{display: flex; width: 100%; height: auto; background-color: var(--color-grey-400);"  # Change bg color
        "padding: 5% 5%; border-radius: var(--border-radius-xl);"  # Change padding to increase width and height
        "font-size: 14px; color: var(--color-white); box-shadow: var(--box-shadow-m); transition-duration: 0.3s;}"
        ".button-youtube:hover{background-color: var(--color-error); color: var(--color-white);}"  # Change bg and text hover colors
        "</style>"
        # End styles button
        "</head>"
        "<div class='vertical-block'>"
        "<a href='https://www.youtube.com/channel/UCczfV4nMrDbvWzcieE5x3DA' target='_blank'>"  # link button
        "<div class='button-youtube'>"
        "<img src='https://asset.brandfetch.io/idVfYwcuQz/id2kTxk9Xc.svg' alt='YouTube Logo' style='width: 32px; height: 32px; margin: auto;'>"  # logo button
        "</div>"
        "</div>"
    )

    result['link_button_medium'] = (
        "<head>"
        # Start styles button
        "<style>"
        ".vertical-block"
        "{display: contents; position: relative; width: 100%; height: 100%;}"
        #
        ".button-medium"
        "{display: flex; width: 100%; height: auto; background-color: var(--color-grey-400);"  # Change bg color
        "padding: 5% 5%; border-radius: var(--border-radius-xl);"  # Change padding to increase width and height
        "font-size: 14px; color: var(--color-black); box-shadow: var(--box-shadow-m); transition-duration: 0.3s;}"
        ".button-medium:hover{background-color: var(--color-grey-700); color: var(--color-white);}"  # Change bg and text hover colors
        "</style>"
        # End styles button
        "</head>"
        "<a href='https://medium.com/@shimoku' target='_blank'>"  # link button
        "<div class='button-medium'>"
        "<img src='https://asset.brandfetch.io/idIlQtGZ76/idZjmnIZEk.svg' alt='medium Logo' style='width: 32px; height: 32px; margin: auto;'>"  # logo button
        "</div>"
        "</a>"
        "</div>"
    )
    #-------------- CHROMA ECHART --------------#
    result['chroma_heatmap_options'] = {
        'toolbox': {'show': False},
        'grid': {
            'left': '2%',
            'right': '2%',
            'bottom': '8%',
            'top': '8%',
            'containLabel': True
        },
        'xAxis': {
            'nameLocation': 'middle',
            'nameGap': 35,
            'name': 'Time',
            'type': 'category',
        },
        'yAxis': {
            'name': 'Pitch',
            'nameLocation': 'middle',
            'nameGap': 35,
            'type': 'category',
        },
        'visualMap': {
            'min': 0,
            'max': 1,
            'type': 'piecewise',
            'orient': 'horizontal',
            'top': 'top',
            'left': 'center',
        },
        'series': [{
            'type': 'heatmap',
            'label': {'show': False},
            'animation': False,
            'progressive': 100,
        }]
    }
    #-------------- FOR EACH SONG --------------#
    yt_codes = ['ZwvkDlLOkr0', 'Z2BVPNDWPmI', 'lQtvpAp8xN0']
    song_tuples = retrieve_songs_data(yt_codes)
    result['song_tuples'] = [(name, url) for name, _, url in song_tuples]
    for name, song_data, url in song_tuples:
        result[name] = {
            'amplitude': calculate_amplitude_df(song_data, n_samples),
            'fft': calculate_fft_df(song_data, n_samples),
            'chroma': calculate_chroma_df(song_data, n_samples)
        }
        # This is a premium feature, by default use the local files
        # s.activity.execute_activity('Separate Instruments', params: {'song_data': song})
        # Make sure to have the necessary files in the separated songs folder
        # for track in ['bass', 'other', 'drums']:
        #     track_loaded = librosa.load(f'separated_songs/{name}/{track}.mp3')
        #     result[name][track] = {
        #         'amplitude': calculate_amplitude_df(track_loaded, n_samples),
        #         'chroma': calculate_chroma_df(track_loaded, n_samples)
        #     }

    return result

