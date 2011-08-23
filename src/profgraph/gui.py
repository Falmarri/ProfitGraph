from PyQt4 import QtGui, QtCore
import PyQt4

import plot
import position
import sys
import settings
import model

_WINDOW_TITLE = 'Plot'

_DEBUG = True

_HOTKEYS = {
            'quit'          :   QtCore.Qt.CTRL + QtCore.Qt.Key_Q,
            'save'          :   QtCore.Qt.CTRL + QtCore.Qt.Key_S,        
            'superimpose'   :   QtCore.Qt.CTRL + QtCore.Qt.Key_I
}



class BaseDialog(QtGui.QDialog):
    
    def __init__(self, parent=None, flags = None, callable=None):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.callable = callable
        
        #self.main_widget = QtGui.QWidget(self)
        #self.main_layout=QtGui.QVBoxLayout()
        self.main_layout=QtGui.QGridLayout()
        
        self.textfields = {}
        

    def _add_footer(self):
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        self.connect(button_box, QtCore.SIGNAL('accepted()'), self.accept)
        self.connect(button_box, QtCore.SIGNAL('rejected()'), self.reject)
        self.main_layout.addWidget(button_box, self.main_layout.rowCount(), 0, 1, -1)#|QtCore.Qt.AlignRight)
        self.setLayout(self.main_layout)
        
    def _make(self):
        self.data = dict((k.replace('&', ''), str(v.text())) for (k, v) in self.textfields)
        
    def accept(self):
        if self.callable is not None:
            self._make()
            self._save()
            self.callable(self.data)

        QtGui.QDialog.accept(self)
    
    def _save(self):
        pass
    
    def reject(self):
        QtGui.QDialog.reject(self)
        
        
    def _create_buddy(self, bud):
        n, e = bud
        hlay = QtGui.QHBoxLayout()
        nlabel = QtGui.QLabel(n, self)
        nlabel.setBuddy(e)
        hlay.addWidget(nlabel)
        hlay.addWidget(e)
        return hlay
    
class PositionDialog(BaseDialog):
    
    def __init__(self, parent=None, flags=None):
        BaseDialog.__init__(self, parent, flags)

        

    

        
        
        
class StockDialog(BaseDialog):
    
    
    def __init__(self, parent=None, flags=0, callable=None):
        BaseDialog.__init__(self, parent, flags, callable)
        
        self.textfields = [('&Ticker', QtGui.QLineEdit(self)),
                           ('&Price', QtGui.QLineEdit(self)),
                           ('P&osition', QtGui.QLineEdit(self)),
                           ]

        count = 0
        for x in self.textfields:
            tlabel = QtGui.QLabel(x[0])
            tlabel.setBuddy(x[1])
            self.main_layout.addWidget(tlabel, count, 0)
            self.main_layout.addWidget(x[1], count,1)
            count = count+1
        

        self._add_footer()

class OptionDialog(BaseDialog):
    
    def __init__(self, parenet=None, flag=0):
        
        self.ticker_edit= QtGui.QPlainTextEdit(self)
        self.price_edit= QtGui.QPlainTextEdit(self)
        self.position_edit=QtGui.QPlainTextEdit(self)

        
        self.expiration_edit=QtGui.QPlainTextEdit(self)
        self.strike_edit=QtGui.QPlainTextEdit(self)


class ApplicationWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.setWindowtitle(_WINDOW_TITLE)
        
        self.plots = []
        self.quotes = []
        self.positions = []
        
        
        self.populate_plots()
        self.build_model()
        
        
        self.make_menu()
        

        self.main_widget = QtGui.QWidget(self)
        self.root_layout = QtGui.QHBoxLayout(self.main_widget)
        

        self.make_leftlayout()
        self.make_plotlayout()
        

        
        self.main_widget.setFocus()
        
        self.setCentralWidget(self.main_widget)
        self.connect(self.plot_views, QtCore.SIGNAL('clicked(const QModelIndex&)'), self.position_selected)
        self.statusBar().showMessage("Matplotlib", 2000)
        
    def fileQuit(self):
        self.close()


    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About", "This is a plotting thing")
        
        
    def setPlot(self, plot):
        pass
        
    def make_plotlayout(self):
        self.plot_layout = QtGui.QGridLayout()
        self.plot_layout.setGeometry(QtCore.QRect(200,200,200,200))
        #self.plot_layout.
        self.plots.append(plot.Plot())
        
        
        self.root_layout.addLayout(self.plot_layout)
        self.plot_layout.addWidget(self.plots[0])

        
    def build_model(self, pos=None, *posi):
        from modeltest import ModelTest

        self.position_model = model.TreeModel(position.build_positions(settings.load('quotes.json')))
        #self.modeltest = ModelTest(self.position_model, self)

          
    def add_position(self, pos):
        pass
    
    def remove_position(self, pos):
        pass
    
    def refresh_model(self):
        pass
    
    def position_selected(self, index):
        item = index.internalPointer()
        it = item.data(index.column(), QtCore.Qt.UserRole)
        
        
        if isinstance(it, position.position):
            for i in range(self.plot_layout.count()):
                self.plot_layout.takeAt(i)
            
            self.plot_layout.addWidget(plot.Plot(position=it))
        elif isinstance(it, position._security):
            pass
        
    def make_leftlayout(self):
        self.plot_views = QtGui.QTreeView()
        
        self.plot_views.setSelectionMode(1)
        
        #mod = model.TreeModel(self.position_model)
 
        self.plot_views.setModel(self.position_model)
        
        
        

        
        self.plot_views.selectAll()
        
        self.plot_views.selectedIndexes()
        '''
        home = mod.setRootPath(d.path())
        self.left_view.setRootIndex(home)
        '''
        self.root_layout.addWidget(self.plot_views)
        
    def refresh_plot_tree(self):
        pass
        
    def display_plot(self, *args, **kwargs):
        self.plot_layout.removeWidget(x for x in self.plots)
    
    def make_menu(self):
        
        #===============
        # FILE menu
        file_menu = QtGui.QMenu('&File', self)
        #===============
        

       
        #---------------
        # File->New
        filesubmenu = file_menu.addMenu('&New')
        #---------------
        
        
        filesubmenu.addAction('&Plot', self.newPlot)
        filesubmenu.addAction('&Position', self.newPosition)
        filesubmenu.addAction('&Quote', self.newQuote)
        
        

        file_menu.addSeparator()
        
        file_menu.addAction('&Import', self._import)
        file_menu.addAction('&Export', self._export)
        
        
        file_menu.addSeparator()
        
        
        file_menu.addAction('&Quit', self.fileQuit,
                          _HOTKEYS['quit'])

               
        self.menuBar().addMenu(file_menu)

        
        #===============
        # View
        view_menu = QtGui.QMenu('&View', self)
        #===============
        
        
        
        self.menuBar().addMenu(view_menu)
        #===============
        # Tools
        tools_menu = QtGui.QMenu('&Tools', self)
        #===============
        
        
        self.menuBar().addMenu(tools_menu)
        #===============
        # Plot
        self.plot_menu = QtGui.QMenu('&Plot', self)
        #===============
        
        self.plot_menu.setEnabled(True)
        self.plot_menu.addAction('Super&impose', self.superimpose_plot, _HOTKEYS['superimpose'])

        self.menuBar().addMenu(self.plot_menu)
        
        
        #===============
        # Settings
        settings_menu = QtGui.QMenu('S&ettings', self)
        #===============
        self.menuBar().addMenu(settings_menu)
        #===============
        # HELP menu
        help_menu = QtGui.QMenu('&Help', self)
        #===============

        
        self.menuBar().addSeparator()
        self.menuBar().addMenu(help_menu)

        help_menu.addAction('&About', self.about)
        
    def superimpose_plot(self):
        pass
 
    def newPlot(self):
        #diag = QtGui.QDialog(self.main_widget).show()
        #diag.setWindowTitle()
        pass
    def newPosition(self):
        pass
 
    def newQuote(self):
        StockDialog(self, callable=self._make_stock).show()
        
    def _make_stock(self, data):
        st = position.Stock(data['Ticker'], data['Price'], data['Position'])
        self.quotes.append(st)
        
        #debug
        po = position.position
        
        
    def populate_plots(self):
        pass
        
    def _import(self):
        pass
    
    def _export(self):
        pass
    
def set_hotkeys():
    pass

if __name__ == '__main__':
    
    from optparse import OptionParser
    
    parser = OptionParser()
    
    
    
    options, args = parser.parse_args()
    
    
    qApp = QtGui.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(qApp.exec_())


        