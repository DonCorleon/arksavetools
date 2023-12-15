from arksavetools.property.arkObjectReference import ObjectReference
from arksavetools.property.arkValueType import ArkValueType
from arksavetools.structs.arkStructType import from_type_name
from arksavetools.structs.arkUnknownStruct import UnknownStruct
from arksavetools.config import *

class ArkProperty:
    def __init__(self, name, type, position, unknown_byte, value):
        self.name = name
        self.type = type
        self.position = position
        self.unknown_byte = unknown_byte
        self.value = value
        #logger.debug(f'    AP >> value:{self.value}')

    def __str__(self):
        return f'Description >> name : {self.name}, type : {self.type}, value : {self.value}'
    
    @staticmethod
    def read_property(byte_buffer, in_array=False):
        key = byte_buffer.read_main_name()
        if key is None or key == "None":
            return None

        value_type_name = byte_buffer.read_name()
        if value_type_name is None:
            return None

        data_size = byte_buffer.read_int()
        position = byte_buffer.read_int()

        start_data_position = byte_buffer.get_position()

        if value_type_name == "BoolProperty":
            value = byte_buffer.read_short()
            return ArkProperty(key, value_type_name, position, 0, value != 0)
        elif value_type_name == "FloatProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_float())
        elif value_type_name == "NameProperty":
            unknown_byte = byte_buffer.read_byte()
            name = byte_buffer.read_single_name()
            unknown_int = byte_buffer.read_int()
            return ArkProperty(key, value_type_name, position, unknown_byte, name)
        elif value_type_name == "IntProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_int())
        elif value_type_name == "Int8Property":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_byte())
        elif value_type_name == "DoubleProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_double())
        elif value_type_name == "UInt32Property":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_uint32())
        elif value_type_name == "UInt64Property":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_uint64())
        elif value_type_name == "UInt16Property":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_uint16())
        elif value_type_name == "Int16Property":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_short())
        elif value_type_name == "Int64Property":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_long())
        elif value_type_name == "StrProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_string())
        elif value_type_name == "ByteProperty":
            enum_type = byte_buffer.read_name()
            if enum_type == "None":
                return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_byte())
            else:
                return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_name())
        elif value_type_name == "StructProperty":
            struct_type = byte_buffer.read_name()
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), ArkProperty.read_struct_property(byte_buffer, data_size, struct_type, in_array))
        elif value_type_name == "ObjectProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), ArkProperty.read_object_property(byte_buffer))
        elif value_type_name == "SoftObjectProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), byte_buffer.read_bytes_as_hex(data_size))
        elif value_type_name == "ArrayProperty":
            return ArkProperty.read_array_property(key, value_type_name, position, byte_buffer, data_size)
        elif value_type_name == "MapProperty":
            return ArkProperty(key, value_type_name, position, byte_buffer.read_byte(), ArkProperty.read_property(byte_buffer))
        else:
            logger.error("Unknown property type {} with data size {} at position {}".format(value_type_name, data_size, start_data_position))
            raise RuntimeError("Unknown property type {} with data size {} at position {}".format(value_type_name, data_size, start_data_position))

    @staticmethod
    def read_struct_array(byte_buffer, array_type, count):
        struct_array = []
        name = byte_buffer.read_name()
        value_type = byte_buffer.read_name()
        data_size = byte_buffer.read_int()
        position = byte_buffer.read_int()
        struct_type = byte_buffer.read_name()
        unknown_byte = byte_buffer.read_byte()
        byte_buffer.skip_bytes(16)
        for _ in range(count):
            struct_array.append(ArkProperty.read_struct_property(byte_buffer, data_size, struct_type, True))
        return struct_array

    @staticmethod
    def read_object_property(byte_buffer):
        return ObjectReference(byte_buffer)

    @staticmethod
    def read_array_object_property(byte_buffer):
        is_name = byte_buffer.read_short() == 1
        if is_name:
            return byte_buffer.read_name()
        else:
            object_id = byte_buffer.read_uuid()
            return object_id

    @staticmethod
    def read_struct_property(byte_buffer, data_size, struct_type, in_array):
        start_position = byte_buffer.get_position()
        if not in_array:
            byte_buffer.skip_bytes(16)
        ark_struct_type = from_type_name(struct_type)
        if ark_struct_type is not None:
            return ark_struct_type(byte_buffer)

        position = byte_buffer.get_position()
        try:
            properties = ArkProperty.read_struct_properties(byte_buffer)
            if byte_buffer.get_position() != position + data_size and not in_array:
                raise Exception("Position {} before reading struct type {} of size {}, expecting end at {}, but was {} after reading struct".format(position, struct_type, data_size, position + data_size, byte_buffer.get_position()))
            return properties
        except Exception as e:
            logger.error(f"read_struct_property >> Failed to read struct, reading as blob {e}")
            byte_buffer.set_position(start_position)
            data = byte_buffer.read_bytes(data_size - 4)
            logger.error(data)
            return UnknownStruct(struct_type, byte_buffer.bytes_to_hex(data))

    @staticmethod
    def read_struct_properties(byte_buffer):
        properties = []
        struct_property = ArkProperty.read_property(byte_buffer)
        while struct_property is not None:
            properties.append(struct_property)
            struct_property = ArkProperty.read_property(byte_buffer)
        return properties

    @staticmethod
    def read_array_property(key, data_type, position, byte_buffer, data_size):
        array_type = byte_buffer.read_name()
        end_of_struct = byte_buffer.read_byte()
        array_length = byte_buffer.read_int()
        buffer_position = byte_buffer.get_position()
        if array_type == "StructProperty":
            try:
                struct_array = ArkProperty.read_struct_array(byte_buffer, array_type, array_length)
                bytes_left = buffer_position + data_size - 4 - byte_buffer.get_position()
                if bytes_left != 0:
                    logger.error(f"Struct array read incorrectly, Key:{key}, Type:{array_type}, Length:{array_length}")
                    logger.error(f"Struct array read incorrectly, bytes left to read {bytes_left} of {data_size}: {struct_array}")
                    if bytes_left > 0:
                        byte_buffer.debug_binary_data(byte_buffer.read_bytes(bytes_left))
                return ArrayProperty(key, data_type, position, end_of_struct, array_type, array_length, struct_array, None)
            except Exception as e:
                logger.error("Failed to read struct array \n {e}")
                byte_buffer.set_position(buffer_position)
                data = byte_buffer.read_bytes(data_size - 4)
                byte_buffer.debug_binary_data(data)

                return ArrayProperty(key, data_type, position, end_of_struct, array_type, array_length, byte_buffer.bytes_to_hex(data))
        else:
            expected_end_of_array_position = buffer_position + data_size - 4
            array = []
            value_type = ArkValueType.from_name(array_type)
            if value_type is None:
                raise RuntimeError(f"Unknown array type {array_type} at position {byte_buffer.get_position()}")
            try:
                for i in range(array_length):
                    result = ArkProperty.read_property_value(array_type, byte_buffer)
                    array.append(result)
                if expected_end_of_array_position != byte_buffer.get_position():
                    raise RuntimeError(f"Array read incorrectly, bytes left: {expected_end_of_array_position - byte_buffer.get_position()} of {data_size}({expected_end_of_array_position}) (reading as binary data instead)")
            except Exception as e:
                byte_buffer.set_position(buffer_position)
                content = f'{array_type} : {byte_buffer.bytes_to_hex(byte_buffer.read_bytes(data_size - 4))}'
                logger.error(f"Array {key} of type {array_type} and length {array_length} read incorrectly at {buffer_position}, returning blob data instead:{CustomFormatter.yellow} {content}\n{e}")
                logger.info(array)
                return ArrayProperty(key, data_type, position, end_of_struct, array_type, array_length, content)

            return ArrayProperty(key, data_type, position, end_of_struct, array_type, array_length, array)

    @staticmethod
    def read_soft_object_property_value(byte_buffer):
        obj_name = byte_buffer.read_name()
        expected_bytes = byte_buffer.read_bytes_as_hex(4)
        byte_buffer.expect("00 00 00 00 ", expected_bytes)
        return obj_name


    @staticmethod
    def read_property_value(value_type, byte_buffer):
        if value_type in [ArkValueType.Byte, ArkValueType.Int8]:
            return byte_buffer.read_byte()
        elif value_type == ArkValueType.Double:
            return byte_buffer.read_double()
        elif value_type == ArkValueType.Float:
            return byte_buffer.read_float()
        elif value_type == ArkValueType.Int:
            return byte_buffer.read_int()
        elif value_type == ArkValueType.Object:
            return ArkProperty.read_object_property(byte_buffer)
        elif value_type == ArkValueType.String:
            return byte_buffer.read_string()
        elif value_type == ArkValueType.UInt32:
            return byte_buffer.read_uint32()
        elif value_type == ArkValueType.UInt64:
            return byte_buffer.read_uint64()
        elif value_type == ArkValueType.UInt16:
            return byte_buffer.read_uint16()
        elif value_type == ArkValueType.Int16:
            return byte_buffer.read_short()
        elif value_type == ArkValueType.Int64:
            return byte_buffer.read_long()
        elif value_type == ArkValueType.Name:
            return byte_buffer.read_name()
        elif value_type == ArkValueType.Boolean:
            return byte_buffer.read_short() == 1
        elif value_type == ArkValueType.Struct:
            return ArkProperty.read_struct_property(byte_buffer, byte_buffer.read_int())
        elif value_type == ArkValueType.SoftObject:
            return ArkProperty.read_soft_object_property_value(byte_buffer)
        else:
            raise RuntimeError("Cannot read value type yet: " + str(value_type) + " at position " + str(byte_buffer.get_position()))


class ArrayProperty(ArkProperty):
    def __init__(self, key, type, index, end_of_struct, array_type, array_length, data, rest=None):
        super().__init__(key, type, index, end_of_struct, data)
        self.array_type = array_type
        self.array_length = array_length
        self.rest = rest

