import pandas as pd
import streamlit as st
import json
from pyquery import PyQuery as pq
import urllib
import requests
from PIL import Image
from io import BytesIO

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings_small.csv')
links = pd.read_csv('links.csv')
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
        doc = pq('https://www.themoviedb.org/movie/' + str(links.loc[links['movieId']==j[0]]['tmdbId'].values[0]))
        image = doc('.image_content.backdrop img').attr('src')
        poster = requests.get(image)
        posters.append(poster)
      except IndexError:
        print('Movie\'s title is not found in the database')
      except urllib.error.HTTPError as exception:
        print('Movie\'s poster is not found!')
        posters.append(404)

    # film_dict = {'film': films}
    # st.write("""Recommended films for you:""")
    # st.dataframe(pd.DataFrame(film_dict))

  else:
    # st.write("""Recommended films for you:""")
    # st.dataframe(movies['title'].sample(n=10, random_state=1))

    films = [_ for _ in movies['title'].sample(n=10, random_state=1)]
    for film in films:
      try:
        doc = pq('https://www.themoviedb.org/movie/' + str(film))
        image = doc('.image_content.backdrop img').attr('data-src')
        poster = requests.get(image)
        posters.append(poster)
      except urllib.error.HTTPError as exception:
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
      film_link = 'https://www.themoviedb.org/movie/' + str(
        int(links.loc[links['movieId'] == film_ID]['tmdbId'].values[0]))
    except:
      film_link = 'https://www.themoviedb.org/movie/'
    st.image(img, use_column_width=True)
    st.write("""#### **[{}]({})**""".format(film_name, film_link))
