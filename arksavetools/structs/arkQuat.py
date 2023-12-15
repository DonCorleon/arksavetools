class ArkQuat:
    def __init__(self, byte_buffer):
        self.x = byte_buffer.read_double()
        self.y = byte_buffer.read_double()
        self.z = byte_buffer.read_double()
        self.w = byte_buffer.read_double()

    def __repr__(self):
        return f'x : {self.x}, y : {self.y}, z : {self.z}, w : {self.w}'
