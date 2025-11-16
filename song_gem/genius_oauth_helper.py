#!/usr/bin/env python3
"""
Ayudante para configuración OAuth de Genius API
Guía paso a paso para obtener API keys y redirect URI
"""

import webbrowser
import urllib.parse

def show_genius_setup_guide():
    """Muestra la guía completa de configuración de Genius API"""
    print("🎵 Guía de Configuración de Genius API para SongGem")
    print("=" * 60)
    
    print("\n📋 PASO 1: Crear Aplicación en Genius")
    print("-" * 40)
    print("1. Abre tu navegador y ve a:")
    print("   https://genius.com/api-clients")
    print("2. Inicia sesión con tu cuenta de Genius")
    print("3. Haz clic en 'New App' o edita una existente")
    
    print("\n⚙️ PASO 2: Configurar la Aplicación")
    print("-" * 40)
    print("Llena estos campos exactamente:")
    print("""
    Application Name: SongGem
    Application Website URL: http://localhost:8080
    Redirect URI: http://localhost:8080/callback
    
    Description: Sistema de generación de canciones con IA
    """)
    
    print("\n🔑 PASO 3: Obtener Credenciales")
    print("-" * 40)
    print("Después de crear la aplicación, Genius te mostrará:")
    print("""
    ✅ Client ID: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ✅ Client Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ✅ Access Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    """)
    
    print("\n🎯 Solo necesitas el ACCESS TOKEN para SongGem")
    
    print("\n🚀 PASO 4: Probar la Configuración")
    print("-" * 40)
    print("Guarda tu Access Token:")
    print("""
    export GENIUS_API_KEY="tu_genius_access_token_aqui"
    export GEMINI_API_KEY="tu_gemini_api_key_aqui"
    """)
    
    print("\nY ejecuta SongGem:")
    print("python src/main.py --interactive")

def test_genius_api(api_key: str):
    """Prueba si la API key de Genius funciona"""
    try:
        import lyricsgenius
        genius = lyricsgenius.Genius(api_key)
        
        print("🔍 Probando conexión con Genius API...")
        artist = genius.search_artist("Taylor Swift", max_songs=1)
        
        if artist:
            print("✅ Conexión exitosa con Genius API!")
            print(f"📵 Encontrado: {artist.name}")
            print(f"🎵 Canciones disponibles: {len(artist.songs)}")
            return True
        else:
            print("❌ No se encontró al artista - Verifica tu API key")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando con Genius API: {e}")
        print("💡 Asegúrate de que estás usando el Access Token, no el Client ID")
        return False

def open_genius_dashboard():
    """Abre el dashboard de Genius en el navegador"""
    url = "https://genius.com/api-clients"
    print(f"🌐 Abriendo {url} en tu navegador...")
    try:
        webbrowser.open(url)
        print("✅ Dashboard abierto")
    except:
        print("❌ No se pudo abrir el navegador automáticamente")
        print(f"🔗 Abre manualmente: {url}")

def show_redirect_uri_options():
    """Muestra las opciones de Redirect URI"""
    print("\n🔗 Opciones de Redirect URI:")
    print("-" * 30)
    
    options = [
        {
            'name': 'Local Development',
            'uri': 'http://localhost:8080/callback',
            'description': 'Ideal para desarrollo local'
        },
        {
            'name': 'Out-of-Band (OOB)',
            'uri': 'urn:ietf:wg:oauth:2.0:oob',
            'description': 'No requiere servidor local'
        },
        {
            'name': 'Custom Local',
            'uri': 'http://127.0.0.1:5000/auth/complete',
            'description': 'Puerto personalizado'
        }
    ]
    
    for i, option in enumerate(options, 1):
        print(f"\n{i}. {option['name']}")
        print(f"   URI: {option['uri']}")
        print(f"   Uso: {option['description']}")
    
    print("\n💡 Recomendación: Usa 'http://localhost:8080/callback'")

def interactive_setup():
    """Asistente interactivo de configuración"""
    print("🎵 Asistente de Configuración de Genius API")
    print("=" * 50)
    
    while True:
        print("\n¿Qué te gustaría hacer?")
        print("1. Ver guía completa de configuración")
        print("2. Abrir dashboard de Genius en navegador")
        print("3. Probar mi API key de Genius")
        print("4. Ver opciones de Redirect URI")
        print("5. Salir")
        
        choice = input("\nElige una opción (1-5): ").strip()
        
        if choice == '1':
            show_genius_setup_guide()
        elif choice == '2':
            open_genius_dashboard()
        elif choice == '3':
            api_key = input("Ingresa tu Genius API key (Access Token): ").strip()
            if api_key:
                test_genius_api(api_key)
            else:
                print("❌ Debes ingresar una API key")
        elif choice == '4':
            show_redirect_uri_options()
        elif choice == '5':
            print("👋 ¡Configura tus API keys y vuelve a SongGem!")
            break
        else:
            print("❌ Opción no válida")

def main():
    """Función principal"""
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        if len(sys.argv) > 2:
            test_genius_api(sys.argv[2])
        else:
            print("Uso: python genius_oauth_helper.py test <api_key>")
    else:
        interactive_setup()

if __name__ == "__main__":
    import sys
    main()