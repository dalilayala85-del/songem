#!/usr/bin/env python3
"""
Script de instalación automática para SongGem
Instala todas las dependencias y configura el entorno
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Función principal de instalación"""
    print("🎵 SongGem - Script de Instalación Automática 🎵")
    print("=" * 50)
    
    # Verificar Python 3.8+
    if sys.version_info < (3, 8):
        print("❌ SongGem requiere Python 3.8 o superior")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias de Python...")
    
    dependencies = [
        ("pip install -r requirements.txt", "Dependencias principales"),
        ("python -m nltk.downloader punkt stopwords wordnet omw-1.4", "Modelos NLTK"),
    ]
    
    for command, description in dependencies:
        if not run_command(command, description):
            print(f"⚠️ Error instalando {description}, continuando...")
    
    # Instalar spaCy
    print("\n🧠 Instalando spaCy...")
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✅ Modelo spaCy ya está instalado")
        except OSError:
            print("📥 Descargando modelo spaCy...")
            if run_command("python -m spacy download en_core_web_sm", "Modelo spaCy"):
                print("✅ Modelo spaCy instalado")
            else:
                print("⚠️ Error instalando spaCy, puedes instalarlo manualmente más tarde")
    except ImportError:
        print("❌ spaCy no está instalado, instálalo con: pip install spacy")
    
    # Crear directorios necesarios
    print("\n📁 Creando estructura de directorios...")
    directories = [
        "data/lyrics_cache",
        "data/style_profiles", 
        "data/generated_songs",
        "data/rewritten_songs",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")
    
    # Verificar instalación
    print("\n🔍 Verificando instalación...")
    
    try:
        import google.generativeai
        import lyricsgenius
        import nltk
        import spacy
        import pandas
        import textblob
        print("✅ Todas las dependencias principales están instaladas")
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    # Crear archivo de configuración de ejemplo
    print("\n⚙️ Creando configuración de ejemplo...")
    
    config_example = """
# Configuración de SongGem
# Copia este archivo a settings.py y añade tus API keys

GEMINI_API_KEY = "tu_gemini_api_key_aqui"
GENIUS_API_KEY = "tu_genius_api_key_aqui"

# Obtén tus keys en:
# Gemini: https://makersuite.google.com/app/apikey
# Genius: https://genius.com/api-clients
"""
    
    with open("config/settings_example.py", "w") as f:
        f.write(config_example)
    
    print("✅ Archivo de configuración creado: config/settings_example.py")
    
    # Instrucciones finales
    print("\n" + "=" * 50)
    print("🎉 ¡Instalación completada!")
    print("\n📋 Próximos pasos:")
    print("1. 🔑 Obtén tus API keys:")
    print("   - Gemini: https://makersuite.google.com/app/apikey")
    print("   - Genius: https://genius.com/api-clients")
    print("     • Application Name: SongGem")
    print("     • Redirect URI: http://localhost:8080/callback")
    print("     • ¡Usa el Access Token, no el Client ID!")
    
    print("\n2. ⚙️ Configura tus keys:")
    print("   export GEMINI_API_KEY='tu_gemini_api_key'")
    print("   export GENIUS_API_KEY='tu_genius_access_token'")
    print("   # O usa el asistente:")
    print("   python genius_oauth_helper.py")
    
    print("\n3. 🚀 Ejecuta SongGem:")
    print("   cd src")
    print("   python main.py --interactive")
    print("   # O con keys explícitas:")
    print("   python main.py --interactive --gemini-key $GEMINI_API_KEY --genius-key $GENIUS_API_KEY")
    
    print("\n4. 🧪 Prueba tu configuración:")
    print("   python genius_oauth_helper.py test $GENIUS_API_KEY")
    
    print("\n📖 Para más información, lee README.md y config/genius_oauth_guide.md")
    print("=" * 50)

if __name__ == "__main__":
    main()