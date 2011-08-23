import datetime



_periods = ['1m', '3m', '5m', '10m', '30m', '1h', '4h', '1d', '3d', '5d']

class DataSet(object):
    
    def __init__(self, security):
        pass
    


class data(object):
    
    def __init__(self, equity, start_time, time_length):
        self.equity = equity
        
    @property
    def open(self):
        pass
    
    @property
    def close(self):
        pass
        
    @property
    def high(self):
        pass
    
    @property
    def low(self):
        pass
    
    @property
    def volume(self):
        pass
    
    @property
    def time_frame(self):
        pass
    

    
    @time_frame.set
    def time_frame(self, frame):
        self.frame=frame
        



class stock(object):
    
    def __init__(self):
        pass
    
    def bid(self, level=1):
        """
        @param level: Depth
        @return Tuple of length [level] containing a tuple (price, amount)
        """
        pass
    
    def ask(self, level=1):
        """
        @param level: Depth
        @return Tuple of length [level] containing a tuple (price, amount)
        """
        pass

    @property
    def last(self):
        """
        @return Tuple, (price, time)
        """
        pass
    
    
    
    
class trade(object):
    
    def __init__(self, item, date, amount, shares):
        self.item = item
        self.date = date
        self.amount = amount
        self.shares = shares
    
    @property
    def cost(self):
        return self.shares*self.amount
    


class option(object):
    
    def __init__(self, name, derivative, strike, expiration):
        pass
    
    @property
    def strike(self):
        pass
    
    @property
    def expiration(self):
        pass
    
    @property
    def bid(self):
        pass
    
    @property
    def ask(self):
        pass
    
    @property
    def last(self):
        return 0, datetime.datetime.now()
    
    