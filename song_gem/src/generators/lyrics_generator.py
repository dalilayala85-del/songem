import google.generativeai as genai
import json
import re
from typing import Dict, List, Optional
from pathlib import Path

class LyricsGenerator:
    """Generador de letras usando Gemini API basado en estilos de artistas"""
    
    def __init__(self, api_key: str):
        """
        Inicializa el generador con la API key de Gemini
        
        Args:
            api_key: API key de Google Gemini
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.generation_config = {
            "temperature": 0.8,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 2000,
        }
    
    def _create_style_prompt(self, style_profile: Dict, original_song_info: Dict = None) -> str:
        """
        Crea un prompt detallado basado en el perfil de estilo del artista
        
        Args:
            style_profile: Perfil de estilo del artista
            original_song_info: Información de la canción original (si aplica)
            
        Returns:
            Prompt para Gemini
        """
        artist = style_profile['artist_name']
        
        # Extraer características del estilo
        vocab = style_profile.get('vocabulary_profile', {})
        sentiment = style_profile.get('sentiment_profile', {})
        structure = style_profile.get('structure_profile', {})
        themes = sentiment.get('dominant_themes', [])
        
        # Construir descripción del estilo
        style_description = f"""
ESTILO MUSICAL DE {artist.upper()}:

CARACTERÍSTICAS PRINCIPALES:
- Vocabulario: {"rico y diverso" if vocab.get('vocabulary_richness', 0) > 0.4 else "directo y accesible"}
- Tono emocional: {sentiment.get('average_sentiment', {}).get('compound', 0):.2f} ({"positivo" if sentiment.get('average_sentiment', {}).get('compound', 0) > 0 else "melancólico" if sentiment.get('average_sentiment', {}).get('compound', 0) < 0 else "neutral"})
- Estructura preferida: {structure.get('common_structures', [{}])[0].get('structure', 'Verse-Chorus')}

TEMAS RECURRENTES:
{chr(10).join([f"- {theme['theme'].title()}: {theme['percentage']:.1f}% de prevalencia" for theme in themes[:5]])}

PALABRAS CARACTERÍSTICAS:
{', '.join([word[0] for word in vocab.get('most_common_words', [])[:10]])}

PATRONES DE ESCRITURA:
{style_profile.get('writing_style_summary', '')}

REGLAS CRÍTICAS DE ORIGINALIDAD:
1. NUNCA copiar versos, frases o rimas exactas de canciones existentes
2. Usar el ESPÍRITU y estilo del artista, no sus letras específicas
3. Crear metáforas e imágenes originales pero con la misma sensibilidad
4. Mantener la estructura emocional pero con contenido completamente nuevo
5. Evitar referencias directas a canciones conocidas del artista
"""
        
        # Si hay una canción original, agregar contexto sin copiar
        if original_song_info:
            style_description += f"""

CONTEXTO DE LA CANCIÓN ORIGINAL (SOLO PARA INSPIRACIÓN TEMÁTICA):
- Título original: {original_song_info.get('title', '')}
- Tema principal: {original_song_info.get('theme', '')}
- Emoción dominante: {original_song_info.get('emotion', '')}

IMPORTANTE: NO usar las mismas palabras, metáforas o estructuras de la canción original.
Capturar solo la ESENCIA temática y emocional, no el contenido literal.
"""
        
        return style_description
    
    def _create_generation_prompt(self, style_description: str, 
                                new_theme: str, 
                                emotion: str = None,
                                structure: str = None,
                                length: str = "standard") -> str:
        """
        Crea el prompt final para generación de letras
        
        Args:
            style_description: Descripción del estilo del artista
            new_theme: Nuevo tema para la canción
            emotion: Emoción deseada
            structure: Estructura deseada
            length: Longitud deseada
            
        Returns:
            Prompt completo para generación
        """
        prompt = f"""
{style_description}

TAREA DE GENERACIÓN:
Escribe una canción completamente ORIGINAL al estilo del artista descrito arriba con las siguientes especificaciones:

TEMA: {new_theme}
EMOCIÓN: {emotion if emotion else "siguiendo el tono natural del artista"}
ESTRUCTURA: {structure if structure else "siguiendo las preferencias del artista"}
LONGITUD: {length}

REQUISITOS ESTRICTOS:
1. Originalidad absoluta - cero plagio o similitud con canciones existentes
2. Capturar la esencia estilística del artista (tono, vocabulario, ritmo)
3. Letras coherentes y emocionalmente resonantes
4. Estructura clara (versos, coro, puente si aplica)
5. Contenido completamente nuevo pero auténtico al estilo

