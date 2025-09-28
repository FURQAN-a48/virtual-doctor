"""
Medicine service for handling medicine-related operations.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, or_
from models.medicine import Medicine, Symptom, PatientCondition, MedicineSymptom, MedicineContraindication
import math

class MedicineService:
    """Service for medicine-related operations."""
    
    def __init__(self, database_url="sqlite:///data/medicines.db"):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_medicines(self, page=1, per_page=20, search=""):
        """Get medicines with pagination and search."""
        query = self.session.query(Medicine)
        
        # Apply search filter
        if search:
            search_filter = or_(
                Medicine.brand_name.ilike(f"%{search}%"),
                Medicine.generic_name.ilike(f"%{search}%"),
                Medicine.manufacturer.ilike(f"%{search}%"),
                Medicine.active_ingredients.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        medicines = query.offset(offset).limit(per_page).all()
        
        return {
            'items': medicines,
            'total': total,
            'pages': math.ceil(total / per_page)
        }
    
    def get_medicine_by_id(self, medicine_id):
        """Get medicine by ID."""
        return self.session.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    def get_medicine_by_name(self, name):
        """Get medicine by brand or generic name."""
        return self.session.query(Medicine).filter(
            or_(
                Medicine.brand_name.ilike(f"%{name}%"),
                Medicine.generic_name.ilike(f"%{name}%")
            )
        ).first()
    
    def search_medicines_by_symptoms(self, symptoms):
        """Search medicines that treat specific symptoms."""
        if not symptoms:
            return []
        
        # Get symptom IDs
        symptom_objects = self.session.query(Symptom).filter(
            Symptom.name.in_(symptoms)
        ).all()
        
        if not symptom_objects:
            return []
        
        symptom_ids = [s.id for s in symptom_objects]
        
        # Get medicines that treat these symptoms
        medicine_symptoms = self.session.query(MedicineSymptom).filter(
            and_(
                MedicineSymptom.symptom_id.in_(symptom_ids),
                MedicineSymptom.contraindicated == False
            )
        ).all()
        
        medicine_ids = [ms.medicine_id for ms in medicine_symptoms]
        
        if not medicine_ids:
            return []
        
        medicines = self.session.query(Medicine).filter(
            Medicine.id.in_(medicine_ids)
        ).all()
        
        return medicines
    
    def get_medicines_by_condition(self, condition_name):
        """Get medicines suitable for a specific condition."""
        condition = self.session.query(PatientCondition).filter(
            PatientCondition.name.ilike(f"%{condition_name}%")
        ).first()
        
        if not condition:
            return []
        
        # Get medicines that are NOT contraindicated for this condition
        contraindicated_medicines = self.session.query(MedicineContraindication).filter(
            MedicineContraindication.condition_id == condition.id
        ).all()
        
        contraindicated_ids = [c.medicine_id for c in contraindicated_medicines]
        
        # Get all medicines except contraindicated ones
        query = self.session.query(Medicine)
        if contraindicated_ids:
            query = query.filter(Medicine.id.notin_(contraindicated_ids))
        
        return query.all()
    
    def get_symptoms(self):
        """Get all available symptoms."""
        return self.session.query(Symptom).all()
    
    def get_conditions(self):
        """Get all available patient conditions."""
        return self.session.query(PatientCondition).all()
    
    def get_medicine_contraindications(self, medicine_id):
        """Get contraindications for a specific medicine."""
        contraindications = self.session.query(MedicineContraindication).filter(
            MedicineContraindication.medicine_id == medicine_id
        ).all()
        
        result = []
        for contraindication in contraindications:
            condition = self.session.query(PatientCondition).filter(
                PatientCondition.id == contraindication.condition_id
            ).first()
            
            if condition:
                result.append({
                    'condition': condition.to_dict(),
                    'severity': contraindication.severity,
                    'notes': contraindication.notes
                })
        
        return result
    
    def get_medicine_effectiveness(self, medicine_id, symptom_id):
        """Get effectiveness score for a medicine-symptom combination."""
        relationship = self.session.query(MedicineSymptom).filter(
            and_(
                MedicineSymptom.medicine_id == medicine_id,
                MedicineSymptom.symptom_id == symptom_id
            )
        ).first()
        
        if relationship:
            return relationship.effectiveness_score
        
        return 0.0
    
    def is_medicine_contraindicated(self, medicine_id, condition_id):
        """Check if a medicine is contraindicated for a condition."""
        contraindication = self.session.query(MedicineContraindication).filter(
            and_(
                MedicineContraindication.medicine_id == medicine_id,
                MedicineContraindication.condition_id == condition_id
            )
        ).first()
        
        return contraindication is not None
    
    def get_medicine_safety_info(self, medicine_id, patient_conditions=None):
        """Get safety information for a medicine given patient conditions."""
        medicine = self.get_medicine_by_id(medicine_id)
        if not medicine:
            return None
        
        safety_info = {
            'medicine': medicine.to_dict(),
            'contraindications': [],
            'warnings': [],
            'pregnancy_safety': medicine.pregnancy_category,
            'pediatric_use': medicine.pediatric_use,
            'geriatric_use': medicine.geriatric_use
        }
        
        # Check contraindications
        if patient_conditions:
            for condition_name in patient_conditions:
                condition = self.session.query(PatientCondition).filter(
                    PatientCondition.name.ilike(f"%{condition_name}%")
                ).first()
                
                if condition and self.is_medicine_contraindicated(medicine_id, condition.id):
                    contraindication = self.session.query(MedicineContraindication).filter(
                        and_(
                            MedicineContraindication.medicine_id == medicine_id,
                            MedicineContraindication.condition_id == condition.id
                        )
                    ).first()
                    
                    if contraindication:
                        safety_info['contraindications'].append({
                            'condition': condition.name,
                            'severity': contraindication.severity,
                            'notes': contraindication.notes
                        })
        
        return safety_info
    
    def close(self):
        """Close database session."""
        self.session.close()
