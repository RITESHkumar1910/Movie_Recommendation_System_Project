import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9127d095f6954560b521fb07962366d0&language=en-US"

        response = requests.get(url, timeout=30)

        print("Status Code:", response.status_code)

        data = response.json()
        print(data)

        return "https://image.tmdb.org/t/p/w500" + data['poster_path']

    except Exception as e:
        print("ERROR:", e)
        return "https://via.placeholder.com/500x750?text=No+Poster"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    disctances = sm[movie_index]
    movies_list = sorted(list(enumerate(disctances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

sm = pickle.load(open('sm.pkl','rb'))

movies_dict = pickle.load(open('mve.pkl','rb'))
movies = pd.DataFrame(movies_dict)


st.title("🎬MOVIE_SUGGESTION_SYSTEM")

selected_movie_name = st.selectbox(
    'What movie would you like recommendations for? ⭐',
    movies['title'].values
)

if st.button('🎬Get Recommendations'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4 , col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])


