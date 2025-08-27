import random
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DiseasePredictor:
    """Predictor de enfermedades basado en síntomas."""
    
    def __init__(self):
        # Base de conocimiento médico simplificada
        self.medical_knowledge = {
            'infarto_agudo_miocardio': {
                'symptoms': ['dolor', 'pecho', 'respirar', 'sudor', 'nausea', 'brazo'],
                'severity': 'critico',
                'description': 'Ataque cardíaco - bloqueo del flujo sanguíneo al corazón',
                'recommendations': [
                    'Llamar inmediatamente al 911',
                    'Administrar aspirina si no hay alergias',
                    'Mantener al paciente en reposo',
                    'Monitorizar signos vitales'
                ]
            },
            'asma_bronquial': {
                'symptoms': ['respirar', 'tos', 'pecho', 'silbido', 'aire'],
                'severity': 'moderado',
                'description': 'Inflamación y estrechamiento de las vías respiratorias',
                'recommendations': [
                    'Usar inhalador de rescate',
                    'Mantener posición sentado',
                    'Evitar desencadenantes conocidos'
                ]
            },
            'neumonia': {
                'symptoms': ['tos', 'respirar', 'pecho', 'fiebre', 'escalofrios'],
                'severity': 'moderado_alto',
                'description': 'Infección pulmonar que inflama los sacos de aire',
                'recommendations': [
                    'Antibióticos según prescripción',
                    'Reposo en cama',
                    'Hidratación abundante'
                ]
            },
            'migrana': {
                'symptoms': ['cabeza', 'vision', 'nausea', 'luz', 'ruido'],
                'severity': 'moderado',
                'description': 'Dolor de cabeza intenso con síntomas neurológicos',
                'recommendations': [
                    'Medicamentos para migraña',
                    'Reposo en lugar oscuro',
                    'Aplicar compresas frías'
                ]
            },
            'accidente_cerebrovascular': {
                'symptoms': ['confusion', 'hablar', 'brazo', 'pierna', 'vision', 'mareo'],
                'severity': 'critico',
                'description': 'Interrupción del flujo sanguíneo al cerebro',
                'recommendations': [
                    'Activar código ictus inmediatamente',
                    'No dar medicamentos orales',
                    'Evaluar escala NIHSS'
                ]
            },
            'gastroenteritis': {
                'symptoms': ['nausea', 'vomito', 'diarrea', 'estomago', 'deshidratacion'],
                'severity': 'leve_moderado',
                'description': 'Inflamación del tracto gastrointestinal',
                'recommendations': [
                    'Hidratación oral gradual',
                    'Dieta blanda',
                    'Evitar lácteos temporalmente'
                ]
            },
            'apendicitis': {
                'symptoms': ['dolor', 'abdominal', 'nausea', 'vomito', 'fiebre'],
                'severity': 'alto',
                'description': 'Inflamación del apéndice',
                'recommendations': [
                    'Evaluación quirúrgica urgente',
                    'No administrar analgésicos hasta diagnóstico',
                    'Mantener en ayunas'
                ]
            },
            'hipertension_arterial': {
                'symptoms': ['cabeza', 'mareo', 'vision', 'palpitacion'],
                'severity': 'moderado',
                'description': 'Presión arterial elevada',
                'recommendations': [
                    'Monitorizar presión arterial',
                    'Medicación antihipertensiva',
                    'Reposo relativo'
                ]
            },
            'diabetes_descompensada': {
                'symptoms': ['sed', 'orina', 'debilidad', 'confusion', 'nausea'],
                'severity': 'alto',
                'description': 'Descontrol de los niveles de glucosa',
                'recommendations': [
                    'Medir glucemia inmediatamente',
                    'Insulina según protocolo',
                    'Hidratación controlada'
                ]
            },
            'ansiedad_crisis': {
                'symptoms': ['palpitacion', 'respirar', 'sudor', 'mareo', 'miedo'],
                'severity': 'leve_moderado',
                'description': 'Episodio agudo de ansiedad',
                'recommendations': [
                    'Técnicas de respiración',
                    'Ambiente tranquilo',
                    'Apoyo emocional'
                ]
            },
            'resfriado_comun': {
                'symptoms': ['tos', 'secrecion', 'estornudos', 'garganta'],
                'severity': 'leve',
                'description': 'Infección viral de vías respiratorias superiores',
                'recommendations': [
                    'Reposo',
                    'Hidratación abundante',
                    'Analgésicos si es necesario'
                ]
            },
            'intoxicacion_alimentaria': {
                'symptoms': ['nausea', 'vomito', 'diarrea', 'estomago', 'fiebre'],
                'severity': 'moderado',
                'description': 'Enfermedad causada por alimentos contaminados',
                'recommendations': [
                    'Hidratación oral',
                    'Dieta líquida inicial',
                    'Evitar antidiarreicos'
                ]
            }
        }
        
        # Inicializar vectorizador TF-IDF
        self.vectorizer = TfidfVectorizer()
        self._prepare_disease_vectors()
    
    def _prepare_disease_vectors(self):
        """Prepara vectores TF-IDF para las enfermedades."""
        disease_texts = []
        self.disease_names = []
        
        for disease, info in self.medical_knowledge.items():
            # Crear texto combinando síntomas y descripción
            text = ' '.join(info['symptoms']) + ' ' + info['description']
            disease_texts.append(text)
            self.disease_names.append(disease)
        
        # Entrenar vectorizador
        self.disease_vectors = self.vectorizer.fit_transform(disease_texts)
    
    def predict_diseases(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """Predice posibles enfermedades basadas en los síntomas."""
        if not symptoms:
            return []
        
        # Crear texto de consulta con los síntomas
        query_text = ' '.join(symptoms)
        query_vector = self.vectorizer.transform([query_text])
        
        # Calcular similitudes
        similarities = cosine_similarity(query_vector, self.disease_vectors)[0]
        
        # Crear lista de predicciones
        predictions = []
        for i, disease in enumerate(self.disease_names):
            confidence = similarities[i]
            
            # Solo incluir si la confianza es mayor a un umbral
            if confidence > 0.1:  # Umbral mínimo
                disease_info = self.medical_knowledge[disease].copy()
                prediction = {
                    'disease': disease.replace('_', ' ').title(),
                    'confidence': confidence,
                    'severity': disease_info['severity'],
                    'description': disease_info['description'],
                    'recommendations': disease_info['recommendations'],
                    'matching_symptoms': self._get_matching_symptoms(symptoms, disease_info['symptoms'])
                }
                predictions.append(prediction)
        
        # Ordenar por confianza descendente
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Añadir factores de ajuste basados en severidad de síntomas
        predictions = self._adjust_predictions(predictions, symptoms)
        
        return predictions[:5]  # Retornar top 5
    
    def _get_matching_symptoms(self, patient_symptoms: List[str], disease_symptoms: List[str]) -> List[str]:
        """Obtiene los síntomas que coinciden entre el paciente y la enfermedad."""
        matching = []
        for p_symptom in patient_symptoms:
            for d_symptom in disease_symptoms:
                if d_symptom in p_symptom or p_symptom in d_symptom:
                    matching.append(d_symptom)
                    break
        return list(set(matching))
    
    def _adjust_predictions(self, predictions: List[Dict], symptoms: List[str]) -> List[Dict]:
        """Ajusta las predicciones basado en la severidad de los síntomas."""
        # Palabras clave que indican severidad alta
        high_severity_keywords = ['severo', 'intenso', 'agudo', 'insoportable', 'crítico']
        
        has_severe_symptoms = any(
            keyword in ' '.join(symptoms).lower() 
            for keyword in high_severity_keywords
        )
        
        for prediction in predictions:
            # Aumentar confianza para enfermedades críticas si hay síntomas severos
            if has_severe_symptoms and prediction['severity'] in ['critico', 'alto']:
                prediction['confidence'] = min(prediction['confidence'] * 1.3, 1.0)
            
            # Calcular score de confianza más comprensible
            prediction['confidence_score'] = self.calculate_confidence_score(
                prediction['confidence'], 
                len(prediction['matching_symptoms'])
            )
        
        # Re-ordenar después de los ajustes
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return predictions
    
    def calculate_confidence_score(self, raw_confidence: float, matching_symptoms_count: int) -> float:
        """Calcula un score de confianza más interpretable."""
        # Normalizar basado en similitud y número de síntomas coincidentes
        symptom_factor = min(matching_symptoms_count / 3, 1.0)  # Máximo factor de 1.0
        
        # Combinar factores
        final_score = (raw_confidence * 0.7) + (symptom_factor * 0.3)
        
        return min(final_score, 1.0)
    
    def generate_medical_advice(self, top_predictions: List[Dict]) -> str:
        """Genera consejos médicos basados en las predicciones principales."""
        if not top_predictions:
            return "No se pueden generar recomendaciones específicas. Consulte con un profesional médico."
        
        top_prediction = top_predictions[0]
        advice = f"Basado en los síntomas, la condición más probable es: {top_prediction['disease']}\n\n"
        advice += f"Descripción: {top_prediction['description']}\n\n"
        advice += "Recomendaciones inmediatas:\n"
        
        for i, recommendation in enumerate(top_prediction['recommendations'], 1):
            advice += f"{i}. {recommendation}\n"
        
        advice += "\n⚠️ IMPORTANTE: Estas son recomendaciones generales. Siempre consulte con un profesional médico para un diagnóstico y tratamiento adecuados."
        
        return advice