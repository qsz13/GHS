__author__ = 'danielqiu'


class Edge(object):
    """
    edge represents the link between two nodes

    """

    def __init__(self, id, u, v, w):
        super(Edge, self).__init__()
        self.id = id
        self.node1 = u
        self.node2 = v
        self.weight = w


    def send_connect(self, sender, level):
        if self.node1 is sender:
            self.node2.respond_to_connect(self, sender, level)
        elif self.node2 is sender:
            self.node1.respond_to_connect(self, sender, level)

    def send_initiate(self, sender, level, fragment_id, state):
        print self.node2
        if self.node1 is sender:
            self.node2.respond_to_initiate(self, sender, level, fragment_id, state)
        elif self.node2 is sender:
            self.node1.respond_to_initiate(self, sender, level, fragment_id, state)

    def send_test(self, sender, level, fragment_id):
        if self.node1 is sender:
            self.node2.respond_to_test(self, sender, level, fragment_id)
        elif self.node2 is sender:
            self.node1.respond_to_test(self, sender, level, fragment_id)

    def send_accept(self, sender):
        if self.node1 is sender:
            self.node2.respond_to_accept(self, sender)
        elif self.node2 is sender:
            self.node1.respond_to_accept(self, sender)

    def send_reject(self, sender):
        if self.node1 is sender:
            self.node2.respond_to_reject(self, sender)
        elif self.node2 is sender:
            self.node1.respond_to_reject(self, sender)

    def send_report(self, sender, weight):
        if self.node1 is sender:
            self.node2.respond_to_report(self, sender, weight)
        elif self.node2 is sender:
            self.node1.respond_to_report(self, sender, weight)

    def send_change_root(self, sender):
         if self.node1 is sender:
            self.node2.respond_to_change(self, sender)
         elif self.node2 is sender:
            self.node1.respond_to_change(self, sender)
