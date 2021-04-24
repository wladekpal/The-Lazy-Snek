from .blocks import *
import enum

class EntityKind(enum.Enum):
    UNKNOWN = 1
    BLOCK = 2
    FIELD = 3

# for swapping block id to object it represents
BLOCKS_DICT = {
    1 : (lambda: None),
    2 : (lambda: Wall()),
    3 : (lambda: TurnLeft()),
    4 : (lambda: TurnRight()),
    5 : (lambda: Skull()),
    6 : (lambda: Spikes()),
    7 : (lambda: Apple()),
    8 : (lambda: Box()),
    9 : (lambda: InfityTail())
}

# for swapping block id to object it represents
FIELDS_DICT = {

}

def get_entity_kind(id):
    if id in BLOCKS_DICT.keys():
        return EntityKind.BLOCK
    elif id in FIELDS_DICT.keys():
        return EntityKind.FIELD
    else:
        return EntityKind.UNKNOWN

def get_block_from_id(id):
    if get_entity_kind(id) != EntityKind.BLOCK:
        raise EntityDifferentingKindError
    return BLOCKS_DICT[id]()

def get_field_from_id():
    if get_entity_kind(id) != EntityKind.FIELD:
        raise EntityDifferentingKindError
    return FIELDS_DICT[id]()



class EntityDifferentingKindError(Exception):
    pass

