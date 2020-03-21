from source.item import Item


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