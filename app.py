import streamlit as st
import requests

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ================= BACKGROUND ================= */
/* Fully self-contained (no external image fetch to fail): layered
   animated radial glows + soft grid + film-grain noise, on a deep navy base. */
.stApp {
    background-color: #07080f;
    background-image:
        radial-gradient(ellipse 900px 600px at 12% 8%, rgba(255,120,60,0.20), transparent 60%),
        radial-gradient(ellipse 800px 700px at 88% 18%, rgba(168,85,247,0.18), transparent 60%),
        radial-gradient(ellipse 900px 800px at 50% 100%, rgba(255,60,111,0.14), transparent 65%),
        repeating-linear-gradient(0deg, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 1px, transparent 1px, transparent 42px),
        repeating-linear-gradient(90deg, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 1px, transparent 1px, transparent 42px);
    background-attachment: fixed;
    color: #f5f5f7;
    animation: bgshift 18s ease-in-out infinite alternate;
}
@keyframes bgshift {
    0%   { background-position: 0% 0%, 100% 0%, 50% 100%, 0 0, 0 0; }
    100% { background-position: 5% 10%, 90% 5%, 55% 95%, 0 0, 0 0; }
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] { background: transparent !important; }

/* ================= HERO ================= */
.hero-wrap { text-align: center; padding: 2rem 1rem 0.6rem 1rem; }
.hero-badge {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #ffb84c;
    background: rgba(255,184,76,0.12);
    border: 1px solid rgba(255,184,76,0.3);
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 3.4rem;
    line-height: 1.05;
    background: linear-gradient(90deg, #ffb84c, #ff3c6f 50%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    letter-spacing: -1.5px;
}
.hero-subtitle {
    color: #9a9bb0;
    font-size: 1.08rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}

/* ================= GLASS CONTAINER (native st.container(border=True)) ================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.045) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

.section-label {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1.2rem;
    color: #fff;
    margin: 0 0 0.4rem 0;
    line-height: 1.3;
}
.section-sub { color: #83849a; font-size: 0.88rem; margin: 0 0 1.4rem 0; }

label, .stSelectbox label, .stSlider label {
    color: #d8d9e6 !important;
    font-weight: 600 !important;
    font-size: 0.74rem !important;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    white-space: normal !important;
    overflow-wrap: break-word;
    word-break: break-word;
    line-height: 1.35 !important;
    display: block;
    margin-bottom: 0.25rem;
}

/* give the filter row a bit more breathing room so labels never crowd the edge */
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {
    gap: 1.4rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 1.5rem 1.5rem !important;
}
.st-key-filter_panel div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"].st-key-filter_panel {
    padding: 1.9rem 2.1rem !important;
}
[class*="st-key-movie_card_"] div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"][class*="st-key-movie_card_"] {
    padding: 1.1rem 1.1rem 1.4rem 1.1rem !important;
    height: 100%;
}

div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #fff !important;
}

