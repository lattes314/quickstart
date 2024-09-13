"""
Custom Beamer template for articles (with git support).
"""

import os
import shutil
import sys

def generate_project(directory):
    # src directory
    src_directory = os.path.join(os.path.dirname(__file__),"src","beamer")

    # Copy the folder and all its contents
    shutil.copytree(src_directory, directory, dirs_exist_ok=True)

generate_project(sys.argv[1])