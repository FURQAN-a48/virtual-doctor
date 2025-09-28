"""
Demo script for Virtual Doctor app.
This script demonstrates the key features of the application.
"""

import os
import sys
import time
import requests
import json
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.medicine_service import MedicineService
from services.symptom_checker import SymptomChecker
from services.tablet_recognition import TabletRecognitionService

class VirtualDoctorDemo:
    """Demo class for Virtual Doctor app."""
    
    def __init__(self):
        self.base_url = "http://localhost:5000/api"
        self.medicine_service = MedicineService()
        self.symptom_checker = SymptomChecker()
        self.tablet_recognition = TabletRecognitionService()
    
    def check_api_health(self):
        """Check if the API is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is running and healthy")
                return True
            else:
                print(f"❌ API returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ API is not running: {e}")
            return False
    
    def demo_medicine_database(self):
        """Demonstrate medicine database functionality."""
        print("\n" + "="*50)
        print("🏥 MEDICINE DATABASE DEMO")
        print("="*50)
        
        # Get all medicines
        medicines = self.medicine_service.get_medicines(page=1, per_page=5)
        print(f"\n📊 Found {medicines['total']} medicines in database")
        
        # Display sample medicines
        print("\n📋 Sample Medicines:")
        for i, medicine in enumerate(medicines['items'][:3], 1):
            print(f"{i}. {medicine.brand_name or medicine.generic_name}")
            print(f"   Generic: {medicine.generic_name}")
            print(f"   Manufacturer: {medicine.manufacturer}")
            print(f"   Strength: {medicine.strength}")
            print()
        
        # Search for specific medicine
        print("🔍 Searching for 'Tylenol'...")
        tylenol = self.medicine_service.get_medicine_by_name("Tylenol")
        if tylenol:
            print(f"✅ Found: {tylenol.brand_name} ({tylenol.generic_name})")
        else:
            print("❌ Tylenol not found")
    
    def demo_symptom_checker(self):
        """Demonstrate symptom checker functionality."""
        print("\n" + "="*50)
        print("🤒 SYMPTOM CHECKER DEMO")
        print("="*50)
        
        # Test symptoms
        test_cases = [
            {
                "symptoms": ["Fever", "Headache"],
                "conditions": [],
                "age": 30,
                "gender": "male"
            },
            {
                "symptoms": ["Cough", "Sore Throat"],
                "conditions": ["Diabetes"],
                "age": 45,
                "gender": "female"
            },
            {
                "symptoms": ["Body Pain"],
                "conditions": ["High Blood Pressure"],
                "age": 60,
                "gender": "male"
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n🧪 Test Case {i}:")
            print(f"   Symptoms: {', '.join(case['symptoms'])}")
            print(f"   Conditions: {', '.join(case['conditions']) if case['conditions'] else 'None'}")
            print(f"   Age: {case['age']}, Gender: {case['gender']}")
            
            # Get recommendations
            recommendations = self.symptom_checker.get_recommendations(
                symptoms=case['symptoms'],
                conditions=case['conditions'],
                age=case['age'],
                gender=case['gender']
            )
            
            if recommendations:
                print(f"   💊 Recommendations ({len(recommendations)}):")
                for j, rec in enumerate(recommendations[:3], 1):
                    medicine = rec['medicine']
                    print(f"      {j}. {medicine['brand_name'] or medicine['generic_name']}")
                    print(f"         Effectiveness: {rec['effectiveness']:.1%}")
                    print(f"         Score: {rec['score']:.2f}")
            else:
                print("   ❌ No recommendations found")
    
    def demo_chat_interface(self):
        """Demonstrate chat interface functionality."""
        print("\n" + "="*50)
        print("💬 CHAT INTERFACE DEMO")
        print("="*50)
        
        # Test chat messages
        chat_messages = [
            "I have a fever and headache",
            "I'm a 25 year old female with diabetes and I have a cough",
            "I have body pain and I'm pregnant",
            "I can't sleep and I feel dizzy"
        ]
        
        for i, message in enumerate(chat_messages, 1):
            print(f"\n💭 Chat Message {i}: '{message}'")
            
            # Process chat message
            response = self.symptom_checker.process_chat_message(message)
            
            print(f"🤖 Bot Response: {response['message']}")
            
            if response['symptoms_found']:
                print(f"🔍 Symptoms detected: {', '.join(response['symptoms_found'])}")
            
            if response['patient_info']:
                info = response['patient_info']
                if 'age' in info:
                    print(f"👤 Age detected: {info['age']}")
                if 'gender' in info:
                    print(f"👤 Gender detected: {info['gender']}")
                if 'conditions' in info:
                    print(f"🏥 Conditions detected: {', '.join(info['conditions'])}")
            
            if response['recommendations']:
                print(f"💊 Recommendations provided: {len(response['recommendations'])}")
    
    def demo_tablet_recognition(self):
        """Demonstrate tablet recognition functionality."""
        print("\n" + "="*50)
        print("📷 TABLET RECOGNITION DEMO")
        print("="*50)
        
        # Get model info
        model_info = self.tablet_recognition.get_model_info()
        print(f"🤖 Model Status: {'Loaded' if model_info['model_loaded'] else 'Not Loaded'}")
        print(f"📊 Number of Classes: {model_info['num_classes']}")
        
        if model_info['classes']:
            print(f"🏷️  Available Classes: {', '.join(model_info['classes'][:5])}")
            if len(model_info['classes']) > 5:
                print(f"   ... and {len(model_info['classes']) - 5} more")
        
        # Note: Actual image recognition would require a real image file
        print("\n📝 Note: To test tablet recognition with real images:")
        print("   1. Start the web application")
        print("   2. Go to the Tablet Recognition page")
        print("   3. Upload an image of a tablet")
        print("   4. The AI will identify the medicine")
    
    def demo_api_endpoints(self):
        """Demonstrate API endpoints."""
        print("\n" + "="*50)
        print("🌐 API ENDPOINTS DEMO")
        print("="*50)
        
        if not self.check_api_health():
            print("❌ API is not running. Please start the backend server first.")
            return
        
        # Test various endpoints
        endpoints = [
            ("/health", "Health Check"),
            ("/medicines?page=1&per_page=3", "Get Medicines"),
            ("/symptoms", "Get Symptoms"),
            ("/conditions", "Get Conditions")
        ]
        
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {description}: {response.status_code}")
                    if isinstance(data, list):
                        print(f"   📊 Returned {len(data)} items")
                    elif isinstance(data, dict) and 'medicines' in data:
                        print(f"   📊 Returned {len(data['medicines'])} medicines")
                else:
                    print(f"❌ {description}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"❌ {description}: {e}")
    
    def run_full_demo(self):
        """Run the complete demo."""
        print("🏥 VIRTUAL DOCTOR + TABLET RECOGNITION DEMO")
        print("="*60)
        print("This demo showcases the key features of the application.")
        print("Make sure the backend server is running (python backend/app.py)")
        print("="*60)
        
        # Check API health
        if not self.check_api_health():
            print("\n❌ Please start the backend server first:")
            print("   python backend/app.py")
            return
        
        # Run all demos
        self.demo_medicine_database()
        self.demo_symptom_checker()
        self.demo_chat_interface()
        self.demo_tablet_recognition()
        self.demo_api_endpoints()
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETED!")
        print("="*60)
        print("To explore the full application:")
        print("1. Start the backend: python backend/app.py")
        print("2. Start the frontend: cd frontend && npm start")
        print("3. Open http://localhost:3000 in your browser")
        print("\nFeatures available:")
        print("• Symptom Checker with AI recommendations")
        print("• Tablet Recognition using CNN models")
        print("• Comprehensive Medicine Database")
        print("• Chat Interface for natural language interaction")
        print("• Safety checks and contraindication warnings")

def main():
    """Main demo function."""
    demo = VirtualDoctorDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()
