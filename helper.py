import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd




def create_folder(folders: list):
    """
    Creates folder indicated by path.
    Args:
        folders: list - List of folders to create
    """

    for folder in folders:
        try:
            os.mkdir(folder)

        except FileExistsError:
            pass


def read_files(args: dict) -> dict:
    """
    Reads files from argumentparser into DataFrames.
    Args:
        args:

    Returns:
        dict_df: dict of pd.DataFrames - DataFrame containing data of excitationa and emmision spectra.
    """
    df_dict = dict()
    df_dict['excitation_spectra'] = pd.read_csv(args['excitation_file'],
                                                index_col='wavelength',
                                                sep=args['separator'])
    df_dict['excitation_spectra'].name = 'excitation'

    df_dict['emission_spectra'] = pd.read_csv(args['emission_file'],
                                              index_col='wavelength',
                                              sep=args['separator'])
    df_dict['emission_spectra'].name = 'emission'

    return df_dict


def subtract_blank(dfs: dict) -> dict:
    """
    Substracts blank from samples.
    Args:
        dfs: dict of pd.DataFrames - Contains excitation and emission dataframes

    Returns:
        dfs: dict of pd.DataFrames - blank subtracted intensity values.
    """

    for condition in dfs.keys():
        dfs[condition] = dfs[condition].subtract(dfs[condition]['blank'], axis=0)
        dfs[condition].drop(columns=['blank'], inplace=True)

    return dfs


def normalize(data: pd.Series):
    """
    normalizes the data by the highest value
    Args:
        data: pd.Series - input data

    Returns:
        data_norm: pd.Series - normalized input data

    """
    data_norm = data / max(data)

    return data_norm


def determine_color(data: pd.Series, gamma=0.8) -> tuple:
    """
    Determines color of plot dependent on the
    intensity maximum of the meassured wavelength.

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    and Noah Spurrier
    http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

    Args:
        data: pd.DataSeries
        gamma: float - Default 0.8

    Returns:
        color: sting - color of the spectra

    """
    max_nm = data.idxmax()

    wavelength = float(max_nm)
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255

    return float(R/255), float(G/255), float(B/255)


def plotting(dfs: dict):
    """
    Plots fluorescent spectra of the given excitation and emission spectra

    Args:
        dfs: dict of pd.DataFrame - contains excitation and emission spectra
    """
    PLOT_PATH = os.path.join(os.getcwd(), 'plots')
    create_folder([PLOT_PATH])

    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    samples = dfs['excitation_spectra'].columns

    ex_nm = dfs['excitation_spectra'].index
    em_nm = dfs['emission_spectra'].index

    fontdic = {'fontweight': 30}

    for sample in samples:
        ex_data = dfs['excitation_spectra'][sample]
        em_data = dfs['emission_spectra'][sample]

        ex_data = normalize(ex_data)
        em_data = normalize(em_data)

        ex_col = determine_color(ex_data)
        em_col = determine_color(em_data)

        for wavelength, data, color, style, label in zip([ex_nm, em_nm],
                                                         [ex_data, em_data],
                                                         [ex_col, em_col],
                                                         ['dashed', 'solid'],
                                                         ['excitation spectra', 'emission spectra']):

            plt.plot(wavelength,
                     data,
                     color=color,
                     linestyle=style,
                     label=label)

        plt.legend(frameon=False,
                   loc='center',
                   bbox_to_anchor=(0.5, 1.04),
                   ncol=2,
                   fontsize=13)

        plt.yticks(np.arange(0, 1.1, 0.2),
                   fontsize=13)

        plt.ylabel('relative intensity (%)')

        plt.xticks(np.arange(np.min(ex_nm),
                             np.max(em_nm) + 10,
                             20),
                   fontsize=13)

        plt.xlabel('wavelength (nm)')

        plt.xlim(np.min(ex_nm),
                 np.max(em_nm))

        plt.title(f'{sample}',
                  pad=25,
                  fontsize=16)

        plt.savefig(os.path.join(PLOT_PATH, f'{current_date}_{sample}.png'),
                    dpi=600)

        plt.figure(figsize=(8, 5))
        plt.clf()

