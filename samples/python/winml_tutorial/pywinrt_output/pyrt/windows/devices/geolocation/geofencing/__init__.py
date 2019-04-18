# WARNING: Please don't edit this file. It was generated by Python/WinRT

from pyrt import _import_ns
import typing
import enum

__ns__ = _import_ns("Windows.Devices.Geolocation.Geofencing")

try:
    import pyrt.windows.devices.geolocation
except:
    pass

try:
    import pyrt.windows.foundation
except:
    pass

try:
    import pyrt.windows.foundation.collections
except:
    pass

class GeofenceMonitorStatus(enum.IntEnum):
    Ready = 0
    Initializing = 1
    NoData = 2
    Disabled = 3
    NotInitialized = 4
    NotAvailable = 5

class GeofenceRemovalReason(enum.IntEnum):
    Used = 0
    Expired = 1

class GeofenceState(enum.IntFlag):
    NONE = 0
    Entered = 0x1
    Exited = 0x2
    Removed = 0x4

class MonitoredGeofenceStates(enum.IntFlag):
    NONE = 0
    Entered = 0x1
    Exited = 0x2
    Removed = 0x4

Geofence = __ns__.Geofence
GeofenceMonitor = __ns__.GeofenceMonitor
GeofenceStateChangeReport = __ns__.GeofenceStateChangeReport
