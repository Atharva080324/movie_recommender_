import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: rgba(0, 0, 0, 0.7);
            background-blend-mode: overlay;
        }}
        .main {{
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 2rem;
            border-radius: 10px;
        }}
        .stSelectbox > div > div > input {{
            color: white !important;
            background-color: rgba(0, 0, 0, 0.7) !important;
        }}
        .stSelectbox > div > div > svg {{
            color: white !important;
        }}
        .stButton>button {{
            background-color: #E50914;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-weight: bold;
        }}
        .stButton>button:hover {{
            background-color: #F40612;
            color: white;
        }}
        .title {{
            color: #E50914;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        .recommendation-header {{
            margin-top: 2rem;
            margin-bottom: 1.5rem;
            text-align: center;
            font-size: 1.5rem;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        .movie-title {{
            margin-top: 0.8rem;
            font-weight: bold;
            text-align: center;
            font-size: 1.1rem;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        .movie-poster {{
            width: 100%;
            min-width: 180px;
            border-radius: 8px;
            transition: transform 0.3s;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}
        .movie-poster:hover {{
            transform: scale(1.05);
        }}
        .hero-text {{
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 2rem;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_from_local('image.png')


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e72c97240189426290c5c96153ab34b&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w780" + data['poster_path']


def recommend(movie):
    m_index = movies[movies['title'] == movie].index[0]
    dist = similarity[m_index]
    m_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movie_poster = []
    for i in m_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movie_poster


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('simi.pkl', 'rb'))

# Main content container
with st.container():
    st.markdown('<h1 class="title">Movie Recommender</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-text">
            See what's next.<br>
        </div>
        """, unsafe_allow_html=True)

    # Movie selection
    movie_name = st.selectbox(
        'Select a movie you like',
        movies['title'].values,
        key='movie_select'
    )

    # Recommendation button
    if st.button('Get Recommendations', key='recommend_btn'):
        with st.spinner('Finding your perfect matches...'):
            names, posters = recommend(movie_name)

            st.markdown(f"""
                <div class="recommendation-header">
                    Because you liked <span style="color: #E50914;">{movie_name}</span>
                </div>
                """, unsafe_allow_html=True)

            # Display recommendations in a row
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    st.markdown(
                        f'<img src="{posters[i]}" class="movie-poster">',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="movie-title">{names[i]}</p>',
                        unsafe_allow_html=True
                    )
