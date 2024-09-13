"""
Basic Latex template for articles (with git support) :
    - .gitignore ;
    - main.tex with usual macros for articles ;
    - biblio.bib (empty) ;
    - /figures for storing figures.
"""

import os
import shutil
import sys

def generate_project(directory):
    # src directory
    src_directory = os.path.join(os.path.dirname(__file__),"src","article")
    
    # copy gitignore file
    shutil.copyfile(os.path.join(src_directory,"LateXgitignore.gitignore"),os.path.join(directory,".gitignore"))
    # copy Latex main file
    shutil.copyfile(os.path.join(src_directory,"LateXmain.tex"),os.path.join(directory,"main.tex"))
    # biblio file
    with open(os.path.join(directory, "biblio.bib"), 'x') as f:
        f.write(f"% Bibtek file\n")
    # figures directory
    os.mkdir(os.path.join(directory,"figures"))

generate_project(sys.argv[1])
