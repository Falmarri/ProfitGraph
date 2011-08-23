'''
Created on Nov 27, 2010

@author: falmarri
'''

import matplotlib
import numpy as np
import itertools
from PyQt4 import QtGui, QtCore 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import ystockquote


class Plot(FigureCanvas):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100, position=None, name=''):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        self.data=[0]
        self.pos = position
        self.current_price = self.get_current_price()
        self.compute_initial_figure()
        
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)
        self.mpl_connect('button_press_event', self.on_click)
        
        
    def get_current_price(self):
        return float(ystockquote.get_price(str(self.pos)))
    
    
    def _get_range(self, per):
        return (self.current_price - self.current_price * per, self.current_price + self.current_price * per)
    
    def compute_initial_figure(self):
        if self.pos is not None:
            self.data = self.pos.plot(*self._get_range(.2))
        self._update()
        
    def recompute(self):
        self.compute_initial_figure()
        self._update()
        self.draw()

    def add_data(self, data, update=None):
        self.data = list(itertools.chain(self.data, data))
        self.recompute()

    def plot(self, data):
        self.data = data
        self.recompute()
    
    def _update(self):
        if self.data is not None:
            self.axes.plot(*self.data)
            
    def superimpose(self):
        self.pos.superimpose()
        self.recompute()

    def on_click(self, event):
        print 'you pressed', event.button
        
    def contextMenuEvent(self, event):
        if event.reason() == event.Mouse:
            pos = event.globalPos() 
        else:
            pos = None
        menu = QtGui.QMenu(self)
        
        menu.addAction('&Superimpose', self.superimpose)
        menu.popup(pos) 
        event.accept()
        
     