from lib import *
import uuid


class Data:
    def __init__(self):
        from node import Node
        self.nodes: [Node] = []
        self.items: [Item] = []

    def json(self):
        return {
            'nodes': self.nodes,
            'items': self.items
        }

    def add_item(self, item):
        self.items.append(item)

    def add_node(self, node):
        self.nodes.append(node)

    def get_node(self, id):
        node = [n for n in self.nodes if n.id == id]
        if node:
            return node[0]

    def clear_nodes(self):
        self.nodes.clear()


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

    def __repr__(self):
        return self.name

    def __init__(self):
        self.id = uuid.uuid1()

        self.name = ''
        self.description = ''
        self.owned = False


class NodeDetail:
    def __init__(self, node):
        self.node = node
        self.title = f'{node.name}_{str(node.id)[0:5]}'
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
        items = data.get('items', [])
        detail.items = []
        for item in items:
            detail.items.append(Item.FromJson(item))
        required_items = data.get('required_items', [])
        detail.required_items = []
        for item in required_items:
            detail.required_items.append(Item.FromJson(item))
        return detail

    def add_required_item(self, item):
        self.required_items.append(item)

    def remove_required_item(self, item):
        self.required_items.remove(item)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)
