'''
Created on Nov 28, 2010

@author: falmarri
'''

from PyQt4 import QtCore
import os.path as path
import os


import yaml
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper



import model
import position


_ROOT_FOLDER= os.path.expanduser('~/.profitgraph/')
_SAVE = 'prof.json'
_CACHE = '.cache'


_HOTKEYS = {
            'quit'          :   QtCore.Qt.CTRL + QtCore.Qt.Key_Q,
            'save'          :   QtCore.Qt.CTRL + QtCore.Qt.Key_S,        
            'superimpose'   :   QtCore.Qt.CTRL + QtCore.Qt.Key_I
}




if not path.isdir(_ROOT_FOLDER):
    os.mkdir(_ROOT_FOLDER) 



_SAVE_FILE = path.join((path.expanduser(_ROOT_FOLDER), _SAVE))


_saved_data = None

def save(pos=None, *args, **kwargs):
    pass

def load(fp = None):
    if not fp:
        fil = _SAVE_FILE
    else:
        fil = fp
    with open(fil, 'r') as f:
        return f.read()



def build_from_save(mod=None):
    
    position_objects = []
    data = load('quotes.json')
    pos = data['positions']
    for ticker, lst in pos.iteritems():
        p = []
        for quoteitem in lst:
            i = model._QUOTE_TYPES[quoteitem['type']](ticker=ticker, **quoteitem)
            p.append(i)
        position_objects.append(position.position(*p))
        
    root = model.create_header()    
    for pos in position_objects:
        p = model.PositionItem([pos], root)
        for q in pos.quotes():
            p.appendChild(model.PositionItem([q], p))
        root.appendChild(p)
    return root
        
   
    
if __name__ == '__main__':
    print load('quotes.json')