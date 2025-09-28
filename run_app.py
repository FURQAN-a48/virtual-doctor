"""
Main script to run the Virtual Doctor app.
This script starts both the backend and frontend servers.
"""

import os
import sys
import subprocess
import time
import threading
import signal
import platform
from pathlib import Path

class AppRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def start_backend(self):
        """Start the Flask backend server."""
        print("🚀 Starting backend server...")
        try:
            if platform.system() == 'Windows':
                self.backend_process = subprocess.Popen([
                    sys.executable, 'backend/app.py'
                ], cwd=os.getcwd())
            else:
                self.backend_process = subprocess.Popen([
                    sys.executable, 'backend/app.py'
                ], cwd=os.getcwd())
            
            print("✅ Backend server started on http://localhost:5000")
            return True
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the React frontend server."""
        print("🚀 Starting frontend server...")
        try:
            frontend_dir = Path('frontend')
            if not frontend_dir.exists():
                print("❌ Frontend directory not found")
                return False
            
            if platform.system() == 'Windows':
                self.frontend_process = subprocess.Popen([
                    'npm', 'start'
                ], cwd=frontend_dir, shell=True)
            else:
                self.frontend_process = subprocess.Popen([
                    'npm', 'start'
                ], cwd=frontend_dir)
            
            print("✅ Frontend server started on http://localhost:3000")
            return True
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def stop_servers(self):
        """Stop both servers."""
        print("\n🛑 Stopping servers...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend server stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend server stopped")
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals."""
        print(f"\n🛑 Received signal {signum}")
        self.stop_servers()
        sys.exit(0)
    
    def run(self):
        """Run the application."""
        print("🏥 Virtual Doctor + Tablet Recognition App")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check if virtual environment exists
        if not os.path.exists('venv'):
            print("❌ Virtual environment not found. Please run setup.py first.")
            return False
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend
        if not self.start_frontend():
            self.stop_servers()
            return False
        
        print("\n" + "=" * 50)
        print("🎉 Application is running!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:5000")
        print("📚 API Docs: http://localhost:5000/api/health")
        print("\nPress Ctrl+C to stop the application")
        print("=" * 50)
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend server stopped unexpectedly")
                    break
                
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend server stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_servers()
        
        return True

def main():
    """Main function."""
    runner = AppRunner()
    success = runner.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
