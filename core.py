class GameElement(object):
    IMAGE = "StoneBlock"
    CAN_PASS = False
    
    def __init__(self):
        self.sprite = None
        self.board = None
        self.x = None
        self.y = None

    def interact(self):
        pass

    def __str__(self):
        return "<%s located at %r, %r>"%(type(self).__name__, self.x, self.y)

    def update(self, dt):
        pass
