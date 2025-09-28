"""
Symptom checker service for intelligent medicine recommendations.
"""

from services.medicine_service import MedicineService
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.medicine import Symptom, PatientCondition, MedicineSymptom, MedicineContraindication
import re
import json

class SymptomChecker:
    """Service for symptom checking and medicine recommendations."""
    
    def __init__(self, database_url="sqlite:///data/medicines.db"):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.medicine_service = MedicineService(database_url)
    
    def get_recommendations(self, symptoms, conditions=None, age=None, gender=None, severity='moderate'):
        """Get medicine recommendations based on symptoms and patient conditions."""
        if not symptoms:
            return []
        
        # Get medicines that treat the symptoms
        medicines = self.medicine_service.search_medicines_by_symptoms(symptoms)
        
        if not medicines:
            return []
        
        # Score medicines based on effectiveness and safety
        scored_medicines = []
        
        for medicine in medicines:
            score = self._calculate_medicine_score(
                medicine, symptoms, conditions, age, gender, severity
            )
            
            if score > 0:  # Only include medicines with positive scores
                scored_medicines.append({
                    'medicine': medicine.to_dict(),
                    'score': score,
                    'effectiveness': self._get_effectiveness_for_symptoms(medicine, symptoms),
                    'safety_warnings': self._get_safety_warnings(medicine, conditions, age)
                })
        
        # Sort by score (highest first)
        scored_medicines.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_medicines[:10]  # Return top 10 recommendations
    
    def _calculate_medicine_score(self, medicine, symptoms, conditions, age, gender, severity):
        """Calculate overall score for a medicine."""
        score = 0.0
        
        # Base effectiveness score
        effectiveness = self._get_effectiveness_for_symptoms(medicine, symptoms)
        score += effectiveness * 0.6  # 60% weight for effectiveness
        
        # Safety score (higher is better)
        safety_score = self._calculate_safety_score(medicine, conditions, age)
        score += safety_score * 0.4  # 40% weight for safety
        
        # Adjust for severity
        if severity == 'mild':
            score *= 0.8  # Prefer milder medicines for mild symptoms
        elif severity == 'severe':
            score *= 1.2  # Prefer stronger medicines for severe symptoms
        
        return max(0, score)  # Ensure non-negative score
    
    def _get_effectiveness_for_symptoms(self, medicine, symptoms):
        """Get effectiveness score for medicine against given symptoms."""
        if not symptoms:
            return 0.0
        
        total_score = 0.0
        symptom_count = 0
        
        for symptom_name in symptoms:
            symptom = self.session.query(Symptom).filter(
                Symptom.name.ilike(f"%{symptom_name}%")
            ).first()
            
            if symptom:
                effectiveness = self.medicine_service.get_medicine_effectiveness(
                    medicine.id, symptom.id
                )
                total_score += effectiveness
                symptom_count += 1
        
        return total_score / symptom_count if symptom_count > 0 else 0.0
    
    def _calculate_safety_score(self, medicine, conditions, age):
        """Calculate safety score for a medicine."""
        safety_score = 1.0  # Start with perfect safety score
        
        # Check contraindications
        if conditions:
            for condition_name in conditions:
                condition = self.session.query(PatientCondition).filter(
                    PatientCondition.name.ilike(f"%{condition_name}%")
                ).first()
                
                if condition and self.medicine_service.is_medicine_contraindicated(medicine.id, condition.id):
                    contraindication = self.session.query(MedicineContraindication).filter(
                        and_(
                            MedicineContraindication.medicine_id == medicine.id,
                            MedicineContraindication.condition_id == condition.id
                        )
                    ).first()
                    
                    if contraindication:
                        if contraindication.severity == 'severe':
                            safety_score -= 1.0  # Completely unsafe
                        elif contraindication.severity == 'moderate':
                            safety_score -= 0.5  # Moderately unsafe
                        elif contraindication.severity == 'mild':
                            safety_score -= 0.2  # Slightly unsafe
        
        # Age-based adjustments
        if age:
            if age < 12:  # Pediatric
                if not medicine.pediatric_use:
                    safety_score -= 0.3
            elif age > 65:  # Geriatric
                if not medicine.geriatric_use:
                    safety_score -= 0.2
        
        # Pregnancy safety
        if medicine.pregnancy_category == 'X':
            safety_score -= 0.8  # Very unsafe during pregnancy
        elif medicine.pregnancy_category == 'D':
            safety_score -= 0.5  # Unsafe during pregnancy
        elif medicine.pregnancy_category == 'C':
            safety_score -= 0.2  # Use with caution during pregnancy
        
        return max(0, safety_score)  # Ensure non-negative score
    
    def _get_safety_warnings(self, medicine, conditions, age):
        """Get safety warnings for a medicine."""
        warnings = []
        
        # Pregnancy warnings
        if medicine.pregnancy_category == 'X':
            warnings.append("DO NOT USE during pregnancy - may cause birth defects")
        elif medicine.pregnancy_category == 'D':
            warnings.append("Avoid during pregnancy - may cause harm to fetus")
        elif medicine.pregnancy_category == 'C':
            warnings.append("Use with caution during pregnancy - consult doctor")
        
        # Age warnings
        if age and age < 12:
            if not medicine.pediatric_use:
                warnings.append("Not recommended for children under 12")
        elif age and age > 65:
            if not medicine.geriatric_use:
                warnings.append("Use with caution in elderly patients")
        
        # Condition-specific warnings
        if conditions:
            for condition_name in conditions:
                condition = self.session.query(PatientCondition).filter(
                    PatientCondition.name.ilike(f"%{condition_name}%")
                ).first()
                
                if condition and self.medicine_service.is_medicine_contraindicated(medicine.id, condition.id):
                    contraindication = self.session.query(MedicineContraindication).filter(
                        and_(
                            MedicineContraindication.medicine_id == medicine.id,
                            MedicineContraindication.condition_id == condition.id
                        )
                    ).first()
                    
                    if contraindication:
                        warnings.append(f"Contraindicated for {condition.name}: {contraindication.notes}")
        
        return warnings
    
    def get_safety_warnings(self, recommendations, conditions, age):
        """Get overall safety warnings for recommendations."""
        warnings = []
        
        # Check for high-risk combinations
        if conditions and 'Pregnancy' in conditions:
            warnings.append("⚠️ You are pregnant. Consult your doctor before taking any medication.")
        
        if conditions and 'Liver Disease' in conditions:
            warnings.append("⚠️ You have liver disease. Some medications may be harmful.")
        
        if conditions and 'Kidney Disease' in conditions:
            warnings.append("⚠️ You have kidney disease. Some medications may be harmful.")
        
        if age and age < 18:
            warnings.append("⚠️ You are under 18. Consult a pediatrician before taking any medication.")
        
        if age and age > 65:
            warnings.append("⚠️ You are over 65. Some medications may affect you differently.")
        
        return warnings
    
    def process_chat_message(self, message, history=None):
        """Process chat message and return response."""
        if not history:
            history = []
        
        # Extract symptoms from message
        symptoms = self._extract_symptoms_from_text(message)
        
        # Extract patient information
        patient_info = self._extract_patient_info(message)
        
        # Generate response
        response = self._generate_chat_response(message, symptoms, patient_info, history)
        
        return response
    
    def _extract_symptoms_from_text(self, text):
        """Extract symptoms from text using keyword matching."""
        text_lower = text.lower()
        symptoms = []
        
        # Get all available symptoms
        all_symptoms = self.session.query(Symptom).all()
        
        for symptom in all_symptoms:
            symptom_name = symptom.name.lower()
            
            # Check for exact match
            if symptom_name in text_lower:
                symptoms.append(symptom.name)
                continue
            
            # Check for partial match
            words = symptom_name.split()
            for word in words:
                if len(word) > 3 and word in text_lower:
                    symptoms.append(symptom.name)
                    break
        
        return symptoms
    
    def _extract_patient_info(self, text):
        """Extract patient information from text."""
        info = {}
        
        # Extract age
        age_match = re.search(r'(\d+)\s*(?:years?|yrs?|old)', text.lower())
        if age_match:
            info['age'] = int(age_match.group(1))
        
        # Extract gender
        if any(word in text.lower() for word in ['male', 'man', 'boy', 'he', 'him']):
            info['gender'] = 'male'
        elif any(word in text.lower() for word in ['female', 'woman', 'girl', 'she', 'her']):
            info['gender'] = 'female'
        
        # Extract conditions
        conditions = []
        all_conditions = self.session.query(PatientCondition).all()
        
        for condition in all_conditions:
            condition_name = condition.name.lower()
            if condition_name in text.lower():
                conditions.append(condition.name)
        
        if conditions:
            info['conditions'] = conditions
        
        return info
    
    def _generate_chat_response(self, message, symptoms, patient_info, history):
        """Generate chat response based on message analysis."""
        response = {
            'message': '',
            'symptoms_found': symptoms,
            'patient_info': patient_info,
            'recommendations': [],
            'questions': []
        }
        
        if symptoms:
            # Get recommendations
            recommendations = self.get_recommendations(
                symptoms=symptoms,
                conditions=patient_info.get('conditions', []),
                age=patient_info.get('age'),
                gender=patient_info.get('gender')
            )
            
            response['recommendations'] = recommendations[:3]  # Top 3 recommendations
            
            if recommendations:
                response['message'] = f"I found {len(symptoms)} symptom(s): {', '.join(symptoms)}. Here are some recommendations:"
            else:
                response['message'] = f"I found {len(symptoms)} symptom(s): {', '.join(symptoms)}. However, I don't have specific recommendations for these symptoms. Please consult a healthcare professional."
        else:
            response['message'] = "I didn't detect any specific symptoms in your message. Could you describe what symptoms you're experiencing?"
            response['questions'] = [
                "What symptoms are you experiencing?",
                "How long have you had these symptoms?",
                "Are you taking any other medications?",
                "Do you have any medical conditions I should know about?"
            ]
        
        return response
    
    def close(self):
        """Close database session."""
        self.session.close()
