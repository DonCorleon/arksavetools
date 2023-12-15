from typing import Optional, Dict
from uuid import UUID

from arksavetools.structs.arkVector import ArkVector


class SaveContext:
    def __init__(self):
        self.parts = []
        self.names = False
        self.actorLocations: Dict[UUID, ArkVector] = {}
        self.saveVersion: int = 0
        self.gameTime: float = 0.0  # Uncertain, presumed to be a float

    def has_name_table(self):
        if self.names != False:
            return True
        return False

    def get_actor_location(self, uuid: UUID) -> Optional[ArkVector]:
        return self.actorLocations.get(uuid)

    def set_parts(self, parts):
        self.parts = parts

    def set_names(self, names):
        self.names = names

    def __str__(self):
        return f'gameTime : {self.gameTime}, saveVersion : {self.saveVersion}, names : {self.names}, parts : {self.parts}'
