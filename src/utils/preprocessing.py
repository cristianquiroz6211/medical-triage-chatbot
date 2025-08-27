"""Preprocessing utilities for medical text data"""

import re
import string
from typing import List, Dict, Any
from textblob import TextBlob

class MedicalTextPreprocessor:
    """Preprocesador especializado para texto médico."""
    
    def __init__(self):
        # Abreviaciones médicas comunes
        self.medical_abbreviations = {
            'iam': 'infarto agudo miocardio',
            'avc': 'accidente cerebrovascular',
            'hta': 'hipertension arterial',
            'dm': 'diabetes mellitus',
            'epoc': 'enfermedad pulmonar obstructiva cronica',
            'itu': 'infeccion tracto urinario',
            'ira': 'insuficiencia renal aguda',
            'icc': 'insuficiencia cardiaca congestiva',
            'tce': 'traumatismo craneoencefalico',
            'pcr': 'paro cardiorespiratorio'
        }
        
        # Sinónimos médicos
        self.medical_synonyms = {
            'doler': 'dolor',
            'duele': 'dolor',
            'doloroso': 'dolor',
            'malestar': 'molestia',
            'respiracion': 'respirar',
            'palpitaciones': 'palpitacion',
            'nauseas': 'nausea',
            'vomitos': 'vomito',
            'cefalea': 'dolor cabeza',
            'migrana': 'dolor cabeza',
            'taquicardia': 'corazon rapido',
            'bradicardia': 'corazon lento'
        }
        
        # Patrones de limpieza
        self.cleaning_patterns = [
            (r'[^\w\sáéíóúñü]', ' '),  # Caracteres especiales
            (r'\d+', ' '),  # Números
            (r'\s+', ' '),  # Espacios múltiples
        ]
    
    def clean_text(self, text: str) -> str:
        """Limpia y normaliza texto médico."""
        if not text:
            return ""
        
        # Convertir a minúsculas
        text = text.lower().strip()
        
        # Expandir abreviaciones
        text = self._expand_abbreviations(text)
        
        # Normalizar sinónimos
        text = self._normalize_synonyms(text)
        
        # Aplicar patrones de limpieza
        for pattern, replacement in self.cleaning_patterns:
            text = re.sub(pattern, replacement, text)
        
        # Limpiar espacios
        text = ' '.join(text.split())
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expande abreviaciones médicas."""
        words = text.split()
        expanded_words = []
        
        for word in words:
            # Buscar abreviación
            if word in self.medical_abbreviations:
                expanded_words.append(self.medical_abbreviations[word])
            else:
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
    
    def _normalize_synonyms(self, text: str) -> str:
        """Normaliza sinónimos médicos."""
        for synonym, standard in self.medical_synonyms.items():
            text = text.replace(synonym, standard)
        
        return text
    
    def extract_medical_entities(self, text: str) -> Dict[str, List[str]]:
        """Extrae entidades médicas del texto."""
        entities = {
            'symptoms': [],
            'body_parts': [],
            'severity': [],
            'temporal': []
        }
        
        # Listas de entidades médicas
        symptom_words = [
            'dolor', 'nausea', 'vomito', 'fiebre', 'tos', 'mareo', 
            'palpitacion', 'dificultad', 'sangrado', 'inflamacion'
        ]
        
        body_parts = [
            'cabeza', 'pecho', 'abdomen', 'brazo', 'pierna', 'espalda',
            'corazon', 'pulmon', 'estomago', 'garganta'
        ]
        
        severity_words = [
            'severo', 'intenso', 'leve', 'moderado', 'agudo', 'cronico'
        ]
        
        temporal_words = [
            'repentino', 'gradual', 'constante', 'intermitente', 
            'hace', 'desde', 'durante'
        ]
        
        # Extraer entidades
        words = text.lower().split()
        
        for word in words:
            if any(symptom in word for symptom in symptom_words):
                entities['symptoms'].append(word)
            elif any(part in word for part in body_parts):
                entities['body_parts'].append(word)
            elif any(sev in word for sev in severity_words):
                entities['severity'].append(word)
            elif any(temp in word for temp in temporal_words):
                entities['temporal'].append(word)
        
        # Eliminar duplicados
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def tokenize_medical_text(self, text: str) -> List[str]:
        """Tokeniza texto médico preservando términos importantes."""
        # Limpiar texto
        cleaned_text = self.clean_text(text)
        
        # Tokenizar manteniendo frases médicas importantes
        medical_phrases = [
            'dolor de pecho', 'dificultad para respirar', 
            'perdida de conciencia', 'dolor de cabeza',
            'falta de aire', 'palpitaciones cardiacas'
        ]
        
        # Proteger frases médicas
        for i, phrase in enumerate(medical_phrases):
            placeholder = f"MEDICAL_PHRASE_{i}"
            cleaned_text = cleaned_text.replace(phrase, placeholder)
        
        # Tokenizar
        tokens = cleaned_text.split()
        
        # Restaurar frases médicas
        final_tokens = []
        for token in tokens:
            if token.startswith('MEDICAL_PHRASE_'):
                phrase_index = int(token.split('_')[-1])
                final_tokens.append(medical_phrases[phrase_index])
            else:
                final_tokens.append(token)
        
        return final_tokens
    
    def correct_medical_spelling(self, text: str) -> str:
        """Corrige errores ortográficos comunes en texto médico."""
        # Correcciones comunes
        corrections = {
            'doler': 'dolor',
            'respiracion': 'respirar',
            'coracon': 'corazon',
            'pulomes': 'pulmones',
            'estomago': 'estomago',
            'caveza': 'cabeza',
            'mareos': 'mareo'
        }
        
        corrected_text = text.lower()
        for error, correction in corrections.items():
            corrected_text = corrected_text.replace(error, correction)
        
        return corrected_text
    
    def analyze_text_complexity(self, text: str) -> Dict[str, Any]:
        """Analiza la complejidad del texto médico."""
        if not text:
            return {'complexity': 'low', 'word_count': 0, 'sentence_count': 0}
        
        blob = TextBlob(text)
        
        word_count = len(blob.words)
        sentence_count = len(blob.sentences)
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        
        # Determinar complejidad
        if avg_words_per_sentence > 15 or word_count > 50:
            complexity = 'high'
        elif avg_words_per_sentence > 8 or word_count > 20:
            complexity = 'medium'
        else:
            complexity = 'low'
        
        return {
            'complexity': complexity,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'medical_terms_count': self._count_medical_terms(text)
        }
    
    def _count_medical_terms(self, text: str) -> int:
        """Cuenta términos médicos en el texto."""
        medical_terms = list(self.medical_abbreviations.keys()) + list(self.medical_synonyms.keys())
        
        count = 0
        text_lower = text.lower()
        
        for term in medical_terms:
            if term in text_lower:
                count += 1
        
        return count