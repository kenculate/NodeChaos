from enum import Enum


class KnobType(Enum):
    Input = 1
    Output = 2

    def json(self):
        return self.value
