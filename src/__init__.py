"""
Medical Triage Chatbot Package

A comprehensive medical triage system that uses AI and NLP to analyze symptoms,
predict diseases, and classify patient priority levels for emergency departments.

Modules:
- chatbot: Core chatbot functionality
- data: Data management and processing
- models: Machine learning models
- utils: Utility functions and helpers
"""

__version__ = "1.0.0"
__author__ = "Cristian David Quiroz Salas"
__email__ = "Cristian.quiroz6211@uco.net.co"

from .chatbot import SymptomAnalyzer, DiseasePredictor, TriageClassifier

__all__ = [
    'SymptomAnalyzer',
    'DiseasePredictor', 
    'TriageClassifier'
]