import pandas as pd


movies = pd.read_csv("movies.csv", header=0)
ratings = pd.read_csv("ratings_small.csv", header=0)

def promote():
    # top 150 most rated movies
    top = ratings.groupby('movieId').count().sort_values('userId', ascending=False)[:150].index
    # 10 best rated movies considering rating population & scores
    best = ratings[ratings.index.isin(top)].groupby('movieId').mean()['rating'].sort_values(0, ascending=False)[:10].index
    recommendation = movies[movies.index.isin(best)][['id', 'title']]
    return recommendation