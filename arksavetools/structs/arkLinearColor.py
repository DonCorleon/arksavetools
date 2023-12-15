class ArkLinearColor:
    def __init__(self, byte_buffer):
        self.r = byte_buffer.read_float()
        self.g = byte_buffer.read_float()
        self.b = byte_buffer.read_float()
        self.a = byte_buffer.read_float()

    def __repr__(self):
        return f'r : {self.r}, g : {self.g}, b : {self.b}, a : {self.a}'
