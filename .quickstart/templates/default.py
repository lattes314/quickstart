"""
Default template that use the temp template.
"""

import os
import sys
import subprocess

def generate_project(directory):
    TEMPLATE_DIR = os.path.dirname(__file__)
    template_path = os.path.join(TEMPLATE_DIR, "temp.py")
    # Load and execute the template
    subprocess.run(['python', template_path, directory])
        
generate_project(sys.argv[1])
