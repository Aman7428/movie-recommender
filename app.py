import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8122dd55e78f655eb140f2997ed5425d&language=en-US')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies based on the selected movie
def recommend(movie):
    if movie not in movies['title'].values:
        st.error(f"'{movie}' not found in the database. Please try another movie.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load the movie dictionary and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.markdown("<h1 style='text-align: center; color: red;'>Movie Recommender System</h1>", unsafe_allow_html=True)

# Add CSS styling for Netflix-like appearance
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    div[data-testid="stSidebar"] {
        background-color: #1c1c1c;
    }
    img {
        transition: transform 0.3s ease;
    }
    img:hover {
        transform: scale(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Text input for movie search
selected_movie_name = st.text_input("Search for a movie:", "")

# Filter movie suggestions based on user input
if selected_movie_name:
    filtered_movies = movies[movies['title'].str.lower().str.startswith(selected_movie_name.lower(), na=False)]
else:
    filtered_movies = pd.DataFrame(columns=['title'])  # Empty DataFrame if no input

# Dropdown for suggestions
movie_suggestion = st.selectbox("Select a movie:", options=filtered_movies['title'].tolist())

# Button to get recommendations
if st.button('Recommend'):
    if not movie_suggestion:
        st.warning("Please select a movie.")
    else:
        # Display loading spinner while fetching recommendations
        with st.spinner('Fetching recommendations...'):
            names, posters = recommend(movie_suggestion)
            if names and posters:
                st.markdown("<h3 style='text-align: center;'>Recommended Movies</h3>", unsafe_allow_html=True)

                # Streamlit columns for displaying recommendations
                cols = st.columns(len(names))
                for i, col in enumerate(cols):
                    with col:
                        st.image(posters[i], caption=names[i], use_container_width=True)














