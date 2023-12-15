from arksavetools.structs.arkColor import ArkColor
from arksavetools.structs.arkLinearColor import ArkLinearColor
from arksavetools.structs.arkQuat import ArkQuat
from arksavetools.structs.arkRotator import ArkRotator
from arksavetools.structs.arkUniqueNetIdRepl import ArkUniqueNetIdRepl
from arksavetools.structs.arkVector import ArkVector


class ArkStructType:
    def __init__(self, type_name, constructor):
        self.type_name = type_name
        self.constructor = constructor

ark_struct_types = {
    "LinearColor": ArkLinearColor,
    "Quat": ArkQuat,
    "Vector": ArkVector,
    "Rotator": ArkRotator,
    "UniqueNetIdRepl": ArkUniqueNetIdRepl,
    "Color": ArkColor
}

def from_type_name(type_name):
    return ark_struct_types.get(type_name)
