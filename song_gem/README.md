# 🎵 SongGem - Sistema de Generación de Canciones con Gemini AI

SongGem es un sistema completo de IA que utiliza la API de Google Gemini para generar canciones originales al estilo de cualquier artista. El sistema analiza el estilo lírico de artistas, extrae patrones de escritura y crea contenido completamente nuevo manteniendo la esencia del artista seleccionado.

## 🌟 Características Principales

### 📊 **Análisis de Estilo Profundo**
- Extracción de canciones usando Genius API
- Análisis de vocabulario y patrones lingüísticos
- Detección de temas recurrentes y sentimientos
- Análisis de estructuras y esquemas de rima

### 🎼 **Generación de Letras Original**
- Creación de canciones 100% originales
- Adaptación al estilo específico del artista
- Control de emociones y estructuras
- Validación de originalidad

### 🔄 **Reescritura Estilística**
- Transformar canciones existentes a nuevos estilos
- Mantener la esencia temática con nuevo enfoque
- Preservar la coherencia emocional

### 🎯 **Modo Interactivo**
- Interfaz amigable por línea de comandos
- Asistente guiado para generar canciones
- Gestión de perfiles de artistas

## 🚀 Instalación Rápida

### 1. Clonar el proyecto
```bash
git clone <repository-url>
cd song_gem
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Descargar modelos adicionales
```bash
python -m nltk.downloader punkt stopwords wordnet omw-1.4
python -m spacy download en_core_web_sm
```

### 4. 🔑 Configurar API Keys

#### Para Google Gemini:
- Ve a: [AI Studio](https://makersuite.google.com/app/apikey)
- Crea nueva API key
- Copia tu key

#### Para Genius (con Redirect URI):
- Ve a: [Genius API](https://genius.com/api-clients)
- Crea nueva aplicación con estos datos:
  ```
  Application Name: SongGem
  Application Website URL: http://localhost:8080
  Redirect URI: http://localhost:8080/callback
  ```
- Obtén tu **Access Token** (no el Client ID)
- Copia el Access Token

#### 🎯 Asistente de Configuración:
```bash
python genius_oauth_helper.py
```

### 5. Configurar variables de entorno
```bash
export GEMINI_API_KEY='tu_gemini_api_key'
export GENIUS_API_KEY='tu_genius_access_token'
```

## 📖 Uso Básico

### Modo Interactivo (Recomendado)
```bash
cd song_gem/src
python main.py --interactive \
  --gemini-key TU_GEMINI_API_KEY \
  --genius-key TU_GENIUS_API_KEY
```

### Línea de Comandos

#### Analizar un Artista
```bash
python main.py --analyze "Taylor Swift" \
  --gemini-key TU_GEMINI_API_KEY \
  --genius-key TU_GENIUS_API_KEY
```

#### Generar Nueva Canción
```bash
python main.py --generate \
  --artist "Bad Bunny" \
  --theme "amor en la ciudad" \
  --emotion "melancólico" \
  --gemini-key TU_GEMINI_API_KEY \
  --genius-key TU_GENIUS_API_KEY
```

#### Reescribir Canción
```bash
python main.py --rewrite \
  --target-artist "Drake" \
  --original-artist "Taylor Swift" \
  --original-title "Love Story" \
  --new-angle "perspectiva urbana moderna" \
  --gemini-key TU_GEMINI_API_KEY \
  --genius-key TU_GENIUS_API_KEY
```

## 🏗️ Arquitectura del Sistema

```
song_gem/
├── src/
│   ├── main.py              # Interfaz principal
│   ├── scrapers/
│   │   └── lyrics_scraper.py # Extracción de letras
│   ├── analyzers/
│   │   └── style_analyzer.py # Análisis de estilo
│   ├── generators/
│   │   └── lyrics_generator.py # Generación con Gemini
│   └── utils/
├── config/
│   └── settings.py          # Configuración del sistema
├── data/
│   ├── lyrics_cache/        # Caché de letras
│   ├── style_profiles/      # Perfiles de estilo
│   ├── generated_songs/     # Canciones generadas
│   └── rewritten_songs/     # Canciones reescritas
└── docs/
```

## 🎛️ Parámetros de Generación

### Emociones Disponibles
- `positive` - Optimista y alegre
- `emotional` - Sentimental y profundo
- `melancholic` - Melancólico y reflexivo
- `energetic` - Enérgico y vibrante
- `romantic` - Romántico y tierno

### Estructuras Musicales
- `Verse-Chorus` - Estructura convencional
- `Verse-Bridge` - Sin coro repetitivo
- `Verse-Only` - Verso continuo
- `Free-form` - Estructura experimental

### Longitudes de Canción
- `short` - 2-3 versos con coro
- `standard` - Estructura completa (default)
- `extended` - Versos adicionales y puente
- `epic` - Estructura completa con múltiples puentes

## 🔧 Configuración Avanzada

Editar `config/settings.py` para personalizar:

```python
# Límites de extracción
MAX_SONGS_PER_ARTIST = 50
MIN_LYRICS_LENGTH = 100

