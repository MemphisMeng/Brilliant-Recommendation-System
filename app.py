import pandas as pd
import streamlit as st
from pyquery import PyQuery as pq
import urllib
import requests
from PIL import Image
from requests.exceptions import MissingSchema
from io import BytesIO

movies = pd.read_csv('truncated_movies.csv', index_col=0)
movies.drop_duplicates(inplace=True)
df_predict = pd.read_csv('TFIDF.csv').set_index('movieId')
ratings = pd.read_csv('ratings_small.csv')


def recommender(user_no):
    # user predicted rating to all films
    user_predicted_rating = df_predict[df_predict.columns[user_no - 1]]

    # combine film rating and film detail
    user_rating_film = pd.merge(user_predicted_rating, movies, left_on='movieId', right_on='id')

    # films already watched by user
    already_watched = ratings[ratings['userId'].isin([user_no])]['movieId']

    # recommendation without films being watched by user
    all_rec = user_rating_film[~user_rating_film.index.isin(already_watched)]

    return all_rec.sort_values(by=str(user_no), ascending=False, axis=0).iloc[0:10][['id', 'title']]


# streamlit app design
st.header('Welcome to MovieLens Recommendation System!')
st.sidebar.header('Please enter your User ID:')
id_ = st.sidebar.number_input('Your ID')
button = st.sidebar.button('Confirm')

films, posters = [], []
if button:
    if int(id_) in ratings.userId.unique():
        recommended_movies = recommender(int(id_))
        for j in range(10):
            try:
                films.append(recommended_movies['title'].iloc[j])
                doc = pq('https://www.themoviedb.org/movie/' + str(recommended_movies['id'].iloc[j]))
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

    else:
        films = [_ for _ in movies['title'].sample(n=10, random_state=1)]
        for film in films:
            try:
                doc = pq('https://www.themoviedb.org/movie/' + str(movies.loc[movies['title'] == film]['id'].values[0]))
                image = doc('.image_content.backdrop img').attr('data-src')
                poster = requests.get(image)
                posters.append(poster)
            except urllib.error.HTTPError as exception:
                print('Movie\'s link is broken!')
                posters.append(404)
            except MissingSchema as exception:
                print('Movie\'s poster is not found!')
                posters.append(404)

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
