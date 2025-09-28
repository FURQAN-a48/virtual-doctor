"""
Setup script for Virtual Doctor app.
This script initializes the database and sets up the environment.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment."""
    if not os.path.exists('venv'):
        return run_command('python -m venv venv', 'Creating virtual environment')
    else:
        print("✅ Virtual environment already exists")
        return True

def activate_virtual_environment():
    """Get the activation command for the virtual environment."""
    if platform.system() == 'Windows':
        return 'venv\\Scripts\\activate'
    else:
        return 'source venv/bin/activate'

def install_requirements():
    """Install Python requirements."""
    activate_cmd = activate_virtual_environment()
    if platform.system() == 'Windows':
        pip_cmd = f'{activate_cmd} && pip install -r requirements.txt'
    else:
        pip_cmd = f'{activate_cmd} && pip install -r requirements.txt'
    
    return run_command(pip_cmd, 'Installing Python requirements')

def initialize_database():
    """Initialize the database with sample data."""
    activate_cmd = activate_virtual_environment()
    if platform.system() == 'Windows':
        init_cmd = f'{activate_cmd} && python scripts/init_database.py'
    else:
        init_cmd = f'{activate_cmd} && python scripts/init_database.py'
    
    return run_command(init_cmd, 'Initializing database')

def install_frontend_dependencies():
    """Install frontend dependencies."""
    if not os.path.exists('frontend/node_modules'):
        return run_command('cd frontend && npm install', 'Installing frontend dependencies')
    else:
        print("✅ Frontend dependencies already installed")
        return True

def create_directories():
    """Create necessary directories."""
    directories = [
        'data',
        'data/raw',
        'data/processed',
        'backend/ml',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Virtual Doctor + Tablet Recognition App")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install Python requirements
    if not install_requirements():
        return False
    
    # Initialize database
    if not initialize_database():
        return False
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo start the application:")
    print("1. Backend: python backend/app.py")
    print("2. Frontend: cd frontend && npm start")
    print("\nThe app will be available at:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
