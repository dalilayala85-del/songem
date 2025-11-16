# 🎵 Sistema de Generación de Canciones con Gemini API

## Objetivo
Crear un gem completo que pueda escribir canciones al estilo de cualquier artista, basándose en la esencia y estilo lírico del artista, sin copiar directamente las letras originales.

## Fases del Proyecto

### [x] 1. Configuración del Entorno
- [x] Instalar dependencias necesarias
- [x] Configurar Google Gemini API
- [x] Configurar LyricsGenius API
- [x] Crear estructura de archivos

### [x] 2. Módulo de Extracción de Letras
- [x] Implementar scraper de Genius API
- [x] Extraer canciones de cualquier artista
- [x] Limpiar y procesar las letras
- [x] Guardar en base de datos local

### [x] 3. Módulo de Análisis de Estilo
- [x] Analizar patrones de rima
- [x] Detectar temas recurrentes
- [x] Analizar sentimientos y emociones
- [x] Extraer características de vocabulario
- [x] Identificar estructura de canciones

### [x] 4. Módulo de Generación con Gemini
- [x] Configurar prompts para Gemini
- [x] Implementar generación basada en estilo
- [x] Asegurar originalidad de letras
- [x] Validar coherencia y calidad

### [x] 5. Interfaz Principal
- [x] Crear CLI interactivo
- [x] Implementar entrada de artista
- [x] Mostrar opciones de generación
- [x] Presentar resultados formateados

### [x] 6. Testing y Validación
- [x] Probar con múltiples artistas
- [x] Validar originalidad
- [x] Mejorar prompts y análisis
- [x] Documentar uso

## 🎉 Proyecto Completado Exitosamente

### ✅ Componentes Implementados:

1. **🔧 Scraper de Letras** (`src/scrapers/lyrics_scraper.py`)
   - Integración con Genius API
   - Caché inteligente de canciones
   - Limpieza y procesamiento de texto

2. **📊 Analizador de Estilo** (`src/analyzers/style_analyzer.py`)
   - Análisis de vocabulario y complejidad
   - Detección de sentimientos y temas
   - Análisis de estructuras y rimas
   - Perfiles de estilo completos

3. **🎼 Generador con Gemini** (`src/generators/lyrics_generator.py`)
   - Prompts optimizados para generación
   - Validación de originalidad
   - Control de emociones y estructuras
   - Reescritura estilística

4. **🖥️ Interfaz Principal** (`src/main.py`)
   - CLI interactivo completo
   - Modo por línea de comandos
   - Gestión de perfiles
   - Manejo de errores robusto

5. **⚙️ Configuración y Documentación**
   - Sistema de configuración flexible
   - README completo con ejemplos
   - Script de instalación automática
   - Demo interactiva

6. **📦 Estructura de Proyecto**
   - Organización modular clara
   - Manejo de datos locales
   - Caché de resultados
   - Exportación de resultados

### 🚀 Características Principales:

- **🎵 Análisis Profundo**: Extrae patrones de escritura de cualquier artista
- **✨ Generación Original**: Crea letras 100% originales manteniendo el estilo
- **🔄 Reescritura Estilística**: Transforma canciones a nuevos estilos
- **🎯 Modo Interactivo**: CLI amigable con asistente guiado
- **💾 Caché Inteligente**: Almacena análisis para reutilización
- **📊 Análisis Detallado**: Sentimientos, temas, vocabulario, estructura

### 📖 Uso:

```bash
# Instalación
python install.py

# Modo interactivo
python src/main.py --interactive \
  --gemini-key TU_KEY --genius-key TU_KEY

# Generación directa
python src/main.py --generate \
  --artist "Bad Bunny" --theme "amor urbano" \
  --gemini-key TU_KEY --genius-key TU_KEY
```

### 🎯 Resultado:
Un sistema completo y funcional que cumple con todos los requisitos solicitados:
- Analiza cualquier artista extrayendo sus canciones
- Genera contenido original basado en el estilo (no en las letras)
- Nunca repite versos o ejemplos de canciones existentes
- Utiliza la esencia del artista para crear nueva música
- Interfaz profesional y fácil de usar

## 🏆 Proyecto FINALIZADO y LISTO para usar