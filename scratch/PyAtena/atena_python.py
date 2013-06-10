from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, UItem, Group, HGroup, OKButton, CodeEditor, Tabbed, SetEditor
import numpy as np
import subprocess
import multiprocessing
import os
import shutil
import threading
import time
import datetime
import re


ATENA_CMD = 'AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}" "{}" "{}" "{}"'

def prepare_dir(d):
    '''Prepare directory if does not exist. If exist then delete it and create again.
    '''
    if os.path.exists(d):
        shutil.rmtree(d)
        os.mkdir(d)
    else:
        os.mkdir(d)

def execute_pool(func, cpu_num, args_lst, kwds):
    try:
        pool = multiprocessing.Pool(processes=cpu_num)
        for arg in args_lst:
            pool.apply_async(func, args=arg, kwds=kwds)
        print 'pool apply complete'
    except (KeyboardInterrupt, SystemExit):
        print 'got ^C while pool mapping, terminating the pool'
        pool.terminate()
        print 'pool is terminated'
    except Exception, e:
        print 'got exception: %r, terminating the pool' % (e,)
        pool.terminate()
        print 'pool is terminated'
    finally:
        print 'joining pool processes'
        pool.close()
        pool.join()
        print 'join complete'
    print 'the end'


class ProjectInfo(HasTraits):
    '''
    '''

    project_dir = Directory
    '''Main directory of the project containing all data of the project
    '''

    input_file = File
    '''Input file generated from ATENA (model data and definition of initial 
    steps). Values of variables that will be modified have to be replaced with 
    string '{v}'. 
    '''

    basename = Property(Str, depends_on='input_file')
    '''Base-name of input file
    '''
    @cached_property
    def _get_basename(self):
        return os.path.splitext(os.path.basename(self.input_file))[0]

    task_name_pattern = Property(Str, depends_on='input_file')
    '''Pattern of task name composed of base-name of input file and number of 
    simulation
    '''
    @cached_property
    def _get_task_name_pattern(self):
        return self.basename + '_{:03d}'

    task_name_regex = Property(Str, depends_on='input_file')
    '''Pattern of task name for re
    '''
    @cached_property
    def _get_task_name_regex(self):
        return self.basename + '_(\d+)'

    view = View(
              'project_dir',
              'input_file',
              Item('task_name_pattern', style='readonly'),
                )


