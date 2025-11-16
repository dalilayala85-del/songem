#!/usr/bin/env python3
"""
Ejemplo completo de uso de SongGem
Demuestra todas las funcionalidades del sistema
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

def ejemplo_analisis_artista():
    """Ejemplo de análisis de estilo de un artista"""
    print("🎵 EJEMPLO 1: Análisis de Estilo de Artista")
    print("=" * 50)
    
    # Configurar tus API keys aquí o usar variables de entorno
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "tu_gemini_api_key")
    GENIUS_API_KEY = os.getenv("GENIUS_API_KEY", "tu_genius_api_key")
    
    if GEMINI_API_KEY == "tu_gemini_api_key" or GENIUS_API_KEY == "tu_genius_api_key":
        print("❌ Configura tus API keys en las variables de entorno o en el código")
        print("export GEMINI_API_KEY='tu_gemini_api_key'")
        print("export GENIUS_API_KEY='tu_genius_api_key'")
        return
    
    try:
        from main import SongGemSystem
        
        # Inicializar sistema
        system = SongGemSystem(GEMINI_API_KEY, GENIUS_API_KEY)
        
        # Analizar artista
        artista = "Taylor Swift"
        print(f"🔍 Analizando estilo de {artista}...")
        
        perfil = system.analyze_artist(artista, max_songs=10)
        
        if perfil:
            print(f"✅ Análisis completado")
            print(f"📝 Resumen: {perfil.get('writing_style_summary', '')}")
            print(f"📚 Canciones analizadas: {perfil.get('total_songs_analyzed', 0)}")
            print(f"💭 Sentimiento dominante: {perfil.get('sentiment_profile', {}).get('average_sentiment', {}).get('compound', 0):.2f}")
            
            # Mostrar temas principales
            temas = perfil.get('sentiment_profile', {}).get('dominant_themes', [])
            if temas:
                print(f"🎭 Temas principales:")
                for tema in temas[:3]:
                    print(f"   • {tema['theme'].title()}: {tema['percentage']:.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def ejemplo_generacion_cancion():
    """Ejemplo de generación de nueva canción"""
    print("\n🎼 EJEMPLO 2: Generación de Nueva Canción")
    print("=" * 50)
    
    try:
        from main import SongGemSystem
        
        # Configurar API keys (reemplaza con tus keys)
        GEMINI_API_KEY = "tu_gemini_api_key"
        GENIUS_API_KEY = "tu_genius_api_key"
        
        if GEMINI_API_KEY == "tu_gemini_api_key":
            print("📝 Este es un ejemplo simulado. Para usar real:")
            print("1. Configura tus API keys")
            print("2. Ejecuta el código con keys reales")
            print()
        
        # Simular sistema para demostración
        class DemoSystem:
            def generate_song(self, artista, tema, emocion=None, estructura=None):
                print(f"🎵 Generando canción al estilo de {artista}...")
                print(f"📝 Tema: {tema}")
                if emocion:
                    print(f"💭 Emoción: {emocion}")
                if estructura:
                    print(f"🎼 Estructura: {estructura}")
                
                # Canción de ejemplo
                cancion = {
                    'success': True,
                    'artist_style': artista,
                    'theme': tema,
                    'emotion': emocion,
                    'lyrics': {
                        '[Verse 1]': "Walking down these empty streets tonight\nSearching for a reason to feel right\nThe city lights are dancing in the rain\nWashing away all the memory and pain",
                        '[Chorus]': "But I'm stronger than I was before\nEvery heartbeat makes me want more\nI'm finding my way through the storm\nBreaking free and staying warm",
                        '[Verse 2]': "The mirror shows a different face\nSomeone full of strength and grace\nNo longer bound by yesterday\nTomorrow's light will show the way",
                        '[Chorus]': "But I'm stronger than I was before\nEvery heartbeat makes me want more\nI'm finding my way through the storm\nBreaking free and staying warm",
                        '[Bridge]': "Every scar tells where I've been\nEvery tear washed clean within\nThis is my time, my moment now\nI'll rise above and show them how",
                        '[Chorus]': "But I'm stronger than I was before\nEvery heartbeat makes me want more\nI'm finding my way through the storm\nBreaking free and staying warm"
                    },
                    'originality_score': 0.95
                }
                
                return cancion
        
        system = DemoSystem()
        
        # Generar canción
        resultado = system.generate_song(
            artista="Adele",
            tema="superación personal",
            emocion="empoderadora",
            estructura="Verse-Chorus"
        )
        
        if resultado.get('success'):
            print("✅ Canción generada exitosamente")
            print(f"🎯 Originalidad: {resultado.get('originality_score', 0):.1%}")
            
            # Mostrar canción
            print("\n" + "=" * 50)
            print(f"🎵 CANCIÓN GENERADA 🎵")
            print("=" * 50)
            
            lyrics = resultado.get('lyrics', {})
            for seccion, contenido in lyrics.items():
                print(f"\n{seccion}")
                print(contenido)
            
            print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def ejemplo_reescritura():
    """Ejemplo de reescritura de canción"""
    print("\n🔄 EJEMPLO 3: Reescritura Estilística")
    print("=" * 50)
    
    print("📝 Escenario: Reescribir 'Shape of You' al estilo de Bad Bunny")
    print()
    
    # Simular resultado
    resultado_reescritura = {
        'success': True,
        'original_title': 'Shape of You',
        'original_artist': 'Ed Sheeran',
        'target_artist': 'Bad Bunny',
        'new_angle': 'perspectiva latina urbana',
        'lyrics': {
            '[Intro]': "Brrr! Yo vi tu forma en la disco\nY mi mente se hizo un lío\nTú movimiento me provoca\nEsto es algo serio, mami",
            '[Verse 1]': "Con tu flow tan diferente\nTu manera de moverte\nBailando reggaetón lento\nTú eres lo que siempre soñé\nTu cintura no miente\nCuando bailas y me sientes\nEn la calle como en la cama\nTú eres mi dama, mi hermana",
            '[Chorus]': "Me encanta tu shape, tu figure\nTu cuerpo es puro arte, qué dure\nContigo siento el ritmo, la pulsión\nEres mi inspiración, mi canción\nMe encanta tu shape, tu manera\nEn la pista eres la primera\nBunny y tú, conexión pura\nEsto es cultura, es aventura",
            '[Verse 2]': "No hablamos el mismo idioma\nPero el cuerpo lo explica\nTu mirada me reclama\nEsta noche nos ganamos\nDel club hasta la mañana\nSin parar la provocación\nDime si es casualidad\nO si esto es realidad",
            '[Chorus]': "Me encanta tu shape, tu figure\nTu cuerpo es puro arte, qué dure\nContigo siento el ritmo, la pulsión\nEres mi inspiración, mi canción\nMe encanta tu shape, tu manera\nEn la pista eres la primera\nBunny y tú, conexión pura\nEsto es cultura, es aventura"
        },
        'originality_score': 0.88
    }
    
    print("✅ Reescritura completada")
    print(f"🎵 Original: '{resultado_reescritura['original_title']}' por {resultado_reescritura['original_artist']}")
    print(f"🎯 Nuevo estilo: {resultado_reescritura['target_artist']}")
    print(f"💡 Enfoque: {resultado_reescritura['new_angle']}")
    print(f"📊 Originalidad: {resultado_reescritura['originality_score']:.1%}")
    
    # Mostrar resultado
    print("\n" + "=" * 50)
    print("🎵 CANCIÓN REESCRITA 🎵")
    print("=" * 50)
    
    for seccion, contenido in resultado_reescritura['lyrics'].items():
        print(f"\n{seccion}")
        print(contenido)
    
    print("=" * 50)

def ejemplo_configuracion():
    """Ejemplo de configuración del sistema"""
    print("\n⚙️ EJEMPLO 4: Configuración del Sistema")
    print("=" * 50)
    
    print("📝 Configuración básica:")
    print("""
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
export GEMINI_API_KEY='tu_gemini_api_key'
export GENIUS_API_KEY='tu_genius_api_key'

