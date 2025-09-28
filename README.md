# Virtual Doctor + Tablet Recognition App

A comprehensive healthcare application that combines AI-powered tablet recognition with intelligent symptom checking to provide personalized medicine recommendations.

## 🎯 Project Overview

This project demonstrates multiple advanced skills:
- **AI/ML**: CNN-based tablet recognition using transfer learning
- **NLP**: Intelligent symptom analysis and medicine recommendation
- **Backend**: Flask API with database integration
- **Frontend**: React-based user interface
- **Data Science**: FDA drug data processing and analysis

## 🚀 Features

### Phase 1: Medicine Database
- Extract and clean FDA drug labeling data
- Store comprehensive medicine information
- Support complex queries and filtering

### Phase 2: Tablet Recognition
- CNN model for tablet identification from images
- Transfer learning with MobileNet/ResNet
- Real-time image processing and classification

### Phase 3: Virtual Doctor
- Intelligent symptom checker with decision trees
- Patient condition consideration (BP, diabetes, pregnancy, age)
- Safe medicine recommendation system

### Phase 4: Full Integration
- RESTful API backend
- Modern React frontend
- Seamless tablet recognition and symptom checking

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- TensorFlow (ML)
- OpenCV (Image Processing)

**Frontend:**
- React 18
- Material-UI
- Axios (HTTP Client)

**Database:**
- SQLite (Development)
- MySQL (Production)

## 📦 Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd virtual-doctor-app
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Quick Start

1. **Initialize the database:**
```bash
python scripts/init_database.py
```

2. **Load FDA drug data:**
```bash
python scripts/load_fda_data.py
```

3. **Start the backend:**
```bash
python app.py
```

4. **Start the frontend:**
```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
virtual-doctor-app/
├── backend/
│   ├── app.py                 # Flask application
│   ├── models/                # Database models
│   ├── routes/                # API routes
│   ├── services/              # Business logic
│   └── ml/                    # Machine learning models
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   └── utils/             # Utility functions
│   └── public/
├── data/                      # Raw and processed data
├── scripts/                   # Data processing scripts
├── tests/                     # Test files
└── docs/                      # Documentation
```

## 🔧 Development Phases

- [x] **Phase 1**: Medicine Database Setup
- [x] **Phase 2**: Tablet Recognition Module
- [x] **Phase 3**: Symptom Checker Chatbot
- [x] **Phase 4**: Full Application Integration
- [x] **Phase 5**: Testing & Improvements
- [x] **Phase 6**: Deployment & Showcase

## 📊 API Endpoints

- `GET /api/medicines` - List all medicines
- `POST /api/medicines/search` - Search medicines by symptoms
- `POST /api/identify` - Identify tablet from image
- `POST /api/recommend` - Get medicine recommendations
- `GET /api/symptoms` - List available symptoms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for educational purposes only. Always consult with healthcare professionals for medical advice and treatment.
