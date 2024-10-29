import streamlit as st
import pandas as pd

# Load your processed DataFrame (assuming it's named df)
# Make sure to adjust the path as per your file location
df = pd.read_csv('spotify_large_dataset.csv')

# Function to get recommendations based on track ID and filters
def get_recommendations(track_id, genre=None, danceability=None, energy=None, tempo=None):
    recommendations = df.copy()

    # Filter by genre
    if genre:
        recommendations = recommendations[recommendations['genre'] == genre]

    # Filter by danceability, energy, and tempo
    if danceability:
        recommendations = recommendations[(recommendations['danceability'] >= danceability[0]) & 
                                          (recommendations['danceability'] <= danceability[1])]
    if energy:
        recommendations = recommendations[(recommendations['energy'] >= energy[0]) & 
                                          (recommendations['energy'] <= energy[1])]
    if tempo:
        recommendations = recommendations[(recommendations['tempo'] >= tempo[0]) & 
                                          (recommendations['tempo'] <= tempo[1])]

    # Sort by popularity
    recommendations = recommendations.sort_values(by='popularity', ascending=False)

    # Display top 5 recommendations
    return recommendations[['track_id', 'track_name', 'artist_name', 'popularity']].head(5)

# Streamlit app layout
st.title("Music Recommendation System")

# Track selection
track_id_input = st.text_input("Enter a track ID or name")

# Genre filter
genre_filter = st.selectbox("Select Genre", options=df['genre'].unique())

# Audio feature filters
danceability_range = st.slider("Danceability", 0.0, 1.0, (0.2, 0.8))
energy_range = st.slider("Energy", 0.0, 1.0, (0.3, 0.9))
tempo_range = st.slider("Tempo", 50.0, 200.0, (80.0, 120.0))

# Show recommendations
if st.button("Get Recommendations"):
    if track_id_input:
        recommendations = get_recommendations(track_id_input, genre=genre_filter,
                                              danceability=danceability_range,
                                              energy=energy_range,
                                              tempo=tempo_range)
        st.write("Top Recommendations:")
        st.dataframe(recommendations)
    else:
        st.warning("Please enter a track ID or name.")
