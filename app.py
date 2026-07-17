import streamlit as st
import requests

# Set the page configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# App Title
st.title("🍿 Feature-Based Movie Recommender")
st.write("Don't know what to watch? Tell us what you like, and we'll recommend some movies!")

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter your TMDB API Key:", type="password")

# --- TMDB Genre Mapping ---
GENRE_MAP = {
    "Action": 28, "Comedy": 35, "Drama": 18, "Sci-Fi": 878, 
    "Horror": 27, "Romance": 10749, "Thriller": 53, "Animation": 16,
    "Fantasy": 14, "Mystery": 9648
}

# --- TMDB Region Mapping ---
# Using None for Global so we don't send a country filter to the API
REGION_MAP = {
    "🌍 Global (Entire World)": None,
    "🇮🇳 India": "IN",
    "🇺🇸 United States": "US",
    "🇰🇷 South Korea": "KR",
    "🇯🇵 Japan": "JP"
}

# --- User Input Features ---
st.subheader("1. Select Your Preferences")

# Using 4 columns to fit the new Region dropdown
col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_genre = st.selectbox("Choose a Genre:", list(GENRE_MAP.keys()))
with col2:
    selected_region = st.selectbox("Choose a Region:", list(REGION_MAP.keys()))
with col3:
    min_year = st.slider("Minimum Release Year:", 1970, 2026, 2010)
with col4:
    min_rating = st.slider("Minimum Rating (out of 10):", 1.0, 10.0, 7.0)

# --- Recommendation Logic ---
st.subheader("2. Get Recommendations")

if st.button("Recommend Movies"):
    if not api_key:
        st.warning("⚠️ Please enter your TMDB API Key in the sidebar first.")
    else:
        try:
            discover_url = "https://api.themoviedb.org/3/discover/movie"
            
            # Setting up our base feature parameters
            params = {
                "api_key": api_key,
                "with_genres": GENRE_MAP[selected_genre],
                "primary_release_date.gte": f"{min_year}-01-01",
                "vote_average.gte": min_rating,
                "vote_count.gte": 200, 
                "sort_by": "popularity.desc" 
            }
            
            # If the user selected a specific country (not Global), add it to the search
            if REGION_MAP[selected_region] is not None:
                params["with_origin_country"] = REGION_MAP[selected_region]
            
            with st.spinner(f"Finding the perfect {selected_genre} movies for you..."):
                response = requests.get(discover_url, params=params)
                response.raise_for_status() 
                data = response.json()

            # Get the top 5 results
            recommendations = data.get('results', [])[:5]

            if recommendations:
                st.success(f"Here are your top {len(recommendations)} recommendations:")
                
                # Loop through each recommended movie and display it
                for movie in recommendations:
                    title = movie.get('title', 'Unknown Title')
                    overview = movie.get('overview', 'No synopsis available.')
                    release_date = movie.get('release_date', 'Unknown Date')
                    rating = movie.get('vote_average', 'N/A')
                    poster_path = movie.get('poster_path')
                    
                    movie_col1, movie_col2 = st.columns([1, 4])
                    
                    with movie_col1:
                        if poster_path:
                            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
                            st.image(poster_url)
                        else:
                            st.info("No poster")
                            
                    with movie_col2:
                        st.markdown(f"### {title} ({release_date[:4]})")
                        st.markdown(f"**⭐ TMDB Rating:** {rating}/10")
                        st.write(overview)
                    
                    st.divider() 
                    
            else:
                st.warning("No movies found matching all those exact features. Try lowering the rating or changing the year!")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while connecting to TMDB: {e}")