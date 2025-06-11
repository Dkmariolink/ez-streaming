# build.py
import os
import subprocess
import shutil
import sys

def build_executable():
    """Build the executable using PyInstaller"""
    # Create dist directory if it doesn't exist
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Determine the correct path separator for --add-data
    # For PyInstaller, on Windows it's ';', on other OS it's ':'
    data_separator = ';' if sys.platform.startswith('win') else ':'
    
    # Run PyInstaller
    subprocess.run([
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--icon=assets/icon.ico',
        f'--add-data=assets{data_separator}assets', # Added for bundling assets
        '--name=EZStreaming',
        'src/main.py'
    ])
    
    # Copy additional files
    shutil.copytree('assets', 'dist/EZStreaming/assets', dirs_exist_ok=True)
    
    print("Build complete! Executable is in the dist/EZStreaming folder.")

if __name__ == "__main__":
    build_executable()
