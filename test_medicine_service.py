"""
Tests for medicine service functionality.
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.medicine_service import MedicineService
from models.medicine import Medicine, Symptom, PatientCondition

class TestMedicineService(unittest.TestCase):
    """Test cases for MedicineService."""
    
    def setUp(self):
        """Set up test database."""
        # Create temporary database
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        self.database_url = f"sqlite:///{self.db_path}"
        
        # Initialize service
        self.service = MedicineService(self.database_url)
        
        # Create test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up test database."""
        self.service.close()
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
        
        self.service.session.add(medicine1)
        self.service.session.add(medicine2)
        self.service.session.commit()
        
        # Create test symptoms
        symptom1 = Symptom(name="Fever", description="Elevated temperature")
        symptom2 = Symptom(name="Headache", description="Head pain")
        
        self.service.session.add(symptom1)
        self.service.session.add(symptom2)
        self.service.session.commit()
        
        # Create test conditions
        condition1 = PatientCondition(name="Diabetes", description="High blood sugar")
        condition2 = PatientCondition(name="Hypertension", description="High blood pressure")
        
        self.service.session.add(condition1)
        self.service.session.add(condition2)
        self.service.session.commit()
    
    def test_get_medicines(self):
        """Test getting medicines with pagination."""
        result = self.service.get_medicines(page=1, per_page=10)
        
        self.assertIn('items', result)
        self.assertIn('total', result)
        self.assertIn('pages', result)
        self.assertEqual(len(result['items']), 2)
        self.assertEqual(result['total'], 2)
    
    def test_get_medicines_with_search(self):
        """Test getting medicines with search."""
        result = self.service.get_medicines(search="Test Medicine 1")
        
        self.assertEqual(len(result['items']), 1)
        self.assertEqual(result['items'][0].brand_name, "Test Medicine 1")
    
    def test_get_medicine_by_id(self):
        """Test getting medicine by ID."""
        medicines = self.service.session.query(Medicine).all()
        medicine_id = medicines[0].id
        
        medicine = self.service.get_medicine_by_id(medicine_id)
        
        self.assertIsNotNone(medicine)
        self.assertEqual(medicine.id, medicine_id)
    
    def test_get_medicine_by_name(self):
        """Test getting medicine by name."""
        medicine = self.service.get_medicine_by_name("Test Medicine 1")
        
        self.assertIsNotNone(medicine)
        self.assertEqual(medicine.brand_name, "Test Medicine 1")
    
    def test_get_symptoms(self):
        """Test getting all symptoms."""
        symptoms = self.service.get_symptoms()
        
        self.assertEqual(len(symptoms), 2)
        symptom_names = [s.name for s in symptoms]
        self.assertIn("Fever", symptom_names)
        self.assertIn("Headache", symptom_names)
    
    def test_get_conditions(self):
        """Test getting all conditions."""
        conditions = self.service.get_conditions()
        
        self.assertEqual(len(conditions), 2)
        condition_names = [c.name for c in conditions]
        self.assertIn("Diabetes", condition_names)
        self.assertIn("Hypertension", condition_names)
    
    def test_search_medicines_by_symptoms(self):
        """Test searching medicines by symptoms."""
        medicines = self.service.search_medicines_by_symptoms(["Fever"])
        
        # This should return empty list since no relationships are set up
        self.assertEqual(len(medicines), 0)
    
    def test_get_medicines_by_condition(self):
        """Test getting medicines by condition."""
        medicines = self.service.get_medicines_by_condition("Diabetes")
        
        # This should return all medicines since no contraindications are set up
        self.assertEqual(len(medicines), 2)
    
    def test_is_medicine_contraindicated(self):
        """Test checking medicine contraindications."""
        medicines = self.service.session.query(Medicine).all()
        conditions = self.service.session.query(PatientCondition).all()
        
        # No contraindications set up, so should return False
        is_contraindicated = self.service.is_medicine_contraindicated(
            medicines[0].id, conditions[0].id
        )
        
        self.assertFalse(is_contraindicated)

if __name__ == '__main__':
    unittest.main()
