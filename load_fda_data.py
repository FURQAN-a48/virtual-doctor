"""
Script to load and process FDA drug labeling data.
This script handles the 7 parts of FDA Drug Labeling dataset.
"""

import json
import os
import pandas as pd
import requests
from datetime import datetime
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.medicine import Medicine, Symptom, PatientCondition, MedicineSymptom, MedicineContraindication, Base

class FDADataLoader:
    """Handles loading and processing of FDA drug data."""
    
    def __init__(self, database_url="sqlite:///data/medicines.db"):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def download_fda_data(self, output_dir="data/raw"):
        """Download FDA drug labeling data from OpenFDA API."""
        os.makedirs(output_dir, exist_ok=True)
        
        # FDA API endpoints for different data types
        endpoints = {
            'drug_labels': 'https://api.fda.gov/drug/label.json',
            'drug_events': 'https://api.fda.gov/drug/event.json',
            'drug_enforcement': 'https://api.fda.gov/drug/enforcement.json',
            'drug_recalls': 'https://api.fda.gov/drug/recall.json',
            'drug_ndc': 'https://api.fda.gov/drug/ndc.json',
            'drug_drugsfda': 'https://api.fda.gov/drug/drugsfda.json',
            'drug_application': 'https://api.fda.gov/drug/application.json'
        }
        
        downloaded_files = {}
        
        for name, url in endpoints.items():
            print(f"Downloading {name}...")
            try:
                # Download with pagination (limit to 1000 records per request)
                all_data = []
                skip = 0
                limit = 1000
                
                while True:
                    params = {
                        'limit': limit,
                        'skip': skip
                    }
                    
                    response = requests.get(url, params=params, timeout=30)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if 'results' not in data or not data['results']:
                        break
                    
                    all_data.extend(data['results'])
                    skip += limit
                    
                    # Limit total records to avoid overwhelming the system
                    if skip >= 5000:  # Adjust as needed
                        break
                    
                    time.sleep(0.1)  # Be respectful to the API
                
                # Save to file
                file_path = os.path.join(output_dir, f"{name}.json")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, indent=2, ensure_ascii=False)
                
                downloaded_files[name] = file_path
                print(f"Downloaded {len(all_data)} records to {file_path}")
                
            except Exception as e:
                print(f"Error downloading {name}: {e}")
                continue
        
        return downloaded_files
    
    def process_drug_labels(self, file_path):
        """Process drug labels data and extract medicine information."""
        print("Processing drug labels...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        medicines = []
        
        for record in data:
            try:
                # Extract basic information
                openfda = record.get('openfda', {})
                brand_name = openfda.get('brand_name', [''])[0] if openfda.get('brand_name') else None
                generic_name = openfda.get('generic_name', [''])[0] if openfda.get('generic_name') else None
                
                if not generic_name:
                    continue
                
                # Extract detailed information
                medicine = Medicine(
                    brand_name=brand_name,
                    generic_name=generic_name,
                    manufacturer=openfda.get('manufacturer_name', [''])[0] if openfda.get('manufacturer_name') else None,
                    product_type=openfda.get('product_type', [''])[0] if openfda.get('product_type') else None,
                    
                    # Extract text fields
                    indications_and_usage=self._extract_text_field(record, 'indications_and_usage'),
                    dosage_and_administration=self._extract_text_field(record, 'dosage_and_administration'),
                    warnings=self._extract_text_field(record, 'warnings'),
                    adverse_reactions=self._extract_text_field(record, 'adverse_reactions'),
                    contraindications=self._extract_text_field(record, 'contraindications'),
                    drug_interactions=self._extract_text_field(record, 'drug_interactions'),
                    
                    # Extract active ingredients
                    active_ingredients=self._extract_text_field(record, 'active_ingredient'),
                    
                    # Extract strength and route
                    strength=openfda.get('product_ndc', [''])[0] if openfda.get('product_ndc') else None,
                    route_of_administration=openfda.get('route', [''])[0] if openfda.get('route') else None,
                    
                    # Extract pregnancy category
                    pregnancy_category=self._extract_pregnancy_category(record),
                    
                    # Extract FDA information
                    fda_application_number=record.get('application_number'),
                    fda_approval_date=self._parse_date(record.get('effective_time'))
                )
                
                medicines.append(medicine)
                
            except Exception as e:
                print(f"Error processing record: {e}")
                continue
        
        return medicines
    
    def _extract_text_field(self, record, field_name):
        """Extract text field from FDA record."""
        if field_name in record and record[field_name]:
            if isinstance(record[field_name], list):
                return ' '.join(record[field_name])
            return str(record[field_name])
        return None
    
    def _extract_pregnancy_category(self, record):
        """Extract pregnancy category from record."""
        pregnancy_info = self._extract_text_field(record, 'pregnancy')
        if pregnancy_info:
            pregnancy_info = pregnancy_info.lower()
            if 'category a' in pregnancy_info:
                return 'A'
            elif 'category b' in pregnancy_info:
                return 'B'
            elif 'category c' in pregnancy_info:
                return 'C'
            elif 'category d' in pregnancy_info:
                return 'D'
            elif 'category x' in pregnancy_info:
                return 'X'
        return None
    
    def _parse_date(self, date_str):
        """Parse date string to datetime object."""
        if not date_str:
            return None
        
        try:
            # Try different date formats
            for fmt in ['%Y%m%d', '%Y-%m-%d', '%m/%d/%Y']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
        except:
            pass
        
        return None
    
    def save_medicines(self, medicines):
        """Save medicines to database."""
        print(f"Saving {len(medicines)} medicines to database...")
        
        try:
            for medicine in medicines:
                self.session.add(medicine)
            
            self.session.commit()
            print("Medicines saved successfully!")
            
        except Exception as e:
            print(f"Error saving medicines: {e}")
            self.session.rollback()
    
    def create_sample_symptoms(self):
        """Create sample symptoms for testing."""
        symptoms_data = [
            {'name': 'Fever', 'description': 'Elevated body temperature', 'category': 'general'},
            {'name': 'Cough', 'description': 'Reflex action to clear throat', 'category': 'respiratory'},
            {'name': 'Headache', 'description': 'Pain in head or neck', 'category': 'neurological'},
            {'name': 'Nausea', 'description': 'Feeling of sickness', 'category': 'gastrointestinal'},
            {'name': 'Body Pain', 'description': 'General muscle or joint pain', 'category': 'musculoskeletal'},
            {'name': 'Sore Throat', 'description': 'Pain or irritation in throat', 'category': 'respiratory'},
            {'name': 'Runny Nose', 'description': 'Excessive nasal discharge', 'category': 'respiratory'},
            {'name': 'Fatigue', 'description': 'Extreme tiredness', 'category': 'general'},
            {'name': 'Dizziness', 'description': 'Feeling of unsteadiness', 'category': 'neurological'},
            {'name': 'Insomnia', 'description': 'Difficulty sleeping', 'category': 'sleep'}
        ]
        
        for symptom_data in symptoms_data:
            symptom = Symptom(**symptom_data)
            self.session.add(symptom)
        
        self.session.commit()
        print("Sample symptoms created!")
    
    def create_sample_conditions(self):
        """Create sample patient conditions."""
        conditions_data = [
            {'name': 'High Blood Pressure', 'description': 'Hypertension', 'affects_medication': True},
            {'name': 'Diabetes', 'description': 'High blood sugar', 'affects_medication': True},
            {'name': 'Pregnancy', 'description': 'Pregnant state', 'affects_medication': True},
            {'name': 'Heart Disease', 'description': 'Cardiovascular conditions', 'affects_medication': True},
            {'name': 'Liver Disease', 'description': 'Hepatic conditions', 'affects_medication': True},
            {'name': 'Kidney Disease', 'description': 'Renal conditions', 'affects_medication': True},
            {'name': 'Allergies', 'description': 'Allergic reactions', 'affects_medication': True},
            {'name': 'Asthma', 'description': 'Respiratory condition', 'affects_medication': True}
        ]
        
        for condition_data in conditions_data:
            condition = PatientCondition(**condition_data)
            self.session.add(condition)
        
        self.session.commit()
        print("Sample conditions created!")
    
    def create_sample_medicine_symptoms(self):
        """Create sample medicine-symptom relationships."""
        # This would typically be done by medical professionals
        # For demo purposes, we'll create some basic relationships
        
        medicines = self.session.query(Medicine).limit(10).all()
        symptoms = self.session.query(Symptom).all()
        
        # Create some basic relationships
        for medicine in medicines:
            for symptom in symptoms[:3]:  # Associate with first 3 symptoms
                relationship = MedicineSymptom(
                    medicine_id=medicine.id,
                    symptom_id=symptom.id,
                    effectiveness_score=0.7,  # Placeholder score
                    contraindicated=False
                )
                self.session.add(relationship)
        
        self.session.commit()
        print("Sample medicine-symptom relationships created!")
    
    def load_all_data(self):
        """Load all FDA data and create sample data."""
        print("Starting FDA data loading process...")
        
        # Download data
        downloaded_files = self.download_fda_data()
        
        # Process drug labels if available
        if 'drug_labels' in downloaded_files:
            medicines = self.process_drug_labels(downloaded_files['drug_labels'])
            self.save_medicines(medicines)
        
        # Create sample data
        self.create_sample_symptoms()
        self.create_sample_conditions()
        self.create_sample_medicine_symptoms()
        
        print("Data loading completed!")
    
    def close(self):
        """Close database session."""
        self.session.close()


def main():
    """Main function to run the data loader."""
    loader = FDADataLoader()
    
    try:
        loader.load_all_data()
    except Exception as e:
        print(f"Error during data loading: {e}")
    finally:
        loader.close()


if __name__ == "__main__":
    main()
