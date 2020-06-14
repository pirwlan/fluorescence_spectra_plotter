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


def read_files(args: dict) -> tuple:
    """
    Reads files from argumentparser into DataFrames.
    Args:
        args:

    Returns:
        df_excitation, df_emision: tuple of pd.DataFrames - DataFrame containing data of excitationa and emmision spectra.
    """
    df_excitation = pd.read_csv(args['excitation_file'],
                                index_col='wavelength',
                                sep=args['separator'])

    df_emission = pd.read_csv(args['emission_file'],
                              index_col='wavelength',
                              sep=args['separator'])

    return df_excitation, df_emission


def subtract_blank(dfs: list) -> list:
    """
    Substracts blank from samples.
    Args:
        dfs: list of pd.DataFrames - Excitation and emission dataframes

    Returns:
        dfs: list of pd.DataFrames - blank subtracted intensity values.
    """
    dfs_blank_subtracted = list()
    for df in dfs:
        df_blank_subtracted = df.subtract(df['blank'], axis=0)
        df_blank_subtracted.drop(columns=['blank'], inplace=True)
        dfs_blank_subtracted.append(df_blank_subtracted)

    return dfs_blank_subtracted
