"""
Initialize the database with sample data for development.
"""

import os
import sys
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.medicine import create_database, get_session, Medicine, Symptom, PatientCondition, MedicineSymptom, MedicineContraindication

def create_sample_medicines():
    """Create sample medicines for testing."""
    session = get_session()
    
    sample_medicines = [
        {
            'brand_name': 'Tylenol',
            'generic_name': 'Acetaminophen',
            'manufacturer': 'Johnson & Johnson',
            'product_type': 'OTC',
            'indications_and_usage': 'Temporary relief of minor aches and pains due to headache, muscle aches, backache, minor pain of arthritis, toothache, menstrual cramps, and for the reduction of fever.',
            'dosage_and_administration': 'Adults and children 12 years and over: Take 2 tablets every 4-6 hours as needed. Do not exceed 6 tablets in 24 hours.',
            'warnings': 'Do not take more than directed. If you are pregnant or nursing, ask a health professional before use.',
            'adverse_reactions': 'Rare cases of severe skin reactions have been reported.',
            'active_ingredients': 'Acetaminophen 500mg',
            'strength': '500mg',
            'route_of_administration': 'Oral',
            'pregnancy_category': 'B',
            'tablet_shape': 'Oval',
            'tablet_color': 'White',
            'imprint_code': 'TYLENOL'
        },
        {
            'brand_name': 'Advil',
            'generic_name': 'Ibuprofen',
            'manufacturer': 'Pfizer',
            'product_type': 'OTC',
            'indications_and_usage': 'Temporarily relieves minor aches and pains due to headache, toothache, backache, menstrual cramps, the common cold, or minor pain of arthritis.',
            'dosage_and_administration': 'Adults and children 12 years and over: Take 1 tablet every 4-6 hours while symptoms persist. Do not exceed 6 tablets in 24 hours.',
            'warnings': 'Do not take if you have ever had an allergic reaction to any other pain reliever/fever reducer.',
            'adverse_reactions': 'Stomach bleeding warning: This product contains an NSAID, which may cause severe stomach bleeding.',
            'active_ingredients': 'Ibuprofen 200mg',
            'strength': '200mg',
            'route_of_administration': 'Oral',
            'pregnancy_category': 'C',
            'tablet_shape': 'Round',
            'tablet_color': 'White',
            'imprint_code': 'ADVIL'
        },
        {
            'brand_name': 'Aspirin',
            'generic_name': 'Acetylsalicylic Acid',
            'manufacturer': 'Bayer',
            'product_type': 'OTC',
            'indications_and_usage': 'Temporarily relieves minor aches and pains due to headache, toothache, backache, menstrual cramps, the common cold, or minor pain of arthritis.',
            'dosage_and_administration': 'Adults and children 12 years and over: Take 1-2 tablets every 4 hours as needed. Do not exceed 12 tablets in 24 hours.',
            'warnings': 'Reye\'s syndrome: Children and teenagers who have or are recovering from chicken pox or flu-like symptoms should not use this product.',
            'adverse_reactions': 'Stomach bleeding warning: This product contains an NSAID, which may cause severe stomach bleeding.',
            'active_ingredients': 'Acetylsalicylic Acid 325mg',
            'strength': '325mg',
            'route_of_administration': 'Oral',
            'pregnancy_category': 'D',
            'tablet_shape': 'Round',
            'tablet_color': 'White',
            'imprint_code': 'BAYER'
        },
        {
            'brand_name': 'Benadryl',
            'generic_name': 'Diphenhydramine',
            'manufacturer': 'Johnson & Johnson',
            'product_type': 'OTC',
            'indications_and_usage': 'Temporarily relieves symptoms due to hay fever or other upper respiratory allergies.',
            'dosage_and_administration': 'Adults and children 12 years and over: Take 1-2 tablets every 4-6 hours as needed. Do not exceed 8 tablets in 24 hours.',
            'warnings': 'May cause drowsiness. Alcohol, sedatives, and tranquilizers may increase the drowsiness effect.',
            'adverse_reactions': 'Drowsiness, dizziness, constipation, stomach upset, blurred vision, or dry mouth/nose/throat may occur.',
            'active_ingredients': 'Diphenhydramine HCl 25mg',
            'strength': '25mg',
            'route_of_administration': 'Oral',
            'pregnancy_category': 'B',
            'tablet_shape': 'Round',
            'tablet_color': 'Pink',
            'imprint_code': 'BENADRYL'
        },
        {
            'brand_name': 'Robitussin',
            'generic_name': 'Guaifenesin',
            'manufacturer': 'Pfizer',
            'product_type': 'OTC',
            'indications_and_usage': 'Temporarily relieves cough due to minor throat and bronchial irritation as may occur with a cold.',
            'dosage_and_administration': 'Adults and children 12 years and over: Take 2 teaspoons every 4 hours. Do not exceed 6 doses in 24 hours.',
            'warnings': 'Do not use if you are now taking a prescription monoamine oxidase inhibitor (MAOI).',
            'adverse_reactions': 'Drowsiness, dizziness, nausea, or vomiting may occur.',
            'active_ingredients': 'Guaifenesin 200mg',
            'strength': '200mg',
            'route_of_administration': 'Oral',
            'pregnancy_category': 'C',
            'tablet_shape': 'Capsule',
            'tablet_color': 'Red',
            'imprint_code': 'ROBITUSSIN'
        }
    ]
    
    for medicine_data in sample_medicines:
        medicine = Medicine(**medicine_data)
        session.add(medicine)
    
    session.commit()
    print(f"Created {len(sample_medicines)} sample medicines")

