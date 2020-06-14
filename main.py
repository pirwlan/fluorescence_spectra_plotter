import argparse
import helper as h
import matplotlib.pyplot as plt
import os
import pandas as pd


def make_plots(args):

    df_ex, df_em = h.read_files(args)
    df_ex, df_em = h.subtract_blank([df_ex, df_em])
    print(df_em)


if __name__ == '__main__':

    DATA_PATH = os.path.join(os.getcwd(), 'data')
    PLOT_PATH = os.path.join(os.getcwd(), 'plots')

    h.create_folder([PLOT_PATH])

    # ap = argparse.ArgumentParser()
    # ap.add_argument("-ex", "--excitation_file",
    #                 type=str, required=True,
    #                 help="path to input file")
    #
    # ap.add_argument("-em", "--emission_file",
    #                 type=str, required=True,
    #                 help="path to input file")
    #
    # args = vars(ap.parse_args())
    args = dict()
    args['excitation_file'] = '03_ex420-490_em530.csv'
    args['emission_file'] = '01_ex450_em472-574.csv'
    args['separator'] = ';'
    make_plots(args)

