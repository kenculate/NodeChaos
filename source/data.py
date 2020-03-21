from source.item import Item


class Data:
    initial_node = None
    nodes = []
    items = []

    @staticmethod
    def json():
        return {
            'initial_node': str(Data.initial_node),
            'nodes': Data.nodes,
            'items': Data.items
        }

    @staticmethod
    def add_item(item):
        Data.items.append(item)

    @staticmethod
    def add_node(node):
        Data.nodes.append(node)
        if len(Data.nodes) == 1:
            Data.initial_node = Data.nodes[0].id

    @staticmethod
    def remove_node(node):
        Data.nodes.remove(node)

    @staticmethod
    def get_node(id):
        node = [n for n in Data.nodes if n.id == id]
        if node:
            return node[0]

    @staticmethod
    def clear():
        Data.nodes.clear()
        Data.items.clear()
        Data.initial_node = None






