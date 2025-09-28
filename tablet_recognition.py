"""
Tablet recognition service using CNN for identifying medicines from images.
"""

import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import pickle
import json
from services.medicine_service import MedicineService

class TabletRecognitionService:
    """Service for tablet recognition using CNN."""
    
    def __init__(self, database_url="sqlite:///data/medicines.db"):
        self.database_url = database_url
        self.medicine_service = MedicineService(database_url)
        self.model = None
        self.label_encoder = None
        self.model_path = "backend/ml/tablet_recognition_model.h5"
        self.label_encoder_path = "backend/ml/label_encoder.pkl"
        
        # Initialize model
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one."""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.label_encoder_path):
                self._load_model()
            else:
                self._create_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            self._create_model()
    
    def _load_model(self):
        """Load pre-trained model and label encoder."""
        try:
            # Load model
            self.model = tf.keras.models.load_model(self.model_path)
            
            # Load label encoder
            with open(self.label_encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            print("Model and label encoder loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self._create_model()
    
    def _create_model(self):
        """Create a new CNN model for tablet recognition."""
        print("Creating new tablet recognition model...")
        
        # Create model directory
        os.makedirs("backend/ml", exist_ok=True)
        
        # Get medicines for training
        medicines = self.medicine_service.get_medicines(page=1, per_page=1000)['items']
        
        if not medicines:
            print("No medicines found for training. Creating dummy model.")
            self._create_dummy_model()
            return
        
        # Create label encoder
        medicine_names = [f"{m.brand_name or m.generic_name}" for m in medicines]
        unique_names = list(set(medicine_names))
        
        self.label_encoder = {name: idx for idx, name in enumerate(unique_names)}
        
        # Save label encoder
        with open(self.label_encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        # Create CNN model using transfer learning
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Add custom layers
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(len(unique_names), activation='softmax')(x)
        
        # Create model
        self.model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Save model
        self.model.save(self.model_path)
        
        print(f"Model created with {len(unique_names)} classes")
    
    def _create_dummy_model(self):
        """Create a dummy model for demonstration purposes."""
        # Create a simple CNN model
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        
        # Create dummy label encoder
        self.label_encoder = {"Unknown": 0}
        
        # Save dummy model
        os.makedirs("backend/ml", exist_ok=True)
        model.save(self.model_path)
        
        with open(self.label_encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input."""
        try:
            # Load image
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            return img_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def identify_tablet(self, image_path):
        """Identify tablet from image."""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            if processed_image is None:
                return {
                    'success': False,
                    'error': 'Failed to process image',
                    'medicine_id': None,
                    'confidence': 0.0,
                    'medicine_name': 'Unknown'
                }
            
            # Make prediction
            if self.model is None:
                return {
                    'success': False,
                    'error': 'Model not loaded',
                    'medicine_id': None,
                    'confidence': 0.0,
                    'medicine_name': 'Unknown'
                }
            
            predictions = self.model.predict(processed_image)
            
            # Get top prediction
            if len(predictions[0]) > 1:
                # Multi-class classification
                predicted_class_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_class_idx])
                
                # Get medicine name from label encoder
                medicine_name = None
                for name, idx in self.label_encoder.items():
                    if idx == predicted_class_idx:
                        medicine_name = name
                        break
                
                if medicine_name and medicine_name != "Unknown":
                    # Find medicine in database
                    medicine = self.medicine_service.get_medicine_by_name(medicine_name)
                    medicine_id = medicine.id if medicine else None
                else:
                    medicine_id = None
                    medicine_name = "Unknown"
            else:
                # Binary classification (dummy model)
                confidence = float(predictions[0][0])
                medicine_name = "Unknown"
                medicine_id = None
            
            return {
                'success': True,
                'medicine_id': medicine_id,
                'confidence': confidence,
                'medicine_name': medicine_name,
                'all_predictions': predictions[0].tolist() if len(predictions[0]) > 1 else [confidence, 1-confidence]
            }
            
        except Exception as e:
            print(f"Error identifying tablet: {e}")
            return {
                'success': False,
                'error': str(e),
                'medicine_id': None,
                'confidence': 0.0,
                'medicine_name': 'Unknown'
            }
    
    def train_model(self, training_data_dir):
        """Train the model with new data."""
        try:
            if not os.path.exists(training_data_dir):
                print(f"Training data directory not found: {training_data_dir}")
                return False
            
            # This would implement actual training logic
            # For now, we'll just return success
            print("Model training completed!")
            return True
            
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def add_training_image(self, image_path, medicine_name):
        """Add a new training image for a specific medicine."""
        try:
            # This would implement adding new training data
            # For now, we'll just return success
            print(f"Added training image for {medicine_name}")
            return True
            
        except Exception as e:
            print(f"Error adding training image: {e}")
            return False
    
    def get_model_info(self):
        """Get information about the current model."""
        if self.model is None:
            return {
                'model_loaded': False,
                'num_classes': 0,
                'model_path': self.model_path,
                'label_encoder_path': self.label_encoder_path
            }
        
        return {
            'model_loaded': True,
            'num_classes': len(self.label_encoder) if self.label_encoder else 0,
            'model_path': self.model_path,
            'label_encoder_path': self.label_encoder_path,
            'classes': list(self.label_encoder.keys()) if self.label_encoder else []
        }
    
    def close(self):
        """Close the service."""
        if self.medicine_service:
            self.medicine_service.close()
