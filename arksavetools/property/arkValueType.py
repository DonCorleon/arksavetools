from collections import OrderedDict
from typing import List

class ArkValueType():
    Boolean = "BoolProperty"
    Byte = "ByteProperty"
    Float = "FloatProperty"
    Int = "IntProperty"
    Name = "NameProperty"
    Object = "ObjectProperty"
    String = "StrProperty"
    Struct = "StructProperty"
    Array = "ArrayProperty"
    Double = "DoubleProperty"
    Int16 = "Int16Property"
    Int64 = "Int64Property"
    Int8 = "Int8Property"
    UInt16 = "UInt16Property"
    UInt32 = "UInt32Property"
    UInt64 = "UInt64Property"
    SoftObject = "SoftObjectProperty"
    Map = "MapProperty"


    def __init__(self, name, clazz):
        self.name = name
        self.clazz = clazz


    def from_name(struct_type):
        types= {
                "BoolProperty": 'Boolean',
                "ByteProperty": 'Byte',
                "FloatProperty": 'Float',
                "IntProperty": 'Int',
                "NameProperty": 'Name',
                "ObjectProperty": 'Object',
                "StrProperty": 'String',
                "StructProperty": 'Struct',
                "ArrayProperty": 'Array',
                "DoubleProperty": 'Double',
                "Int16Property": 'Int16',
                "Int64Property": 'Int64',
                "Int8Property": 'Int8',
                "UInt16Property": 'UInt16',
                "UInt32Property": 'UInt32',
                "UInt64Property": 'UInt64',
                "SoftObjectProperty": 'SoftObject',
                "MapProperty": 'Map'
        }
        try:
            return types[struct_type]
        except:
            return None
