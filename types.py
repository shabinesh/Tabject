from decimal import Decimal

class Integer:
    def __init__(self, val=None):
        self.val = int(val)
    def __repr__(self):
        return self.val

class Text:
    def __init__(self, val=None):
        self.val = str(val)
    def __repr__(self):
        return self.val

class Bool:
    def __init__(self, val=None):
        self.val = bool(val)
    def __repr__(self):
        return self.val

class Real:
    def __init__(self, val=None):
        self.val = Decimal(val)
    def __repr__(self):
        return self.val

class Date:
    pass
