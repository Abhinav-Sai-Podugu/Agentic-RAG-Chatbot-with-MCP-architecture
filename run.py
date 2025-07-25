#!/usr/bin/env python3
"""
Agentic RAG Chatbot - Entry Point
Run this file to start the application
"""

import os
import sys
import subprocess
from pathlib import Path


def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import sentence_transformers
        import sklearn
        import PyPDF2
        import docx
        import pptx
        import requests
        import numpy
        from dotenv import load_dotenv
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False


def check_env_file():
    """Check if .env file exists"""
    env_path = Path('.env')
    if not env_path.exists():
        print("⚠️  .env file not found!")
        print("Please create .env file from .env.example:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenRouter API key")
        return False

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key or api_key == 'your_openrouter_api_key_here':
        print("⚠️  OpenRouter API key not configured!")
        print("Please add your API key to .env file")
        return False

    print("✅ Environment configuration loaded!")
    return True


def main():
    """Main entry point"""
    print("🚀 Starting Agentic RAG Chatbot...")
    print("=" * 50)

    # Check dependencies
    if not check_requirements():
        sys.exit(1)

    # Check environment
    if not check_env_file():
        sys.exit(1)

    # Start Streamlit app
    print("🌐 Starting Streamlit server...")
    ui_path = Path(__file__).parent / "ui" / "app.py"

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(ui_path),
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()