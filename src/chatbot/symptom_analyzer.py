import re
import spacy
from typing import List, Dict, Any
from textblob import TextBlob
from langdetect import detect

class SymptomAnalyzer:
    """Analizador de síntomas que extrae y categoriza síntomas del texto de entrada."""
    
    def __init__(self):
        # Intentar cargar el modelo de spaCy en español
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except OSError:
            print("Modelo spaCy 'es_core_news_sm' no encontrado. Usando procesamiento básico.")
            self.nlp = None
        
        # Diccionario de síntomas por categoría
        self.symptom_keywords = {
            'dolor': {
                'keywords': ['dolor', 'duele', 'doloroso', 'molestia', 'punzada', 'pinchazo', 
                           'quemazn', 'ardor', 'calambre', 'opresion', 'presion'],
                'severity_indicators': {
                    'severo': ['severo', 'intenso', 'fuerte', 'insoportable', 'terrible', 'agudo'],
                    'moderado': ['moderado', 'medio', 'regular', 'constante'],
                    'leve': ['leve', 'ligero', 'poco', 'suave']
                }
            },
            'respiratorio': {
                'keywords': ['respirar', 'respiro', 'aire', 'pecho', 'pulmon', 'tos', 'toser',
                           'ahogar', 'ahogo', 'falta', 'dificultad', 'jadeo', 'silbido'],
                'severity_indicators': {
                    'severo': ['no puedo', 'imposible', 'muy dificil', 'ahogo', 'asfixia'],
                    'moderado': ['dificil', 'cuesta', 'trabajo'],
                    'leve': ['poco', 'ligero', 'leve']
                }
            },
            'cardiovascular': {
                'keywords': ['corazon', 'palpitacion', 'latido', 'taquicardia', 'presion',
                           'sudor', 'sudoracion', 'mareo', 'mareado', 'desmayo'],
                'severity_indicators': {
                    'severo': ['muy rapido', 'descontrolado', 'irregular', 'fuerte'],
                    'moderado': ['rapido', 'acelerado', 'notable'],
                    'leve': ['ligero', 'poco', 'leve']
                }
            },
            'neurologico': {
                'keywords': ['cabeza', 'mareo', 'confusion', 'vision', 'hablar', 'brazo',
                           'pierna', 'entumecimiento', 'hormigueo', 'debilidad'],
                'severity_indicators': {
                    'severo': ['muy confuso', 'no puedo', 'perdida', 'total'],
                    'moderado': ['dificil', 'cuesta', 'parcial'],
                    'leve': ['ligero', 'poco', 'leve']
                }
            },
            'digestivo': {
                'keywords': ['nausea', 'vomito', 'diarrea', 'estomago', 'abdominal', 'barriga'],
                'severity_indicators': {
                    'severo': ['constante', 'no para', 'muy frecuente'],
                    'moderado': ['frecuente', 'varias veces'],
                    'leve': ['ocasional', 'poco', 'leve']
                }
            }
        }
        
        # Patrones de urgencia
        self.urgency_patterns = [
            r'\b(severo|intenso|fuerte|insoportable|terrible)\b',
            r'\b(no puedo|imposible|muy dificil)\b',
            r'\b(emergencia|urgente|inmediato)\b',
            r'\b(sangre|hemorragia|sangrando)\b'
        ]
    
    def extract_symptoms(self, text: str) -> List[Dict[str, Any]]:
        """Extrae síntomas del texto de entrada."""
        if not text or not text.strip():
            return []
        
        text = text.lower().strip()
        symptoms = []
        
        # Procesar cada categoría de síntomas
        for category, data in self.symptom_keywords.items():
            for keyword in data['keywords']:
                if keyword in text:
                    # Encontrar síntoma
                    symptom_info = {
                        'symptom': keyword,
                        'category': category,
                        'severity': self._assess_severity(text, keyword, data['severity_indicators']),
                        'urgency_level': self._analyze_urgency_level(text)
                    }
                    symptoms.append(symptom_info)
        
        # Eliminar duplicados
        unique_symptoms = []
        seen_symptoms = set()
        for symptom in symptoms:
            key = (symptom['symptom'], symptom['category'])
            if key not in seen_symptoms:
                seen_symptoms.add(key)
                unique_symptoms.append(symptom)
        
        return unique_symptoms
    
    def _assess_severity(self, text: str, symptom: str, severity_indicators: Dict) -> str:
        """Evalua la severidad de un síntoma."""
        # Buscar indicadores de severidad cerca del síntoma
        for severity, indicators in severity_indicators.items():
            for indicator in indicators:
                if indicator in text:
                    return severity
        
        # Severidad por defecto
        return 'moderado'
    
    def _analyze_urgency_level(self, text: str) -> int:
        """Analiza el nivel de urgencia basado en patrones de texto."""
        urgency_score = 0
        
        for pattern in self.urgency_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                urgency_score += 1
        
        # Convertir score a nivel (1-5, donde 1 es más urgente)
        if urgency_score >= 3:
            return 1  # Crítico
        elif urgency_score >= 2:
            return 2  # Urgente
        elif urgency_score >= 1:
            return 3  # Moderado
        else:
            return 4  # Menor
    
    def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analiza el sentimiento del texto para detectar ansiedad/dolor."""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Clasificar sentimiento
            if polarity < -0.3:
                sentiment = 'negativo'  # Puede indicar dolor/malestar
            elif polarity > 0.3:
                sentiment = 'positivo'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'anxiety_indicators': subjectivity > 0.7 and polarity < 0
            }
        except:
            return {
                'sentiment': 'unknown',
                'polarity': 0,
                'subjectivity': 0,
                'anxiety_indicators': False
            }