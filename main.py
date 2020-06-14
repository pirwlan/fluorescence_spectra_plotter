import argparse
import helper as h
import os


def make_plots(args):

    data_dict = h.read_files(args)
    data_dict = h.subtract_blank(data_dict)
    h.plotting(data_dict)


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-ex", "--excitation_file",
                    type=str, required=True,
                    help="path to excitation file")

    ap.add_argument("-em", "--emission_file",
                    type=str, required=True,
                    help="path to emission file")

    ap.add_argument("-s", "--separator",
                    type=str, default=',',
                    help="separator of the csv file")

    args = vars(ap.parse_args())
    make_plots(args)

