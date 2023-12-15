class UnknownStruct:
    def __init__(self, struct_type, value):
        self.struct_type = struct_type
        self.value = value
    def __repr__(self):
        return f'type : {self.struct_type}, value : {self.value}'
