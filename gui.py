import PySimpleGUI as sg
import sys
import os
import csv
import pygad as ga
from production import Part,Machine,WorkOrder, ProductionManager
import random
import numpy as np
import SchedulePlot as sp
import argparse
from importlib import reload
import json

# Defined layout for GUI

page1_layout = [
    [sg.Text('Select a CSV file for machines:')],
    [sg.Input(key='machines'), sg.FileBrowse()],
    [sg.Text('Select a CSV file for parts:')],
    [sg.Input(key='parts'), sg.FileBrowse()],
    [sg.Text('Select a CSV file for work orders:')],
    [sg.Input(key='workorders'), sg.FileBrowse()],
    [sg.Button('Next')]
]

page2_layout = [
    [sg.Text('Figure 1:')],
    [sg.Canvas(key='canvas1')],
]

page3_layout = [
    [sg.Text('Figure 2:')],
    [sg.Canvas(key='canvas2')],
]

# Tab element with the 3 pages
tab = sg.TabGroup([[sg.Tab('Home', page1_layout), sg.Tab('Schedule', page2_layout), sg.Tab('F vs G', page3_layout)]])

# Create the GUI window
window = sg.Window('WORKORDER-PLANER', [[tab]])

# Event loop to process events and get input from the user
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

        
    

# Close the GUI window
window.close()