def create_sample_symptoms():
    """Create sample symptoms."""
    session = get_session()
    
    symptoms_data = [
        {'name': 'Fever', 'description': 'Elevated body temperature above normal', 'category': 'general'},
        {'name': 'Cough', 'description': 'Reflex action to clear throat and airways', 'category': 'respiratory'},
        {'name': 'Headache', 'description': 'Pain in head or neck area', 'category': 'neurological'},
        {'name': 'Body Pain', 'description': 'General muscle or joint pain', 'category': 'musculoskeletal'},
        {'name': 'Sore Throat', 'description': 'Pain or irritation in throat', 'category': 'respiratory'},
        {'name': 'Runny Nose', 'description': 'Excessive nasal discharge', 'category': 'respiratory'},
        {'name': 'Nausea', 'description': 'Feeling of sickness with urge to vomit', 'category': 'gastrointestinal'},
        {'name': 'Fatigue', 'description': 'Extreme tiredness and lack of energy', 'category': 'general'},
        {'name': 'Dizziness', 'description': 'Feeling of unsteadiness or lightheadedness', 'category': 'neurological'},
        {'name': 'Insomnia', 'description': 'Difficulty falling or staying asleep', 'category': 'sleep'},
        {'name': 'Allergic Reaction', 'description': 'Immune system response to allergens', 'category': 'allergic'},
        {'name': 'Chest Congestion', 'description': 'Build-up of mucus in chest', 'category': 'respiratory'}
    ]
    
    for symptom_data in symptoms_data:
        symptom = Symptom(**symptom_data)
        session.add(symptom)
    
    session.commit()
    print(f"Created {len(symptoms_data)} sample symptoms")

def create_sample_conditions():
    """Create sample patient conditions."""
    session = get_session()
    
    conditions_data = [
        {'name': 'High Blood Pressure', 'description': 'Hypertension - elevated blood pressure', 'affects_medication': True},
        {'name': 'Diabetes', 'description': 'High blood sugar levels', 'affects_medication': True},
        {'name': 'Pregnancy', 'description': 'Pregnant state', 'affects_medication': True},
        {'name': 'Heart Disease', 'description': 'Cardiovascular conditions', 'affects_medication': True},
        {'name': 'Liver Disease', 'description': 'Hepatic conditions affecting liver function', 'affects_medication': True},
        {'name': 'Kidney Disease', 'description': 'Renal conditions affecting kidney function', 'affects_medication': True},
        {'name': 'Allergies', 'description': 'Allergic reactions to substances', 'affects_medication': True},
        {'name': 'Asthma', 'description': 'Respiratory condition causing breathing difficulties', 'affects_medication': True},
        {'name': 'GERD', 'description': 'Gastroesophageal reflux disease', 'affects_medication': True},
        {'name': 'Arthritis', 'description': 'Joint inflammation and pain', 'affects_medication': True}
    ]
    
    for condition_data in conditions_data:
        condition = PatientCondition(**condition_data)
        session.add(condition)
    
    session.commit()
    print(f"Created {len(conditions_data)} sample conditions")

