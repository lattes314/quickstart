"""
Minimal working example for a template :
    - this triple quote comment is displayed when typed "quickstart info -t boiler"
    - a generate_project(directory) function ;
    - the generate_project(os.sys.argv[2]).
"""

import os
import sys

def generate_project(directory: os.PathLike):
    """
    All the actions performed to create the template : basically creating files !
    "directory" contains the full path of the new directory created for the project.
    If you want to copy some files I recommend :
        - store the models in the /src folder ;
        - use the shutil library (see temp.py) to copy them.
    """

    with open(os.path.join(directory, "boiler.txt"), 'x') as f:
        f.write(f"Your new text file !")

generate_project(sys.argv[1])
