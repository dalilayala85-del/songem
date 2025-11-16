#!/usr/bin/env python3
"""
SongGem - Sistema de Generación de Canciones con Gemini API
Crea canciones originales al estilo de cualquier artista
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent))

from scrapers.lyrics_scraper import LyricsScraper
from analyzers.style_analyzer import StyleAnalyzer
from generators.lyrics_generator import LyricsGenerator
from config.settings import *

class SongGemSystem:
    """Sistema principal de SongGem"""
    
    def __init__(self, gemini_api_key: str, genius_api_key: str):
        """
        Inicializa el sistema
        
        Args:
            gemini_api_key: API key de Google Gemini
            genius_api_key: API key de Genius
        """
        self.scraper = LyricsScraper(genius_api_key, LYRICS_CACHE_DIR)
        self.analyzer = StyleAnalyzer()
        self.generator = LyricsGenerator(gemini_api_key)
        
        # Crear directorios necesarios
        Path(LYRICS_CACHE_DIR).mkdir(parents=True, exist_ok=True)
        Path(STYLE_PROFILES_DIR).mkdir(parents=True, exist_ok=True)
    
    def analyze_artist(self, artist_name: str, max_songs: int = None) -> Dict:
        """
        Analiza el estilo de un artista
        
        Args:
            artist_name: Nombre del artista
            max_songs: Número máximo de canciones a analizar
            
        Returns:
            Perfil de estilo del artista
        """
        max_songs = max_songs or MAX_SONGS_PER_ARTIST
        
        print(f"🎵 Analizando estilo de {artist_name}...")
        
        # Extraer canciones
        songs = self.scraper.get_artist_songs(artist_name, max_songs)
        
        if not songs:
            print(f"❌ No se encontraron canciones para {artist_name}")
            return {}
        
        print(f"✅ Se encontraron {len(songs)} canciones")
        
        # Analizar estilo
        style_profile = self.analyzer.generate_style_profile(artist_name, songs)
        
        # Guardar perfil
        profile_path = Path(STYLE_PROFILES_DIR) / f"{artist_name.lower().replace(' ', '_')}_style.json"
        self.analyzer.save_style_profile(style_profile, str(profile_path))
        
        print(f"✅ Perfil de estilo guardado en {profile_path}")
        
        return style_profile
    
    def generate_song(self, 
                     artist_name: str,
                     theme: str,
                     emotion: str = None,
                     structure: str = None,
                     recreate_style: bool = False) -> Dict:
        """
        Genera una canción al estilo de un artista
        
        Args:
            artist_name: Artista cuyo estilo se usará
            theme: Tema de la nueva canción
            emotion: Emoción deseada
            structure: Estructura deseada
            recreate_style: Si True, reanaliza al artista
            
        Returns:
            Canción generada
        """
        print(f"🎵 Generando canción al estilo de {artist_name}...")
        
        # Cargar o crear perfil de estilo
        profile_path = Path(STYLE_PROFILES_DIR) / f"{artist_name.lower().replace(' ', '_')}_style.json"
        
        if profile_path.exists() and not recreate_style:
            print("📂 Cargando perfil de estilo existente...")
            style_profile = self.analyzer.load_style_profile(str(profile_path))
        else:
            print("🔍 Analizando nuevo perfil de estilo...")
            style_profile = self.analyze_artist(artist_name)
        
        if not style_profile:
            print(f"❌ No se pudo obtener el perfil de estilo de {artist_name}")
            return {}
        
        # Generar canción
        song_data = self.generator.generate_lyrics(
            style_profile=style_profile,
            new_theme=theme,
            emotion=emotion,
            structure=structure
        )
        
        if song_data.get('success'):
            # Guardar canción
            output_dir = Path("data/generated_songs")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{artist_name.lower().replace(' ', '_')}_{theme.lower().replace(' ', '_')}.json"
            output_path = output_dir / filename
            
            self.generator.save_generated_song(song_data, str(output_path))
            print(f"✅ Canción guardada en {output_path}")
            
            # Mostrar resultado
            print("\n" + "="*60)
            print(self.generator.format_song_for_display(song_data))
            print("="*60)
        else:
            print(f"❌ Error generando canción: {song_data.get('error')}")
        
        return song_data
    
    def rewrite_song_in_style(self,
                             target_artist: str,
                             original_artist: str,
                             original_song_title: str,
                             new_angle: str = None) -> Dict:
        """
        Reescribe una canción al estilo de otro artista
        
        Args:
            target_artist: Artista cuyo estilo se adoptará
            original_artist: Artista de la canción original
            original_song_title: Título de la canción original
            new_angle: Nuevo enfoque para la canción
            
        Returns:
            Canción reescrita
        """
        print(f"🔄 Reescribiendo '{original_song_title}' al estilo de {target_artist}...")
        
        # Obtener canción original
        original_song = self.scraper.search_song(original_artist, original_song_title)
        
        if not original_song:
            print(f"❌ No se encontró la canción '{original_song_title}' de {original_artist}")
            return {}
        
        print(f"✅ Canción original encontrada: '{original_song['title']}'")
        
        # Analizar estilo del artista objetivo
        style_profile = self.analyze_artist(target_artist)
        
        if not style_profile:
            print(f"❌ No se pudo analizar el estilo de {target_artist}")
            return {}
        
        # Reescribir canción
        rewritten_data = self.generator.rewrite_song_in_style(
            style_profile=style_profile,
            original_song=original_song,
            new_angle=new_angle
        )
        
        if rewritten_data.get('success'):
            # Guardar resultado
            output_dir = Path("data/rewritten_songs")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{original_artist.lower().replace(' ', '_')}_{original_song_title.lower().replace(' ', '_')}_as_{target_artist.lower().replace(' ', '_')}.json"
            output_path = output_dir / filename
            
            self.generator.save_generated_song(rewritten_data, str(output_path))
            print(f"✅ Canción reescrita guardada en {output_path}")
            
            # Mostrar resultado
            print("\n" + "="*60)
            print("🎵 CANCIÓN REESCRITA 🎵")
            print(f"Original: '{original_song['title']}' por {original_artist}")
            print(f"Estilo: {target_artist}")
            if new_angle:
                print(f"Nuevo enfoque: {new_angle}")
            print("="*60)
            print(self.generator.format_song_for_display(rewritten_data))
            print("="*60)
        else:
            print(f"❌ Error reescribiendo canción: {rewritten_data.get('error')}")
        
        return rewritten_data
    
    def interactive_mode(self):
        """Modo interactivo del sistema"""
        print("🎵 SongGem - Sistema Interactivo de Generación de Canciones 🎵")
        print("="*60)
        
        while True:
            print("\n¿Qué te gustaría hacer?")
            print("1. Analizar estilo de un artista")
            print("2. Generar una nueva canción")
            print("3. Reescribir una canción existente")
            print("4. Ver artistas analizados")
            print("5. Salir")
            
            choice = input("\nElige una opción (1-5): ").strip()
            
            if choice == '1':
                artist = input("Nombre del artista: ").strip()
                if artist:
                    max_songs = input(f"Número máximo de canciones (default {MAX_SONGS_PER_ARTIST}): ").strip()
                    max_songs = int(max_songs) if max_songs.isdigit() else MAX_SONGS_PER_ARTIST
                    
                    profile = self.analyze_artist(artist, max_songs)
                    if profile:
                        print(f"\n✅ Análisis completado para {artist}")
                        print(f"Resumen: {profile.get('writing_style_summary', '')}")
            
            elif choice == '2':
                artist = input("Artista cuyo estilo usarás: ").strip()
                theme = input("Tema de la nueva canción: ").strip()
                emotion = input("Emoción deseada (opcional): ").strip() or None
                structure = input("Estructura deseada (opcional): ").strip() or None
                
                if artist and theme:
                    self.generate_song(artist, theme, emotion, structure)
            
            elif choice == '3':
                target_artist = input("Estilo del artista a adoptar: ").strip()
                original_artist = input("Artista de la canción original: ").strip()
                original_title = input("Título de la canción original: ").strip()
                new_angle = input("Nuevo enfoque (opcional): ").strip() or None
                
                if all([target_artist, original_artist, original_title]):
                    self.rewrite_song_in_style(target_artist, original_artist, original_title, new_angle)
            
            elif choice == '4':
                self.show_analyzed_artists()
            
            elif choice == '5':
                print("¡Gracias por usar SongGem! 🎵")
                break
            
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
    
    def show_analyzed_artists(self):
        """Muestra los artistas que han sido analizados"""
        profiles_dir = Path(STYLE_PROFILES_DIR)
        
        if not profiles_dir.exists():
            print("No hay artistas analizados aún.")
            return
        
        profiles = list(profiles_dir.glob("*_style.json"))
        
        if not profiles:
            print("No hay artistas analizados aún.")
            return
        
        print("\n🎵 Artistas Analizados:")
        print("-" * 30)
        
        for profile_file in profiles:
            try:
                profile = self.analyzer.load_style_profile(str(profile_file))
                if profile:
                    artist = profile.get('artist_name', 'Unknown')
                    songs = profile.get('total_songs_analyzed', 0)
                    summary = profile.get('writing_style_summary', '')
                    
                    print(f"• {artist}")
                    print(f"  Canciones analizadas: {songs}")
                    print(f"  Estilo: {summary}")
                    print()
            except Exception as e:
                print(f"Error leyendo {profile_file.name}: {e}")


def main():
    """Función principal del sistema"""
    parser = argparse.ArgumentParser(description='SongGem - Generador de Canciones con IA')
    parser.add_argument('--gemini-key', required=True, help='API key de Google Gemini')
    parser.add_argument('--genius-key', required=True, help='API key de Genius')
    parser.add_argument('--interactive', action='store_true', help='Modo interactivo')
    parser.add_argument('--analyze', help='Analizar estilo de un artista')
    parser.add_argument('--generate', help='Generar canción (requiere --artist y --theme)')
    parser.add_argument('--artist', help='Artista para generación')
    parser.add_argument('--theme', help='Tema para nueva canción')
    parser.add_argument('--emotion', help='Emoción deseada')
    parser.add_argument('--structure', help='Estructura deseada')
    parser.add_argument('--rewrite', action='store_true', help='Reescribir canción')
    parser.add_argument('--target-artist', help='Artista objetivo para reescritura')
    parser.add_argument('--original-artist', help='Artista original')
    parser.add_argument('--original-title', help='Título original')
    parser.add_argument('--new-angle', help='Nuevo enfoque para reescritura')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    try:
        system = SongGemSystem(args.genius_key, args.gemini_key)
    except Exception as e:
        print(f"❌ Error inicializando el sistema: {e}")
        return 1
    
    # Ejecutar modo correspondiente
    if args.interactive:
        system.interactive_mode()
    
    elif args.analyze:
        system.analyze_artist(args.analyze)
    
    elif args.generate and args.artist and args.theme:
        system.generate_song(
            args.artist,
            args.theme,
            args.emotion,
            args.structure
        )
    
    elif args.rewrite and all([args.target_artist, args.original_artist, args.original_title]):
        system.rewrite_song_in_style(
            args.target_artist,
            args.original_artist,
            args.original_title,
            args.new_angle
        )
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())