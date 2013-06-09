from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, UItem, Group, HGroup, OKButton, CodeEditor
import numpy as np
import subprocess
import multiprocessing
import os
import shutil
import threading
import time
import datetime


def prepare_dir(d):
    '''Prepare directory if does not exist. If exist then delete it and create again.
    '''
    if os.path.exists(d):
        shutil.rmtree(d)
        os.mkdir(d)
    else:
        os.mkdir(d)


class Preprocessor(HasTraits):
    '''Preprocessor (preparing of solution)
    '''

    project_dir = Directory
    '''Main directory of the project containing all data of the project
    '''

    input_file = File
    '''Input file generated from ATENA (model data and definition of initial 
    steps). Values of variables that will be modified have to be replaced with 
    string '{v}'. 
    '''

    freet_txt = File
    '''Table of variables ordered according to their position in input file. 
    The first row (header) contains names of variables.
    '''

    task_name_pattern = Property(Str, depends_on='input_file')
    '''Pattern of task name composed of base-name of input file and number of 
    simulation
    '''
    @cached_property
    def _get_task_name_pattern(self):
        return os.path.splitext(os.path.basename(self.input_file))[0] + '_{:03d}'

    input_data = Property(Str, depends_on='input_file')
    '''Loaded input file
    '''
    @cached_property
    def _get_input_data(self):
        infile = open(self.input_file, 'r')
        data = infile.read()
        infile.close()
        return data

    freet_data = Property(Array, depends_on='freet_txt')
    '''Loaded freet_txt
    '''
    @cached_property
    def _get_freet_data(self):
        return np.loadtxt(self.freet_txt, skiprows=1, delimiter='\t')

    n_var_input = Property(Int, depends_on='input_file')
    '''Number of variables to be replaced in input file
    '''
    @cached_property
    def _get_n_var_input(self):
        if self.input_file == '':
            return None
        else:
            return self.input_data.count('{v}')

    n_var_freet = Property(Int, depends_on='freet_txt')
    '''Number of variables available from free_txt
    '''
    @cached_property
    def _get_n_var_freet(self):
        if self.freet_txt == '':
            return None
        else:
            return self.freet_data.shape[1]

    n_sim_start = Int(1)
    '''Number of starting simulation
    '''

    n_sim_stop = Int(2)
    '''Number of the last simulation
    '''

    task_name_lst = Property(List)
    '''List of generated task names for all simulations
    '''
    @cached_property
    def _get_task_name_lst(self):
        task_name_lst = []
        for i in range(self.n_sim_start, self.n_sim_stop + 1):
            task_name_lst.append(self.task_name_pattern.format(i))
        return task_name_lst

    generate_test = Button(label='Generate testing input file')
    '''Generate testing input file. Values of variables that will be modified 
    will be replaced with name of variable (header) in free_txt file. 
    '''
    def _generate_test_fired(self):
        infile = open(os.path.join(self.project_dir, self.freet_txt), 'r')
        line_1 = infile.readline()[:-1].split('\t')
        vals = ['<' + var_name + '>' for var_name in line_1]
        if self.n_var_input > 0:
            outfile = open(os.path.join(self.project_dir, 'test.inp'), 'w')
            self.__insert_vars_to_inp(outfile, vals)
            outfile.close()
            print 'Testing file created'

    generate = Button(label='Generate tasks')
    '''Generate task folders containing input file for individual simulation. 
    '''
    def _generate_fired(self):
        if confirm(None, 'All results will be deleted!') == YES:
            for idx, task in enumerate(self.task_name_lst):
                task_dir = os.path.join(self.project_dir, task)
                prepare_dir(task_dir)
                outfile = open(os.path.join(task_dir, task + '.inp'), 'w')
                if self.n_var_input > 0:
                    self.__insert_vars_to_inp(outfile, self.freet_data[idx, :])
                outfile.close()
                print 'TASK ' + task + ' created'

    def __insert_vars_to_inp(self, outfile, var_list):
        '''Write values of variables into the input file
        '''
        data = self.input_data.format(v='{}')
        outfile.write(data.format(*var_list))

    view = View('project_dir',
                'input_file',
                'freet_txt',
                Item('task_name_pattern', style='readonly'),
                Item('n_var_input', label='Number of input variables',
                    style='readonly', tooltip='Number of variables in input file'),
                Item('n_var_freet', label='Number of freet variables',
                    style='readonly', tooltip='Number of variables in freet file'),
                HGroup(
                       Item('n_sim_start', label='First simulation', springy=True),
                       Item('n_sim_stop', label='Last simulation', springy=True),
                       ),
                UItem('generate_test'),
                UItem('generate'),
                )


class PyAtena(HasTraits):
    preprocessor = Instance(Preprocessor, ())

    view = View(
                Group(
                      UItem('preprocessor@'),
                      dock='tab',
                      label='Preprocessor'
                      ),
                Group(
                      UItem('preprocessor@'),
                      dock='tab',
                      label='Processing'
                      ),
                Group(
                      UItem('preprocessor@'),
                      dock='tab',
                      label='Postprocessor'
                      ),
                title='PyAtena',
                resizable=True,
                height=0.5,
                width=0.5,
                )



if __name__ == '__main__':
    preprocessor = Preprocessor(project_dir=os.getcwd(),
                              input_file='input_final.inp',
                              freet_txt='input.txt')
    pyatena = PyAtena(preprocessor=preprocessor)
    pyatena.configure_traits()

