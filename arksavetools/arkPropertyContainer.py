from typing import Type, List, Optional, Union
from arksavetools.config import *
from property.arkProperty import ArkProperty

class ArkPropertyContainer:
    def __init__(self):
        self.properties = []

    def __repr__(self):
        result=[]
        for prop in self.properties:
            result.append(prop)
        return str(result)


    def read_properties(self, byte_buffer):
        last_property_position = byte_buffer.get_position()
        try:
            ark_property = ArkProperty.read_property(byte_buffer)
            while byte_buffer.has_more():
                if ark_property is not None:
                    self.properties.append(ark_property)
                last_property_position = byte_buffer.byte_buffer.position()
                ark_property = ArkProperty.read_property(byte_buffer)
                if ark_property is None or ark_property.name == "None":
                    return
        except Exception as e:
            logger.debug(f"Could not read properties, {last_property_position} -  {e}")
            byte_buffer.set_position(last_property_position)
            byte_buffer.debug_binary_data(byte_buffer.read_bytes(byte_buffer.size() - byte_buffer.get_position()))
            raise e

    def has_property(self, name: str) -> bool:
        return any(element.name == name for element in self.properties)

    def find_property(self, name: str) -> Optional[ArkProperty]:
        return next((element for element in self.properties if element.name == name), None)

    def find_property_by_position(self, name: str, position: int) -> Optional[ArkProperty]:
        return next((element for element in self.properties if element.name == name and element.position == position), None)

    def get_property_value(self, name: str, clazz: Type):
        element = self.find_property(name)
        return element.value if element else None

    def get_property_value_by_position(self, name: str, position: int, clazz: Type):
        property = self.find_property_by_position(name, position)
        return property.value if property else None

    def get_properties(self, name: str, clazz: Type):
        return [property for property in self.properties if property.name == name]

    def get_properties_by_position(self, name: str, clazz: Type):
        properties = self.get_properties(name, clazz)
        return {property.position: property.value for property in properties}
