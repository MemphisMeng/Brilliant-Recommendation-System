import pandas as pd
import streamlit as st
import json

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings_small.csv')
with open('topN.json') as json_file:
  top_n = json.load(json_file)

# streamlit app design
st.header('Welcome to MovieLens Recommendation System!')
st.sidebar.header('Please enter your User ID:')
id_ = st.sidebar.number_input('Your ID')
films = []

if int(id_) in ratings.userId.unique():
  for j in top_n[str(int(id_))]:
    try:
      films.append(movies.loc[movies['id']==j[0]]['title'].values[0])
    except:
      print('Movie\'s title is not found in the database')

  film_dict = {'film': films}
  st.write("""Recommended films for you:""")
  st.dataframe(pd.DataFrame(film_dict))

else:
  st.write("""Recommended films for you:""")
  st.dataframe(movies['title'].sample(n=10, random_state=1))