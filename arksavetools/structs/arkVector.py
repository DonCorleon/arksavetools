import math


class ArkVector:
    def __init__(self, byte_buffer):
        self.x = byte_buffer.read_double()
        self.y = byte_buffer.read_double()
        self.z = byte_buffer.read_double()

    def lat_long_conversion(self):
        lat = math.floor(self.y / 685) / 10 + 50
        lon = math.floor(self.x / 685) / 10 + 50
        return [lat, lon]

    def __repr__(self):
        return f'x : {self.x}, y : {self.y}, z : {self.z}, lat/lon : {self.lat_long_conversion()}'
