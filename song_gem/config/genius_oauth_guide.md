# 🎵 Guía de Configuración OAuth para Genius API

## 📋 Pasos para Configurar Redirect URI

### 1. **Crear/Editar Aplicación en Genius**

1. Ve a: https://genius.com/api-clients
2. Inicia sesión con tu cuenta de Genius
3. Crea nueva aplicación o edita la existente

### 2. **Configuración de la Aplicación**

```
Application Name: SongGem
Application Website URL: http://localhost:8080
Redirect URI: http://localhost:8080/callback
```

### 3. **Opciones de Redirect URI**

**Opción A - Local Development:**
```
http://localhost:8080/callback
```

**Opción B - Out-of-Band (OOB):**
```
urn:ietf:wg:oauth:2.0:oob
```

**Opción C - Custom Local:**
```
http://127.0.0.1:5000/auth/complete
```

### 4. **Obtener Credenciales**

Genius te proporcionará:

```
Client ID: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Client Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Access Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🔧 Configuración en SongGem

### Método 1: Usar Access Token Directo (Recomendado)

```python
from song_gem.src.main import SongGemSystem

# Solo necesitas el Access Token
system = SongGemSystem(
    gemini_key="tu_gemini_api_key",
    genius_key="tu_genius_access_token"  # Access Token de Genius
)
```

### Método 2: OAuth Completo (si necesitas autenticación de usuario)

```python
from song_gem.src.scrapers.lyrics_scraper import LyricsScraper

scraper = LyricsScraper(
    api_key="tu_client_id",
    redirect_uri="http://localhost:8080/callback"
)
```

## 🚀 Uso Inmediato

Después de configurar, ejecuta:

```bash
# Con variables de entorno
export GEMINI_API_KEY="tu_gemini_api_key"
export GENIUS_API_KEY="tu_genius_access_token"

python src/main.py --interactive
```

## ❓ Preguntas Comunes

**¿Necesito OAuth para SongGem?**
- No, con el Access Token es suficiente

**¿Qué URI debo usar?**
- `http://localhost:8080/callback` es suficiente

**¿Dónde encuentro el Access Token?**
- En tu dashboard de Genius API después de crear la aplicación

## 🔍 Verificación

Para verificar que todo funciona:

```python
from song_gem.src.scrapers.lyrics_scraper import LyricsScraper

scraper = LyricsScraper("tu_access_token")
songs = scraper.get_artist_songs("Taylor Swift", 5)
print(f"Se encontraron {len(songs)} canciones")
```

Si funciona, verás las canciones extraídas correctamente.