import numpy as np
import re
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List,Code
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton,CodeEditor, TextEditor
from pyface.image_resource import ImageResource
import pandas as pd
from io import StringIO

sourceEncoding = "cp1250"
targetEncoding = "utf-8"

def _locate_line(file_object, info_pattern):
    '''
    Reads lines from file_object until it reaches a line which matches the RegEx pattern
    given in 'info_pattern'. Used to position file cursor to the correct place for 
    reading in arbitraty order.
    '''
    info_matcher = re.compile(info_pattern)
    info_line = ' '
    while not info_matcher.search(info_line) and info_line != '':
        info_line = file_object.readline()
    return info_line

def _extract_monitors(data):
    # extract monitor data to separate files
    infile = data #open(data, 'r', encoding=sourceEncoding)
    monitors = []
    while 1:
        line = _locate_line(infile, r'Specifikace monitoru')
        if not line:
            break
        monitor = ''
        for line in infile:
            if line.split() != []:
                print(line)
                monitor += line
            else:
                break
        monitors.append(monitor.encode())
    infile.close()
    return monitors

def _list_to_array(inlist):
    res_lengths = [len(item) for item in inlist]
    res_y = np.max(res_lengths)
    res_x = len(res_lengths)
    out_arr = np.array([])
    out_arr.resize((res_y, res_x))
    for idx, item in enumerate(inlist):
        out_arr[:len(item), idx] = item
    return out_arr

# monitor_num = _extract_monitors('atena_out.txt')
# atena_excel = []
# for i in range(monitor_num + 1):
#    steps, vals = np.loadtxt('monitor_%02i.txt' % i, skiprows=10).T
#    if i == 0:
#        atena_excel.append(steps)
#        atena_excel.append(vals)
#    else:
#        atena_excel.append(vals)


def gen_excel(data):
    # specielne pro dany pripad (steps, mon1, mon2, mon3) -> (steps,mon2,mon1,mon3)
    monitors = _extract_monitors(data)
    atena_excel = []
    for mi, monitor in enumerate(monitors):
        monitor_vals = pd.read_csv('monitor_00.txt', skiprows=10, header=None, names=['step', 'val'], index_col=None, sep='\s+')
        if mi == 0:
            atena_excel.append(monitor_vals['step'].to_numpy())
            atena_excel.append(monitor_vals['val'].to_numpy())
        else:
            atena_excel.append(monitor_vals['val'].to_numpy())
    excel_arr = np.array(atena_excel).T
    return excel_arr




class Replacer(HasTraits):
    input_str = Str
    output_str = Str


    replace = Button
    def _replace_fired(self):
        excel_arr = gen_excel(StringIO(self.input_str))
        df = pd.DataFrame(excel_arr)
        self.output_str = df.to_string(index=None, header=None)
        df.to_clipboard(index=None, header=None)

    traits_view = View(
                       Item('input_str', editor=CodeEditor(lexer='bibtex', show_line_numbers=False)),
                       Item('replace'),
                       Item('output_str', editor=CodeEditor(lexer='bibtex', show_line_numbers=False)),
                        title='Replacer',
                        id='',
                        dock='tab',
                        resizable=True,
                        width=.4,
                        height=.5,
                        icon = ImageResource('w.ico'),
                        buttons=[]) # OKButton

Replacer().configure_traits()
