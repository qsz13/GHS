__author__ = 'danielqiu'


class Message(object):

    def __init__(self, type, arg):
        super(Message, self).__init__()
        self.type = type
        self.arg = arg