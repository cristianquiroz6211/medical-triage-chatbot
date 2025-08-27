from enum import Enum
from typing import List, Dict, Any
from dataclasses import dataclass

class TriageLevel(Enum):
    """Niveles de triaje según protocolo hospitalario estándar."""
    LEVEL_1 = (1, "Resucitación", "Rojo", "Inmediata", "Emergencia crítica, riesgo vital inmediato")
    LEVEL_2 = (2, "Emergencia", "Naranja", "10 minutos", "Urgencia alta, requiere atención prioritaria")
    LEVEL_3 = (3, "Urgencia", "Amarillo", "30 minutos", "Urgencia moderada")
    LEVEL_4 = (4, "Semi-urgente", "Verde", "60 minutos", "Urgencia menor, puede esperar")
    LEVEL_5 = (5, "No urgente", "Azul", "120 minutos", "Atención diferida, no urgente")
    
    def __init__(self, level, triage_name, color, max_wait, description):
        self.level = level
        self.triage_name = triage_name
        self.color = color
        self.max_wait = max_wait
        self.description = description

@dataclass
class TriageResult:
    """Resultado de la clasificación de triaje."""
    triage_level: int
    triage_name: str
    color: str
    max_wait_time: str
    description: str
    recommendation: str
    reasoning: List[str]
    vital_signs_required: bool

