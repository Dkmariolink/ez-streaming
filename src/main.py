#!/usr/bin/env python3
"""
EZ Streaming - A simple launcher for streaming applications
Entry point for the application
"""

import os
import sys
from app import StreamerApp

def main():
    """Main entry point for EZ Streaming application"""
    # Add the current directory to the path so we can import modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Start the application
    app = StreamerApp()
    app.run()

if __name__ == "__main__":
    main()