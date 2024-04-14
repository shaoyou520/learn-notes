from enum import Enum


class UserStatusEm(Enum):
    HIGH_QUALITY = 'high'
    MID_QUALITY = 'middling'
    DEVELOP_QUALITY = 'develop'
    DOCKED_QUALITY = "docked"
    NEW_QUALITY = "new"
    DELETE = "delete"


class GoodStatusEm(Enum):
    ONLINE = 'online'
    OFF_LINE = 'off_line'
    DELETE = "delete"


class OrderStatusEm(Enum):
    CREATED = 'created'
    PAYING = 'paying'
    PAYED = "payed"
    STAY_PICKING = "stay_picking"
    PICKED = "picked"
    STAY_SEND = "stay_send"
    TRANSPORT = "transport"
    STAY_RECEIVE = "stay_receive"
    RECEIVE = "receive"
    END = "end"


class SexEm(Enum):
    MALE = "X"
    FEMALE = "O"


def choices(em):
    return [(tag.value, tag.name) for tag in em]

