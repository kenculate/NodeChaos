from lib import *
import uuid

class NodeData:
    def __init__(self):
        from node import Node
        self.nodes: [Node] = []
        self.items: [Item] = []
        # self.nodes.append(ChaosNode(V2d(100, 100), name='Node1'))
        # self.nodes.append(ChaosNode(V2d(350, 100), name='Node2'))

    def json(self):
        return {
            'nodes': self.nodes,
            'items': self.items
        }


class Item:
    @staticmethod
    def FromJson(data):
        item = Item()
        item.id = data.get('id', 0)
        item.name = data.get('name', '')
        item.description = data.get('description', '')
        item.owned = data.get('owned', False)
        return item

    def json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'owned': self.owned
        }

    def __init__(self):
        self.id = uuid.uuid1()

        self.name = ''
        self.description = ''
        self.owned = False


class NodeDetail:
    def __init__(self, node):
        self.node = node
        self.title = ''
        self.text = ''
        self.items: [Item] = []
        self.required_items: [Item] = []

    def json(self):
        return {
            'title': self.title,
            'text': self.text,
            'items': self.items,
            'required_items': self.required_items
            # 'node': str(self.node.id)
        }

    @staticmethod
    def FromJson(node, data):
        detail = NodeDetail(node)
        detail.title = data.get('title', '')
        detail.text = data.get('text', '')
        detail.items = data.get('items', [])
        detail.required_items = data.get('required_items', [])
        return detail
