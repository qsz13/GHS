__author__ = 'danielqiu'


from Edge import Edge
from Node import Node
from EdgeState import EdgeState

edge_list = []
node_list = []

def main():
    input_file = open("graph")
    node_number, edge_number = [int(x) for x in input_file.readline().split()]

    input_list = []

    for line in input_file:
        input_list.append([int(x) for x in line.split()])
        # print input_list[len(input_list)-1]

    for i in range(0,node_number):
        node = Node(i)
        node_list.append(node)

    for index, line in enumerate(input_list):
        node1 = node_list[line[0]]
        node2 = node_list[line[1]]
        if node2 is None:
            print "None error"
        weight = line[2]
        edge = Edge(index, node1, node2, weight)
        # print edge.node2, edge.node1
        edge_list.append(edge)
        node1.add_adjacent_edge(edge)
        # print node_list[line[0]].id, len(node_list[line[0]].adjacent_edge)
        node2.add_adjacent_edge(edge)

    start_GHS()
    print "done"
    for node in node_list:
        print "node"+str(node.id)

        for k,v in node.adjacent_edge_state.iteritems():
            if v is EdgeState.branch:
                print "edge  " + str(k.weight)
                # print

def start_GHS():


    # node_list[0].wakeup()
    # node_list[1].wakeup()
    # node_list[2].wakeup()
    # node_list[3].wakeup()
    # node_list[4].wakeup()
    # node_list[5].wakeup()
    # node_list[6].wakeup()
    # node_list[7].wakeup()
    # node_list[8].wakeup()
    # node_list[9].wakeup()
    # node_list[10].wakeup()


    node_list[0].wakeup()
    # message_queue_empty = False
    # while not message_queue_empty:
    #     message_queue_empty = True
    #     print "123"
    #     for node in node_list:
    #         if node.message_queue:
    #             print len(node.message_queue)
    #             message_queue_empty = False
    #             message = node.message_queue.pop(0)
    #             edge = message[1]
    #             sender = message[2]
    #             if message[0] is "connect":
    #                 print "connect"
    #                 edge.send_connect(sender, message[3])
    #             elif message[0] is "test":
    #                 print "test"
    #                 edge.send_test(sender, message[3],message[4])
    #             elif message[0] is "report":
    #                 print "report"
    #                 edge.send_report(sender, message[3])




if __name__ == '__main__':
	main()

