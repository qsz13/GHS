import sys
from EdgeState import EdgeState
from NodeState import NodeState



__author__ = 'danielqiu'


class Node(object):
    """
    Node represents the vertex of the graph
    a node is either a connection point, a redistribution point or a communication endpoint.
    The definition of a node depends on the network and protocol layer referred to.
    A physical network node is an active electronic device that is attached to a network, and is capable of sending, receiving, or forwarding information over a communications channel.
    A passive distribution point such as a distribution frame or patch panel is consequently not a node.

    ASSUMPTIONS:
    Each edge has a unique cost.
    Each node has a unique integer identifier (UID).
    Each process knows the cost and neighbor UID for each of its incident edges.
    Processes can send messages over edges to their neighbors.
    Each message eventually arrives and contains the UID of the sender.
    """
    def __init__(self, id):
        super(Node, self).__init__()
        self.id = id
        self.state = NodeState.sleeping
        self.level = 0
        self.fragment_id = self.id
        self.best_edge = None
        self.adjacent_edge = []
        self.adjacent_edge_state = {}
        self.best_edge = None
        self.best_wt = None
        self.test_edge = None
        self.in_branch = None
        self.find_count = None
        self.message_queue=[]

    def add_adjacent_edge(self, edge):
        self.adjacent_edge.append(edge)
        self.adjacent_edge_state[edge] = EdgeState.basic


    def wakeup(self):
        min_edge = self.get_min_weight_adjacent_edge()
        print "min_edge" + str(min_edge.weight)
        self.adjacent_edge_state[min_edge] = EdgeState.branch
        self.level = 0
        self.state = NodeState.found
        self.find_count = 0
        print "wake" + str(self.id)
        min_edge.send_connect(self, 0)



    def get_min_weight_adjacent_edge(self):
        if self.adjacent_edge:

            min_edge = self.adjacent_edge[0]
            min_weight = min_edge.weight

            for edge in self.adjacent_edge:
                if edge.weight < min_weight:
                    min_weight = edge.weight
                    min_edge = edge

            return min_edge
        else:
            return None

    def respond_to_connect(self, edge, sender, level):
        if self.state is NodeState.sleeping:
            self.wakeup()


        if level < self.level:
            self.adjacent_edge_state[edge] = EdgeState.branch
            edge.send_initiate(self,self.level, self.fragment_id, self.state)
            if self.state is NodeState.find:
                self.find_count += 1

        elif self.adjacent_edge_state[edge] is EdgeState.basic:
            self.message_queue.append(["connect", edge, sender, level])

        else:
            edge.send_initiate(self,self.level + 1, edge.weight, NodeState.find)

        # self.check_message_list()


    def respond_to_initiate(self, edge, sender, level, fragment_id, state):
        print "init"
        self.level = level
        self.check_test_message()
        self.fragment_id = fragment_id
        self.state = state
        self.in_branch = edge
        self.best_edge = None
        self.best_wt = sys.maxint

        for e in self.adjacent_edge:
            if e is edge or self.adjacent_edge_state[e] is not EdgeState.branch:
                continue
            else:
                e.send_initiate(self, level, fragment_id, state)
                if state is NodeState.find:
                    self.find_count += 1


        if state is NodeState.find:
            print
            self.test()

        self.check_report_message()


        # self.check_message_list()


    def test(self):


        if self.has_basic_edge():
            self.test_edge = self.get_min_weight_adjacent_edge()
            self.test_edge.send_test(self, self.level,self.fragment_id)
        else:
            self.test_edge = None
            self.report()


    def respond_to_test(self, edge, sender, level, fragment_id):
        if self.state is NodeState.sleeping:
            self.wakeup()

        if level > self.level:
            self.message_queue.append(["test", edge, sender, level, fragment_id])
        elif fragment_id is not self.fragment_id:
            edge.send_accept(self)
        else:
            if self.adjacent_edge_state[edge] is EdgeState.basic:
                self.adjacent_edge_state[edge] = EdgeState.rejected
                self.check_connect_message()

            if self.test_edge is not edge:
                edge.send_reject(self)
            else:
                self.test()




    def respond_to_accept(self, edge, sender):
        self.test_edge = None
        if edge.weight < self.best_wt:
            print edge
            self.best_edge = edge
            self.best_wt = edge.weight
            self.report()





    def respond_to_reject(self, edge, sender):
        if self.adjacent_edge_state[edge] is EdgeState.basic:
            self.adjacent_edge_state[edge] = EdgeState.rejected
            self.test()
            self.check_connect_message()




    def report(self):
        if self.find_count is 0 and self.test_edge is None:
            self.state = NodeState.found
            self.in_branch.send_report(self,self.best_wt)
            self.check_report_message()


    def respond_to_report(self, edge, sender, weight):
        if self.in_branch is not edge:
            self.find_count -= 1
            if weight < self.best_wt:
                self.best_wt = weight
                print "!!!"
                print edge
                self.best_edge = edge
                self.report()
        elif self.state is NodeState.find:
            self.message_queue.append(["report", edge, sender, weight])

        elif weight > self.best_wt:
            self.change_root()
        elif weight is sys.maxint and self.best_wt is sys.maxint:
            return





    def has_basic_edge(self):
        for k,v in self.adjacent_edge_state.iteritems():
            if v is EdgeState.basic:
                return True

        return False

    def get_min_weight_adjacent_edge(self):

        min_weight = sys.maxint
        min_weight_edge = None

        for k,v in self.adjacent_edge_state.iteritems():
            if v is EdgeState.basic:
                if k.weight <= min_weight:
                    min_weight = k.weight
                    min_weight_edge = k


        return  min_weight_edge


    def change_root(self):
        if self.adjacent_edge_state[self.best_edge] is EdgeState.branch:
            self.best_edge.send_change_root(self)
        else:
            self.best_edge.send_connect(self, self.level)
            self.adjacent_edge_state[self.best_edge] = EdgeState.branch


    def respond_to_change_root(self):
        self.change_root()




    def check_test_message(self):
        for message in self.message_queue:
            if message[0] is "test":
                edge = message[1]
                sender = message[2]
                level = message[3]
                fragment_id = message[4]
                self.respond_to_test(edge, sender, level, fragment_id)

    def check_connect_message(self):
        for message in self.message_queue:
            if message[0] is "connect":
                edge = message[1]
                sender = message[2]
                level = message[3]

                self.respond_to_connect(edge, sender, level)

    def check_report_message(self):
        for message in self.message_queue:
            if message[0] is "report":
                edge = message[1]
                sender = message[2]
                weight = message[3]
                self.respond_to_report(edge, sender, weight)

