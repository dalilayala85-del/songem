#!/usr/bin/env python3
"""
Demo de SongGem - Ejemplo completo de uso del sistema
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

def demo_basic_usage():
    """Demostración básica del funcionamiento"""
    print("🎵 SongGem - Demostración Completa 🎵")
    print("=" * 60)
    
    # Verificar que tenemos las API keys configuradas
    gemini_key = os.getenv("GEMINI_API_KEY")
    genius_key = os.getenv("GENIUS_API_KEY")
    
    if not gemini_key or not genius_key:
        print("❌ Configura las variables de entorno:")
        print("export GEMINI_API_KEY='tu_gemini_api_key'")
        print("export GENIUS_API_KEY='tu_genius_api_key'")
        return
    
    try:
        from main import SongGemSystem
        
        # Inicializar sistema
        print("🚀 Inicializando SongGem...")
        system = SongGemSystem(gemini_key, genius_key)
        
        # Demo 1: Análisis de artista
        print("\n📊 Demo 1: Análisis de Estilo de Artista")
        print("-" * 40)
        
        artist = "Adele"
        print(f"Analizando estilo de {artist}...")
        
        # Aquí normalmente analizaríamos, pero para el demo usaremos datos simulados
        # profile = system.analyze_artist(artist, max_songs=10)
        
        # Simulación de perfil para demo
        mock_profile = {
            'artist_name': artist,
            'total_songs_analyzed': 10,
            'writing_style_summary': f"{artist} presenta un estilo con vocabulario rico y diverso, tendencia melancólica y emotiva, estructura convencional con coros memorables.",
            'vocabulary_profile': {
                'vocabulary_richness': 0.45,
                'most_common_words': [('love', 45), ('heart', 32), ('time', 28), ('never', 25), ('feel', 22)]
            },
            'sentiment_profile': {
                'average_sentiment': {'compound': -0.15, 'positive': 0.25, 'negative': 0.35, 'neutral': 0.40},
                'dominant_themes': [
                    {'theme': 'heartbreak', 'score': 15, 'percentage': 35.0},
                    {'theme': 'love', 'score': 12, 'percentage': 28.0},
                    {'theme': 'struggle', 'score': 8, 'percentage': 19.0}
                ]
            },
            'structure_profile': {
                'common_structures': [{'structure': 'Verse-Chorus', 'frequency': 8}],
                'avg_verse_length': 4.2,
                'avg_chorus_length': 4.0
            }
        }
        
        print(f"✅ Análisis completado para {artist}")
        print(f"📝 Resumen: {mock_profile['writing_style_summary']}")
        print(f"📚 Vocabulario: {mock_profile['vocabulary_profile']['vocabulary_richness']:.2f} riqueza")
        print(f"💭 Sentimiento promedio: {mock_profile['sentiment_profile']['average_sentiment']['compound']:.2f}")
        print(f"🎼 Estructura común: {mock_profile['structure_profile']['common_structures'][0]['structure']}")
        
        # Demo 2: Generación de canción
        print("\n🎼 Demo 2: Generación de Nueva Canción")
        print("-" * 40)
        
        theme = "superación tras una pérdida"
        emotion = "esperanzadora"
        
        print(f"Generando canción al estilo de {artist}...")
        print(f"Tema: {theme}")
        print(f"Emoción: {emotion}")
        
        # Para el demo, simularemos una canción generada
        mock_song = {
            'success': True,
            'artist_style': artist,
            'theme': theme,
            'emotion': emotion,
            'lyrics': {
                '[Verse 1]': "The silence breaks with morning light\nAnother day to face the fight\nYesterday's tears have dried away\nNew strength is rising with the day",
                '[Chorus]': "I'm walking through the fire\nBurning through the pain\nFinding my desire\nTo rise and shine again\nStronger than before\nMy heart will heal and soar",
                '[Verse 2]': "The memories still visit me\nBut they don't have the same hold\nEach step I take is setting free\nThe story that needs to be told",
                '[Chorus]': "I'm walking through the fire\nBurning through the pain\nFinding my desire\nTo rise and shine again\nStronger than before\nMy heart will heal and soar",
                '[Bridge]': "Every scar tells where I've been\nBut they don't define where I'll go\nThis new chapter begins within\nWatch my spirit start to glow",
                '[Chorus]': "I'm walking through the fire\nBurning through the pain\nFinding my desire\nTo rise and shine again\nStronger than before\nMy heart will heal and soar"
            },
            'originality_score': 0.92
        }
        
        print("✅ Canción generada exitosamente")
        print(f"🎯 Score de originalidad: {mock_song['originality_score']:.2f}")
        
        # Mostrar la canción
        print("\n" + "=" * 50)
        print(f"🎵 CANCIÓN GENERADA AL ESTILO DE {artist.upper()} 🎵")
        print("=" * 50)
        
        for section, content in mock_song['lyrics'].items():
            print(f"\n{section}")
            print(content)
        
        print("=" * 50)
        print(f"Tema: {mock_song['theme']}")
        print(f"Emoción: {mock_song['emotion']}")
        print(f"Originalidad: {mock_song['originality_score']:.1%}")
        print("Generado con SongGem & Gemini AI")
        print("=" * 50)
        
        # Demo 3: Análisis de características
        print("\n📈 Demo 3: Análisis de Características Generadas")
        print("-" * 40)
        
        full_lyrics = "\n".join(mock_song['lyrics'].values())
        
        # Análisis básico
        word_count = len(full_lyrics.split())
        line_count = len([line for line in full_lyrics.split('\n') if line.strip()])
        unique_words = len(set(full_lyrics.lower().split()))
        
        print(f"📊 Estadísticas de la canción generada:")
        print(f"   • Palabras totales: {word_count}")
        print(f"   • Líneas: {line_count}")
        print(f"   • Palabras únicas: {unique_words}")
        print(f"   • Diversidad léxica: {unique_words/word_count:.2f}")
        
        # Detectar emociones básicas
        positive_words = ['light', 'strength', 'rising', 'desire', 'shine', 'stronger', 'heal', 'glow']
        negative_words = ['silence', 'tears', 'fire', 'pain', 'scar']
        
        lyrics_lower = full_lyrics.lower()
        pos_count = sum(lyrics_lower.count(word) for word in positive_words)
        neg_count = sum(lyrics_lower.count(word) for word in negative_words)
        
        print(f"   • Palabras positivas: {pos_count}")
        print(f"   • Palabras desafiantes: {neg_count}")
        print(f"   • Balance emocional: {'Positivo' if pos_count > neg_count else 'Equilibrado'}")
        
        print("\n🎉 ¡Demo completada exitosamente!")
        print("\n📖 Para usar SongGem con datos reales:")
        print("1. Configura tus API keys")
        print("2. Ejecuta: python src/main.py --interactive")
        print("3. Sigue las instrucciones del asistente")
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("Ejecuta: pip install -r requirements.txt")
    
    except Exception as e:
        print(f"❌ Error en la demo: {e}")

def demo_features():
    """Demostración de características avanzadas"""
    print("\n🚀 Características Avanzadas de SongGem")
    print("=" * 50)
    
    features = [
        {
            'name': 'Análisis de Estilo',
            'description': 'Extrae patrones de vocabulario, sentimiento y estructura',
            'example': 'Detecta que Adele usa vocabulario emotivo y estructura Verso-Coro'
        },
        {
            'name': 'Generación Original',
            'description': 'Crea letras 100% originales basadas en el estilo del artista',
            'example': 'Genera canción sobre "tecnología" al estilo de Taylor Swift'
        },
        {
            'name': 'Reescritura Estilística',
            'description': 'Transforma canciones existentes a nuevos estilos',
            'example': 'Reescribe "Bohemian Rhapsody" al estilo de Bad Bunny'
        },
        {
            'name': 'Análisis de Sentimiento',
            'description': 'Detecta emociones y temas recurrentes',
            'example': 'Identifica temas de heartbreak en el 35% de las canciones'
        },
        {
            'name': 'Detección de Estructuras',
            'description': 'Analiza patrones estructurales y de rima',
            'example': 'Detecta preferencia por esquemas AABB y coros memorables'
        },
        {
            'name': 'Caché Inteligente',
            'description': 'Almacenamiento local para evitar repetir análisis',
            'example': 'Reutiliza perfiles de artistas ya analizados'
        }
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"\n{i}. 🎯 {feature['name']}")
        print(f"   📝 {feature['description']}")
        print(f"   💡 Ejemplo: {feature['example']}")

if __name__ == "__main__":
    demo_basic_usage()
    demo_features()
    
    print("\n" + "=" * 60)
    print("🎵 SongGem - La creatividad musical encuentra la IA 🎵")
    print("📚 Más información en README.md")
    print("⚙️ Configura tus API keys para empezar")
    print("=" * 60)