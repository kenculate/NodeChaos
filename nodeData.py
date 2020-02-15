from lib import *


class NodeData:
    def __init__(self):
        from node import ChaosNode
        self.nodes: [ChaosNode] = []
        # self.nodes.append(ChaosNode(V2d(100, 100), name='Node1'))
        # self.nodes.append(ChaosNode(V2d(350, 100), name='Node2'))

    def json(self):
        return [n.json() for n in self.nodes]


class NodeDetail:
    def __init__(self, node):
        self.node = node
        self.title = ''
        self.text = ''

    def json(self):
        return {'title': self.title, 'text':self.text}

    @staticmethod
    def FromJson(node, data):
        detail = NodeDetail(node)
        detail.title = data.get('title', '')
        detail.text = data.get('text', '')
        return detail