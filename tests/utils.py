class MockStore(object):
    def __init__(self, values=None):
        self.values = values if values is not None else {}

    def load_values(self, values):
        return {
            key: value for key, value in self.values.items() if key in values
        }
