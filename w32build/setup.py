from distutils.core import setup
import os
import sys
import py2exe
sys.path.append( os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin'))

option = {
    "compressed"    :    1,
    "optimize"      :    2,
    "bundle_files"  :    1
}

setup(name="pybootstrap",
    options = {
        "py2exe"    :    option
    },
    console = [
        {"script"   :    "pybootstrap.py"}
    ],
    zipfile = None
)
