import pandas as pd
import streamlit as st
import numpy as np
from pyquery import PyQuery as pq
import urllib
import requests
from PIL import Image
from requests.exceptions import MissingSchema
from default_promotion import promote
from io import BytesIO
from pymongo import MongoClient
import os

list_of_genres = ['animation', 'western', 'fantasy', 'thriller', 'drama', 'history', 'crime', 'comedy',
                          'tv movie', 'documentary', 'mystery', 'adventure', 'family', 'romance', 'action', 'horror',
                          'war', 'music', 'science fiction', 'foreign']

# connect to the MongoDb cluster for predicted ranks
MONGODB_URI = os.environ['MONGODB_URI']
client = MongoClient(MONGODB_URI)
db = client['MovieLens']
TFIDF_collection = db['TFIDF']
idf_collection = db['idf']
user_profile_collection = db['user_profile']
movie_profile_collection = db['movie_profile']

# read from local
movies = pd.read_csv('data/movies.csv')
movies.drop_duplicates(inplace=True)
ratings = pd.read_csv('data/ratings_small.csv')

# read from mongo DB
user_profile = pd.DataFrame(list(user_profile_collection.find()))
TFIDF = pd.DataFrame(list(idf_collection.find()))
movie_profile = pd.DataFrame(list(movie_profile_collection.find()))
df_predict = pd.DataFrame(list(TFIDF_collection.find()))


def recommender(user_no):
    # user predicted rating to all films
    user_predicted_rating = df_predict[['movieId', df_predict.columns[user_no]]]
    # combine film rating and film detail
    user_rating_film = pd.merge(user_predicted_rating, movies, left_on='movieId', right_on='id')
    # films already watched by user
    already_watched = ratings[ratings['userId'].isin([user_no])]['movieId']
    # recommendation without films being watched by user
    all_rec = user_rating_film[~user_rating_film.index.isin(already_watched)]
    return all_rec.sort_values(by=str(user_no), ascending=False, axis=0).iloc[0:10][['movieId', 'title']]


def display():
    st.write("""Recommended films for you:""")
    for i in range(len(films)):
        if posters[i] != 404:
            img = Image.open(BytesIO(posters[i].content))
        else:
            img = Image.open('404NF.png')

        film_name = films[i]
        film_ID = movies.loc[movies['title'] == film_name]['id'].values[0]
        try:
            film_link = 'https://www.themoviedb.org/movie/' + str(film_ID)
        except:
            film_link = 'https://www.themoviedb.org/movie/'

        st.write("""#### **[{}]({})**""".format(film_name, film_link))
        try:
            st.image(img, use_column_width=True)
        except:
            st.image(img.convert('RGB'))
        st.write()


# streamlit app design
st.header('Welcome to MovieLens Recommendation System!')
st.sidebar.header('Please enter your User ID:')
id_ = st.sidebar.number_input('Your ID')
st.sidebar.subheader('New User Only!')
default = st.sidebar.radio("Do you want our default recommendation?", ('Yes', 'No'))
options = st.sidebar.multiselect('Your Choice of Genres', list_of_genres)
button = st.sidebar.button('Confirm')

films, posters = [], []
if button:
    if int(id_) in ratings.userId.unique():
        recommended_movies = recommender(int(id_))
        for j in range(10):
            try:
                films.append(recommended_movies['title'].iloc[j])
                doc = pq('https://www.themoviedb.org/movie/' + str(recommended_movies['movieId'].iloc[j]))
                image = doc('.image_content.backdrop img').attr('data-src')
                poster = requests.get(image)
                posters.append(poster)
            except IndexError:
                print('Movie\'s title is not found in the database')
            except urllib.error.HTTPError as exception:
                print('Movie\'s URL is broken!')
                posters.append(404)
            except MissingSchema as exception:
                print('Movie\'s poster is not found!')
                posters.append(404)

        display()

    # newcomer
    else:
        # customized choice
        if default == 'No':
            rates = dict()
            for option in list_of_genres:
                if option in options:
                    rates[option] = [user_profile.mean(axis=0)[option]]
                else:
                    rates[option] = [0]

            preference = pd.DataFrame(rates, index=[int(id_)]).T.sort_index(axis=0)
            test_list = np.dot(TFIDF, preference)
            movie_ranks = pd.DataFrame(data=test_list, index=movie_profile['movieId'].unique(), columns=[int(id_)])
            recommended_movies = pd.merge(movie_ranks, movies, left_on=movie_ranks.index, right_on='id') \
                                     .sort_values(by=int(id_), ascending=False, axis=0).iloc[0:10][['id', 'title']]

        # default recommendation
        elif default == 'Yes':
            recommended_movies = promote()

        for i in range(10):
            try:
                films.append(recommended_movies['title'].iloc[i])
                doc = pq('https://www.themoviedb.org/movie/' + str(recommended_movies['id'].iloc[i]))
                image = doc('.image_content.backdrop img').attr('data-src')
                poster = requests.get(image)
                posters.append(poster)
            except urllib.error.HTTPError as exception:
                print('Movie\'s link is broken!')
                posters.append(404)
            except MissingSchema as exception:
                print('Movie\'s poster is not found!')
                posters.append(404)

        display()