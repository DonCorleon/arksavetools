import uuid

from arksavetools.arkPropertyContainer import ArkPropertyContainer
from arksavetools.arkSaveContext import SaveContext
from arksavetools.structs.arkRotator import ArkRotator
from arksavetools.structs.arkVector import ArkVector
import json

class ArkObject(ArkPropertyContainer):
    def __init__(self, reader):
        super().__init__()
        self.uuid = uuid.UUID(bytes_le=reader.read_bytes(16))
        self.className = reader.read_string()
        self.item = reader.read_boolean()
        self.names = reader.read_strings_array()
        self.fromDataFile = reader.read_boolean()
        self.dataFileIndex = reader.read_int()
        if reader.read_boolean():
            self.vector = ArkVector(reader)
            self.rotator = ArkRotator(reader)
        else:
            self.vector = None
            self.rotator = None
        self.propertiesOffset = reader.read_int()
        reader.expect(0, reader.read_int())
        self.reader = reader
        #self.save_context = SaveContext()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):
        return f"UUID: {self.uuid}, item: {self.item}, dataFileIndex: {self.dataFileIndex}, className: {self.className}, dataFileIndex: {self.dataFileIndex}, propertiesOffset: {self.propertiesOffset}, vector : {self.vector}, rotator : {self.rotator}, names: {self.names}"
