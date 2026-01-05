from app.models.schemas import MusicResponse

from youtubesearchpython import VideosSearch
import random

def get_music_recommendation(temperature: float, weather_code: int) -> MusicResponse:
    """
    Recommend a Bollywood song based on weather conditions using real YouTube search.
    """
    try:
        query = ""
        mood = ""
        
        # Rain codes: 51, 53, 55, 61, 63, 65, 80, 81, 82
        rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
        
        if weather_code in rain_codes:
            query = "Bollywood monsoon songs romantic"
            mood = "Monsoon Magic"
        elif temperature < 10:
            query = "Bollywood romantic acoustic songs cozy"
            mood = "Cozy & Romantic"
        elif 10 <= temperature < 20:
            query = "Bollywood soulful pleasant songs"
            mood = "Pleasant Chill"
        elif 20 <= temperature < 30:
            query = "Bollywood happy travel songs"
            mood = "Sunny Vibes"
        else: # Hot >= 30
            query = "Bollywood high energy party songs"
            mood = "High Energy"

        # Search for 10 videos to provide variety
        videos_search = VideosSearch(query, limit=10)
        results = videos_search.result()

        if results and 'result' in results and len(results['result']) > 0:
            # Pick a random video from the top results
            video = random.choice(results['result'])
            return MusicResponse(
                video_id=video['id'],
                title=video['title'],
                artist=video.get('channel', {}).get('name', 'Unknown Artist'),
                mood=mood
            )
        else:
            # Fallback if search fails/returns empty
            raise Exception("No results found")

    except Exception as e:
        print(f"Music search failed: {e}")
        # Default Fallback (Ilahi)
        return MusicResponse(
            video_id="0WtRNGubWGA",
            title="Ilahi",
            artist="Arijit Singh",
            mood="Fallback Vibes"
        )
