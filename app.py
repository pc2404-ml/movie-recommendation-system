import streamlit as st
import pickle
import pandas as pd
import requests



def fetch_poster(movie_id):
    api_key=your_tmdb_api_key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    response = requests.get(url)
    print(response.text)
    data=response.json()
    poster_path = data.get("poster_path")
    base_url = "https://image.tmdb.org/t/p/w500"  # you can also use w200, w780, original, etc.
    full_poster_url = base_url + poster_path if poster_path else "No poster found"
    return full_poster_url


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies =[]
    recommended_movies_posters= []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


st.title('Movie Recommendor')
movies_dict=pickle.load(open('movies_dict.pkl','rb'))

movies=pd.DataFrame(movies_dict)

selected_movie_name=st.selectbox('Select Movie Name',movies['title'].values)


similarity=pickle.load(open('similarity.pkl','rb'))

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])


