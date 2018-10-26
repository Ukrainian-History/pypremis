from pypremis.nodes import *
from pypremis.lib import PremisRecord

dum = PremisRecord(frompath="kitchen-sink.xml")
dummer = dum.get_event_list()
print(dummer)
