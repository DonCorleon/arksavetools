import sqlite3
import uuid
from pathlib import Path

from arksavetools.arkBinaryData import ArkBinaryData
from arksavetools.arkGameObject import ArkGameObject
from arksavetools.arkSaveContext import SaveContext

from arksavetools.config import *
from arksavetools.constants import constants
from arksavetools.libs.helpers import timer_func


class BaseConfig:
    def __init__(self):
        self.uuid_Filter = ''
        self.class_name_filter = 'Character_BP_C'
        self.game_object_filter = ''

@timer_func
class ArkSaveDatabase:
    MAX_IN_LIST = 10000

    def __init__(self, ark_file):
        self.sqlite_db = ark_file
        self.connection = sqlite3.connect(ark_file)
        self.save_context = SaveContext()
        self.read_header()
        self.read_actor_locations()
        self.progress = 0

    def output_json(self):
        pass

    def output_object(self, reader_configuration, wanted_object):
        with self.connection as conn:
            logger.info(f'Looking for {wanted_object}')
            cursor = conn.execute("SELECT key, value FROM game")
            for row in cursor:
                uuid = str(self.byte_array_to_uuid(row[0]))
                if uuid == wanted_object or wanted_object.lower() == 'all':
                    filename = f'binfiles/{uuid}.bin'
                    byte_buffer = row[1]
                    logger.debug(byte_buffer)
                    logger.info(f'Record {uuid} found. Outputting to file...')
                    with open(filename, 'wb') as f:
                        f.write(byte_buffer)
        self.connection.close()

    def player_locations(self, actor_objects=None):
            players = []
            if not actor_objects:
                actors = []
                for actor in self.save_context.actorLocations:
                    actors.append(str(actor))
                actor_objects = self.get_game_objects_by_ids(actors)
            for actor in actor_objects:
                try:
                    if 'player' in actor_objects[actor].name.lower():
                        name = None
                        location = None
                        for element in actor_objects[actor].properties:
                            if element.name == 'PlayerName':
                                name = element.value
                            if element.name == 'SavedBaseWorldLocation':
                                location = element.value
                        if name != None and location != None:
                            players.append({'name': name, 'location': location})
                except Exception as e:
                    logger.warning(f"Couldn't locate {actor} in  actorTransforms : {e}")
            return players

    def read_actor_locations(self):
        actors = self.get_custom_value('ActorTransforms')
        if actors:
            self.save_context.actorLocations = actors.read_actor_transforms()
            logger.info(f'Found {len(self.save_context.actorLocations)} Actor Locations')
        else:
            logger.debug('No actor transforms found')
    def read_header(self):
        header_data = self.get_custom_value("SaveHeader")
        self.save_context.save_version = header_data.read_short()
        logger.info(f'Save Version {self.save_context.save_version}')

        name_table_offset = header_data.read_int()
        logger.info(f'Name Table Offset {name_table_offset}')

        self.save_context.game_time = header_data.read_double()
        logger.info(f'Game Time {self.save_context.game_time}')

        self.save_context.set_parts(self.read_parts(header_data))

        # Unknown data, seems to be always 0...
        header_data.expect(0, header_data.read_int())
        header_data.expect(0, header_data.read_int())

        number_of_names = header_data.read_int()
        logger.info(f'Names in Table : {number_of_names}')

        self.save_context.set_names(self.read_names(header_data))

    def read_parts(self, header_data):
        parts = []
        number_of_parts = header_data.read_uint32()
        for i in range(number_of_parts):
            try:
                self.progress = (100 / number_of_parts) * i
            except:
                self.progress = 0
            try:
                name = header_data.read_string()
                parts.append(name)
                header_data.read_int()
            except Exception as e:
                logger.warning(f'Part {i} had an issue reading the name : {e}')
        logger.info(f'Completed reading {number_of_parts} parts. Added {len(parts)}')
        self.progress = 100
        return parts

    @timer_func
    def get_game_objects(self, reader_configuration):
        with self.connection as conn:
            cursor = conn.execute("SELECT key, value FROM game")
            game_objects = {}
            row_count = len(cursor.fetchall())
            cursor = conn.execute("SELECT key, value FROM game")
            i = 0
            for row in cursor:
                i += 1
                try:
                    self.progress = (100 / row_count) * i
                except:
                    self.progress = 0
                uuid = self.byte_array_to_uuid(row[0])
                if reader_configuration.uuid_Filter is None:
                    continue
                byte_buffer = ArkBinaryData(row[1], self.save_context)
                class_name = byte_buffer.read_name()
                if reader_configuration.class_name_filter is None:
                    continue
                start_of_object = byte_buffer.get_position()
                try:
                    ark_game_object = ArkGameObject(uuid, class_name, byte_buffer)
                    if reader_configuration.game_object_filter is None:
                        continue

                    game_objects[uuid] = ark_game_object
                except Exception as e:
                    logging.error(f"Error parsing {uuid}, debug info following: {e}")
                    byte_buffer.set_position(start_of_object)
                    ArkGameObject(uuid, class_name, byte_buffer)
                    raise e
            return game_objects

    def remove_leading_slash(self, path):
        if path.startswith("/"):
            return Path(path[1:])
        return Path(path)

    def read_names(self, header_data):
        names = {}
        while header_data.has_more():
            identifier = header_data.read_int()
            name = header_data.read_string()
            names[identifier] = name
        return names

    def get_custom_value(self, key):
        cursor = self.connection.execute(f"SELECT value FROM custom WHERE key = '{key}' LIMIT 1")
        result = cursor.fetchone()
        if result is not None:
            return ArkBinaryData(result[0])
        return None

    def close(self):
        self.connection.close()

    def get_game_objects_by_ids(self, uuids):
        if not uuids:
            return {}

        if len(uuids) > self.MAX_IN_LIST:
            game_objects = {}
            uuid_list = list(uuids)
            for i in range(0, len(uuid_list), self.MAX_IN_LIST):
                game_objects.update(self.get_game_objects_by_ids(uuid_list[i:i + self.MAX_IN_LIST]))
            return game_objects
        placeholders=[]
        for uuid in uuids:
            placeholders.append(self.uuid_to_byte_array(uuid))
        game_objects = {}

        with self.connection as conn:
            cursor = conn.execute(f"SELECT key, value FROM game")

            for row in cursor:
                if row[0] in placeholders:
                    actual_uuid = self.byte_array_to_uuid(row[0])
                    byte_buffer = ArkBinaryData(row[1], self.save_context)
                    class_name = byte_buffer.read_name()
                    game_objects[actual_uuid] = ArkGameObject(actual_uuid, class_name, byte_buffer)

        return game_objects

    def get_game_object_by_id(self, uuid):
        return self.get_game_objects_by_ids([uuid]).get(uuid)

    @staticmethod
    def byte_array_to_uuid(bytes_data):
        return uuid.UUID(bytes=bytes_data)

    @staticmethod
    def uuid_to_byte_array(uu_id):
        uuid_bytes = uuid.UUID(uu_id)
        return uuid_bytes.bytes

    @staticmethod
    def get_tamed_dinos(objects, isbaby=False):
        tamed_dinos = []
        for object in objects:
            has_tamed_property=False
            has_baby_property=False
            if 'Character_BP_' in objects[object].name:
                for element in objects[object].properties:
                    if 'TamedAtTime' in element.name:
                        has_tamed_property = True
                    if 'bIsBaby' in element.name:
                        has_baby_property = True
            if isbaby:
                if has_tamed_property and has_baby_property:
                    tamed_dinos.append(objects[object].uuid)
            else:
                if has_tamed_property:
                    tamed_dinos.append(objects[object].uuid)
        return tamed_dinos

    @staticmethod
    def get_wild_dinos(objects):
        wild_dinos = []
        for object in objects:
            has_tamed_property=False
            if 'Character_BP_C' in objects[object].name:
                for element in objects[object].properties:
                    if 'TamedAtTime' in element.name:
                        has_tamed_property = True
                        break
            if has_tamed_property == False:
                wild_dinos.append(objects[object].uuid)
        return wild_dinos

    @staticmethod
    def get_dinos(objects):
        dinos = []
        for object in objects:
            if 'Character_BP_C' in objects[object].name:
                dinos.append(objects[object].uuid)
        return dinos

    @staticmethod
    def get_event_dinos(objects):
        event_dinos = []
        for object in objects:
            if '_Character_BP_Event_C' in objects[object].name:
                event_dinos.append(objects[object].uuid)
        return event_dinos

    @staticmethod
    def get_object_types(objects, remove_filter=[], search=[]):
        object_types = {}
        for object in objects:
            if search:
                is_it_there = False
                for filter_element in search:
                    if filter_element in objects[object].name:
                        is_it_there = True
                if is_it_there:
                    object_types.update({objects[object].name: 0})
            elif remove_filter:
                is_it_there = True
                for filter_element in remove_filter:
                    if filter_element in objects[object].name:
                        is_it_there = False
                if is_it_there:
                    object_types.update({objects[object].name: 0})
            else:
                object_types.update({objects[object].name: 0})
        return object_types


