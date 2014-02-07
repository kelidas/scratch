'''
Created on May 12, 2011

@author: kelidas
'''

from traits.api import HasTraits, Property, cached_property, Event, \
    Array, Instance, Int, Directory, Range, on_trait_change, Bool, Trait, Constant, \
    Tuple, Interface, implements, Enum, File, Str, List, Float, Button
from traits.trait_types import DelegatesTo
from traitsui.api import Item, View, HGroup, RangeEditor, Group, \
    HSplit, VGroup, FileEditor, Handler, EnumEditor, OKButton
from matplotlib.figure import Figure
from mpl_figure_editor import MPLFigureEditor
from numpy import array, vstack, linspace, unique, loadtxt, min, array, arange, \
    ones_like, cumsum, vstack, hstack, sum, zeros_like, zeros, ones, where, unique, \
    pi, invert, prod, dtype
from os.path import split as os_path_split, join
import matplotlib.pyplot as plt
import numpy as np
import os
import re

CURR_DIR = os.path.abspath('.')

class OOHandler(Handler):
    reaction_node = List()
    displ_node = List()
    reaction_idof = List()
    displ_idof = List()

    def object_reaction_data_changed(self, info):
        self.reaction_node = list(np.int32(unique(info.object.reaction_data[:, 1])))

        info.object.reaction_node = self.reaction_node[0]

    def object_reaction_node_changed(self, info):
        self.reaction_idof = list(np.array(unique(info.object.reaction_data[info.object.reaction_mask][:, 2]), dtype='int'))
        if len(self.reaction_idof) == 0:
            info.object.reaction_idof = 1
        else:
            info.object.reaction_idof = self.reaction_idof[0]

    def object_dof_data_changed(self, info):
        self.displ_node = list(np.int32(unique(info.object.dof_data[:, 1])))

        info.object.displ_node = self.displ_node[0]

    def object_displ_node_changed(self, info):
        self.displ_idof = list(np.array(unique(info.object.dof_data[info.object.displ_mask][:, 2]), dtype='int'))
        if len(self.displ_idof) == 0:
            info.object.displ_idof = 1
        else:
            info.object.displ_idof = self.displ_idof[0]

class OOData(HasTraits):
    '''
    Prepare data from OOFFEM output file
    '''

    out_file = File(join(CURR_DIR, 'data.out'), filter=[ 'oofem out (*.out)|*.out',
                                            'text files (*.txt)|*.txt',
                                             'all files (*.*)|*.*' ],
                                              source_modified=True)

    reaction_node = Int(conf_modified=True)
    displ_node = Int(conf_modified=True)

    reaction_idof = Int(1, conf_modified=True)
    displ_idof = Int(1, conf_modified=True)

    step_x = Bool(False, conf_modified=True)
    step_y = Bool(False, conf_modified=True)

    export = Button()
    def _export_fired(self):
        force, step = self.plot_reaction_step
        displ, s = self.plot_displ_step
        np.savetxt('export.txt', np.array((step, displ, force)).T)


    reaction_data = Property(Array, depends_on='+source_modified')
    @cached_property
    def _get_reaction_data(self):
        input_file = open(self.out_file, 'r')
        data = array([]).reshape(0, 4)
        step = 1
        while 1:
            line, m = self._locate_line(input_file, r'^\s+Node\s+(\d+)\s+iDof\s+(\d+)\s+reaction\s+([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)')
            if not line: break
            data = vstack([data, array([float(step), float(m.group(1)), float(m.group(2)), float(m.group(3))]) ])
            l = input_file.readline()
            while 1:
                if re.match(r'^\s+Node\s+(\d+)\s+iDof\s+(\d+)\s+reaction\s+([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)', l):
                    sm = re.match(r'^\s+Node\s+(\d+)\s+iDof\s+(\d+)\s+reaction\s+([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)', l)
                    data = vstack([data, array([float(step), float(sm.group(1)), float(sm.group(2)), float(sm.group(3))]) ])
                else:
                    break
                l = input_file.readline()
            step += 1
        input_file.close()
        print 'reaction data loaded'
        return data

    dof_data = Property(Array, depends_on='+source_modified')
    @cached_property
    def _get_dof_data(self):
        input_file = open(self.out_file, 'r')
        data = array([]).reshape(0, 4)
        step = 1
        while 1:
            line, m = self._locate_line(input_file, r'Node\s+\d+\s\(\s+(\d+)\):')
            if not line: break
            node_num = int(m.group(1))
            l = input_file.readline()
            while 1:
                if re.match(r'Node\s+\d+\s\(\s+(\d+)\):', l):
                    sm = re.match(r'Node\s+\d+\s\(\s+(\d+)\):', l)
                    node_num = int(sm.group(1))
                elif re.match(r'\s+dof\s(\d+)\s+d\s+([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)', l):
                    sm = re.match(r'\s+dof\s(\d+)\s+d\s+([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)', l)
                    data = np.vstack([data, np.array([step, node_num, int(sm.group(1)), float(sm.group(2))])])
                else:
                    data = np.vstack([data, np.array([step, node_num, int(sm.group(1)), float(sm.group(2))])])
                    break
                l = input_file.readline()
            step += 1
        input_file.close()
        print 'dof data loaded'
        return data

    displ_mask = Property(Array)
    def _get_displ_mask(self):
        return self.dof_data[:, 1] == self.displ_node

    displ_plot_mask = Property(Array)
    def _get_displ_plot_mask(self):
        return (self.dof_data[:, 1] == self.displ_node) * (self.dof_data[:, 2] == self.displ_idof)

    reaction_mask = Property(Array)
    def _get_reaction_mask(self):
        return self.reaction_data[:, 1] == self.reaction_node

    reaction_plot_mask = Property(Array)
    def _get_reaction_plot_mask(self):
        return (self.reaction_data[:, 1] == self.reaction_node) * (self.reaction_data[:, 2] == self.reaction_idof)

    plot_reaction_step = Property(Tuple, conf_modified=True)
    def _get_plot_reaction_step(self):
        return (hstack([0, self.reaction_data[self.reaction_plot_mask][:, 3]]),
                hstack([0, self.reaction_data[self.reaction_plot_mask][:, 0]]))

    plot_displ_step = Property(Tuple, conf_modified=True)
    def _get_plot_displ_step(self):
        return (hstack([0, self.dof_data[self.displ_plot_mask][:, 3]]),
                hstack([0, self.dof_data[self.displ_plot_mask][:, 0]]))

    def _locate_line(self, file_object, info_pattern):
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

    traits_view = View(
                       VGroup(
                           Item('out_file', style='simple', springy=True),
                           Item('out_file', style='custom', springy=True, show_label=False),
                           '_',
                           Group(
                                   Item('step_x'),
                               HGroup(
                                   Item('displ_node', editor=EnumEditor(name='handler.displ_node'), springy=True, label='Node'),
                                   Item('displ_node', springy=True, show_label=False),
                                   ),
                               HGroup(
                                   Item('displ_idof', editor=EnumEditor(name='handler.displ_idof'), springy=True, label='Dof'),
                                   Item('displ_idof', springy=True, show_label=False),
                                   ),
                                 label='Plot X',
                                 show_border=True,
                                 ),
                           Group(
                                   Item('step_y'),
                               HGroup(
                                   Item('reaction_node', editor=EnumEditor(name='handler.reaction_node'), springy=True, label='Node'),
                                   Item('reaction_node', springy=True, show_label=False),
                                   ),
                               HGroup(
                                   Item('reaction_idof', editor=EnumEditor(name='handler.reaction_idof'), springy=True, label='Dof'),
                                   Item('reaction_idof', springy=True, show_label=False),
                                   ),
                                 label='Plot Y',
                                 show_border=True,
                                 ),
                           Item('export', show_label=False),
                           ),
                           handler=OOHandler(),
                       )

