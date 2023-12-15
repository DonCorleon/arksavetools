class ArkUniqueNetIdRepl:
    def __init__(self, byte_buffer):
        self.unknown = byte_buffer.read_byte()
        self.value_type = byte_buffer.read_string()
        length = byte_buffer.read_byte()
        self.value = byte_buffer.read_bytes_as_hex(length)

    def __repr__(self):
        return f'value_type : {self.value_type}, value : {self.value}'
