import pandas as pd
import numpy as np
from tqdm import tqdm

movies = pd.read_csv("movies.csv", header=0)
ratings = pd.read_csv("ratings_small.csv", header=0)

movies = movies.replace({np.nan: None})
# drop implicit duplicates as many as possible
movies.drop_duplicates(inplace=True)
movies.drop_duplicates(['id'], inplace=True)

# extract movies' content
movie_profile = movies[['id', 'title', 'genres']]
movie_profile.rename(columns={'id': 'movieId'}, inplace=True)

# one-hot encoding the genres
all_genres = [s.split(", ") for s in movies[movies.genres.notnull()].genres]
genres = [item.strip() for l in all_genres for item in l]
unique_genres = set(genres)
for genre in unique_genres:
    movie_profile[genre] = 0

for i in range(len(movie_profile)):
    if type(movie_profile['genres'].iloc[i]) != None.__class__:
        Genres = movie_profile.iloc[i].genres.split(', ')
        for g in Genres:
            movie_profile[g].iloc[i] = 1

movie_profile = movie_profile.drop(columns=['title', 'genres']).set_index('movieId')
movie_profile.sort_index(axis=0, inplace=True)

# generate users' content
user_x_movie = pd.pivot_table(ratings, values='rating', index=['movieId'], columns=['userId'])
user_x_movie.sort_index(axis=0, inplace=True)
userIDs = user_x_movie.columns
user_profile = pd.DataFrame(columns=movie_profile.columns)

for i in tqdm(range(len(user_x_movie.columns))):
    working_df = movie_profile.mul(user_x_movie.iloc[:, i], axis=0)
    working_df.replace(0, np.NaN, inplace=True)
    user_profile.loc[userIDs[i]] = working_df.mean(axis=0)

# apply TFIDF for similarity comparison
df = movie_profile.sum()
idf = (len(movies) / df).apply(np.log)  # log inverse of DF
TFIDF = movie_profile.mul(idf.values)
df_predict = pd.DataFrame()

for i in tqdm(range(len(user_x_movie.columns))):
    working_df = TFIDF.mul(user_profile.iloc[i], axis=1)
    df_predict[user_x_movie.columns[i]] = working_df.sum(axis=1)

df_predict.to_csv('TFIDF.csv')