# Parámetros de generación
GENERATION_TEMPERATURE = 0.8
MAX_TOKENS = 2000

# Umbrales de análisis
SENTIMENT_THRESHOLD = 0.1
RHHEME_ANALYSIS_DEPTH = 3
```

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis Completo
```python
from song_gem.src.main import SongGemSystem

# Inicializar sistema
system = SongGemSystem(gemini_key="...", genius_key="...")

# Analizar artista
profile = system.analyze_artist("Ed Sheeran", max_songs=30)
print(f"Estilo: {profile['writing_style_summary']}")
```

### Ejemplo 2: Generación Personalizada
```python
# Generar canción con parámetros específicos
song = system.generate_song(
    artist_name="Adele",
    theme="superación personal",
    emotion="empoderadora",
    structure="Verse-Chorus"
)
```

### Ejemplo 3: Batch de Generación
```python
# Múltiples canciones con diferentes temas
themes = ["amor nocturno", "ciudad futurista", "memorias infancia"]
artist = "The Weeknd"

for theme in themes:
    song = system.generate_song(artist, theme)
    # Guardar o procesar resultados
```

## 🎯 Casos de Uso Recomendados

### 🎵 **Para Compositores**
- Superar bloqueos creativos
- Explorar nuevos estilos de escritura
- Generar ideas para canciones

### 🎤 **Para Artistas**
- Crear contenido en colaboración
- Experimentar con diferentes estilos
- Desarrollar versatilidad lírica

### 📚 **Para Educadores**
- Enseñar análisis de estilos musicales
- Demostrar técnicas de composición
- Explorar evolución de artistas

### 🎮 **Para Desarrolladores**
- Integrar en aplicaciones musicales
- Crear APIs de generación de contenido
- Desarrollar herramientas creativas

## ⚠️ Consideraciones Importantes

### 🚫 **Sobre Originalidad**
- SongGem genera contenido 100% original
- No copia ni reproduce letras existentes
- Se basa en patrones estilísticos, no en contenido específico
- Cumple con derechos de autor y fair use

### 📊 **Limitaciones Técnicas**
- Requiere conexión a internet para APIs
- Tiempo de análisis varía por cantidad de canciones
- Rate limits de APIs externas
- Calidad depende de la disponibilidad de letras

### 🔒 **Privacidad y Seguridad**
- Las API keys se manejan localmente
- Datos cacheados almacenados localmente
- No se comparten datos con terceros
- Respeto por propiedades intelectuales

## 🛠️ Solución de Problemas

### Problemas Comunes

#### ❌ "API key inválida"
```bash
# Verificar que las keys son correctas
curl -H "Authorization: Bearer TU_GEMINI_API_KEY" \
  "https://generativelanguage.googleapis.com/v1beta/models"
```

#### ❌ "No se encuentra el artista"
- Verificar el nombre exacto del artista
- Usar nombres en inglés si es posible
- Revisar ortografía y acentos

#### ❌ "Error en generación"
- Reducir `max_tokens` en configuración
- Verificar conexión a internet
- Intentar con un tema más simple

### Depuración

```bash
# Modo verbose para debugging
python main.py --interactive --verbose \
  --gemini-key ... --genius-key ...
```

## 🤝 Contribución

¡Contribuciones bienvenidas!

1. Fork del proyecto
2. Crear feature branch
3. Implementar cambios con tests
4. Submit Pull Request

### Áreas de Mejora Sugeridas
- Soporte para más APIs de letras
- Análisis de métricas musicales
- Interfaz web/visual
- Integración con DAWs
- Soporte multilingüe

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para detalles.

## 🙏 Agradecimientos

- Google Gemini API por la tecnología de generación
- Genius API por el acceso a letras
- Comunidades de IA y música por inspiración
- Contribuidores y testers de la comunidad

## 📞 Contacto y Soporte

- Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Discusiones: [GitHub Discussions](https://github.com/your-repo/discussions)
- Email: song-gem@example.com

---

**🎵 SongGem - Donde la IA encuentra la creatividad musical 🎵**