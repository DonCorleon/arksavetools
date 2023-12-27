class ArkSet:
    def __init__(self, value_type, values):
        self.value_type = value_type
        self.values = values

    def __repr__(self):
        return f'ArkSet(value_type : {self.value_type}, values : {self.values})'