class TriageClassifier:
    """Clasificador de triaje médico basado en protocolos hospitalarios."""
    
    def __init__(self):
        # Criterios críticos para Nivel 1 (Resucitación)
        self.level_1_criteria = {
            'cardiovascular_critical': [
                'infarto', 'paro', 'cardíaco', 'chest pain severo', 
                'dolor pecho irradiado', 'sudoracion profusa'
            ],
            'respiratory_critical': [
                'no puedo respirar', 'asfixia', 'cianosis', 
                'dificultad respiratoria severa', 'ahogo'
            ],
            'neurological_critical': [
                'accidente cerebrovascular', 'ictus', 'convulsiones',
                'perdida conciencia', 'coma', 'confusion severa'
            ],
            'trauma_critical': [
                'hemorragia masiva', 'trauma craneal', 'politraumatismo',
                'fractura expuesta', 'quemaduras extensas'
            ]
        }
        
        # Criterios para Nivel 2 (Emergencia)
        self.level_2_criteria = {
            'respiratory': [
                'dificultad respirar', 'asma severa', 'neumonia',
                'tos con sangre', 'dolor pecho'
            ],
            'cardiovascular': [
                'palpitaciones severas', 'hipertension severa',
                'dolor precordial', 'taquicardia'
            ],
            'neurological': [
                'migraña severa', 'cefalea intensa', 'vision borrosa',
                'mareo severo', 'entumecimiento'
            ],
            'abdominal': [
                'dolor abdominal severo', 'apendicitis', 'obstruccion',
                'sangrado digestivo'
            ]
        }
        
        # Criterios para Nivel 3 (Urgencia)
        self.level_3_criteria = [
            'fiebre alta', 'dolor moderado', 'vomito persistente',
            'diarrea severa', 'infeccion', 'fractura simple'
        ]
        
        # Criterios para Nivel 4 (Semi-urgente)
        self.level_4_criteria = [
            'dolor leve', 'fiebre baja', 'tos', 'resfriado',
            'lesion menor', 'esguince'
        ]
    
    def classify_triage(self, symptoms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Clasifica el nivel de triaje basado en los síntomas."""
        if not symptoms:
            return self._create_triage_result(TriageLevel.LEVEL_5, 
                                            ["No se detectaron síntomas específicos"])
        
        # Extraer texto de síntomas para análisis
        symptom_text = ' '.join([s.get('symptom', '') for s in symptoms]).lower()
        severity_levels = [s.get('severity', 'leve') for s in symptoms]
        categories = [s.get('category', '') for s in symptoms]
        
        # Verificar criterios de Nivel 1 (Crítico)
        level_1_reasons = self._check_level_1_criteria(symptom_text, symptoms)
        if level_1_reasons:
            return self._create_triage_result(TriageLevel.LEVEL_1, level_1_reasons)
        
        # Verificar criterios de Nivel 2 (Emergencia)
        level_2_reasons = self._check_level_2_criteria(symptom_text, symptoms)
        if level_2_reasons:
            return self._create_triage_result(TriageLevel.LEVEL_2, level_2_reasons)
        
        # Verificar criterios de Nivel 3 (Urgencia)
        level_3_reasons = self._check_level_3_criteria(symptom_text, severity_levels)
        if level_3_reasons:
            return self._create_triage_result(TriageLevel.LEVEL_3, level_3_reasons)
        
        # Verificar criterios de Nivel 4 (Semi-urgente)
        level_4_reasons = self._check_level_4_criteria(symptom_text)
        if level_4_reasons:
            return self._create_triage_result(TriageLevel.LEVEL_4, level_4_reasons)
        
        # Por defecto, Nivel 5 (No urgente)
        return self._create_triage_result(TriageLevel.LEVEL_5, 
                                        ["Síntomas de severidad leve, no requiere atención inmediata"])
    
    def _check_level_1_criteria(self, symptom_text: str, symptoms: List[Dict]) -> List[str]:
        """Verifica criterios para Nivel 1 (Resucitación)."""
        reasons = []
        
        # Verificar cada categoría crítica
        for category, criteria in self.level_1_criteria.items():
            for criterion in criteria:
                if criterion.lower() in symptom_text:
                    reasons.append(f"Criterio crítico detectado: {criterion} ({category})")
        
        # Verificar combinaciones peligrosas
        dangerous_combinations = [
            (['dolor', 'pecho'], ['sudor', 'sudoracion']),
            (['dificultad', 'respirar'], ['dolor', 'pecho']),
            (['confusion'], ['debilidad']),
        ]
        
        for combo in dangerous_combinations:
            if (any(term in symptom_text for term in combo[0]) and 
                any(term in symptom_text for term in combo[1])):
                reasons.append(f"Combinación crítica: {' + '.join(combo[0] + combo[1])}")
        
        # Verificar severidad extrema
        severe_symptoms = [s for s in symptoms if s.get('severity') == 'severo']
        if len(severe_symptoms) >= 2:
            reasons.append("Múltiples síntomas severos detectados")
        
        return reasons
    
    def _check_level_2_criteria(self, symptom_text: str, symptoms: List[Dict]) -> List[str]:
        """Verifica criterios para Nivel 2 (Emergencia)."""
        reasons = []
        
        # Verificar criterios específicos de Nivel 2
        for category, criteria in self.level_2_criteria.items():
            for criterion in criteria:
                if criterion.lower() in symptom_text:
                    reasons.append(f"Criterio de emergencia: {criterion} ({category})")
        
        # Verificar síntomas severos en categorías importantes
        important_categories = ['cardiovascular', 'respiratorio', 'neurologico']
        for symptom in symptoms:
            if (symptom.get('category') in important_categories and 
                symptom.get('severity') == 'severo'):
                reasons.append(f"Síntoma severo en sistema {symptom.get('category')}")
        
        return reasons
    
    def _check_level_3_criteria(self, symptom_text: str, severity_levels: List[str]) -> List[str]:
        """Verifica criterios para Nivel 3 (Urgencia)."""
        reasons = []
        
        # Verificar criterios específicos
        for criterion in self.level_3_criteria:
            if criterion.lower() in symptom_text:
                reasons.append(f"Criterio de urgencia: {criterion}")
        
        # Verificar severidad moderada múltiple
        moderate_count = severity_levels.count('moderado')
        if moderate_count >= 2:
            reasons.append("Múltiples síntomas moderados")
        
        return reasons
    
    def _check_level_4_criteria(self, symptom_text: str) -> List[str]:
        """Verifica criterios para Nivel 4 (Semi-urgente)."""
        reasons = []
        
        for criterion in self.level_4_criteria:
            if criterion.lower() in symptom_text:
                reasons.append(f"Síntoma menor: {criterion}")
        
        return reasons
    
    def _create_triage_result(self, triage_level: TriageLevel, reasoning: List[str]) -> Dict[str, Any]:
        """Crea el resultado de triaje estructurado."""
        
        # Generar recomendaciones basadas en el nivel
        recommendations = {
            1: "ATENCIÓN INMEDIATA REQUERIDA. Traslado inmediato a sala de resucitación. Activar equipo de emergencias.",
            2: "Requiere atención médica urgente. Evaluar en los próximos 10 minutos. Monitorizar signos vitales.",
            3: "Atención médica necesaria. Evaluar dentro de 30 minutos. Realizar triage secundario.",
            4: "Atención médica recomendada. Puede esperar hasta 60 minutos. Monitoreo periódico.",
            5: "Consulta médica no urgente. Tiempo de espera hasta 120 minutos. Cuidados de soporte."
        }
        
        return {
            'triage_level': triage_level.level,
            'triage_name': triage_level.triage_name,
            'color': triage_level.color,
            'max_wait_time': triage_level.max_wait,
            'description': triage_level.description,
            'recommendation': recommendations[triage_level.level],
            'reasoning': reasoning,
            'vital_signs_required': triage_level.level <= 2,
            'immediate_interventions': self._get_immediate_interventions(triage_level.level)
        }
    
    def _get_immediate_interventions(self, level: int) -> List[str]:
        """Obtiene las intervenciones inmediatas según el nivel de triaje."""
        interventions = {
            1: [
                "Asegurar vía aérea",
                "Monitoreo cardíaco continuo",
                "Acceso venoso inmediato",
                "Oxígeno suplementario",
                "Preparar para RCP si es necesario"
            ],
            2: [
                "Monitoreo de signos vitales",
                "Acceso venoso",
                "Oxígeno si es necesario",
                "Evaluación médica rápida"
            ],
            3: [
                "Toma de signos vitales",
                "Historia clínica completa",
                "Exámenes complementarios si es necesario"
            ],
            4: [
                "Evaluación inicial",
                "Signos vitales básicos"
            ],
            5: [
                "Registro de información",
                "Educación al paciente"
            ]
        }
        
        return interventions.get(level, [])