class dino_container():
    def __init__(self):
        self.id = None
        self.sex = 'Male'
        self.level = None
        self.name = None
        self.clazz = None
        self.statvalues = []
        self.statpoints = []
        self.statpointsadded = []
        self.colours = []
        self.experience = None
        self.location = None
        self.stats = {'Health': 0, 'Stamina': 0, 'Oxygen': 0, 'Food': 0, 'Weight': 0, 'Damage': 0, 'Unknown': 0}

    def populate(self, dino_id, objects):
        self.id = dino_id
        self.clazz = objects[dino_id].name
        for element in objects[dino_id].properties:
            if element.name == 'ColorSetIndices':
                self.colours.append(self.add_colours(element.value, element.position))
            if element.name == 'bIsFemale':
                self.sex = 'Female'
            if element.name == 'SavedBaseWorldLocation':
                self.location = element.value.lat_long_conversion()
            if element.name == 'MyCharacterStatusComponent':
                for subelement in objects[element.value].properties:
                    if subelement.name == 'NumberOfLevelUpPointsApplied':
                        self.statpoints.append({'value': subelement.value, 'position': subelement.position})
                        self.add_stats(subelement.position, subelement.value)
                    if subelement.name == 'NumberOfLevelUpPointsAppliedTamed':
                        self.statpointsadded.append({'value': subelement.value, 'position': subelement.position})
                        self.add_stats(subelement.position, subelement.value)
                    if subelement.name == 'CurrentStatusValues':
                        self.statvalues.append({'value': subelement.value, 'position': subelement.position})
                    if subelement.name == 'BaseCharacterLevel':
                        self.level = subelement.value
                    if subelement.name == 'ExperiencePoints':
                        self.experience = subelement.value
    def add_colours(self,colour_index, position):
        for k in constants.krakoen_dino_colours:
            if k['id'] == colour_index:
                colour_name = k['name']
                for key in constants.dino_colors:
                    if colour_name == key['name']:
                        rgb = key['rgb']
                        return [colour_index, colour_name, rgb, position]
        logger.warning(f'Unknown colour found on dino : {colour_index}')
        return [colour_index, 'Unknown', (0, 0, 0), position]
    def add_stats(self, position, value):
        if position == 0:
            self.stats['Health'] += value
        elif position == 1:
            self.stats['Stamina'] += value
        elif position == 3:
            self.stats['Oxygen'] += value
        elif position == 4:
            self.stats['Food'] += value
        elif position == 7:
            self.stats['Weight'] += value
        elif position == 8:
            self.stats['Damage'] += value
        else:
            self.stats['Unknown'] += value

    def __str__(self):
        return f'Class : {self.clazz}, Name : {self.name}, Level : {self.level}'

if __name__ == '__main__':
    class GameObjectReaderConfiguration:
        def __init__(self):
            self.uuid_Filter = ''
            self.class_name_filter = 'Character_BP_C'
            self.game_object_filter = ''


    def is_uuid(test):
        try:
            uuid.UUID(str(test))
            return True
        except:
            return False

    def cheat_doexit():
        save.close()
        logger.info('Closing as requested')
        exit()

    dbfile = 'Z:/ASAServer/ShooterGame/Saved/SavedArks/TheIsland_WP/TheIsland_WP.ark'
    save = ArkSaveDatabase(dbfile)
    readerConfiguration = GameObjectReaderConfiguration()
    objects = save.get_game_objects(readerConfiguration)

    for entry in save.get_object_types(objects, remove_filter=['_Character_BP_C', 'InstancedFoliageActor_', 'InventoryComponent_', 'CharacterStatus_BP_', 'NPC', 'Manager']): #, search=['PrimalItem_RecipeNote']):
        print(entry)
