from arksavetools.arkBinaryData import ArkBinaryData
from arksavetools.arkObject import ArkObject
from arksavetools.arkSaveContext import SaveContext
from arksavetools.config import logger


class ArkArchive:
    def __init__(self, file_path):
        self.data = None
        self.objects = []
        self.load_objects(file_path)
        self.save_context = None

    def load_objects(self, file_path):
        self.save_context = SaveContext()
        with open(file_path, 'rb') as file:
            filedata = file.read()
            self.data = ArkBinaryData(filedata, self.save_context)
            self.save_context.save_version = self.data.read_int()
            logger.info(f'Profile Save Version : {self.save_context.save_version}')

            if self.save_context.save_version != 5:
                raise RuntimeError("Unsupported archive version " + str(self.save_context.save_version))

            count = self.data.read_int()
            logger.info(f'Count : {count}')
            for _ in range(count):
                self.objects.append(ArkObject(self.data))

            logger.info('Loading properties from object/s')
            for obj in self.objects:
                self.data.set_position(obj.propertiesOffset)
                obj.read_properties(self.data)

    def get_object_by_class(self, class_name):
        return next((obj for obj in self.objects if obj.className == class_name), None)

    def get_object_by_uuid(self, uuid):
        return next((obj for obj in self.objects if obj.uuid == uuid), None)

    def get_object_by_index(self, index):
        return self.objects[index]
