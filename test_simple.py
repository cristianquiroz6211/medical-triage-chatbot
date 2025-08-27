"""Test script for medical triage chatbot functionality"""

from src.chatbot.symptom_analyzer import SymptomAnalyzer
from src.chatbot.disease_predictor import DiseasePredictor
from src.chatbot.triage_classifier import TriageClassifier

def test_medical_triage_system():
    """Prueba el sistema completo de triaje médico."""
    
    print("🏥 SISTEMA DE TRIAJE MÉDICO - PRUEBA")
    print("=" * 50)
    
    # Inicializar componentes
    print("🔧 Inicializando componentes del sistema...")
    analyzer = SymptomAnalyzer()
    predictor = DiseasePredictor()
    classifier = TriageClassifier()
    print("✅ Componentes inicializados correctamente\n")
    
    # Casos de prueba
    test_cases = [
        {
            'name': 'Caso Crítico - Infarto',
            'symptoms': 'dolor de pecho severo, dificultad para respirar, sudoración, nausea',
            'expected_triage': 1
        },
        {
            'name': 'Caso Urgente - Asma',
            'symptoms': 'dificultad para respirar, tos, silbido en el pecho',
            'expected_triage': 2
        },
        {
            'name': 'Caso Menor - Resfriado',
            'symptoms': 'tos leve, secreción nasal, dolor de garganta leve',
            'expected_triage': 5
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"🗺️ TEST CASE {i}: {case['name']}")
        print("-" * 40)
        print(f"Síntomas: {case['symptoms']}")
        
        # Análisis de síntomas
        symptoms = analyzer.extract_symptoms(case['symptoms'])
        print(f"\n🔍 Síntomas detectados: {len(symptoms)}")
        for symptom in symptoms:
            print(f"  - {symptom['symptom']} ({symptom['category']}, {symptom['severity']})")
        
        # Predicción de enfermedades
        diseases = predictor.predict_diseases([s['symptom'] for s in symptoms])
        print(f"\n🧠 Posibles enfermedades (Top 3):")
        for disease in diseases[:3]:
            confidence = disease['confidence'] * 100
            print(f"  - {disease['disease']}: {confidence:.1f}%")
        
        # Clasificación de triaje
        triage_result = classifier.classify_triage(symptoms)
        print(f"\n🚨 RESULTADO DE TRIAJE:")
        print(f"  Nivel: {triage_result['triage_level']} - {triage_result['triage_name']}")
        print(f"  Color: {triage_result['color']}")
        print(f"  Tiempo máximo: {triage_result['max_wait_time']}")
        print(f"  Recomendación: {triage_result['recommendation']}")
        
        # Verificar si coincide con lo esperado
        expected = case['expected_triage']
        actual = triage_result['triage_level']
        
        if actual == expected:
            print(f"\n✅ RESULTADO CORRECTO (Esperado: {expected}, Obtenido: {actual})")
        else:
            print(f"\n⚠️ RESULTADO DIFERENTE (Esperado: {expected}, Obtenido: {actual})")
        
        print("\n" + "=" * 50 + "\n")
    
    print("🎉 Pruebas completadas!")
    print("\n⚠️ DISCLAIMER: Este es un sistema de apoyo educacional.")
    print("Siempre consulte con personal médico calificado.")

if __name__ == "__main__":
    test_medical_triage_system()