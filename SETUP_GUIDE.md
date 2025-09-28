# Virtual Doctor + Tablet Recognition App - Setup Guide

## 🎯 Project Overview

This is a comprehensive healthcare application that combines:
- **AI-powered tablet recognition** using CNN models
- **Intelligent symptom checking** with personalized recommendations
- **Comprehensive medicine database** with FDA data
- **Modern web interface** built with React and Flask

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Download from [python.org](https://python.org))
- **Node.js 16+** (Download from [nodejs.org](https://nodejs.org))
- **Git** (Download from [git-scm.com](https://git-scm.com))

### Option 1: Automated Setup (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd virtual-doctor-app
   ```

2. **Run the automated setup:**
   ```bash
   python scripts/setup.py
   ```

3. **Start the application:**
   ```bash
   python run_app.py
   ```

### Option 2: Manual Setup

#### Step 1: Backend Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python scripts/init_database.py
   ```

5. **Start backend server:**
   ```bash
   python backend/app.py
   ```

#### Step 2: Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start frontend server:**
   ```bash
   npm start
   ```

## 📱 Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **API Health Check:** http://localhost:5000/api/health

## 🏗️ Project Structure

```
virtual-doctor-app/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── models/             # Database models
│   ├── services/           # Business logic services
│   └── ml/                 # Machine learning models
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   └── services/       # API services
│   └── public/
├── data/                   # Data storage
│   ├── raw/               # Raw data files
│   └── processed/         # Processed data
├── scripts/               # Utility scripts
│   ├── setup.py          # Automated setup
│   ├── init_database.py  # Database initialization
│   └── load_fda_data.py  # FDA data loading
├── tests/                 # Test files
└── docs/                  # Documentation
```

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

Key configurations:
- `DATABASE_URL`: Database connection string
- `FLASK_DEBUG`: Enable/disable debug mode
- `API_BASE_URL`: Backend API URL
- `MODEL_PATH`: Path to ML model files

### Database Configuration

The app uses SQLite by default. For production, consider MySQL:

```python
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/virtual_doctor"
```

## 🧪 Testing

### Backend Testing

```bash
# Run backend tests
python -m pytest tests/backend/

# Run specific test file
python -m pytest tests/backend/test_medicine_service.py
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 📊 Features

### 1. Symptom Checker
- **Chat Interface:** Natural language symptom description
- **Form Interface:** Structured symptom selection
- **Patient History:** Consider medical conditions and age
- **Safety Checks:** Contraindication warnings

### 2. Tablet Recognition
- **Image Upload:** Drag-and-drop or click to upload
- **CNN Model:** Deep learning for tablet identification
- **Confidence Scores:** Reliability indicators
- **Medicine Details:** Complete drug information

### 3. Medicine Database
- **Search:** Find medicines by name or ingredient
- **Filtering:** Advanced search capabilities
- **Details:** Comprehensive drug information
- **Safety Info:** Pregnancy categories, warnings

### 4. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/medicines` | GET | List medicines |
| `/api/medicines/search` | POST | Search medicines |
| `/api/symptoms` | GET | List symptoms |
| `/api/conditions` | GET | List conditions |
| `/api/identify` | POST | Identify tablet |
| `/api/recommend` | POST | Get recommendations |
| `/api/chat` | POST | Chat with doctor |

## 🔒 Security Considerations

- **Input Validation:** All inputs are validated
- **CORS Configuration:** Proper cross-origin settings
- **Error Handling:** Secure error messages
- **Data Sanitization:** SQL injection prevention

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set DATABASE_URL=your-production-db-url
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

### Docker Deployment

1. **Build Docker image:**
   ```bash
   docker build -t virtual-doctor .
   ```

2. **Run container:**
   ```bash
   docker run -p 5000:5000 virtual-doctor
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Python dependencies not found:**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

3. **Node modules issues:**
   ```bash
   # Clear and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Database connection errors:**
   ```bash
   # Reinitialize database
   python scripts/init_database.py
   ```

### Logs

- **Backend logs:** Check console output
- **Frontend logs:** Check browser console
- **Database logs:** Check `data/` directory

## 📚 Documentation

- **API Documentation:** Available at `/api/health`
- **Code Comments:** Comprehensive inline documentation
- **README:** Main project documentation
- **Setup Guide:** This file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This application is for educational purposes only. Always consult healthcare professionals for medical advice.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue on GitHub
4. Contact the development team

---

**Happy coding! 🎉**
