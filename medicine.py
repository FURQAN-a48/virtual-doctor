"""
Medicine database models for the Virtual Doctor app.
Handles drug information from FDA data.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class Medicine(Base):
    """Medicine model for storing drug information."""
    
    __tablename__ = 'medicines'
    
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(255), nullable=True, index=True)
    generic_name = Column(String(255), nullable=False, index=True)
    manufacturer = Column(String(255), nullable=True)
    product_type = Column(String(100), nullable=True)
    
    # Drug information
    indications_and_usage = Column(Text, nullable=True)
    dosage_and_administration = Column(Text, nullable=True)
    warnings = Column(Text, nullable=True)
    adverse_reactions = Column(Text, nullable=True)
    contraindications = Column(Text, nullable=True)
    drug_interactions = Column(Text, nullable=True)
    
    # Physical properties
    tablet_shape = Column(String(100), nullable=True)
    tablet_color = Column(String(100), nullable=True)
    tablet_size = Column(String(100), nullable=True)
    imprint_code = Column(String(100), nullable=True)
    
    # Medical properties
    active_ingredients = Column(Text, nullable=True)
    strength = Column(String(255), nullable=True)
    route_of_administration = Column(String(255), nullable=True)
    
    # Safety information
    pregnancy_category = Column(String(50), nullable=True)
    pediatric_use = Column(Text, nullable=True)
    geriatric_use = Column(Text, nullable=True)
    
    # Metadata
    fda_application_number = Column(String(100), nullable=True)
    fda_approval_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'brand_name': self.brand_name,
            'generic_name': self.generic_name,
            'manufacturer': self.manufacturer,
            'product_type': self.product_type,
            'indications_and_usage': self.indications_and_usage,
            'dosage_and_administration': self.dosage_and_administration,
            'warnings': self.warnings,
            'adverse_reactions': self.adverse_reactions,
            'contraindications': self.contraindications,
            'drug_interactions': self.drug_interactions,
            'tablet_shape': self.tablet_shape,
            'tablet_color': self.tablet_color,
            'tablet_size': self.tablet_size,
            'imprint_code': self.imprint_code,
            'active_ingredients': self.active_ingredients,
            'strength': self.strength,
            'route_of_administration': self.route_of_administration,
            'pregnancy_category': self.pregnancy_category,
            'pediatric_use': self.pediatric_use,
            'geriatric_use': self.geriatric_use,
            'fda_application_number': self.fda_application_number,
            'fda_approval_date': self.fda_approval_date.isoformat() if self.fda_approval_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Medicine(brand_name='{self.brand_name}', generic_name='{self.generic_name}')>"


class Symptom(Base):
    """Symptom model for symptom checking."""
    
    __tablename__ = 'symptoms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # e.g., 'respiratory', 'gastrointestinal'
    severity_levels = Column(Text, nullable=True)  # JSON string of severity levels
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'severity_levels': json.loads(self.severity_levels) if self.severity_levels else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MedicineSymptom(Base):
    """Junction table for medicine-symptom relationships."""
    
    __tablename__ = 'medicine_symptoms'
    
    id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, nullable=False)
    symptom_id = Column(Integer, nullable=False)
    effectiveness_score = Column(Float, default=0.0)  # 0-1 score
    contraindicated = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'symptom_id': self.symptom_id,
            'effectiveness_score': self.effectiveness_score,
            'contraindicated': self.contraindicated,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PatientCondition(Base):
    """Patient condition model for medical history."""
    
    __tablename__ = 'patient_conditions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    affects_medication = Column(Boolean, default=True)
    severity_levels = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'affects_medication': self.affects_medication,
            'severity_levels': json.loads(self.severity_levels) if self.severity_levels else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MedicineContraindication(Base):
    """Medicine contraindications for patient conditions."""
    
    __tablename__ = 'medicine_contraindications'
    
    id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, nullable=False)
    condition_id = Column(Integer, nullable=False)
    severity = Column(String(50), nullable=False)  # 'mild', 'moderate', 'severe'
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'condition_id': self.condition_id,
            'severity': self.severity,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Database configuration
DATABASE_URL = "sqlite:///data/medicines.db"

def create_database():
    """Create database and tables."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session."""
    engine = create_database()
    Session = sessionmaker(bind=engine)
    return Session()
