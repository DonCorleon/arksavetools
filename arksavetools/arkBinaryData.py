from typing import Dict, Union
import struct
import uuid

from arksavetools.arkSaveContext import SaveContext
from arksavetools.structs.arkActorTransform import ActorTransform
from arksavetools.structs.arkVector import ArkVector
from arksavetools.config import *


class byte_Buffer:
    def __init__(self, data):
        self.data = memoryview(data)
        self.byte_buffer = memoryview(data)
        self._position = 0

    def position(self):
        return self._position

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def inc_position(self,inc):
        self._position += inc

    def new_buff_pos(self, position):
        self.byte_buffer = memoryview(self.data)
        self.byte_buffer = self.byte_buffer[position:]


class ArkBinaryData:

    def __init__(self, data: bytes, save_context: SaveContext = None):
        self.byte_buffer = byte_Buffer(data)
        self.save_context = save_context

    def read_string(self) -> Union[str, None]:
        length = self.read_int()

        if length == 0:
            return None

        is_multi_byte = length < 0
        if is_multi_byte:
            result = self.byte_buffer.byte_buffer[:abs(length) * 2].cast('c').toreadonly().tobytes().decode('utf-16le', errors='ignore')
            self.skip_bytes(abs(length) * 2)
            return result
        read_bytes = self.read_bytes(length - 1)
        result = read_bytes.decode('utf-8')
        self.skip_bytes(1)
        return result

    def read_chars(self, size: int) -> str:
        self.byte_buffer.inc_position(size)
        return self.byte_buffer.byte_buffer[:size * 2].cast('c').toreadonly().tobytes().decode('utf-16le')

    def skip_bytes(self, count: int):
        self.byte_buffer.inc_position(count)
        self.byte_buffer.byte_buffer = self.byte_buffer.byte_buffer[count:]

    def read_int(self) -> int:
        value = int.from_bytes(self.byte_buffer.byte_buffer[:4], 'little', signed=True)
        self.skip_bytes(4)
        return value

    def has_more(self) -> bool:
        return len(self.byte_buffer.byte_buffer) > 0

    def read_bytes(self, count: int) -> bytes:
        data = self.byte_buffer.byte_buffer[:count].tobytes()
        self.skip_bytes(count)
        return data

    def read_boolean(self) -> bool:
        return self.read_int() != 0

    def read_float(self) -> float:
        value = struct.unpack('f', self.byte_buffer.byte_buffer[:4])[0]
        self.skip_bytes(4)
        return value

    def log_rest_of_data_in_hex_form(self):
        data = self.byte_buffer.byte_buffer.tobytes()
        logger.debug(self.bytes_to_hex(data))

    def bytes_to_hex(self, bytes_data: bytes) -> str:
        return ' '.join(f'{b:02X}' for b in bytes_data)

    def size(self) -> int:
        return len(self.byte_buffer.byte_buffer)

    def set_position(self, i: int):
        self.byte_buffer.set_position(i)
        self.byte_buffer.byte_buffer = self.byte_buffer.data[i:]

    def find_names(self):
        if not self.save_context.has_name_table():
            return
        logger.debug("--- Looking for names ---")
        for i in range(self.size() - 4):
            search_int=self.read_int()
            n = self.save_context.names.get(search_int)
            if n is not None:
                self.set_position(i)
                logger.debug(f"Found name: {n} at {i}")
                i += 3

    def read_double(self) -> float:
        value = struct.unpack('d', self.byte_buffer.byte_buffer[:8])[0]
        self.skip_bytes(8)
        return value

    def read_byte(self) -> int:
        value = self.byte_buffer.byte_buffer[0]
        self.skip_bytes(1)
        return value

    def read_name(self) -> str:
        if not self.save_context.has_name_table():
            return self.read_string()
        search_int=self.read_int()
        name = self.save_context.names.get(search_int)
        always_zero = self.read_int()
        if always_zero != 0:
            logger.error(f"Always zero is not zero: {always_zero}")
        return name

    def read_uuid_as_string(self) -> str:
        return self.read_uuid().hex

    def read_uuid(self) -> uuid.UUID:
        return uuid.UUID(bytes=self.read_bytes(16))

    def read_short(self) -> int:
        value = struct.unpack('h', self.byte_buffer.byte_buffer[:2])[0]
        self.skip_bytes(2)
        return value

    def read_bytes_as_hex(self, data_size: int) -> str:
        return self.bytes_to_hex(self.read_bytes(data_size))

    def get_position(self) -> int:
        return self.byte_buffer.position()

    def read_uint32(self) -> int:
        value = struct.unpack('I', self.byte_buffer.byte_buffer[:4])[0]
        self.skip_bytes(4)
        return value

    def read_uint16(self) -> int:
        value = struct.unpack('H', self.byte_buffer.byte_buffer[:2])[0]
        self.skip_bytes(2)
        return value

    def debug_binary_data(self, data: bytes):
        logger.warning("Data that was not recognized: " + self.bytes_to_hex(data))
        ArkBinaryData(data, self.save_context).find_names()

    def read_uint64(self) -> int:
        value = struct.unpack('Q', self.byte_buffer.byte_buffer[:8])[0]
        self.skip_bytes(8)
        return value

    def read_single_name(self) -> str:
        if not self.save_context.has_name_table():
            return self.read_string()
        name = self.save_context.names.get(self.read_int())
        return name
    def read_main_name(self) -> str:
        if not self.save_context.has_name_table():
            return self.read_string()
        name = self.save_context.names.get(self.read_int())
        some_int = self.read_int()
        return name

    def read_long(self) -> int:
        value = struct.unpack('q', self.byte_buffer.byte_buffer[:8])[0]
        self.skip_bytes(8)
        return value

    def read_actor_transforms(self) -> Dict[uuid.UUID, ArkVector]:
        locations = {}
        termination_uuid = uuid.UUID('00000000-0000-0000-0000-000000000000')
        while True:
            uuid_val = self.read_uuid()
            if uuid_val == termination_uuid:
                break
            locations.update({ uuid_val: ActorTransform(self)})
        return locations

    def expect(self, expected, read):
        if expected != read:
            logger.warning(f"Unexpected data, expected {expected}, but was {read}")

    def read_strings_array(self):
        result = []
        count = self.read_uint32()  # Assuming read_uint32() reads an unsigned 32-bit integer
        for i in range(count):
            result.append(self.read_string())  # Assuming read_string() reads a string
        return result

if __name__ == '__main__':
    pass
