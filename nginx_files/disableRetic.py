#!/usr/bin/python3
import sys
import os
sys.path.append('/usr/lib/Retic_Controller/python')
from schedule import disableRetic

print('Content-Type: text/json')
print('')

disableRetic()
