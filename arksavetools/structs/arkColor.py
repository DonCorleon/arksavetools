class ArkColor:
    def __init__(self, ark_binary_data):
        self.r = ark_binary_data.read_byte()
        self.g = ark_binary_data.read_byte()
        self.b = ark_binary_data.read_byte()
        self.a = ark_binary_data.read_byte()

    def __repr__(self):
        return f'r : {self.r}, g : {self.g}, b : {self.b}, a : {self.a}'

