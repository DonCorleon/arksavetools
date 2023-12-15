import math


class ActorTransform:
    def __init__(self, byte_buffer):
        self.x = byte_buffer.read_double()
        self.y = byte_buffer.read_double()
        self.z = byte_buffer.read_double()
        self.pitch = byte_buffer.read_double();
        self.yaw = byte_buffer.read_double();
        self.roll = byte_buffer.read_double();
        byte_buffer.skip_bytes(8);

    def lat_long_conversion(self):
        lat = math.floor(self.y / 685) / 10 + 50
        lon = math.floor(self.x / 685) / 10 + 50
        return [lat, lon]

    def __repr__(self):
        return f'x : {self.x}, y : {self.y}, z : {self.z}, lat/lon : {self.lat_long_conversion()}'

if __name__ == '__main__':
    x = -196926.73090169512
    y = -195115.46730948595
    lat = math.floor(y / 685) / 10 + 50
    lon = math.floor(x / 685) / 10 + 50
    print(lat, lon)
