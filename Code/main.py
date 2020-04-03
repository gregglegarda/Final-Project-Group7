
import pandas as pd

from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QGridLayout
from PyQt5.QtCore import QUrl
import numpy as np
import sys
import os
import pip
#########-------------------------------------- AUTO IMPORTS  -------------------------------------- #########

try:
    from geopy.geocoders import Nominatim, GoogleV3
    import folium
    import qdarkstyle
except:
    #pip.main(['install', 'git+https://github.com/geopy/geopy'])
    #pip.main(['install', 'git+https://github.com/python-visualization/folium'])
    os.system('pip install geopy')
    os.system('pip install folium')
    os.system('pip install qdarkstyle')
    print("imported packages")



#########-------------------------------------- PATHS  -------------------------------------- #########
print("--------------------------PATHS--------------------------")
print("Creating path...")
try:   #Following code (try/except clauses) searches for this script, and then changes the current working directory to the folder that houses it.
    start = '/Users'  #Code from https://stackoverflow.com/questions/43553742/finding-particular-path-in-directory-in-python
    for dirpath, dirnames, filenames in os.walk(start):
        for filename in filenames:
            if filename == "US_Accidents_Dec19.csv":
                filename = os.path.join(dirpath, filename)
                os.chdir(dirpath)
except:
    pass



try:
    start1 = "C:\\Users"
    for dirpath, dirnames, filenames in os.walk(start1):
        for filename in filenames:
            if filename == "US_Accidents_Dec19.csv":
                filename = os.path.join(dirpath, filename)
                os.chdir(dirpath)
except:
    pass
print("Path created")



#########-------------------------------------- PRE PROCESSING  -------------------------------------- #########
print("--------------------------PRE PROCESSING--------------------------")

datafile = "US_Accidents_Dec19.csv"
sample_size = 5000

try:
    import pre_process

except:
    print("import exception")
data_instance = pre_process.data_frame(datafile, sample_size)
data = data_instance.create_dataframe()
data_instance.cleanup_data()


#########-------------------------------------- CREATE APPLICATION  -------------------------------------- #########
print("--------------------------APPLICATION--------------------------\nRunning Application...")
#create application instance. Should only be one running at a time
app = QApplication(sys.argv)


#########-------------------------------------- CREATE MAP -------------------------------------- #########
#create Qwebview Map instance
try:
    import map_view
except:
    print("import exception")

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
mapinstance = map_view.map_webview(file_path, data) #pass datapoints



#########-------------------------------------- CREATE WINDOW -------------------------------------- #########

#create window instance and put the map in
try:
    import main_window
except:
    print("import exception")

mainrun = main_window.runit(app, mapinstance)