class Preprocessor(HasTraits):
    '''Preprocessor (preparing of solution)
    '''

    project_info = Instance(ProjectInfo)

    freet_txt = File
    '''Table of variables ordered according to their position in input file. 
    The first row (header) contains names of variables.
    '''

    input_data = Property(Str, depends_on='project_info.input_file')
    '''Loaded input file
    '''
    @cached_property
    def _get_input_data(self):
        infile = open(self.project_info.input_file, 'r')
        data = infile.read()
        infile.close()
        return data

    freet_data = Property(Array, depends_on='freet_txt')
    '''Loaded freet_txt
    '''
    @cached_property
    def _get_freet_data(self):
        return np.loadtxt(self.freet_txt, skiprows=1, delimiter='\t')

    n_var_input = Property(Int, depends_on='project_info.input_file')
    '''Number of variables to be replaced in input file
    '''
    @cached_property
    def _get_n_var_input(self):
        if self.project_info.input_file == '':
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
            task_name_lst.append(self.project_info.task_name_pattern.format(i))
        return task_name_lst

    generate_test = Button(label='Generate testing input file')
    '''Generate testing input file. Values of variables that will be modified 
    will be replaced with name of variable (header) in free_txt file. 
    '''
    def _generate_test_fired(self):
        infile = open(os.path.join(self.project_info.project_dir, self.freet_txt), 'r')
        line_1 = infile.readline()[:-1].split('\t')
        vals = ['<' + var_name + '>' for var_name in line_1]
        if self.n_var_input > 0:
            outfile = open(os.path.join(self.project_info.project_dir, 'test.inp'), 'w')
            self.__insert_vars_to_inp(outfile, vals)
            outfile.close()
            print 'Testing file created'

    generate = Button(label='Generate tasks')
    '''Generate task folders containing input file for individual simulation. 
    '''
    def _generate_fired(self):
        if confirm(None, 'All results will be deleted!') == YES:
            for idx, task in enumerate(self.task_name_lst):
                task_dir = os.path.join(self.project_info.project_dir, task)
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

    view = View(
                'freet_txt',
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


class TaskSelector(HasTraits):
    '''
    '''

    project_info = Instance(ProjectInfo)

    task_lst = List

    load_task_lst = Button
    def _load_task_lst_fired(self):
        dirs = filter(os.path.isdir, os.listdir(self.project_info.project_dir))
        task_lst = filter(re.compile(self.project_info.task_name_regex).match, dirs)
        self.task_lst = task_lst

    evaluated_tasks = List

    evaluated_tasks_nums = Property(List, depends_on='evaluated_tasks')
    @cached_property
    def _get_task_nums(self):
        task_nums = [self.project_info.task_name_regex.match(task).groups([0])
                     for task in self.evaluated_tasks]
        return task_nums

    view = View(
                UItem('load_task_lst'),
                Item('evaluated_tasks', show_label=False,
                     editor=SetEditor(
                                     name='task_lst',
                                     ordered=True,
                                     can_move_all=True,
                                     left_column_title='Available tasks',
                                     right_column_title='Selected tasks')),
              )



class Solver(HasTraits):
    '''
    '''

    project_info = Instance(ProjectInfo)

    task_selector = Instance(TaskSelector)

    last_steps = Property(Int, depends_on='task_selector.evaluated_tasks')
    @cached_property
    def _get_last_steps(self):
        last_steps = []
        for task in self.task_selector.evaluated_tasks:
            file_lst = os.listdir(os.path.join(self.working_dir,
                                               task,
                                               'results'))
            step_nums = [int(os.path.splitext(f)[1][1:]) for f in file_lst]
            last_steps.append(np.max(step_nums))
        return last_steps

    cpu_num = Int
    def _cpu_num_default(self):
        return multiprocessing.cpu_count() - 1

    evaluate = Button
    def _evaluate_fired(self):
        cmd_lst = []
        for task in self.task_selector.evaluated_tasks:
            DIR = os.path.join(self.project_info.project_dir, task)
            prepare_dir(os.path.join(DIR, 'results'))
            INP = task + '.inp'
            OUT = task + '.out'
            MSG = task + '.msg'
            ERR = task + '.err'
            cmd_lst.append(ATENA_CMD.format(DIR, INP, OUT, MSG, ERR))
        self.__execute(cmd_lst,
                       self.task_selector.evaluated_tasks,
                       self.task_selector.evaluated_tasks_nums)

    add_config_file = File

    step_pattern = Str

    store_pattern = Str

    steps_to_add = Int(400)

    store_step_mult = Int(1)
    '''Multiplier of steps that will be stored. The last step is stored automatically
    '''

    cmd_lst_continue = List

    add_steps = Button
    def _add_steps_fired(self):
        cmd_lst = []
        for task, last_step in zip(self.task_selector.evaluated_tasks, self.last_steps):
            if self.add_config_file == '':
                steps = ''  # self.
            else:
                with open(self.add_config_file, 'r') as f:
                    steps = f.read() + '\n'
            for step in range(last_step + 1, last_step + self.steps_to_add + 1):
                steps += self.step_str.format(step)
                if step % self.store_step_mult == 0:
                    steps += self.store_pattern.format(step) + '\n'
            # add last step to be saved
            if last_step + self.steps_to_add % self.store_step_mult != 0:
                steps += self.store_pattern.format(last_step + self.steps_to_add) + '\n'
            DIR = os.path.join(self.project_info.project_dir, task)
            INP = 'continue_{0:%d}_{0:%m}_{0:%y}_{0:%H}_{0:%M}_{1:s}.inp'.format(datetime.datetime.now(), task)
            outfile = open(os.path.join(DIR, INP), 'w')
            outfile.write('RESTORE "results\\result.{:03d}"\n\n'.format(last_step))
            outfile.write(steps)
            outfile.close()
            OUT = task + '.out'
            MSG = task + '.msg'
            ERR = task + '.err'
            cmd_lst.append(ATENA_CMD.format(DIR, INP, OUT, MSG, ERR))
        self.cmd_lst_continue = cmd_lst

    continue_evaluation = Button
    def _continue_evalution_fired(self):
        self.__execute(self.cmd_lst_continue,
                       self.task_selector.evaluated_tasks,
                       self.task_selector.evaluated_tasks_nums)

    def __execute(self, cmd_lst, task_lst, task_num_lst, **kwds):
        if len(cmd_lst) > 1:
            arg_lst = zip(cmd_lst, task_lst, task_num_lst)
            execute_pool(run_cmd, self.cpu_num, arg_lst, **kwds)
        else:
            run_cmd(cmd_lst, task_lst, task_num_lst, **kwds)


    view = View(
                Group(
                      UItem('task_selector@'),
                      ),
                Item('cpu_num'),
                UItem('evaluate'),
                Item('add_config_file', label='Additional config file'),
                Item('step_pattern', style='custom'),
                Item('store_pattern'),
                Item('steps_to_add'),
                Item('store_step_mult'),
                UItem('add_steps'),
                UItem('continue_evaluation')
                )


def run_cmd(cmd_lst, task_lst, task_num_lst, **kwds):
    p = subprocess.Popen(cmd_lst)
    p.communicate()


class Postprocessor(HasTraits):
    project_info = Instance(ProjectInfo)

    task_selector = Instance(TaskSelector)

    view = View(
                Group(
                      UItem('task_selector@'),
                      ),
                )


class PyAtena(HasTraits):

    project_info = Instance(ProjectInfo, ())

    preprocessor = Instance(Preprocessor)
    def _preprocessor_default(self):
        return Preprocessor(project_info=self.project_info)

    task_selector = Instance(TaskSelector)
    def _task_selector_default(self):
        return TaskSelector(project_info=self.project_info)

    solver = Instance(Solver)
    def _solver_default(self):
        return Solver(project_info=self.project_info,
                      task_selector=self.task_selector)

    postprocessor = Instance(Postprocessor)
    def _postprocessor_default(self):
        return Postprocessor(project_info=self.project_info,
                             task_selector=self.task_selector)

    view = View(
                UItem('project_info@'),
                Tabbed(
                    Group(
                          UItem('preprocessor@'),
                          dock='tab',
                          label='Preprocessor'
                          ),
                    Group(
                          UItem('solver@'),
                          dock='tab',
                          label='Solver'
                          ),
                    Group(
                          UItem('postprocessor@'),
                          dock='tab',
                          label='Postprocessor'
                          ),
                       ),
                title='PyAtena',
                resizable=True,
                height=0.8,
                width=0.5,
                )


if __name__ == '__main__':
#     preprocessor = Preprocessor(project_dir=os.getcwd(),
#                               input_file='input_final.inp',
#                               freet_txt='input.txt')
 #   project_info = ProjectInfo(project_dir=os.getcwd())
    STEP_STR = r'''STEP id {0} STATIC name "Load step No.{0}"
LOAD CASE  1 * 1.0000000  4 * 0.04875  65535 * 1.0000000
EXECUTE
STORE "results\result.{0:03d}"    
'''
    pyatena = PyAtena()  # project_info=project_info)  # preprocessor=preprocessor)
    pyatena.configure_traits()

