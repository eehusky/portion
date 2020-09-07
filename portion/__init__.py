from .const import Bound, inf
from .interval import Interval, open, closed, openclosed, closedopen, empty, singleton, set_tolerance
from .func import iterate
from .io import from_string, to_string, from_data, to_data
from .dict import IntervalDict


__all__ = [
    'inf', 'CLOSED', 'OPEN',
    'Interval',
    'open', 'closed', 'openclosed', 'closedopen', 'singleton', 'empty',
    'set_tolerance', 'set_operator',
    'iterate',
    'from_string', 'to_string', 'from_data', 'to_data',
    'IntervalDict',
]

CLOSED = Bound.CLOSED
OPEN = Bound.OPEN
