"""
Flask application for Virtual Doctor + Tablet Recognition app.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from models.medicine import Medicine, Symptom, PatientCondition, MedicineSymptom, MedicineContraindication, get_session
from services.medicine_service import MedicineService
from services.symptom_checker import SymptomChecker
from services.tablet_recognition import TabletRecognitionService

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/medicines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize services
medicine_service = MedicineService()
symptom_checker = SymptomChecker()
tablet_recognition = TabletRecognitionService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    """Get all medicines with optional filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        medicines = medicine_service.get_medicines(
            page=page,
            per_page=per_page,
            search=search
        )
        
        return jsonify({
            'medicines': [medicine.to_dict() for medicine in medicines['items']],
            'total': medicines['total'],
            'page': page,
            'per_page': per_page,
            'pages': medicines['pages']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    """Get specific medicine by ID."""
    try:
        medicine = medicine_service.get_medicine_by_id(medicine_id)
        if not medicine:
            return jsonify({'error': 'Medicine not found'}), 404
        
        return jsonify(medicine.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicines/search', methods=['POST'])
def search_medicines():
    """Search medicines by symptoms and patient conditions."""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        conditions = data.get('conditions', [])
        age = data.get('age', None)
        gender = data.get('gender', None)
        
        if not symptoms:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        recommendations = symptom_checker.get_recommendations(
            symptoms=symptoms,
            conditions=conditions,
            age=age,
            gender=gender
        )
        
        return jsonify({
            'recommendations': recommendations,
            'symptoms_checked': symptoms,
            'conditions_considered': conditions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms."""
    try:
        symptoms = medicine_service.get_symptoms()
        return jsonify([symptom.to_dict() for symptom in symptoms])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conditions', methods=['GET'])
def get_conditions():
    """Get all available patient conditions."""
    try:
        conditions = medicine_service.get_conditions()
        return jsonify([condition.to_dict() for condition in conditions])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/identify', methods=['POST'])
def identify_tablet():
    """Identify tablet from uploaded image."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Save uploaded image temporarily
        image_path = f"temp_{datetime.now().timestamp()}.jpg"
        image_file.save(image_path)
        
        try:
            # Identify tablet
            result = tablet_recognition.identify_tablet(image_path)
            
            # Get medicine information
            medicine_info = None
            if result['medicine_id']:
                medicine = medicine_service.get_medicine_by_id(result['medicine_id'])
                if medicine:
                    medicine_info = medicine.to_dict()
            
            return jsonify({
                'identification': result,
                'medicine_info': medicine_info
            })
        
        finally:
            # Clean up temporary file
            if os.path.exists(image_path):
                os.remove(image_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_medicine():
    """Get medicine recommendations based on symptoms and patient info."""
    try:
        data = request.get_json()
        
        # Extract patient information
        symptoms = data.get('symptoms', [])
        conditions = data.get('conditions', [])
        age = data.get('age', None)
        gender = data.get('gender', None)
        severity = data.get('severity', 'moderate')
        
        if not symptoms:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        # Get recommendations
        recommendations = symptom_checker.get_recommendations(
            symptoms=symptoms,
            conditions=conditions,
            age=age,
            gender=gender,
            severity=severity
        )
        
        # Add safety warnings
        warnings = symptom_checker.get_safety_warnings(
            recommendations=recommendations,
            conditions=conditions,
            age=age
        )
        
        return jsonify({
            'recommendations': recommendations,
            'warnings': warnings,
            'patient_info': {
                'symptoms': symptoms,
                'conditions': conditions,
                'age': age,
                'gender': gender,
                'severity': severity
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_doctor():
    """Chat interface for symptom checking."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process message and get response
        response = symptom_checker.process_chat_message(
            message=message,
            history=conversation_history
        )
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