# 3. Ejecutar en modo interactivo
python src/main.py --interactive
""")
    
    print("🔧 Configuración avanzada:")
    print("""
# Editar config/settings.py
MAX_SONGS_PER_ARTIST = 50
GENERATION_TEMPERATURE = 0.8
SENTIMENT_THRESHOLD = 0.1

# Ejecutar con parámetros personalizados
python src/main.py --generate \\
  --artist "Drake" \\
  --theme " éxito y fama" \\
  --emotion "confiado" \\
  --structure "Verse-Chorus" \\
  --gemini-key $GEMINI_API_KEY \\
  --genius-key $GENIUS_API_KEY
""")

def ejemplo_errores_comunes():
    """Ejemplo de manejo de errores comunes"""
    print("\n🚨 EJEMPLO 5: Manejo de Errores Comunes")
    print("=" * 50)
    
    errores_soluciones = [
        {
            'error': 'API key inválida',
            'solución': 'Verifica que las API keys sean correctas y estén activas'
        },
        {
            'error': 'No se encuentra el artista',
            'solución': 'Usa el nombre exacto del artista, preferiblemente en inglés'
        },
        {
            'error': 'Error en generación',
            'solución': 'Reduce max_tokens o verifica conexión a internet'
        },
        {
            'error': 'Rate limit excedido',
            'solución': 'Espera unos minutos antes de hacer más solicitudes'
        },
        {
            'error': 'Canción no encontrada',
            'solución': 'Verifica ortografía del artista y título exacto'
        }
    ]
    
    for i, item in enumerate(errores_soluciones, 1):
        print(f"{i}. ❌ Error: {item['error']}")
        print(f"   💡 Solución: {item['solución']}")
        print()

if __name__ == "__main__":
    print("🎵 SongGem - Ejemplos Completo de Uso 🎵")
    print("=" * 60)
    
    # Ejecutar todos los ejemplos
    ejemplo_analisis_artista()
    ejemplo_generacion_cancion()
    ejemplo_reescritura()
    ejemplo_configuracion()
    ejemplo_errores_comunes()
    
    print("\n" + "=" * 60)
    print("🎉 ¡Ejemplos completados!")
    print("\n📖 Para más información:")
    print("• Lee README.md completo")
    print("• Ejecuta python install.py para instalación")
    print("• Prueba el modo interactivo: python src/main.py --interactive")
    print("🚀 SongGem - La creatividad musical encuentra la IA")
    print("=" * 60)