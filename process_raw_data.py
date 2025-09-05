"""A script to process book data."""
import pandas as pd
import argparse
import re
import sys
import csv
import glob
import sqlite3


def author_db():
    """Connect to database"""
    conn = sqlite3.connect('./data/authors.db')
    cursor = conn.cursor()
    # This query gives all the names and ids of authors.
    query = """SELECT * FROM author;"""

    authors_data = pd.read_sql_query(query, conn)
    conn.close()
    return authors_data


def merge_databases(authors, raw_data):
    """Returns a merged database with author names."""
    merged_data = raw_data.merge(
        authors,
        left_on='author_id',
        right_on='id',
        how='left')

    # Rename the name column
    merged_data = merged_data.rename(columns={'name': 'author_name'})

    # Drop the ID columns if you want
    merged_data = merged_data.drop(
        ['author_id', 'id'], axis=1)

    return merged_data


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


def clean_title(title):
    """Remove content in brackets."""
    cleaned = re.sub(r'\(.*?\)', '', str(title))
    return cleaned.strip()


def process_data(data):
    """Process raw data to a csv file."""
    if 'book_title' in data.columns:
        data['title'] = data['book_title'].apply(clean_title)
        data['title'] = data['title'].replace({'nan': None})
    data = data.drop(
        ['index', 'Unnamed: 0.1', 'Unnamed: 0', 'book_title'], axis=1)
    data = data.dropna(subset=['title', 'author_name'])
    for column in ['year', 'ratings', 'Rating']:
        if column in data.columns:
            data[column] = data[column].astype(str).str.replace(
                '`', '').str.replace(',', '.').str.strip()

            data[column] = pd.to_numeric(data[column])
    data = data.dropna()
    if 'ratings' in data.columns:
        data = data.sort_values('ratings', ascending=False)
    return data


def save_to_file(data):
    """Save processed data to CSV file."""
    data.to_csv('PROCESSED_DATA.csv')


if __name__ == "__main__":
    args = get_command_line_arguments()
    raw_data = load_csv_file(args.input_file)
    authors = author_db()
    full_data = merge_databases(authors, raw_data)
    processed = process_data(full_data)
    save_to_file(processed)
    print(processed.head())