.stSlider [data-baseweb="slider"] > div > div { background: linear-gradient(90deg, #ffb84c, #ff3c6f) !important; }
.stSlider [role="slider"] { background: #fff !important; box-shadow: 0 0 0 4px rgba(255,60,111,0.25) !important; }

/* ================= CTA BUTTON ================= */
div[data-testid="stButton"] { width: 100%; }
div[data-testid="stButton"] > button,
.stButton > button {
    width: 100% !important;
    background: linear-gradient(90deg, #ffb84c, #ff3c6f 55%, #a855f7);
    color: white !important;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    border: none;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-top: 0.8rem;
    box-shadow: 0 8px 24px rgba(255, 60, 111, 0.35);
    transition: all 0.25s ease;
    letter-spacing: 0.3px;
}
div[data-testid="stButton"] > button:hover,
.stButton > button:hover { transform: translateY(-2px) scale(1.01); box-shadow: 0 12px 32px rgba(255, 60, 111, 0.5); color: white !important; }
div[data-testid="stButton"] > button:active,
.stButton > button:active { transform: translateY(0px) scale(0.99); }

/* ================= MOVIE CARDS ================= */
.movie-poster-img img {
    border-radius: 14px !important;
    box-shadow: 0 10px 26px rgba(0,0,0,0.5);
    transition: transform 0.25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover .movie-poster-img img { transform: scale(1.02); }

.no-poster-box {
    background: rgba(255,255,255,0.06);
    border: 1px dashed rgba(255,255,255,0.2);
    border-radius: 14px;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.4rem;
}
.movie-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #fff;
    margin: 0.7rem 0 0.15rem 0;
    line-height: 1.3;
    min-height: 2.7em;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.movie-year { color: #83849a; font-size: 0.85rem; font-weight: 500; }
.rating-badge {
    display: inline-block;
    background: linear-gradient(90deg, #ffb84c, #ff7a3c);
    color: #1a1a1a;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 0.22rem 0.65rem;
    border-radius: 999px;
    margin: 0.5rem 0;
}
.movie-overview {
    color: #a9aabc;
    font-size: 0.85rem;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

div[data-testid="stAlert"] { border-radius: 14px !important; backdrop-filter: blur(10px); }
hr { border-color: rgba(255,255,255,0.08) !important; }

.footer-credit {
    text-align: center;
    color: #55566a;
    font-size: 0.8rem;
    padding: 2.5rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <span class="hero-badge">Powered by TMDB</span>
    <div class="hero-title">🍿 CineMatch</div>
    <div class="hero-subtitle">Tell us what you're in the mood for, and we'll find the perfect movie night pick.</div>
</div>
""", unsafe_allow_html=True)

# --- Securely Fetch the API Key ---
if "tmdb_api_key" in st.secrets:
    api_key = st.secrets["tmdb_api_key"]
else:
    st.error("🔑 API Key missing! Please configure it in the Streamlit Secrets settings.")
    st.stop()

# --- TMDB Genre Mapping ---
GENRE_MAP = {
    "Action": 28, "Comedy": 35, "Drama": 18, "Sci-Fi": 878,
    "Horror": 27, "Romance": 10749, "Thriller": 53, "Animation": 16,
    "Fantasy": 14, "Mystery": 9648
}

# --- TMDB Region Mapping ---
REGION_MAP = {
    "🌍 Global (Entire World)": None,
    "🇮🇳 India": "IN",
    "🇺🇸 United States": "US",
    "🇰🇷 South Korea": "KR",
    "🇯🇵 Japan": "JP"
}

GENRE_EMOJI = {
    "Action": "💥", "Comedy": "😂", "Drama": "🎭", "Sci-Fi": "🚀",
    "Horror": "👻", "Romance": "❤️", "Thriller": "🔪", "Animation": "🎨",
    "Fantasy": "🧙", "Mystery": "🕵️"
}

# ============================================================
# USER INPUT PANEL — real st.container so CSS actually wraps it
# ============================================================
st.write("")
with st.container(border=True, key="filter_panel"):
    st.markdown('<div class="section-label">🎯 Select Your Preferences</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Fine-tune the filters below to match your mood.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_genre = st.selectbox("Genre", list(GENRE_MAP.keys()))
    with col2:
        selected_region = st.selectbox("Region", list(REGION_MAP.keys()))
    with col3:
        min_year = st.slider("Min. Release Year", 1970, 2026, 2010)
    with col4:
        min_rating = st.slider("Min. Rating (0–10)", 1.0, 10.0, 7.0)

    find_clicked = st.button(f"{GENRE_EMOJI.get(selected_genre, '🎬')} Recommend Movies")

st.write("")

# ============================================================
# RECOMMENDATION LOGIC
# ============================================================
if find_clicked:
    if not api_key:
        st.warning("⚠️ Please enter your TMDB API Key in the sidebar first.")
    else:
        try:
            discover_url = "https://api.themoviedb.org/3/discover/movie"

            params = {
                "api_key": api_key,
                "with_genres": GENRE_MAP[selected_genre],
                "primary_release_date.gte": f"{min_year}-01-01",
                "vote_average.gte": min_rating,
                "vote_count.gte": 200,
                "sort_by": "popularity.desc"
            }

            if REGION_MAP[selected_region] is not None:
                params["with_origin_country"] = REGION_MAP[selected_region]

            with st.spinner(f"Finding the perfect {selected_genre} movies for you..."):
                response = requests.get(discover_url, params=params)
                response.raise_for_status()
                data = response.json()

            recommendations = data.get('results', [])[:5]

            if recommendations:
                st.success(f"✨ Here are your top {len(recommendations)} recommendations:")

                cols = st.columns(len(recommendations))
                for idx, (col, movie) in enumerate(zip(cols, recommendations)):
                    title = movie.get('title', 'Unknown Title')
                    overview = movie.get('overview', 'No synopsis available.')
                    release_date = movie.get('release_date', 'Unknown Date')
                    rating = movie.get('vote_average', 'N/A')
                    poster_path = movie.get('poster_path')
                    year_str = release_date[:4] if release_date and release_date != "Unknown Date" else "N/A"

                    with col:
                        with st.container(border=True, key=f"movie_card_{idx}"):
                            st.markdown('<div class="movie-poster-img">', unsafe_allow_html=True)
                            if poster_path:
                                poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
                                st.image(poster_url, use_container_width=True)
                            else:
                                st.markdown('<div class="no-poster-box">🎬</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                            st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)
                            st.markdown(f'<span class="movie-year">{year_str}</span>', unsafe_allow_html=True)
                            st.markdown(f'<div class="rating-badge">⭐ {rating}/10</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="movie-overview">{overview}</div>', unsafe_allow_html=True)

            else:
                st.warning("😕 No movies found matching all those exact features. Try lowering the rating or changing the year!")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while connecting to TMDB: {e}")

st.markdown('<div class="footer-credit">Made with ❤️ by Raman Manish Gulhane · Data from The Movie Database (TMDB)</div>', unsafe_allow_html=True)
