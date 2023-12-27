from arksavetools.arkArchive import ArkArchive


class ArkTribe(ArkArchive):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_tribe(self):
        return self.get_object_by_class("/Script/ShooterGame.PrimalTribeData")

if __name__ == '__main__':
    from arksavetools.ArkSAprofileReader import ArkProfile

    dbfile = 'Z:/ASAServer/ShooterGame/Saved/SavedArks/TheIsland_WP/1825661156.arktribe'
    ark_tribe = ArkTribe(dbfile)

    try:

        for object in ark_tribe.objects:
            print(object)
            for property in object.properties:
                if property.name == 'MyData':
                    for subproperty in property.value:
                        print(subproperty.name, subproperty.value)
                else:
                    print(property.name, property.value)

    except Exception as e:
        print(f"Could not read profile: {e}")
