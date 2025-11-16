# Configuración del Sistema de Generación de Canciones

# API Keys (deben ser configuradas por el usuario)
GEMINI_API_KEY = None  # Tu API key de Google Gemini
GENIUS_API_KEY = None  # Tu API key de Genius

# Configuración de scraping
MAX_SONGS_PER_ARTIST = 50  # Máximo de canciones a analizar por artista
MIN_LYRICS_LENGTH = 100    # Longitud mínima de letras para analizar

# Configuración de análisis
SENTIMENT_THRESHOLD = 0.1  # Umbral para análisis de sentimiento
RHHEME_ANALYSIS_DEPTH = 3  # Profundidad de análisis de rimas

# Configuración de generación
GENERATION_TEMPERATURE = 0.8
MAX_TOKENS = 2000

# Paths
DATA_DIR = "../data"
LYRICS_CACHE_DIR = f"{DATA_DIR}/lyrics_cache"
STYLE_PROFILES_DIR = f"{DATA_DIR}/style_profiles"

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"