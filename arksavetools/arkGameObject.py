from arksavetools.arkPropertyContainer import ArkPropertyContainer
from arksavetools.config import logger
import uuid as uUId
import json

class ArkGameObject(ArkPropertyContainer):
    def __init__(self, uuid, blueprint, byte_buffer):
        super().__init__()
        self.uuid = uuid
        self.blueprint = blueprint

        byte_buffer.skip_bytes(8)
        self.name = byte_buffer.read_single_name()
        self.item = byte_buffer.read_boolean()
        self.class_name = byte_buffer.read_single_name()
        byte_buffer.skip_bytes(1)
        self.read_properties(byte_buffer)
        '''
        try:
            if 'Cryopod' in self.name:
                logger.debug(f'name : {self.name}, uuid : {self.uuid}, properties : {self.properties} buffer len : {len(byte_buffer.byte_buffer.byte_buffer)}\n')
        except Exception as e:
            logger.error(f'Error looking for pods in {self},  {e}')
        '''
    def __repr__(self):
        return f"UUID: {self.uuid}, Blueprint: {self.blueprint}, Name: {self.name}, Class Name: {self.class_name}, Item: {self.item}"
