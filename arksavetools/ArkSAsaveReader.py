from arksavetools.arkSaveDatabase import ArkSaveDatabase, dino_container
from arksavetools.config import *

import uuid

from arksavetools.libs.helpers import *


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

if __name__ == '__main__':
    dbfile = 'Z:/ASAServer/ShooterGame/Saved/SavedArks/TheIsland_WP/TheIsland_WP.ark'
    save = ArkSaveDatabase(dbfile)
    readerConfiguration = GameObjectReaderConfiguration()


    ###  Process all game objects
    objects = save.get_game_objects(readerConfiguration)

    ###  Get a list of tamed dino uuids
    tamed = save.get_tamed_dinos(objects=objects, isbaby=False)

    ###  Get a list of wild dino uuids
    wild = save.get_wild_dinos(objects)

    ###  Get Player Names and Locations
    players = save.player_locations(objects)
    for player in players:
        print(f"Player {player['name']} is @ {player['location'].lat_long_conversion()}")
    cheat_doexit()



    creature_search = 'Character_BP_'
    search_string = creature_search
    #search_string = 'Baryonyx_Character_BP_C'
    #search_string = 'Thylacoleo_Character_BP_C'
    #search_string = 'DungBeetle_Character_BP_C'
    #search_string = 'Argent_Character_BP_C'
    search_string = 'Sheep_Character_BP_C'

    spacer = '--------------------------------------------'
    print(spacer)
    dinos = {}
    levels = {}
    count = 0
    min_level = 50
    #'''
    for id in wild:
        if search_string in objects[id].name:
            dino = dino_container()
            dino.populate(id, objects)
            if dino.level >= min_level:
                print()
                print(dino)
                print('    ID     :',dino.id)
                print('    Gender :',dino.sex)
                print('    Level  :',dino.level)
                print('    Stats  :',dino.statvalues)
                print('    Stats+ :',dino.stats)
                print('    Points :',dino.statpoints)
                print('    Added  :',dino.statpointsadded)
                print('    Colours:',dino.colours)
                print('    Exp.   :',dino.experience)
                print('    Loc.   :',dino.location)

    cheat_doexit()

    #'''
    #for object in objects:         #search all entities
    #for object in tamed:           #search only the tamed dinos
    for object in wild:             #search only the wild dinos
        if creature_search in objects[object].name:
            try:
                index = dinos[objects[object].name]
                index += 1
            except:
                index=1
            dinos.update({objects[object].name: index})


        if search_string in objects[object].name: # and len(objects[object].properties) >= 28:
            count += 1
            print(spacer)
            print()
            print()
            print(objects[object].uuid, objects[object].name)
            print(count)
            print(spacer)
            lastdino = objects[object]
            print('|_____',TerminalColors.MAGENTA, f'Items in object : {len(lastdino.properties)}',TerminalColors.RESET)
            for property in lastdino.properties:
                if is_uuid(property.value):
                    if property.value != lastdino.uuid:
                        try:
                            print('     ',property.name,TerminalColors.GREEN, property.value, TerminalColors.BLUE, property.position, TerminalColors.RESET)
                            print('     ','|_____',TerminalColors.MAGENTA, f'Items in object : {len(objects[property.value].properties)}',TerminalColors.RESET)
                            for subproperty in objects[property.value].properties:
                                if subproperty.name == 'InventoryItems':
                                    try:
                                        for inv_item in subproperty.value:
                                            try:
                                                result = objects[inv_item]
                                                print('     ','     ',TerminalColors.YELLOW,result.name,TerminalColors.GREEN, result.item, TerminalColors.BLUE, TerminalColors.RESET)
                                            except:
                                                print('     ','     ',TerminalColors.YELLOW,inv_item,TerminalColors.GREEN, inv_item, TerminalColors.BLUE, TerminalColors.RESET)
                                            for inv_property in result.properties:
                                                print('     ','     ','     ',TerminalColors.CYAN,inv_property.name,TerminalColors.GREEN, inv_property.value, TerminalColors.BLUE, inv_property.position, TerminalColors.RESET)
                                                try:
                                                    for item_property in inv_property.value:
                                                        print('     ','     ','     ','     ',TerminalColors.MAGENTA,item_property.name,TerminalColors.GREEN, item_property.value, TerminalColors.BLUE, item_property.position, TerminalColors.RESET)
                                                except:
                                                    pass
                                    except:
                                        print(TerminalColors.YELLOW,'     ','     ', subproperty.name, TerminalColors.GREEN, subproperty.value, TerminalColors.BLUE, subproperty.position, TerminalColors.RESET)
                                elif subproperty.name == 'BaseCharacterLevel':
                                    levels.update({objects[object].uuid: [subproperty.value]}) #, lastdino.properties.bIsFemale.value]})
                                    print(TerminalColors.YELLOW,'     ','     ', subproperty.name, TerminalColors.GREEN, subproperty.value, TerminalColors.BLUE, subproperty.position, TerminalColors.RESET)
                                else:
                                    print(TerminalColors.YELLOW,'     ','     ', subproperty.name, TerminalColors.GREEN, subproperty.value, TerminalColors.BLUE, subproperty.position, TerminalColors.RESET)
                        except:
                            print('     ',property.name,TerminalColors.GREEN, property.type, property.value, TerminalColors.BLUE, property.position, TerminalColors.RESET)
                    else:
                        print('     ',property.name,TerminalColors.GREEN, property.value, TerminalColors.BLUE, property.position, TerminalColors.RESET)        # should be Instigator only
                else:
                    print('     ',property.name,TerminalColors.GREEN, property.value, TerminalColors.BLUE, property.position, TerminalColors.RESET)            # should be every other property
                continue
    save.close()
    print(spacer)
    print('Found', count, search_string)
    print(spacer)

    print(spacer)
    print_sorted_dict(dinos)
    print(len(dinos))

    cheat_doexit()

    print(spacer)
    print_dict(levels)
    print(spacer)
    '''
    
    00 00 C1 9A 
    20 BF B1 8B 
    FD 44 A2 BD 
    D1 26 80 44 
    F6 F4
    
    
Sample output

TamerString Don Corleon
TamedName F2
bIsFemale True
bServerInitializedDino True
ColorSetIndices 34
ColorSetIndices 38
ColorSetIndices 34
ColorSetIndices 33
ColorSetIndices 96
ColorSetNames Dino Darker Grey
ColorSetNames Red
ColorSetNames BigFoot5
ColorSetNames Dino Darker Grey
ColorSetNames Dino Dark Brown
ColorSetNames Cammo
RequiredTameAffinity 17000.0
OwningPlayerID 390082751
OwningPlayerName Don Corleon
TamingLastFoodConsumptionTime 200402175.33002028
LastTameConsumedFoodTime 200395653.1473542
DinoID1 395589330
DinoID2 195065948
TamedAggressionLevel 0
UntamedPoopTimeCache 376.1905822753906
LastEggSpawnChanceTime 200401982.19904792
OriginalNPCVolumeName NPCZoneVolume
TamedAtTime 200092028.3535774
LastUpdatedBabyAgeAtTime 200092028.3535774
LastUpdatedMatingAtTime 200402175.33002028
NextAllowedMatingTime 200143540.8255205
bHadStaticBase True
UploadedFromServerName 
DonsArk
TamedOnServerName DonsArk
SavedBaseWorldLocation x : -91230.36525649737, y : 225015.29333049987, z : -14264.988107846555
MyCharacterStatusComponent 56a5424b-73cd-497e-a360-fb31cbedcf50
MyInventoryComponent 4abf1778-2bcf-457c-b7e4-e0556da10e89
LastTimeUpdatedCharacterStatusComponent 200402176.42210305
CharacterSavedDynamicBaseRelativeRotation x : 0.0, y : 0.0, z : 0.0, w : 1.0
Instigator 9c6dc920-16c0-4497-a2e2-281e8f4e86a2
bSavedWhenStasised True
TargetingTeam 390082751
LastEnterStasisTime 200402176.42210305
OriginalCreationTime 200089342.40888298
'''
'''

{"properties":[
    {"name":"TamedName","type":"StrProperty","value":"39/31/40/34/34/37"},
    {"name":"bIsFemale","type":"BoolProperty","value":true},
    {"name":"bEnableTamedMating","type":"BoolProperty","value":true},
    {"name":"bServerInitializedDino","type":"BoolProperty","value":true},
    {"name":"ColorSetIndices","type":"ByteProperty","value":56},
    {"name":"ColorSetIndices","type":"ByteProperty","value":98,"position":1},
    {"name":"ColorSetIndices","type":"ByteProperty","value":24,"position":4},
    {"name":"ColorSetIndices","type":"ByteProperty","value":95,"position":5},
    {"name":"ColorSetNames","type":"NameProperty","value":"DarkTurquoise"},
    {"name":"ColorSetNames","type":"NameProperty","value":"Custard","position":1},
    {"name":"ColorSetNames","type":"NameProperty","value":"Red","position":2},
    {"name":"ColorSetNames","type":"NameProperty","value":"Unused","position":3},
    {"name":"ColorSetNames","type":"NameProperty","value":"Dino Light Green","position":4},
    {"name":"ColorSetNames","type":"NameProperty","value":"Glacial","position":5},
    {"name":"RequiredTameAffinity","type":"FloatProperty","value":5450.0},
    {"name":"TamingTeamID","type":"IntProperty","value":2000000000},
    {"name":"TamingLastFoodConsumptionTime","type":"DoubleProperty","value":2.0213862103686762E8},
    {"name":"LastTameConsumedFoodTime","type":"DoubleProperty","value":2.021351813795442E8},
    {"name":"DinoID1","type":"UInt32Property","value":475686232},
    {"name":"DinoID2","type":"UInt32Property","value":76290524},
    {"name":"UntamedPoopTimeCache","type":"FloatProperty","value":651.94556},
    {"name":"LastEggSpawnChanceTime","type":"DoubleProperty","value":2.021383437397591E8},
    {"name":"OriginalNPCVolumeName","type":"NameProperty","value":"NPCZoneVolume"},
    {"name":"TamedAtTime","type":"DoubleProperty","value":2.0207797134527078E8},
    {"name":"LastUpdatedBabyAgeAtTime","type":"DoubleProperty","value":2.0211002553011334E8},
    {"name":"LastUpdatedMatingAtTime","type":"DoubleProperty","value":2.0213862131142345E8},
    {"name":"NextAllowedMatingTime","type":"DoubleProperty","value":2.022024211410694E8},
    {"name":"ImprinterName","type":"StrProperty","value":"ryno85"},
    {"name":"ImprinterPlayerUniqueNetId","type":"StrProperty","value":"000298efcd0540e397754cf38c5b7dbb"},
    {"name":"BabyCuddleWalkStartingLocation","type":"StructProperty","value":{"x":32007.165103683765,"y":-21601.26174385714,"z":-14235.902111570791}},
    {"name":"BabyNextCuddleTime","type":"DoubleProperty","value":2.0208375080790347E8},
    {"name":"BabyCuddleType","type":"ByteProperty","value":"EBabyCuddleType::FOOD"},
    {"name":"BabyCuddleFood","type":"ObjectProperty","value":"BlueprintGeneratedClass /Game/PrimalEarth/CoreBlueprints/Items/Consumables/PrimalItemConsumable_Kibble_Base_Small.PrimalItemConsumable_Kibble_Base_Small_C"},
    {"name":"bHadStaticBase","type":"BoolProperty","value":true},
    {"name":"UploadedFromServerName","type":"StrProperty","value":"\nDomiNATION #1 Island PvE (3x H/XP/T)"},
    {"name":"TamedOnServerName","type":"StrProperty","value":"DomiNATION #1 Island PvE (3x H/XP/T)"},
    {"name":"DinoAncestors","type":"ArrayProperty","value":[
        {"properties":[
            {"name":"MaleName","type":"StrProperty","value":"39/28/40/34/31/35 - Lvl 219"},
                {"name":"MaleDinoID1","type":"UInt32Property","value":399993663},
                {"name":"MaleDinoID2","type":"UInt32Property","value":56980663},
            {"name":"FemaleName","type":"StrProperty","value":"30/27/29/31/24/37 - Lvl 179"},
                {"name":"FemaleDinoID1","type":"UInt32Property","value":499485272},
                {"name":"FemaleDinoID2","type":"UInt32Property","value":480024209}]},
        {"properties":[
            {"name":"MaleName","type":"StrProperty","value":"39/28/40/34/31/35 - Lvl 219"},
                {"name":"MaleDinoID1","type":"UInt32Property","value":399993663},
                {"name":"MaleDinoID2","type":"UInt32Property","value":56980663},
            {"name":"FemaleName","type":"StrProperty","value":"30/27/40/31/24/37 - Lvl 190"},
                {"name":"FemaleDinoID1","type":"UInt32Property","value":51038128},
                {"name":"FemaleDinoID2","type":"UInt32Property","value":412326021}]},
        {"properties":[
            {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/35 - Lvl 214"},
                {"name":"MaleDinoID1","type":"UInt32Property","value":261679364},
                {"name":"MaleDinoID2","type":"UInt32Property","value":498175300},
            {"name":"FemaleName","type":"StrProperty","value":"39/28/40/34/31/37 - Lvl 210"},
                {"name":"FemaleDinoID1","type":"UInt32Property","value":21739837},
                {"name":"FemaleDinoID2","type":"UInt32Property","value":202330380}]},
        {"properties":[
            {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/37 - Lvl 216"},
                {"name":"MaleDinoID1","type":"UInt32Property","value":428203134},
                {"name":"MaleDinoID2","type":"UInt32Property","value":94695694},
            {"name":"FemaleName","type":"StrProperty","value":"39/28/40/34/34/37 - Lvl 213"},
                {"name":"FemaleDinoID1","type":"UInt32Property","value":317134050},
                {"name":"FemaleDinoID2","type":"UInt32Property","value":345509663}]},
        {"properties":[
            {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/37 - Lvl 216"},
                {"name":"MaleDinoID1","type":"UInt32Property","value":205778521},
                {"name":"MaleDinoID2","type":"UInt32Property","value":374532158},
            {"name":"FemaleName","type":"StrProperty","value":"Spino - Lvl 213"},
                {"name":"FemaleDinoID1","type":"UInt32Property","value":143378752},
                {"name":"FemaleDinoID2","type":"UInt32Property","value":444907930}]}],"arrayType":"StructProperty","arrayLength":5,"rest":null},
    {"name":"DinoAncestorsMale","type":"ArrayProperty","value":[
        {"properties":[
                {"name":"MaleName","type":"StrProperty","value":"38/31/23/34/34/25 - Lvl 240"},
                    {"name":"MaleDinoID1","type":"UInt32Property","value":202866278},
                    {"name":"MaleDinoID2","type":"UInt32Property","value":410903783},
                {"name":"FemaleName","type":"StrProperty","value":"39/28/40/34/31/35 - Lvl 208"},
                    {"name":"FemaleDinoID1","type":"UInt32Property","value":269536560},
                    {"name":"FemaleDinoID2","type":"UInt32Property","value":363884492}]},
            {"properties":[
                {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/35 - Lvl 214"},
                    {"name":"MaleDinoID1","type":"UInt32Property","value":71503306},
                    {"name":"MaleDinoID2","type":"UInt32Property","value":452871758},
                {"name":"FemaleName","type":"StrProperty","value":"39/28/40/34/31/35 - Lvl 208"},
                    {"name":"FemaleDinoID1","type":"UInt32Property","value":258672935},
                    {"name":"FemaleDinoID2","type":"UInt32Property","value":429182019}]},
            {"properties":[
                {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/35 - Lvl 214"},
                    {"name":"MaleDinoID1","type":"UInt32Property","value":261679364},
                    {"name":"MaleDinoID2","type":"UInt32Property","value":498175300},
                {"name":"FemaleName","type":"StrProperty","value":"39/31/40/34/34/37 - Lvl 216"},
                    {"name":"FemaleDinoID1","type":"UInt32Property","value":159503367},
                    {"name":"FemaleDinoID2","type":"UInt32Property","value":48089107}]},
            {"properties":[
                {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/37 - Lvl 216"},
                    {"name":"MaleDinoID1","type":"UInt32Property","value":428203134},
                    {"name":"MaleDinoID2","type":"UInt32Property","value":94695694},
                {"name":"FemaleName","type":"StrProperty","value":"39/31/40/34/34/35 - Lvl 214"},
                    {"name":"FemaleDinoID1","type":"UInt32Property","value":432519682},
                    {"name":"FemaleDinoID2","type":"UInt32Property","value":443539175}]},
            {"properties":[
                {"name":"MaleName","type":"StrProperty","value":"39/31/40/34/34/37 - Lvl 216"},
                    {"name":"MaleDinoID1","type":"UInt32Property","value":205778521},
                    {"name":"MaleDinoID2","type":"UInt32Property","value":374532158},
                {"name":"FemaleName","type":"StrProperty","value":"Spino - Lvl 213"},
                    {"name":"FemaleDinoID1","type":"UInt32Property","value":143378752},
                    {"name":"FemaleDinoID2","type":"UInt32Property","value":444907930}]}],"arrayType":"StructProperty","arrayLength":5,"rest":null},
    {"name":"SavedBaseWorldLocation","type":"StructProperty","value":{"x":31421.452031490266,"y":-20152.305766582405,"z":-13771.951746555644}},
    {"name":"TribeName","type":"StrProperty","value":"Ryno's Spinos"},
    {"name":"MyCharacterStatusComponent","type":"ObjectProperty","value":"8fb89cb2-16d8-5d4f-b513-c5bc09951905"},
    {"name":"MyInventoryComponent","type":"ObjectProperty","value":"1529eaf4-35ad-704d-a804-fd2cca7f2eaf"},
    {"name":"LastTimeUpdatedCharacterStatusComponent","type":"DoubleProperty","value":2.0213862199167904E8},
    {"name":"CharacterSavedDynamicBaseRelativeRotation","type":"StructProperty","value":{"x":0.0,"y":0.0,"z":0.0,"w":1.0}},
    {"name":"Instigator","type":"ObjectProperty","value":"ae1ed699-7f45-b24d-bba5-ea00cdaba864"},
    {"name":"bSavedWhenStasised","type":"BoolProperty","value":true},
    {"name":"TargetingTeam","type":"IntProperty","value":1319128454},
    {"name":"LastEnterStasisTime","type":"DoubleProperty","value":2.0213862199167904E8},
    {"name":"OriginalCreationTime","type":"DoubleProperty","value":2.0207797134527078E8}],
    "uuid":"ae1ed699-7f45-b24d-bba5-ea00cdaba864",
    "blueprint":"/Game/PrimalEarth/Dinos/Spino/Spino_Character_BP.Spino_Character_BP_C",
    "name":null,
    "className":"Spino_Character_BP_C",
    "location":{"x":31421.452031490266,"y":-20152.305766582405,"z":-13771.951746555644},
    "item":true}



{"properties":[
    {"name":"NumberOfLevelUpPointsApplied","type":"ByteProperty","value":39},
    {"name":"NumberOfLevelUpPointsApplied","type":"ByteProperty","value":31,"position":1},
    {"name":"NumberOfLevelUpPointsApplied","type":"ByteProperty","value":40,"position":3},
    {"name":"NumberOfLevelUpPointsApplied","type":"ByteProperty","value":34,"position":4},
    {"name":"NumberOfLevelUpPointsApplied","type":"ByteProperty","value":34,"position":7},
    {"name":"NumberOfLevelUpPointsApplied","type":"ByteProperty","value":37,"position":8},
    {"name":"bReplicateGlobalStatusValues","type":"BoolProperty","value":true},
    {"name":"bAllowLevelUps","type":"BoolProperty","value":true},
    {"name":"bServerFirstInitialized","type":"BoolProperty","value":true},
    {"name":"BaseCharacterLevel","type":"IntProperty","value":216},
    {"name":"ExperiencePoints","type":"FloatProperty","value":2073.2937},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":6160.07},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":1435.0,"position":1},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":0.0,"position":2},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":3250.0,"position":3},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":11418.746,"position":4},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":100.0,"position":5},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":0.0,"position":6},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":20.0,"position":7},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":2.43392,"position":8},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":0.0,"position":9},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":0.0,"position":10},
    {"name":"CurrentStatusValues","type":"FloatProperty","value":0.0,"position":11}],
    "uuid":"8fb89cb2-16d8-5d4f-b513-c5bc09951905","blueprint":"/Game/PrimalEarth/CoreBlueprints/DinoCharacterStatusComponent_BP_Spino.DinoCharacterStatusComponent_BP_Spino_C","name":"Spino_Character_BP_C","className":"DinoCharacterStatus_BP_Spino_C1","location":null,"item":false}

Health = 0
Stamina = 1
Oxygen = 3
Food = 4
Weight = 7
Damage = 8

00 00 00 00
04 00 00 00 

00 00 00 00 
00 01 00 00 

00 22 26 AD 
09 00 00 00 

00 01 00 00 
00 22 31 84 

AC 65 C3 42
'''
