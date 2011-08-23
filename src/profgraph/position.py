'''
Created on Nov 26, 2010

@author: falmarri
'''

import numpy as np
import yaml
import model
from memoize import memoized
from datetime import date

import itertools


_plotres = .01

_colors = ( 'g-', 'c-', 'm-', 'y-', 'k-', 'w-')

_color_iterator = itertools.chain(_colors)
_figure_iterator = itertools.count(1)



class position(yaml.YAMLObject):
    yaml_tag = u'!Position'
    
    def __init__(self, *args, **kwargs):
        self.ticker = kwargs['ticker']
        if 'superimposed' in kwargs:
            self.superimposed = kwargs['superimposed']
        else:
            self.superimposed = False

        if 'positions' in kwargs:
            self.positions = kwargs['positions']
        else:
            self.positions = []
            for posi in args:
                self.positions.append(posi)
                
    @classmethod
    def from_yaml(cls, loader, node):
        return cls(**loader.construct_mapping(node))


    def __str__(self):
        return self.ticker.upper()
        
    def __repr__(self):
        return "%s(ticker=%s, superimposed=%s, positions=%s)" % (
                        self.__class__.__name__, self.ticker, self.superimposed, self.positions)

        
    def columncount(self):
        return 1
        
    def superimpose(self, val=None):
        if val is None:
            self.superimposed = not self.superimposed
        else:
            self.superimposed = val
    
    def data_generator(self, start, end):
        arr = np.arange(start, end, _plotres)
        if self.superimposed:
            return [arr, sum(x.plot(start, end, _plotres)[1] for x in self.positions), 'b-']
        else:
            return list(itertools.chain(*[x.plot(start,end) for x in self.positions]))

    
    def quotes(self):
        return self.positions[:]
    
    def add(self, pos):
        self.pos.append(pos)
        
    def remove(self,pos):
        pass

    def plot(self, low=None, high=None, opteq=None):
        return self.data_generator(low, high)
    
    def _plot(self, low, high):
        pass
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(*self.data_generator(low, high), figure=self.figure)
        plt.axhline(figure=self.figure, color='black', marker='|', markevery=1, ms=20)
        plt.show()
        

        
class _security(yaml.YAMLObject):
    '''
    Base class for securities. Options and Equities inherit from this
    '''
    
    def __init__(self, *args, **kwargs):
        self.ticker = kwargs['ticker']
        self.price = float(kwargs['price'])
        self.position = int(kwargs['position'])
    
    def __str__(self):
        return self.ticker.upper()
    
    

            
    def __eq__(self, other):
        if self is other:
            return True
        try:
            #return all((self.ticker == other.ticker, self.price == other.price, self.position==other.position, self.strike == other.strike, self.expiration == other.expiration))  
            return all((self.profloss(.1) == other.profloss(.1), self.profloss(9999) == other.profloss(9999)))
        except AttributeError:
            return False
        
    def columncount(self):
        return 1
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
    @memoized
    def plot(self, start, end, res=_plotres):
        arr  = np.arange(start, end, _plotres)
        return (arr, np.array([self.profloss(a) for a in arr]))
    
    
    
class Stock(_security):
    
    yaml_tag=u"!Stock"
    
    def __str__(self):
        return "%s - %s @ %s" % (self.ticker.upper(), self.position, self.price)
    
    def __repr__(self):
        return "%s(ticker=%s, price=%s, position=%s)" % (
                        self.__class__.__name__, self.ticker, self.price, self.position)
    
    
    @memoized
    def profloss(self, val):
        return (val - self.price) * self.position


class _option(_security):
    '''
    Base class for options. Can either be a call or a put
    '''
    
    
    dateform = '%Y%m%d'
    tickerform = '{ticker} {expiration}{type}{strike}'
    
    def __init__(self,*args, **kwargs):
        _security.__init__(self, *args, **kwargs)
        self.strike = float(kwargs['strike'])
        if 'expiration' in kwargs:
            exp = kwargs['expiration']
            if hasattr(exp, 'min'):
                self.expiration = exp
            else:
                self.expiration = date(int(exp[:4]), int(exp[4:6]), int(exp[6:8]))    


    def __str__(self):
        return "%s - Jan %s %s @ %s" % (self.ticker.upper(), self.strike, self._type[0], self.price)
    
#    def __repr__(self):
#        return "%s(ticker=%s, price=%s, position=%s, strike=%s, expiration=%s)" % (
#                        self.__class__.__name__, self.ticker, self.price, self.position, self.strike, self.expiration)
#        
    def excersize(self, val, inmoney=None):
        self.ex = val
        if val:
            self.ifinmony=inmoney
            
    def profloss(self, val):
        pass
    

    def inprofit(self, val):
        pass

    
    
class Call(_option):
    
    '''
    Options call
    '''
    _type = 'Call'
    yaml_tag=u"!Call"
    @memoized
    def profloss(self, val):
        ret = max(-1* self.price , (val  - self.strike - self.price))
        return ret * 100 * self.position
    @memoized
    def breakeaven(self):
        return self.strike + self.price * self.position

class Put(_option):
    
    '''
    Options put
    '''
    _type = 'Put'
    yaml_tag=u"!Put"
    @memoized
    def profloss(self, val):
        ret = max(-1* self.price , (-val  + self.strike - self.price))
        return ret * 100 * self.position

    @memoized
    def breakeaven(self):
        return self.strike - self.price * self.position


def build_positions(yamlstr):
    root = model.PositionItem(['Positions'])
    for x in (yaml.load(yamlstr)):
        i = model.PositionItem([x], root)
        for q in x.quotes():
            i.appendChild(model.PositionItem([q],i))
        root.appendChild(i)
    return root
        
    
    

if __name__ == '__main__':
    
    c1 = Stock(ticker='AAPL', price=314, position=100)
    ce = Stock(ticker='AAPL',price= 314,position= 100)
    c2= Call( ticker='AAPL',price= 8.42,position= 2, strike=320,expiration= '20101219')
    

    #n = np.arange(300, 320, .01)
    #print c.plot(n)
    
    pos = position(c2, c1, ticker="AAPL") 
    pos2= position(c2, ce, ticker = "AAPL")
    print yaml.dump([pos, pos2])
    l = yaml.load(yaml.dump([pos, pos2]))
    
    
    print l
    
    pos.superimpose()
    #print pos.plot_generator(300, 320)
    import time  
    
    #pos._plot(290, 350)
    #show()

    
    