FORMATO DE SALIDA:
Presenta la letra con estructura clara:
[Verse 1]
<verso>

[Chorus]
<coro>

[Verse 2]
<verso>

[Chorus]
<coro>

[Bridge] (opcional)
<puente>

[Chorus]
<coro final>

[Outro] (opcional)
<final>

IMPORTANTE: Cada línea debe ser 100% original. No incluir ninguna letra o frase de canciones existentes.
"""
        
        return prompt
    
    def generate_lyrics(self, 
                       style_profile: Dict, 
                       new_theme: str,
                       emotion: str = None,
                       structure: str = None,
                       length: str = "standard",
                       original_song_info: Dict = None) -> Dict:
        """
        Genera letras originales basadas en el estilo de un artista
        
        Args:
            style_profile: Perfil de estilo del artista
            new_theme: Nuevo tema para la canción
            emotion: Emoción deseada
            structure: Estructura deseada
            length: Longitud deseada
            original_song_info: Info de canción original (para reescritura de estilo)
            
        Returns:
            Diccionario con la letra generada y metadatos
        """
        try:
            # Crear prompts
            style_description = self._create_style_prompt(style_profile, original_song_info)
            generation_prompt = self._create_generation_prompt(
                style_description, new_theme, emotion, structure, length
            )
            
            print(f"Generando letra al estilo de {style_profile['artist_name']}...")
            print(f"Tema: {new_theme}")
            
            # Generar con Gemini
            response = self.model.generate_content(
                generation_prompt,
                generation_config=self.generation_config
            )
            
            generated_text = response.text
            
            # Procesar y estructurar la respuesta
            structured_lyrics = self._parse_lyrics_response(generated_text)
            
            # Validar originalidad básica
            originality_score = self._check_originality(structured_lyrics, style_profile)
            
            result = {
                'success': True,
                'artist_style': style_profile['artist_name'],
                'theme': new_theme,
                'emotion': emotion,
                'structure': structure,
                'lyrics': structured_lyrics,
                'raw_response': generated_text,
                'originality_score': originality_score,
                'generation_metadata': {
                    'model': 'gemini-pro',
                    'temperature': self.generation_config['temperature'],
                    'max_tokens': self.generation_config['max_output_tokens']
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'artist_style': style_profile.get('artist_name', 'Unknown'),
                'theme': new_theme
            }
    
    def _parse_lyrics_response(self, response_text: str) -> Dict:
        """
        Procesa la respuesta de Gemini y estructura las letras
        
        Args:
            response_text: Texto crudo de Gemini
            
        Returns:
            Diccionario con letras estructuradas
        """
        sections = {}
        current_section = None
        current_lines = []
        
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detectar encabezados de sección
            if line.startswith('[') and line.endswith(']'):
                # Guardar sección anterior
                if current_section and current_lines:
                    sections[current_section] = '\n'.join(current_lines)
                
                # Iniciar nueva sección
                current_section = line
                current_lines = []
            elif line and not line.startswith('TAREA') and not line.startswith('ESTILO'):
                current_lines.append(line)
        
        # Guardar última sección
        if current_section and current_lines:
            sections[current_section] = '\n'.join(current_lines)
        
        # Si no se detectaron secciones, intentar extraer versos y coros
        if not sections:
            sections = self._fallback_parsing(response_text)
        
        return sections
    
    def _fallback_parsing(self, text: str) -> Dict:
        """Análisis alternativo si no se detectan secciones claras"""
        sections = {}
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return {}
        
        # Dividir en secciones iguales
        total_lines = len(lines)
        
        if total_lines >= 12:
            sections['[Verse 1]'] = '\n'.join(lines[:4])
            sections['[Chorus]'] = '\n'.join(lines[4:8])
            sections['[Verse 2]'] = '\n'.join(lines[8:12])
            if total_lines > 16:
                sections['[Chorus]'] += '\n' + '\n'.join(lines[12:16])
                if total_lines > 20:
                    sections['[Outro]'] = '\n'.join(lines[16:])
        else:
            sections['[Full Song]'] = '\n'.join(lines)
        
        return sections
    
    def _check_originality(self, lyrics: Dict, style_profile: Dict) -> float:
        """
        Verificación básica de originalidad
        
        Args:
            lyrics: Letras generadas
            style_profile: Perfil de estilo del artista
            
        Returns:
            Score de originalidad (0-1)
        """
        all_text = '\n'.join(lyrics.values())
        
        # Verificaciones básicas
        if not all_text or len(all_text) < 50:
            return 0.0
        
        # Verificar que no hay patrones sospechosos de copia
        suspicious_patterns = [
            r'^[A-Z][a-z]+$',  # Solo líneas con una palabra capitalizada
            r'(.{20,})\1{2,}',  # Repeticiones excesivas
            r'\[Verse \d+\]: \[Chorus\]:',  # Formato demasiado simple
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, all_text):
                return 0.3
        
        # Verificar longitud y complejidad
        word_count = len(all_text.split())
        unique_words = len(set(all_text.lower().split()))
        vocabulary_diversity = unique_words / word_count if word_count > 0 else 0
        
        # Score basado en diversidad de vocabulario y complejidad
        originality_score = min(vocabulary_diversity * 1.5, 1.0)
        
        return originality_score
    
    def rewrite_song_in_style(self, 
                             style_profile: Dict,
                             original_song: Dict,
                             new_angle: str = None) -> Dict:
        """
        Reescribe una canción existente al estilo de otro artista
        
        Args:
            style_profile: Perfil del artista cuyo estilo se adoptará
            original_song: Información de la canción original
            new_angle: Nuevo enfoque o perspectiva
            
        Returns:
            Letras reescritas manteniendo el espíritu pero con nuevo estilo
        """
        # Extraer información temática de la original sin copiar contenido
        original_info = {
            'title': original_song.get('title', ''),
            'theme': new_angle or self._extract_theme(original_song.get('lyrics', '')),
            'emotion': self._extract_emotion(original_song.get('lyrics', ''))
        }
        
        return self.generate_lyrics(
            style_profile=style_profile,
            new_theme=original_info['theme'],
            emotion=original_info['emotion'],
            original_song_info=original_info
        )
    
    def _extract_theme(self, lyrics: str) -> str:
        """Extrae el tema principal de una letra"""
        # Análisis simple de palabras clave
        themes = {
            'love': ['love', 'heart', 'kiss', 'romance'],
            'heartbreak': ['break', 'pain', 'goodbye', 'tears'],
            'celebration': ['party', 'dance', 'fun', 'celebrate'],
            'struggle': ['fight', 'battle', 'overcome', 'strong'],
            'success': ['win', 'top', 'king', 'power'],
            'nature': ['sky', 'sun', 'moon', 'stars']
        }
        
        lyrics_lower = lyrics.lower()
        theme_scores = {}
        
        for theme, keywords in themes.items():
            score = sum(lyrics_lower.count(keyword) for keyword in keywords)
            if score > 0:
                theme_scores[theme] = score
        
        return max(theme_scores.items(), key=lambda x: x[1])[0] if theme_scores else 'life'
    
    def _extract_emotion(self, lyrics: str) -> str:
        """Extrae la emoción principal de una letra"""
        positive_words = ['happy', 'joy', 'love', 'bright', 'smile']
        negative_words = ['sad', 'pain', 'cry', 'dark', 'tears']
        
        lyrics_lower = lyrics.lower()
        
        pos_count = sum(lyrics_lower.count(word) for word in positive_words)
        neg_count = sum(lyrics_lower.count(word) for word in negative_words)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'emotional'
        else:
            return 'balanced'
    
    def save_generated_song(self, song_data: Dict, output_path: str):
        """Guarda la canción generada en un archivo"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(song_data, f, ensure_ascii=False, indent=2)
    
    def format_song_for_display(self, song_data: Dict) -> str:
        """Formatea la canción para visualización"""
        if not song_data.get('success'):
            return f"Error generando canción: {song_data.get('error', 'Unknown error')}"
        
        formatted = f"""
🎵 CANCIÓN GENERADA AL ESTILO DE {song_data['artist_style'].upper()} 🎵

Tema: {song_data['theme']}
Emoción: {song_data.get('emotion', 'Natural del artista')}
Score Originalidad: {song_data.get('originality_score', 0):.2f}

{'='*50}

"""
        
        lyrics = song_data.get('lyrics', {})
        for section_name, section_content in lyrics.items():
            formatted += f"\n{section_name}\n"
            formatted += f"{section_content}\n"
        
        formatted += f"\n{'='*50}\n"
        formatted += f"Generado con Gemini AI | Modelo: {song_data.get('generation_metadata', {}).get('model', 'Unknown')}"
        
        return formatted