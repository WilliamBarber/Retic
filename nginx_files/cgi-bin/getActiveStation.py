#!/usr/bin/python3
import sys
import json
sys.path.append('/usr/lib/Retic_Controller/python')
from schedule import getActiveStation

print('Content-Type: text/json')
print('')
active_station = getActiveStation()
print(json.dumps({'active_station': active_station}))
