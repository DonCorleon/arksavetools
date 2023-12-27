from arksavetools.config import logger


class ObjectReference:
    TYPE_ID = 0
    TYPE_PATH = 1
    TYPE_PATH_NO_TYPE = 2
    TYPE_NAME = 3
    TYPE_UUID = 4
    TYPE_UNKNOWN = -1

    def __new__(cls,reader):
        if reader.save_context.has_name_table():
            is_name = reader.read_short() == 1
            if is_name:
                cls.type = cls.TYPE_PATH
                return reader.read_name()
            else:
                cls.type = cls.TYPE_UUID
                cls.value = reader.read_uuid()
            return cls.value
        object_type = reader.read_int()
        if object_type == -1:
            cls.type = cls.TYPE_UNKNOWN
            cls.value = None
        elif object_type == 0:
            cls.type = cls.TYPE_ID
            cls.value = reader.read_int()
        elif object_type == 1:
            cls.type = cls.TYPE_PATH
            cls.value = reader.read_string()
        else:
            reader.skip_bytes(-4)
            cls.type = cls.TYPE_PATH_NO_TYPE
            cls.value = reader.read_string()

    def __repr__(self):
        return self.value

