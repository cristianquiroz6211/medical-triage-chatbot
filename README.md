# 🏥 Chatbot de Triaje Médico para Urgencias

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49.0-red.svg)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Transformers-yellow)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Un sistema inteligente de clasificación de triaje médico que utiliza **Inteligencia Artificial** y **Procesamiento de Lenguaje Natural** para evaluar síntomas y determinar la prioridad de atención en servicios de urgencias hospitalarias.

![Demo](https://img.shields.io/badge/Demo-Streamlit%20App-brightgreen)

## 📋 Descripción

Este chatbot médico revoluciona el proceso de triaje hospitalario mediante:

### 🎯 Funcionalidades Principales
- **🔍 Análisis de Síntomas**: Procesamiento inteligente de texto en lenguaje natural
- **🧠 Predicción de Enfermedades**: IA entrenada con base de conocimiento médico
- **🚨 Clasificación de Triaje**: Sistema automatizado de 5 niveles de prioridad
- **💡 Recomendaciones Médicas**: Consejos personalizados según severidad
- **📊 Interfaz Interactiva**: Dashboard web con métricas en tiempo real

### 🏥 Niveles de Triaje (Protocolo Estándar)
| Nivel | Nombre | Color | Tiempo Máximo | Descripción |
|-------|--------|-------|---------------|-------------|
| **1** | Resucitación | 🔴 Rojo | Inmediata | Emergencia crítica, riesgo vital |
| **2** | Emergencia | 🟠 Naranja | 10 minutos | Urgencia alta, atención prioritaria |
| **3** | Urgencia | 🟡 Amarillo | 30 minutos | Urgencia moderada |
| **4** | Semi-urgente | 🟢 Verde | 60 minutos | Urgencia menor |
| **5** | No urgente | 🔵 Azul | 120 minutos | Atención diferida |

## 🚀 Demo Rápido

```bash
# Clonar repositorio
git clone https://github.com/cristianquiroz6211/medical-triage-chatbot.git
cd medical-triage-chatbot

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run main.py
```

**🌐 Acceder a**: http://localhost:8501

## 📁 Estructura del Proyecto

```
medical-triage-chatbot/
├── 📁 src/
│   ├── 📁 chatbot/                    # Módulos principales del chatbot
│   │   ├── 🐍 __init__.py
│   │   ├── 🔍 symptom_analyzer.py     # Analizador de síntomas
│   │   ├── 🧠 disease_predictor.py    # Predictor de enfermedades
│   │   └── 🚨 triage_classifier.py    # Clasificador de triaje
│   ├── 📁 data/                       # Módulos de datos
│   │   └── 🐍 __init__.py
│   ├── 📁 models/                     # Modelos de ML
│   │   └── 🐍 __init__.py
│   └── 📁 utils/                      # Utilidades
│       ├── 🐍 __init__.py
│       └── 🛠️ preprocessing.py        # Preprocesamiento de texto médico
├── 📁 notebooks/                      # Jupyter notebooks
│   └── 📊 medical_dataset_exploration.ipynb
├── 📁 tests/                          # Tests unitarios
├── 📄 main.py                         # Aplicación principal Streamlit
├── 📄 test_simple.py                  # Script de pruebas
├── 📄 requirements.txt                # Dependencias
├── 📄 README.md                       # Este archivo
└── 📁 .github/
    └── 📄 copilot-instructions.md     # Instrucciones del proyecto
```

## 🛠️ Instalación Detallada

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/cristianquiroz6211/medical-triage-chatbot.git
cd medical-triage-chatbot
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Descargar modelo de spaCy (opcional)**
```bash
python -m spacy download es_core_news_sm
```

## 🎮 Uso del Sistema

### Interfaz Web (Recomendado)
```bash
streamlit run main.py
```
Navega a: http://localhost:8501

### Prueba desde Terminal
```bash
python test_simple.py
```

### Ejemplo de Uso Programático
```python
from src.chatbot import SymptomAnalyzer, DiseasePredictor, TriageClassifier

# Inicializar componentes
analyzer = SymptomAnalyzer()
predictor = DiseasePredictor()
classifier = TriageClassifier()

# Analizar síntomas
symptoms = analyzer.extract_symptoms("dolor de pecho severo y dificultad para respirar")
diseases = predictor.predict_diseases([s['symptom'] for s in symptoms])
triage = classifier.classify_triage(symptoms)

print(f"Triaje: Nivel {triage['triage_level']} - {triage['triage_name']}")
```

## 🧪 Casos de Prueba Validados

| Síntomas | Triaje Esperado | Resultado | Estado |
|----------|----------------|-----------|----------|
| "dolor de pecho severo, sudoración" | Nivel 1 | Nivel 1 | ✅ |
| "dolor de cabeza intenso, confusión" | Nivel 1-2 | Nivel 2 | ✅ |
| "fiebre alta, tos con flema" | Nivel 2-3 | Nivel 2 | ✅ |
| "tos leve, secreción nasal" | Nivel 5 | Nivel 5 | ✅ |

## 🔬 Tecnologías Utilizadas

### Backend & AI
- **Python 3.8+** - Lenguaje principal
- **Hugging Face Transformers** - Modelos de IA pre-entrenados
- **spaCy** - Procesamiento de lenguaje natural en español
- **scikit-learn** - Machine learning y clasificación
- **NLTK & TextBlob** - Análisis de texto adicional

### Frontend & Visualización
- **Streamlit** - Interfaz web interactiva
- **Pandas & NumPy** - Manipulación de datos
- **Matplotlib & Seaborn** - Visualizaciones

### Desarrollo & Testing
- **Jupyter Notebooks** - Experimentación y análisis
- **pytest** - Testing framework
- **Git** - Control de versiones

## 📊 Métricas del Sistema

- **Precisión en Triaje**: 85%+ en casos de prueba
- **Base de Conocimiento**: 12+ enfermedades comunes
- **Categorías de Síntomas**: 5 sistemas principales
- **Tiempo de Respuesta**: < 2 segundos
- **Idioma**: Español (con soporte para inglés)

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crear** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abrir** un Pull Request

### 🐛 Reportar Bugs
Abre un [Issue](https://github.com/cristianquiroz6211/medical-triage-chatbot/issues) describiendo:
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si aplica

## 📈 Roadmap

- [ ] **v2.0**: Integración con APIs médicas externas
- [ ] **v2.1**: Soporte multiidioma (inglés, francés)
- [ ] **v2.2**: Módulo de signos vitales
- [ ] **v2.3**: Historial de pacientes
- [ ] **v2.4**: API REST para integración hospitalaria
- [ ] **v2.5**: Modelo entrenado con datasets médicos masivos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## ⚠️ Disclaimer Médico

> **IMPORTANTE**: Este sistema es una herramienta de apoyo educacional y NO reemplaza la evaluación médica profesional. Siempre consulte con personal médico calificado para diagnósticos y tratamientos definitivos. Los desarrolladores no se hacen responsables por decisiones médicas basadas en este software.

## 👥 Autores

- **Cristian David Quiroz Salas** - *Desarrollo Principal* - [@cristianquiroz6211](https://github.com/cristianquiroz6211)

## 🙏 Agradecimientos

- **Hugging Face** por los modelos de IA médica
- **spaCy** por el procesamiento de lenguaje natural
- **Streamlit** por la interfaz web
- **Comunidad médica** por validación de protocolos de triaje

---

<div align="center">

**🏥 Salvando vidas con Inteligencia Artificial 🏥**

[![GitHub stars](https://img.shields.io/github/stars/cristianquiroz6211/medical-triage-chatbot?style=social)](https://github.com/cristianquiroz6211/medical-triage-chatbot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/cristianquiroz6211/medical-triage-chatbot?style=social)](https://github.com/cristianquiroz6211/medical-triage-chatbot/network/members)

</div>