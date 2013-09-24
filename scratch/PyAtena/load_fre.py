from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton
import re
import numpy as np

def locate_line(file_object, info_pattern):
    '''
    Reads lines from file_object until it reaches a line which matches the RegEx pattern
    given in 'info_pattern'. Used to position file cursor to the correct place for 
    reading in arbitraty order.
    '''
    info_matcher = re.compile(info_pattern)
    info_line = ' '
    while not info_matcher.search(info_line) and info_line != '':
        info_line = file_object.readline()
        m = re.match(info_pattern, info_line)
    return info_line, m



fre_file = open('test.fre', 'r')
data = fre_file.readlines()
fre_file.close()


nsim = int(data[1].split('=')[1])
print 'number of simulation = {}'.format(nsim)

category_lines = []
variable_lines = []
category_names = []
variable_names = []
variable_values = []
for i, line in enumerate(data):
    if line.find(r'[Category]') == 0:
        categ_line = i
        categ_name = data[i + 1][5:-1]
    if line.find(r'[Variable]') == 0:
        category_lines.append(categ_line)
        category_names.append(categ_name)
        variable_lines.append(i)
        variable_names.append(data[i + 1][5:-1])
    if line.find(r'[Values]') == 0:
        variable_values.append(np.array(data[i + 1:i + 1 + nsim], dtype=float))

outfile = open('fre.txt', 'w')

for i, j in zip(category_names, variable_names):
    outfile.write('{:s}{:s}\t'.format(i, j))
outfile.write('\n')

# for i in variable_names:
#     outfile.write('{:s}\t'.format(i))
# outfile.write('\n')


for j in range(nsim):
    for i in range(len(variable_lines)):
        outfile.write('{}\t'.format(variable_values[i][j]))
    outfile.write('\n')
outfile.write('\n')


outfile.close()



