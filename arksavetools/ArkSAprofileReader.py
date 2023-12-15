from arksavetools.arkArchive import ArkArchive


class ArkProfile(ArkArchive):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_profile(self):
        return self.get_object_by_class("/Game/PrimalEarth/CoreBlueprints/PrimalPlayerDataBP.PrimalPlayerDataBP_C")


if __name__ == '__main__':

    dbfile = 'Z:/ASAServer/ShooterGame/Saved/SavedArks/TheIsland_WP/000230efb2b347ec80ee2bb5b99ea631.profilebak'
    ark_profile = ArkProfile(dbfile)

    try:

        for object in ark_profile.objects:
            print(object)
            for property in object.properties:
                if property.name == 'MyData':
                    for subproperty in property.value:
                        print(subproperty.name, subproperty.value)
                else:
                    print(property.name, property.value)

    except Exception as e:
        print(f"Could not read profile: {e}")
