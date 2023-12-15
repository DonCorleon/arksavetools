class ArkRotator:
    def __init__(self, binary_data):
        self.pitch = binary_data.read_double()
        self.yaw = binary_data.read_double()
        self.roll = binary_data.read_double()

    def __repr__(self):
        return f'pitch : {self.pitch}, yaw : {self.yaw}, roll : {self.roll}'
