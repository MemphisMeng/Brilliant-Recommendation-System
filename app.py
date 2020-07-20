import pandas as pd
import streamlit as st
import json
from pyquery import PyQuery as pq
import urllib
import requests
from PIL import Image
from requests.exceptions import MissingSchema
from io import BytesIO

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings_small.csv')
with open('topN.json') as json_file:
  top_n = json.load(json_file)

# streamlit app design
st.header('Welcome to MovieLens Recommendation System!')
st.sidebar.header('Please enter your User ID:')
id_ = st.sidebar.number_input('Your ID')
button = st.sidebar.button('Confirm')

films, posters = [], []
if button:
  if int(id_) in ratings.userId.unique():
    for j in top_n[str(int(id_))]:
      try:
        films.append(movies.loc[movies['id']==j[0]]['title'].values[0])
        doc = pq('https://www.themoviedb.org/movie/' + str(j[0]))
        image = doc('.image_content.backdrop img').attr('data-src')
        poster = requests.get(image)
        posters.append(poster)
      except IndexError:
        print('Movie\'s title is not found in the database')
      except urllib.error.HTTPError as exception:
        print('Movie\'s poster is not found!')
        posters.append(404)

  else:

    films = [_ for _ in movies['id'].sample(n=10, random_state=1)]
    for film in films:
      try:
        doc = pq('https://www.themoviedb.org/movie/' + str(film))
        image = doc('.image_content.backdrop img').attr('data-src')
        poster = requests.get(image)
        posters.append(poster)
      except urllib.error.HTTPError as exception:
        print('Movie\'s poster is not found!')
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

    film_ID = films[i]
    film_name = movies.loc[movies['id'] == film_ID]['title'].values[0]
    try:
      film_link = 'https://www.themoviedb.org/movie/' + str(film_ID)
    except:
      film_link = 'https://www.themoviedb.org/movie/'

    st.write("""#### **[{}]({})**""".format(film_name, film_link))
    st.image(img, use_column_width=True)
    st.write()