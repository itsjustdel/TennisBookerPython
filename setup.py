from distutils.core import setup # Need this to handle modules
import py2exe 
import math # We have to import all modules used in our program

# non bundled
# setup(windows=['main.py']) # Calls setup function to indicate that we're dealing with a single console application

# bundled
setup(
    
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "TennisBooker.py"}],
    zipfile = None,
)

# type in terminal(powershell withg venv) to build in "dist" folder
# python setup.py py2exe