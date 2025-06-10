# predictive.py
import joblib
import numpy as np
import streamlit as st

class DiseasePredictor:
    def __init__(self):
        """Load pre-trained disease risk models"""
        self.models = {
            'anemia': self._load_model('anemia_model.pkl'),
            'diabetes': self._load_model('diabetes_model.pkl')
        }
        self.feature_mapping = {
            'anemia': ['Hemoglobin', 'RBC', 'MCV'],
            'diabetes': ['Glucose', 'HbA1c', 'BMI']
        }

    def _load_model(self, model_path):
        try:
            return joblib.load(f'models/{model_path}')
        except Exception as e:
            st.error(f"Error loading model {model_path}: {str(e)}")
            return None

    def _get_features(self, metrics, disease):
        """Extract and normalize features for prediction"""
        return np.array([
            metrics.get(feature, 0)  # 0 as default if feature missing
            for feature in self.feature_mapping[disease]
        ]).reshape(1, -1)

    def predict_risk(self, metrics):
        """Generate disease risk predictions from medical metrics"""
        predictions = {}
        
        # Anemia prediction
        if self.models['anemia']:
            anemia_features = self._get_features(metrics, 'anemia')
            anemia_prob = self.models['anemia'].predict_proba(anemia_features)[0][1]
            predictions['anemia'] = {
                'probability': float(anemia_prob),
                'advice': self._get_anemia_advice(anemia_prob, metrics)
            }
        
        # Add other disease predictions using same pattern
        return predictions

    def _get_anemia_advice(self, probability, metrics):
        """Generate clinical advice based on anemia risk"""
        hb = metrics.get('Hemoglobin', 0)
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

# Example usage in Streamlit app:
# if 'report_data' in st.session_state:
#     predictor = DiseasePredictor()
#     risks = predictor.predict_risk(st.session_state.report_data)
#     
#     st.subheader("🩺 Disease Risk Assessment")
#     if 'anemia' in risks:
#         st.progress(risks['anemia']['probability'])
#         st.caption(risks['anemia']['advice'])
