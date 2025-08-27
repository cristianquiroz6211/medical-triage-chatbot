import streamlit as st
from src.chatbot.symptom_analyzer import SymptomAnalyzer
from src.chatbot.disease_predictor import DiseasePredictor
from src.chatbot.triage_classifier import TriageClassifier

class MedicalTriageChatbot:
    def __init__(self):
        self.analyzer = SymptomAnalyzer()
        self.predictor = DiseasePredictor()
        self.classifier = TriageClassifier()
    
    def process_patient_input(self, symptoms_text):
        # Análisis de síntomas
        symptoms = self.analyzer.extract_symptoms(symptoms_text)
        
        # Predicción de enfermedades
        diseases = self.predictor.predict_diseases([s['symptom'] for s in symptoms])
        
        # Clasificación de triaje
        triage_result = self.classifier.classify_triage(symptoms)
        
        return {
            'symptoms': symptoms,
            'diseases': diseases,
            'triage': triage_result
        }

def main():
    st.set_page_config(
        page_title="🏥 Chatbot de Triaje Médico",
        page_icon="🏥",
        layout="wide"
    )
    
    # Título principal
    st.title("🏥 Sistema de Triaje Médico Inteligente")
    st.markdown("---")
    
    # Disclaimer médico
    with st.expander("⚠️ DISCLAIMER MÉDICO - LEER ANTES DE USAR"):
        st.error("""
        **IMPORTANTE**: Este sistema es una herramienta de apoyo educacional y NO reemplaza 
        la evaluación médica profesional. Siempre consulte con personal médico calificado 
        para diagnósticos y tratamientos definitivos. Los desarrolladores no se hacen 
        responsables por decisiones médicas basadas en este software.
        """)
    
    # Inicializar chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner("Cargando sistema de IA médica..."):
            st.session_state.chatbot = MedicalTriageChatbot()
    
    # Columnas principales
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Evaluación de Síntomas")
        
        # Información del paciente
        st.subheader("Información del Paciente")
        nombre = st.text_input("Nombre del paciente (opcional)")
        edad = st.number_input("Edad", min_value=0, max_value=120, value=30)
        
        # Entrada de síntomas
        st.subheader("Descripción de Síntomas")
        symptoms_input = st.text_area(
            "Describa los síntomas que presenta:",
            placeholder="Ejemplo: dolor de pecho severo, dificultad para respirar, sudoración",
            height=100
        )
        
        # Botón de análisis
        if st.button("🔍 Analizar Síntomas", type="primary"):
            if symptoms_input.strip():
                with st.spinner("Analizando síntomas con IA..."):
                    try:
                        # Procesar entrada
                        result = st.session_state.chatbot.process_patient_input(symptoms_input)
                        
                        # Guardar resultado en session state
                        st.session_state.last_result = result
                        st.session_state.patient_name = nombre
                        st.session_state.patient_age = edad
                        
                        st.success("✅ Análisis completado")
                        
                    except Exception as e:
                        st.error(f"Error en el análisis: {str(e)}")
            else:
                st.warning("Por favor, ingrese una descripción de síntomas.")
    
    with col2:
        st.header("📊 Información del Sistema")
        
        # Métricas del sistema
        st.metric("Enfermedades en base", "12+")
        st.metric("Categorías de síntomas", "5")
        st.metric("Niveles de triaje", "5")
        
        # Niveles de triaje
        st.subheader("🚨 Niveles de Triaje")
        levels = [
            ("1", "🔴", "Resucitación", "Inmediata"),
            ("2", "🟠", "Emergencia", "10 min"),
            ("3", "🟡", "Urgencia", "30 min"),
            ("4", "🟢", "Semi-urgente", "60 min"),
            ("5", "🔵", "No urgente", "120 min")
        ]
        
        for level, color, name, time in levels:
            st.write(f"{color} **Nivel {level}**: {name} ({time})")
    
    # Mostrar resultados si existen
    if 'last_result' in st.session_state:
        st.markdown("---")
        st.header("📋 Resultados del Análisis")
        
        result = st.session_state.last_result
        
        # Información del paciente
        if st.session_state.patient_name:
            st.write(f"**Paciente**: {st.session_state.patient_name}")
        st.write(f"**Edad**: {st.session_state.patient_age} años")
        
        # Crear columnas para resultados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🔍 Síntomas Detectados")
            if result['symptoms']:
                for symptom in result['symptoms']:
                    severity_color = {
                        'leve': '🟢',
                        'moderado': '🟡', 
                        'severo': '🔴'
                    }.get(symptom['severity'], '⚪')
                    st.write(f"{severity_color} **{symptom['symptom']}**")
                    st.write(f"   Categoría: {symptom['category']}")
                    st.write(f"   Severidad: {symptom['severity']}")
            else:
                st.info("No se detectaron síntomas específicos")
        
        with col2:
            st.subheader("🧠 Posibles Enfermedades")
            if result['diseases']:
                for disease in result['diseases'][:5]:  # Top 5
                    confidence = disease['confidence'] * 100
                    st.write(f"**{disease['disease']}**")
                    st.progress(confidence / 100)
                    st.write(f"Confianza: {confidence:.1f}%")
                    st.write("---")
            else:
                st.info("No se pudieron identificar enfermedades específicas")
        
        with col3:
            st.subheader("🚨 Clasificación de Triaje")
            triage = result['triage']
            
            # Color según nivel
            level_colors = {
                1: "🔴",
                2: "🟠", 
                3: "🟡",
                4: "🟢",
                5: "🔵"
            }
            
            color = level_colors.get(triage['triage_level'], "⚪")
            
            st.markdown(f"""
            ### {color} Nivel {triage['triage_level']}
            **{triage['triage_name']}**
            
            **Tiempo máximo de espera**: {triage['max_wait_time']}
            
            **Recomendación**:
            {triage['recommendation']}
            """)
            
            # Alerta según severidad
            if triage['triage_level'] <= 2:
                st.error("⚠️ ATENCIÓN INMEDIATA REQUERIDA")
            elif triage['triage_level'] == 3:
                st.warning("⚠️ Atención prioritaria necesaria")
            else:
                st.info("ℹ️ Atención médica recomendada")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        🏥 Sistema de Triaje Médico Inteligente | 
        Desarrollado con ❤️ para salvar vidas | 
        Powered by AI & Machine Learning
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()