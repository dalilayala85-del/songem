import re
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from collections import Counter, defaultdict
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import spacy

# Cargar modelos de lenguaje
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Descargando modelo de spaCy...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class StyleAnalyzer:
    """Analiza el estilo lírico de un artista basado en sus canciones"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_rhyme_patterns(self, lyrics: str) -> Dict:
        """Analiza patrones de rima en las letras"""
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        rhymes = defaultdict(list)
        
        for i, line in enumerate(lines):
            words = word_tokenize(line.lower())
            # Obtener la última palabra de cada línea que no sea stop word
            last_words = [w for w in words if w.isalpha() and w not in self.stop_words]
            
            if last_words:
                last_word = last_words[-1]
                # Encontrar palabras que riman (similitud fonética simple)
                rhyme_key = self._get_rhyme_key(last_word)
                rhymes[rhyme_key].append((i, line, last_word))
        
        # Analizar esquemas de rima
        rhyme_schemes = self._detect_rhyme_schemes(rhymes, len(lines))
        
        return {
            'total_lines': len(lines),
            'rhyme_groups': dict(rhymes),
            'rhyme_density': len([g for g in rhymes.values() if len(g) > 1]) / max(len(rhymes), 1),
            'common_rhyme_schemes': rhyme_schemes[:5]
        }
    
    def _get_rhyme_key(self, word: str) -> str:
        """Obtiene una clave simple para identificar rimas"""
        # Extraer los últimos 2-3 caracteres y eliminar consonantes mudas
        word = word.lower()
        if len(word) >= 3:
            return word[-2:] if word[-1] in 'aeiou' else word[-3:]
        return word
    
    def _detect_rhyme_schemes(self, rhymes: Dict, total_lines: int) -> List[str]:
        """Detecta esquemas de rima comunes"""
        schemes = []
        
        for rhyme_key, rhyme_lines in rhymes.items():
            if len(rhyme_lines) >= 2:
                # Crear esquema basado en las posiciones
                positions = [line[0] for line in rhyme_lines]
                if len(positions) == 2:
                    if positions[1] - positions[0] == 1:
                        schemes.append("AABB")
                    elif positions[1] - positions[0] == 2:
                        schemes.append("ABAB")
                elif len(positions) >= 4:
                    schemes.append("AAAA")
        
        # Contar frecuencia de esquemas
        scheme_counts = Counter(schemes)
        return [f"{scheme} ({count} veces)" for scheme, count in scheme_counts.most_common()]
    
    def analyze_vocabulary(self, songs: List[Dict]) -> Dict:
        """Analiza el vocabulario del artista"""
        all_words = []
        all_unique_words = set()
        
        for song in songs:
            words = word_tokenize(song['lyrics'].lower())
            words = [w for w in words if w.isalpha() and w not in self.stop_words]
            all_words.extend(words)
            all_unique_words.update(words)
        
        word_freq = Counter(all_words)
        
        # Analizar complejidad del vocabulario
        avg_word_length = sum(len(word) for word in all_unique_words) / len(all_unique_words)
        rare_words = [word for word, freq in word_freq.items() if freq == 1]
        
        return {
            'total_words': len(all_words),
            'unique_words': len(all_unique_words),
            'vocabulary_richness': len(all_unique_words) / len(all_words),
            'most_common_words': word_freq.most_common(20),
            'avg_word_length': avg_word_length,
            'rare_words_count': len(rare_words),
            'rare_words_sample': rare_words[:20]
        }
    
    def analyze_sentiment_and_themes(self, songs: List[Dict]) -> Dict:
        """Analiza sentimientos y temas recurrentes"""
        sentiments = []
        all_lyrics = ""
        
        for song in songs:
            lyrics = song['lyrics']
            all_lyrics += lyrics + " "
            
            # Análisis de sentimiento con NLTK
            sentiment_scores = self.sia.polarity_scores(lyrics)
            sentiments.append(sentiment_scores)
        
        # Sentimiento promedio
        avg_sentiment = {
            'compound': sum(s['compound'] for s in sentiments) / len(sentiments),
            'positive': sum(s['pos'] for s in sentiments) / len(sentiments),
            'negative': sum(s['neg'] for s in sentiments) / len(sentiments),
            'neutral': sum(s['neu'] for s in sentiments) / len(sentiments)
        }
        
        # Detectar temas usando análisis de palabras clave
        themes = self._detect_themes(all_lyrics)
        
        return {
            'average_sentiment': avg_sentiment,
            'sentiment_distribution': self._categorize_sentiments(sentiments),
            'dominant_themes': themes,
            'emotional_range': {
                'most_positive': max(songs, key=lambda x: self.sia.polarity_scores(x['lyrics'])['compound'])['title'],
                'most_negative': min(songs, key=lambda x: self.sia.polarity_scores(x['lyrics'])['compound'])['title']
            }
        }
    
    def _detect_themes(self, lyrics: str) -> List[Dict]:
        """Detecta temas recurrentes en las letras"""
        # Palabras clave por tema
        theme_keywords = {
            'love': ['love', 'heart', 'kiss', 'romance', 'baby', 'darling', 'sweet', 'forever', 'together'],
            'heartbreak': ['break', 'pain', 'cry', 'tears', 'goodbye', 'alone', 'hurt', 'sad', 'miss'],
            'party': ['party', 'dance', 'club', 'night', 'music', 'drink', 'fun', 'celebrate', 'tonight'],
            'success': ['money', 'fame', 'win', 'success', 'top', 'king', 'queen', 'power', 'rich'],
            'struggle': ['fight', 'struggle', 'hard', 'difficult', 'battle', 'war', 'challenge', 'overcome'],
            'nature': ['sky', 'sun', 'moon', 'stars', 'rain', 'ocean', 'mountain', 'flower', 'tree'],
            'urban': ['city', 'street', 'town', 'building', 'lights', 'traffic', 'downtown', 'neighborhood']
        }
        
        lyrics_lower = lyrics.lower()
        theme_scores = {}
        
        for theme, keywords in theme_keywords.items():
            score = sum(lyrics_lower.count(keyword) for keyword in keywords)
            if score > 0:
                theme_scores[theme] = score
        
        # Normalizar y ordenar por relevancia
        total_themes = sum(theme_scores.values()) if theme_scores else 1
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [{'theme': theme, 'score': score, 'percentage': (score/total_themes)*100} 
                for theme, score in sorted_themes[:10]]
    
    def _categorize_sentiments(self, sentiments: List[Dict]) -> Dict:
        """Categoriza las canciones por sentimiento"""
        categories = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for sentiment in sentiments:
            compound = sentiment['compound']
            if compound >= 0.05:
                categories['positive'] += 1
            elif compound <= -0.05:
                categories['negative'] += 1
            else:
                categories['neutral'] += 1
        
        total = sum(categories.values())
        return {k: {'count': v, 'percentage': (v/total)*100} for k, v in categories.items()}
    
    def analyze_structure_patterns(self, songs: List[Dict]) -> Dict:
        """Analiza patrones estructurales de las canciones"""
        structures = []
        verse_lengths = []
        chorus_lengths = []
        
        for song in songs:
            lyrics = song['lyrics']
            structure = self._detect_song_structure(lyrics)
            structures.append(structure)
            
            # Analizar longitudes de versos y coros
            verse_lens, chorus_lens = self._analyze_section_lengths(lyrics)
            verse_lengths.extend(verse_lens)
            chorus_lengths.extend(chorus_lens)
        
        # Contar estructuras más comunes
        structure_counts = Counter(structures)
        
        return {
            'common_structures': [{'structure': s, 'frequency': f} for s, f in structure_counts.most_common(5)],
            'avg_verse_length': sum(verse_lengths) / len(verse_lengths) if verse_lengths else 0,
            'avg_chorus_length': sum(chorus_lengths) / len(chorus_lengths) if chorus_lengths else 0,
            'structure_diversity': len(structure_counts) / len(songs) if songs else 0
        }
    
    def _detect_song_structure(self, lyrics: str) -> str:
        """Detecta la estructura básica de una canción"""
        lines = lyrics.split('\n')
        has_chorus = any(line.strip() for line in lines if self._is_chorus_line(line))
        has_bridge = any('bridge' in line.lower() for line in lines)
        has_hook = any('hook' in line.lower() for line in lines)
        
        # Simplificación: detectar repeticiones para identificar coros
        line_counts = Counter(line.strip() for line in lines if line.strip())
        has_repetitions = any(count > 1 for count in line_counts.values())
        
        if has_repetitions:
            return "Verse-Chorus"
        elif has_bridge:
            return "Verse-Bridge"
        else:
            return "Verse-Only"
    
    def _is_chorus_line(self, line: str) -> bool:
        """Determina si una línea podría ser parte de un coro (heurística simple)"""
        # Coros suelen tener características específicas
        if not line.strip():
            return False
        
        words = word_tokenize(line.lower())
        # Coros suelen ser más cortos y repetitivos
        return len(words) >= 4 and len(words) <= 12
    
    def _analyze_section_lengths(self, lyrics: str) -> Tuple[List[int], List[int]]:
        """Analiza las longitudes de secciones de la canción"""
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        
        # Simplificación: dividir en secciones basadas en líneas vacías
        sections = []
        current_section = []
        
        for line in lines:
            if not line and current_section:
                sections.append(len(current_section))
                current_section = []
            else:
                current_section.append(line)
        
        if current_section:
            sections.append(len(current_section))
        
        # Heurística simple: secciones impares = versos, pares = coros
        verses = sections[::2]
        choruses = sections[1::2]
        
        return verses, choruses
    
    def generate_style_profile(self, artist_name: str, songs: List[Dict]) -> Dict:
        """Genera un perfil completo del estilo del artista"""
        if not songs:
            return {}
        
        print(f"Analizando estilo de {artist_name} con {len(songs)} canciones...")
        
        # Análisis completos
        vocab_analysis = self.analyze_vocabulary(songs)
        sentiment_analysis = self.analyze_sentiment_and_themes(songs)
        structure_analysis = self.analyze_structure_patterns(songs)
        
        # Análisis de rima (muestra para no sobrecargar)
        sample_lyrics = "\n".join(song['lyrics'] for song in songs[:5])
        rhyme_analysis = self.analyze_rhyme_patterns(sample_lyrics)
        
        # Crear perfil de estilo
        style_profile = {
            'artist_name': artist_name,
            'analysis_date': str(Path().cwd()),
            'total_songs_analyzed': len(songs),
            'vocabulary_profile': vocab_analysis,
            'sentiment_profile': sentiment_analysis,
            'structure_profile': structure_analysis,
            'rhyme_profile': rhyme_analysis,
            'writing_style_summary': self._generate_style_summary(
                vocab_analysis, sentiment_analysis, structure_analysis
            )
        }
        
        return style_profile
    
    def _generate_style_summary(self, vocab: Dict, sentiment: Dict, structure: Dict) -> str:
        """Genera un resumen del estilo de escritura"""
        summary_parts = []
        
        # Vocabulario
        richness = vocab.get('vocabulary_richness', 0)
        if richness > 0.5:
            summary_parts.append("vocabulario rico y diverso")
        elif richness > 0.3:
            summary_parts.append("vocabulario moderadamente diverso")
        else:
            summary_parts.append("vocabulario simple y directo")
        
        # Sentimiento
        avg_sent = sentiment.get('average_sentiment', {}).get('compound', 0)
        if avg_sent > 0.2:
            summary_parts.append("tendencia positiva y optimista")
        elif avg_sent < -0.2:
            summary_parts.append("tendencia melancólica y emotiva")
        else:
            summary_parts.append("balance emocional neutro")
        
        # Estructura
        common_struct = structure.get('common_structures', [{}])[0].get('structure', '')
        if 'Chorus' in common_struct:
            summary_parts.append("estructura convencional con coros memorables")
        else:
            summary_parts.append("estructura libre y experimental")
        
        return "El artista presenta un estilo con " + ", ".join(summary_parts) + "."
    
    def save_style_profile(self, profile: Dict, output_path: str):
        """Guarda el perfil de estilo en un archivo JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    
    def load_style_profile(self, profile_path: str) -> Optional[Dict]:
        """Carga un perfil de estilo desde un archivo"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None