from .blocks import Wall, TurnLeft, TurnRight, Skull, Spikes, Apple, Box, InfinityTail, Finish, Dye, Reverse, VeniceBlock
from .field import Field
from .tunnel import Tunnel
from .teleport import BeginTeleport, EndTeleport
from .hole import Hole
from .direction import Direction
import enum


class EntityKind(enum.Enum):
    UNKNOWN = 1
    BLOCK = 2
    FIELD = 3


# for swapping block id to object it represents
BLOCKS_DICT = {
    2: (lambda: Wall()),
    3: (lambda: TurnLeft()),
    4: (lambda: TurnRight()),
    5: (lambda: Skull()),
    6: (lambda: Spikes()),
    7: (lambda: Apple()),
    8: (lambda: Box()),
    9: (lambda: InfinityTail()),
    10: (lambda: Finish()),
    11: (lambda: Finish(color='green')),
    12: (lambda: Finish(color='red')),
    13: (lambda: Finish(color='blue')),
    14: (lambda: Dye(color='green')),
    15: (lambda: Dye(color='red')),
    16: (lambda: Dye(color='blue')),
    21: (lambda: Reverse()),
    22: (lambda: VeniceBlock(direction=Direction('N'))),
    23: (lambda: VeniceBlock(direction=Direction('W'))),
    24: (lambda: VeniceBlock(direction=Direction('S'))),
    25: (lambda: VeniceBlock(direction=Direction('E'))),
}


# for swapping block id to object it represents
FIELDS_DICT = {
    1: (lambda: Field()),
    17: (lambda: Tunnel(direction=Direction('N'))),
    18: (lambda: Tunnel(direction=Direction('E'))),
    19: (lambda: BeginTeleport()),
    20: (lambda: EndTeleport()),
    26: (lambda: Hole()),
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


def get_field_from_id(id):
    if get_entity_kind(id) != EntityKind.FIELD:
        raise EntityDifferentingKindError
    return FIELDS_DICT[id]()


class EntityDifferentingKindError(Exception):
    pass
