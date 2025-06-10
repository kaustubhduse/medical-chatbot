# predictive.py
import joblib
import numpy as np
import streamlit as st
import os

class DiseasePredictor:
    def __init__(self):
        """Load pre-trained disease risk models"""
        self.model_dir = "models"
        self.models = {
            'anemia': self._load_model('anemia_model.pkl'),
            'diabetes': self._load_model('diabetes_model.pkl')
        }
        self.feature_mapping = {
            'anemia': ['Hemoglobin', 'RBC', 'MCV'],
            'diabetes': ['Glucose', 'HbA1c', 'BMI']
        }

    def _load_model(self, model_filename):
        """Load model with proper path handling and error reporting"""
        model_path = os.path.join(self.model_dir, model_filename)
        try:
            return joblib.load(model_path)
        except Exception as e:
            st.error(f"Error loading model {model_path}: {str(e)}")
            st.info("Ensure model files exist in 'models/' directory")
            return None

    def _get_features(self, metrics, disease):
        """Case-insensitive feature extraction with numeric validation"""
        # Convert metrics to lowercase keys for case-insensitive matching
        metrics_lower = {k.lower(): v for k, v in metrics.items()}
        features = []
        
        for feature in self.feature_mapping[disease]:
            # Get value with case-insensitive match
            value = metrics_lower.get(feature.lower(), 0)
            
            # Ensure numeric value
            try:
                features.append(float(value))
            except (ValueError, TypeError):
                features.append(0.0)  # Use default value if conversion fails
                
        return np.array(features).reshape(1, -1)

    def predict_risk(self, metrics):
        """Generate disease risk predictions with error handling"""
        predictions = {}
        
        # Anemia prediction
        if self.models['anemia'] is not None:
            try:
                anemia_features = self._get_features(metrics, 'anemia')
                anemia_prob = self.models['anemia'].predict_proba(anemia_features)[0][1]
                predictions['anemia'] = {
                    'probability': anemia_prob,
                    'advice': self._get_anemia_advice(anemia_prob, metrics)
                }
            except Exception as e:
                st.error(f"Anemia prediction failed: {str(e)}")
        
        # Add other disease predictions using the same pattern
        return predictions

    def _get_anemia_advice(self, probability, metrics):
        """Generate clinical advice with numeric validation"""
        try:
            hb = float(metrics.get('Hemoglobin', 0))
        except (ValueError, TypeError):
            hb = 0.0

        advice = []
        if probability > 0.7:
            advice.append("🔴 High anemia risk - Consult hematologist immediately")
            if hb < 8:
                advice.append("Consider urgent blood transfusion evaluation")
        elif probability > 0.4:
            advice.append("🟡 Moderate anemia risk - Recommend:")
            advice.append("- Iron studies (serum ferritin, TIBC)")
            advice.append("- Nutritional assessment")
        else:
            advice.append("🟢 Low anemia risk - Maintain iron-rich diet")

        if hb < 11:
            advice.append(f"Current hemoglobin ({hb} g/dL) below recommended threshold")

        return "\n".join(advice)
