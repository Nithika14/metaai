from enum import IntEnum

class CoolingLevel(IntEnum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class RouteDecision(IntEnum):
    STANDBY = 0
    CONTINUE = 1
    REROUTE_URGENT = 2
    
class SyncAction(IntEnum):
    DO_NOTHING = 0
    ATTEMPT_SYNC = 1

class ThermochromicState(IntEnum):
    SAFE = 0
    WARNING = 1
    BREACH = 2

class ConnectionStatus(IntEnum):
    OFFLINE = 0
    ONLINE = 1
