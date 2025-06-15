import subprocess
import os
import sys

main_script = os.path.join(os.path.dirname(__file__), "main.py")

# Use current Python to run streamlit as a module
subprocess.run([sys.executable, "-m", "streamlit", "run", main_script])