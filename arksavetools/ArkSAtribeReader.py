from arksavetools.arkArchive import ArkArchive


class ArkTribe(ArkArchive):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_tribe(self):
        return self.get_object_by_class("/Script/ShooterGame.PrimalTribeData")