def create_medicine_symptom_relationships():
    """Create medicine-symptom relationships."""
    session = get_session()
    
    # Get medicines and symptoms
    medicines = session.query(Medicine).all()
    symptoms = session.query(Symptom).all()
    
    # Create relationships based on common medical knowledge
    relationships = [
        # Tylenol (Acetaminophen)
        ('Tylenol', 'Fever', 0.9, False),
        ('Tylenol', 'Headache', 0.8, False),
        ('Tylenol', 'Body Pain', 0.7, False),
        
        # Advil (Ibuprofen)
        ('Advil', 'Fever', 0.8, False),
        ('Advil', 'Headache', 0.8, False),
        ('Advil', 'Body Pain', 0.9, False),
        ('Advil', 'Arthritis', 0.9, False),
        
        # Aspirin
        ('Aspirin', 'Fever', 0.7, False),
        ('Aspirin', 'Headache', 0.8, False),
        ('Aspirin', 'Body Pain', 0.8, False),
        
        # Benadryl
        ('Benadryl', 'Allergic Reaction', 0.9, False),
        ('Benadryl', 'Runny Nose', 0.7, False),
        ('Benadryl', 'Insomnia', 0.6, False),
        
        # Robitussin
        ('Robitussin', 'Cough', 0.8, False),
        ('Robitussin', 'Chest Congestion', 0.7, False),
        ('Robitussin', 'Sore Throat', 0.6, False)
    ]
    
    for brand_name, symptom_name, score, contraindicated in relationships:
        medicine = session.query(Medicine).filter(Medicine.brand_name == brand_name).first()
        symptom = session.query(Symptom).filter(Symptom.name == symptom_name).first()
        
        if medicine and symptom:
            relationship = MedicineSymptom(
                medicine_id=medicine.id,
                symptom_id=symptom.id,
                effectiveness_score=score,
                contraindicated=contraindicated
            )
            session.add(relationship)
    
    session.commit()
    print(f"Created {len(relationships)} medicine-symptom relationships")

def create_medicine_contraindications():
    """Create medicine contraindications."""
    session = get_session()
    
    contraindications = [
        # Aspirin contraindications
        ('Aspirin', 'Pregnancy', 'severe', 'Can cause bleeding problems in mother and baby'),
        ('Aspirin', 'Liver Disease', 'moderate', 'May worsen liver function'),
        ('Aspirin', 'Kidney Disease', 'moderate', 'May worsen kidney function'),
        
        # Ibuprofen contraindications
        ('Advil', 'Pregnancy', 'moderate', 'May cause problems in late pregnancy'),
        ('Advil', 'Heart Disease', 'moderate', 'May increase risk of heart attack'),
        ('Advil', 'Kidney Disease', 'moderate', 'May worsen kidney function'),
        
        # Acetaminophen contraindications
        ('Tylenol', 'Liver Disease', 'severe', 'Can cause severe liver damage'),
        
        # Benadryl contraindications
        ('Benadryl', 'Pregnancy', 'mild', 'May cause drowsiness in baby'),
        ('Benadryl', 'GERD', 'mild', 'May worsen acid reflux')
    ]
    
    for brand_name, condition_name, severity, notes in contraindications:
        medicine = session.query(Medicine).filter(Medicine.brand_name == brand_name).first()
        condition = session.query(PatientCondition).filter(PatientCondition.name == condition_name).first()
        
        if medicine and condition:
            contraindication = MedicineContraindication(
                medicine_id=medicine.id,
                condition_id=condition.id,
                severity=severity,
                notes=notes
            )
            session.add(contraindication)
    
    session.commit()
    print(f"Created {len(contraindications)} medicine contraindications")

def main():
    """Initialize database with sample data."""
    print("Initializing database with sample data...")
    
    # Create database
    create_database()
    print("Database created successfully!")
    
    # Create sample data
    create_sample_medicines()
    create_sample_symptoms()
    create_sample_conditions()
    create_medicine_symptom_relationships()
    create_medicine_contraindications()
    
    print("Database initialization completed!")

if __name__ == "__main__":
    main()
