import os


def gradeAllSubmissions


def getDirectorySubfolders(folder):
	subfolders = [f.path for f in os.scandir(folder) if f.is_dir() ]  
	return(subfolders)

import importlib

files = ['submission1', 'submission2', 'submission3']

for file in files:
    module = importlib.import_module(file)
    print module
    print module.powerFunction(2,3)