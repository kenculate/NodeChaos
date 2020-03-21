import uuid


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