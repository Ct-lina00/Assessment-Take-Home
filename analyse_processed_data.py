"""A script to analyse book data."""
import pandas as pd
import altair as alt


def load_data():
    return pd.read_csv('PROCESSED_DATA.csv')


def create_decade_chart(data):
    """a pie chart showing the proportion of books released in each decade."""
    data['decade'] = (data['Year'] // 10) * 10
    decade_counts = data['decade'].value_counts().reset_index()
    decade_counts.columns = ['decade', 'count']

    chart = alt.Chart(decade_counts).mark_arc().encode(
        theta=alt.Theta('count:Q'),
        color=alt.Color('decade:N', title='Decade'),
        tooltip=['decade:N', 'count:Q']
    )

    return chart.save('decade_releases.png')


def create_authors_chart(data):
    """a sorted bar chart showing the total number of ratings for the ten most-rated authors."""
    pass


if __name__ == "__main__":
    data = load_data()
    create_authors_chart(data)
