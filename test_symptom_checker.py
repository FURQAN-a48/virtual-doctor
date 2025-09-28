"""
Tests for symptom checker functionality.
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.symptom_checker import SymptomChecker
from models.medicine import Medicine, Symptom, PatientCondition, MedicineSymptom

class TestSymptomChecker(unittest.TestCase):
    """Test cases for SymptomChecker."""
    
    def setUp(self):
        """Set up test database."""
        # Create temporary database
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        self.database_url = f"sqlite:///{self.db_path}"
        
        # Initialize service
        self.checker = SymptomChecker(self.database_url)
        
        # Create test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up test database."""
        self.checker.close()
        shutil.rmtree(self.temp_dir)
    
    def _create_test_data(self):
        """Create test data."""
        # Create test medicines
        medicine1 = Medicine(
            brand_name="Test Medicine 1",
            generic_name="Test Generic 1",
            manufacturer="Test Manufacturer",
            active_ingredients="Test Ingredient 1",
            strength="100mg"
        )
        
        medicine2 = Medicine(
            brand_name="Test Medicine 2",
            generic_name="Test Generic 2",
            manufacturer="Test Manufacturer",
            active_ingredients="Test Ingredient 2",
            strength="200mg"
        )
        
        self.checker.session.add(medicine1)
        self.checker.session.add(medicine2)
        self.checker.session.commit()
        
        # Create test symptoms
        symptom1 = Symptom(name="Fever", description="Elevated temperature")
        symptom2 = Symptom(name="Headache", description="Head pain")
        
        self.checker.session.add(symptom1)
        self.checker.session.add(symptom2)
        self.checker.session.commit()
        
        # Create test conditions
        condition1 = PatientCondition(name="Diabetes", description="High blood sugar")
        condition2 = PatientCondition(name="Hypertension", description="High blood pressure")
        
        self.checker.session.add(condition1)
        self.checker.session.add(condition2)
        self.checker.session.commit()
        
        # Create medicine-symptom relationships
        medicines = self.checker.session.query(Medicine).all()
        symptoms = self.checker.session.query(Symptom).all()
        
        relationship1 = MedicineSymptom(
            medicine_id=medicines[0].id,
            symptom_id=symptoms[0].id,
            effectiveness_score=0.8,
            contraindicated=False
        )
        
        relationship2 = MedicineSymptom(
            medicine_id=medicines[1].id,
            symptom_id=symptoms[1].id,
            effectiveness_score=0.7,
            contraindicated=False
        )
        
        self.checker.session.add(relationship1)
        self.checker.session.add(relationship2)
        self.checker.session.commit()
    
    def test_get_recommendations(self):
        """Test getting medicine recommendations."""
        recommendations = self.checker.get_recommendations(
            symptoms=["Fever"],
            conditions=[],
            age=30,
            gender="male"
        )
        
        self.assertIsInstance(recommendations, list)
        # Should have at least one recommendation for fever
        self.assertGreater(len(recommendations), 0)
    
    def test_get_recommendations_with_conditions(self):
        """Test getting recommendations with patient conditions."""
        recommendations = self.checker.get_recommendations(
            symptoms=["Fever"],
            conditions=["Diabetes"],
            age=30,
            gender="male"
        )
        
        self.assertIsInstance(recommendations, list)
    
    def test_get_recommendations_empty_symptoms(self):
        """Test getting recommendations with empty symptoms."""
        recommendations = self.checker.get_recommendations(
            symptoms=[],
            conditions=[],
            age=30,
            gender="male"
        )
        
        self.assertEqual(len(recommendations), 0)
    
    def test_extract_symptoms_from_text(self):
        """Test extracting symptoms from text."""
        text = "I have a fever and headache"
        symptoms = self.checker._extract_symptoms_from_text(text)
        
        self.assertIn("Fever", symptoms)
        self.assertIn("Headache", symptoms)
    
    def test_extract_patient_info(self):
        """Test extracting patient information from text."""
        text = "I am a 25 year old male with diabetes"
        info = self.checker._extract_patient_info(text)
        
        self.assertEqual(info['age'], 25)
        self.assertEqual(info['gender'], 'male')
        self.assertIn('Diabetes', info['conditions'])
    
    def test_process_chat_message(self):
        """Test processing chat messages."""
        message = "I have a fever"
        response = self.checker.process_chat_message(message)
        
        self.assertIn('message', response)
        self.assertIn('symptoms_found', response)
        self.assertIn('patient_info', response)
        self.assertIn('recommendations', response)
    
    def test_get_safety_warnings(self):
        """Test getting safety warnings."""
        recommendations = [
            {
                'medicine': {'id': 1, 'brand_name': 'Test Medicine'},
                'safety_warnings': ['Test warning']
            }
        ]
        
        warnings = self.checker.get_safety_warnings(
            recommendations=recommendations,
            conditions=['Pregnancy'],
            age=25
        )
        
        self.assertIsInstance(warnings, list)
        # Should have pregnancy warning
        self.assertTrue(any('pregnant' in warning.lower() for warning in warnings))
    
    def test_calculate_medicine_score(self):
        """Test calculating medicine score."""
        medicines = self.checker.session.query(Medicine).all()
        medicine = medicines[0]
        
        score = self.checker._calculate_medicine_score(
            medicine=medicine,
            symptoms=["Fever"],
            conditions=[],
            age=30,
            gender="male",
            severity="moderate"
        )
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)

if __name__ == '__main__':
    unittest.main()
