import lyricsgenius
import json
import os
import time
import re
from typing import List, Dict, Optional
from pathlib import Path

class LyricsScraper:
    """Clase para extraer letras de canciones usando Genius API"""
    
    def __init__(self, api_key: str, cache_dir: str = None, redirect_uri: str = None):
        """
        Inicializa el scraper de letras
        
        Args:
            api_key: API key de Genius (Access Token)
            cache_dir: Directorio para caché de letras
            redirect_uri: URI de redirección para OAuth (si es necesario)
        """
        self.genius = lyricsgenius.Genius(api_key)
        self.genius.remove_section_headers = True  # Eliminar headers como [Verse], [Chorus]
        self.genius.skip_non_songs = True          # Saltar resultados que no son canciones
        self.genius.excluded_terms = ["(Remix)", "(Live)", "(Acoustic)", "(Demo)"]
        
        self.cache_dir = Path(cache_dir) if cache_dir else Path("data/lyrics_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_lyrics(self, lyrics: str) -> str:
        """Limpia las letras de caracteres no deseados y formato"""
        if not lyrics:
            return ""
        
        # Eliminar corchetes y su contenido
        lyrics = re.sub(r'\[.*?\]', '', lyrics)
        # Eliminar paréntesis con información técnica
        lyrics = re.sub(r'\(.*?mix.*?\)', '', lyrics, flags=re.IGNORECASE)
        lyrics = re.sub(r'\(.*?master.*?\)', '', lyrics, flags=re.IGNORECASE)
        # Eliminar múltiples espacios y líneas vacías
        lyrics = re.sub(r'\n+', '\n', lyrics)
        lyrics = re.sub(r' +', ' ', lyrics)
        lyrics = lyrics.strip()
        
        return lyrics
    
    def get_cached_songs(self, artist_name: str) -> Optional[List[Dict]]:
        """Obtiene canciones cacheadas para un artista"""
        cache_file = self.cache_dir / f"{artist_name.lower().replace(' ', '_')}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def cache_songs(self, artist_name: str, songs: List[Dict]):
        """Guarda canciones en caché"""
        cache_file = self.cache_dir / f"{artist_name.lower().replace(' ', '_')}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)
    
    def get_artist_songs(self, artist_name: str, max_songs: int = 50) -> List[Dict]:
        """
        Obtiene todas las canciones de un artista
        
        Args:
            artist_name: Nombre del artista
            max_songs: Máximo número de canciones a obtener
            
        Returns:
            Lista de diccionarios con información de las canciones
        """
        # Verificar caché primero
        cached = self.get_cached_songs(artist_name)
        if cached:
            print(f"Usando {len(cached)} canciones cacheadas para {artist_name}")
            return cached
        
        try:
            print(f"Buscando canciones de {artist_name}...")
            artist = self.genius.search_artist(artist_name, max_songs=max_songs)
            
            if not artist:
                raise ValueError(f"No se encontró al artista: {artist_name}")
            
            songs = []
            for song in artist.songs:
                cleaned_lyrics = self.clean_lyrics(song.lyrics)
                
                if len(cleaned_lyrics) > 100:  # Solo incluir canciones con contenido suficiente
                    song_data = {
                        'title': song.title,
                        'artist': song.artist,
                        'lyrics': cleaned_lyrics,
                        'url': song.url,
                        'release_date': getattr(song, 'release_date_for_display', None),
                        'featured_artists': getattr(song, 'featured_artists', []),
                        'producer_artists': getattr(song, 'producer_artists', []),
                        'writer_artists': getattr(song, 'writer_artists', []),
                        'word_count': len(cleaned_lyrics.split()),
                        'line_count': len(cleaned_lyrics.split('\n'))
                    }
                    songs.append(song_data)
                
                # Pequeña pausa para evitar rate limiting
                time.sleep(0.1)
            
            # Guardar en caché
            self.cache_songs(artist_name, songs)
            print(f"Se extrajeron y cachearon {len(songs)} canciones de {artist_name}")
            
            return songs
            
        except Exception as e:
            print(f"Error extrayendo canciones de {artist_name}: {str(e)}")
            return []
    
    def search_song(self, artist_name: str, song_title: str) -> Optional[Dict]:
        """
        Busca una canción específica
        
        Args:
            artist_name: Nombre del artista
            song_title: Título de la canción
            
        Returns:
            Diccionario con información de la canción o None si no se encuentra
        """
        try:
            song = self.genius.search_song(song_title, artist_name)
            if song:
                cleaned_lyrics = self.clean_lyrics(song.lyrics)
                return {
                    'title': song.title,
                    'artist': song.artist,
                    'lyrics': cleaned_lyrics,
                    'url': song.url,
                    'word_count': len(cleaned_lyrics.split()),
                    'line_count': len(cleaned_lyrics.split('\n'))
                }
        except Exception as e:
            print(f"Error buscando la canción {song_title}: {str(e)}")
        
        return None
    
    def get_lyrics_stats(self, songs: List[Dict]) -> Dict:
        """
        Obtiene estadísticas básicas de las letras
        
        Args:
            songs: Lista de canciones
            
        Returns:
            Diccionario con estadísticas
        """
        if not songs:
            return {}
        
        total_words = sum(song['word_count'] for song in songs)
        total_lines = sum(song['line_count'] for song in songs)
        
        return {
            'total_songs': len(songs),
            'total_words': total_words,
            'total_lines': total_lines,
            'avg_words_per_song': total_words / len(songs),
            'avg_lines_per_song': total_lines / len(songs),
            'longest_song': max(songs, key=lambda x: x['word_count'])['title'],
            'shortest_song': min(songs, key=lambda x: x['word_count'])['title']
        }