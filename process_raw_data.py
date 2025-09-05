"""A script to process book data."""
import pandas as pd
import argparse
import re
import sys
import csv
import glob


def get_command_line_arguments():
    """Returns the given CLI Arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file',
        help='Path to input file'
    )
    return parser.parse_args()


def load_csv_file(input_file: str):
    """ Loading the csv files to the database."""
    data = pd.read_csv(input_file)
    return data


def clean_title():
    """Remove content in brackets."""
    pass


if __name__ == "__main__":
    args = get_command_line_arguments()
    raw_data = load_csv_file(args.input_file)
    print(raw_data.head())
