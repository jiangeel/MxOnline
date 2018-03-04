__author__ = 'Eeljiang'

import re

line = 'boooobasdf\nfdsa'

regex = '^b.*a$'

if re.match(regex, line, re.M|re.I):
    print('yes')