class OOReader(HasTraits):
    '''
    OOFFEM output data reader -- display ld-diagrams
    '''

    data = Instance(OOData)

    figure = Instance(Figure)

    def _figure_default(self):
        figure = Figure()
        figure.add_axes([0.15, 0.15, 0.75, 0.75])
        return figure

    data_changed = Event(True)
    @on_trait_change('data.+conf_modified, data.+source_modified')
    def _redraw(self):
        figure = self.figure
        axes = figure.axes[0]
        axes.clear()
        if self.data.step_x == True and self.data.step_y == True:
            x = self.data.plot_displ_step[1]
            y = self.data.plot_reaction_step[1]
            axes.plot(x, y, 'b-x', linewidth=2)
            axes.set_title(os_path_split(self.data.out_file)[-1])
            axes.set_xlabel('step', fontsize=16)
            axes.set_ylabel('step', fontsize=16)  # , fontsize = 16
        elif self.data.step_x == True and self.data.step_y == False:
            x = self.data.plot_displ_step[1]
            y = self.data.plot_reaction_step[0]
            axes.plot(x, y, 'b-x', linewidth=2)
            axes.set_title(os_path_split(self.data.out_file)[-1])
            axes.set_xlabel('step', fontsize=16)
            axes.set_ylabel('force', fontsize=16)  # , fontsize = 16
        elif self.data.step_x == False and self.data.step_y == True:
            x = self.data.plot_displ_step[0]
            y = self.data.plot_reaction_step[1]
            axes.plot(x, y, 'b-x', linewidth=2)
            axes.set_title(os_path_split(self.data.out_file)[-1])
            axes.set_xlabel('displ', fontsize=16)
            axes.set_ylabel('step', fontsize=16)  # , fontsize = 16
        else:
            x = self.data.plot_displ_step[0]
            y = self.data.plot_reaction_step[0]
            axes.plot(x, y, 'b-x', linewidth=2)
            axes.set_title(os_path_split(self.data.out_file)[-1])
            axes.set_xlabel('displ', fontsize=16)
            axes.set_ylabel('force', fontsize=16)  # , fontsize = 16
        plt.setp(axes.get_xticklabels(), position=(0, -.01))
        self.data_changed = True

    traits_view = View(
                  HSplit(
                        VGroup(Item('data@', show_label=False, springy=True),
                       id='reader.settings',
                       label='settings',
                       dock='tab',
                       ),
                       Group(
                                        Item('figure', editor=MPLFigureEditor(),
                                               show_label=False, resizable=True),
                                        label='Plot sheet',
                                        id='reader.figure_window',
                                        dock='tab',
                                        ),
                                id='reader.hsplit',
                                 ),
                resizable=True,
                buttons=[OKButton],
                id='reader.main.view',
                )






if __name__ == '__main__':
    data = OOData()
    reader = OOReader(data=data)
    reader.configure_traits()











