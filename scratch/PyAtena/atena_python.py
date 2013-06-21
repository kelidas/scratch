from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES, ProgressDialog
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
import sys
import zipfile
import shutil

ATENA_CMD = 'AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}" "{}" "{}" "{}"'

def prepare_dir(d):
    '''Prepare directory if does not exist. If exist then delete it and create again.
    '''
    if os.path.exists(d):
        shutil.rmtree(d)
        os.mkdir(d)
    else:
        os.mkdir(d)

def get_last_step(result_dir):
        file_lst = os.listdir(result_dir)
        step_nums = [int(os.path.splitext(f)[1][1:]) for f in file_lst]
        return np.max(step_nums)

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

def run_cmd(cmd, task, task_num, **kwds):
    print task, 'running ...'
    sys.stdout.flush()
    with open(os.devnull, "w") as fnull:
        # p = subprocess.Popen('konsole -e ls -la', stdout=fnull, shell=True)
        p = subprocess.Popen('start /WAIT ' + cmd, stdout=fnull, shell=True)
        p.communicate()
    print task, 'finished'
    sys.stdout.flush()


class ProjectInfo(HasTraits):
    '''
    '''

    project_dir = Directory
    '''Main directory of the project containing all data of the project
    '''

    input_file = File(filter=['Atena input (*.inp)|*.inp', 'All files (*.*)|*.*'])
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

    result_name_pattern = Str('result.{:03d}')

    view = View(
              'project_dir',
              'input_file',
              Item('task_name_pattern'),
              'result_name_pattern',
                )


class Preprocessor(HasTraits):
    '''Preprocessor (preparing of solution)
    '''

    project_info = Instance(ProjectInfo)

    freet_txt = File(filter=['Atena input (*.txt)|*.txt', 'All files (*.*)|*.*'])
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
    '''List of task available in project directory to be evaluated 
    '''

    load_task_lst = Button
    '''Load available tasks to list
    '''
    def _load_task_lst_fired(self):
        dirs = []
        for d in os.listdir(self.project_info.project_dir):
            if os.path.isdir(os.path.join(self.project_info.project_dir, d)):
                dirs.append(d)
        task_lst = filter(re.compile(self.project_info.task_name_regex).match, dirs)
        self.task_lst = task_lst

    evaluated_tasks = List
    '''List of tasks to be evaluated
    '''

    evaluated_tasks_nums = Property(List, depends_on='evaluated_tasks')
    '''List of numbers of tasks to be evaluated
    '''
    @cached_property
    def _get_evaluated_tasks_nums(self):
        task_nums = [int(re.compile(self.project_info.task_name_regex).match(task).groups()[0])
                     for task in self.evaluated_tasks]
        return task_nums

    last_steps = Property(List)
    '''List of last steps to continue evaluation
    '''
    def _get_last_steps(self):
        last_steps = []
        for task in self.evaluated_tasks:
            last_step = get_last_step(os.path.join(self.project_info.project_dir,
                                                   task, 'results'))
            last_steps.append(last_step)
        return last_steps

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

    cpu_num = Int
    '''Number of CPUs but one that are available for execution 
    '''
    def _cpu_num_default(self):
        return multiprocessing.cpu_count() - 1

    evaluate = Button('Execute/re-execute')
    def _evaluate_fired(self):
        if confirm(None, 'All stored results will be deleted!') == YES:
            cmd_lst = []
            for task in self.task_selector.evaluated_tasks:
                DIR = os.path.join(self.project_info.project_dir, task)
                prepare_dir(os.path.join(DIR, 'results'))
                INP = task + '.inp'
                OUT = task + '.out'
                MSG = task + '.msg'
                ERR = task + '.err'
                cmd_lst.append(ATENA_CMD.format(DIR, INP, OUT, MSG, ERR))
            kwds = {}
            self.__execute(cmd_lst,
                           self.task_selector.evaluated_tasks,
                           self.task_selector.evaluated_tasks_nums,
                           kwds)

    add_config_file = File(filter=['Atena input (*.inp)|*.inp', 'All files (*.*)|*.*'])
    '''Add file with additional configuration (solving method parameters,
    new load cases, etc.)
    '''

    step_pattern = Str('''STEP id {0} STATIC name "Load step No.{0}"\nLOAD CASE  1 * 1.0000000  4 * 0.04875  65535 * 1.0000000\nEXECUTE\n''')
    '''Pattern for inserting of new steps 
    '''

    store_pattern = Str(r'''STORE "results\result.{0:03d}"''')
    '''Pattern for saving evaluated steps in result file
    '''

    steps_to_add = Int(400)
    '''Number of steps that will be added and evaluated
    '''

    store_step_mult = Int(1)
    '''Multiplier of steps that will be stored. The last step is stored automatically
    '''

    cmd_lst_continue = List
    '''List of commands for continue evaluation
    '''

    add_steps = Button
    '''Generate additional steps from pattern, create input file and command
    list for continue to evaluate them 
    '''
    def _add_steps_fired(self):
        cmd_lst = []
        for task, last_step in zip(self.task_selector.evaluated_tasks, self.task_selector.last_steps):
            if self.add_config_file == '':
                steps = ''  # self.
            else:
                with open(self.add_config_file, 'r') as f:
                    steps = f.read() + '\n'
            for step in range(last_step + 1, last_step + self.steps_to_add + 1):
                steps += self.step_pattern.format(step)
                if step % self.store_step_mult == 0:
                    steps += self.store_pattern.format(step) + '\n\n'
                else:
                    steps += '\n'
            # add last step to be saved
            if step % self.store_step_mult != 0:
                steps += self.store_pattern.format(last_step + self.steps_to_add) + '\n'
            DIR = os.path.join(self.project_info.project_dir, task)
            INP = 'continue_{0:%d}_{0:%m}_{0:%y}_{0:%H}_{0:%M}_{1:s}.inp'.format(datetime.datetime.now(), task)
            outfile = open(os.path.join(DIR, INP), 'w')
            result_name = self.project_info.result_name_pattern.format(last_step)
            outfile.write('RESTORE "results\\{}"\n\n'.format(result_name))
            outfile.write(steps)
            outfile.close()
            OUT = task + '.out'
            MSG = task + '.msg'
            ERR = task + '.err'
            cmd_lst.append(ATENA_CMD.format(DIR, INP, OUT, MSG, ERR))
        self.cmd_lst_continue = cmd_lst

    continue_evaluation = Button
    '''Continue evaluation with new settings and steps
    '''
    def _continue_evaluation_fired(self):
        self.__execute(self.cmd_lst_continue,
                       self.task_selector.evaluated_tasks,
                       self.task_selector.evaluated_tasks_nums, {})

    def __execute(self, cmd_lst, task_lst, task_num_lst, kwds):
        '''Execute tasks with multiprocessing.Pool
        '''
        if len(cmd_lst) > 1:
            arg_lst = zip(cmd_lst, task_lst, task_num_lst)
            execute_pool(run_cmd, self.cpu_num, arg_lst, kwds)
        else:
            run_cmd(cmd_lst[0], task_lst[0], task_num_lst[0], **kwds)


    view = View(
                Item('cpu_num', tooltip='Number of CPUs but one'),
                UItem('evaluate'),
                Item('add_config_file', label='Additional config file'),
                Item('step_pattern', style='custom'),
                Item('store_pattern'),
                Item('steps_to_add'),
                Item('store_step_mult'),
                UItem('add_steps'),
                UItem('continue_evaluation')
                )


class Postprocessor(HasTraits):
    project_info = Instance(ProjectInfo)

    task_selector = Instance(TaskSelector)

    monitor_export_available = Bool(False)

    monitor_export_file = File()
    def _monitor_export_file_default(self):
        export_file = os.path.join(self.project_info.project_dir, 'monitor_export.inp')
        if os.path.exists(export_file):
            self.monitor_export_available = True
            return export_file
        else:
            self.monitor_export_available = False
            return 'Monitor export file does not exist. Create monitor_export.inp in project directory.'

    export_file_data = Property(Str, depends_on='monitor_export_file')
    @cached_property
    def _get_export_file_data(self):
        with open(os.path.join(self.working_dir, 'monitor_export.inp'), 'r') as infile:
            return infile.read()

    monitor_export = Button('Export')
    def _evaluate_fired(self):
        if confirm(None, 'All stored exports will be deleted!') == YES:
            cmd_lst = []
            for task in self.task_selector.evaluated_tasks:
                DIR = os.path.join(self.project_info.project_dir, task)
                prepare_dir(os.path.join(DIR, 'exports'))
                outfile = open(os.path.join(self.project_info.project_dir,
                                            task, 'monitor_export.inp'), 'w')
                last_step = self.task_selector.last_steps
                outfile.write('RESTORE "results\{}"\n'.format(last_step))
                outfile.write(self.export_file_data)
                outfile.close()
                INP = task + '.inp'
                OUT = task + '.out'
                MSG = task + '.msg'
                ERR = task + '.err'
                cmd_lst.append(ATENA_CMD.format(DIR, INP, OUT, MSG, ERR))
            kwds = {}
            self.__execute(cmd_lst,
                           self.task_selector.evaluated_tasks,
                           self.task_selector.evaluated_tasks_nums,
                           kwds)

    view = View(
                Item('monitor_export_file', style='readonly'),
                UItem('monitor_export', enabled_when='monitor_export_available')
                )


class Archiver(HasTraits):
    '''
    '''
    project_info = Instance(ProjectInfo)

    task_selector = Instance(TaskSelector)

    delete_directory = Bool(False)
    delete_archive = Bool(False)

    compress = Button
    def _compress_fired(self):
        for task in self.task_selector.evaluated_tasks:
            task_dir = os.path.join(self.project_info.project_dir, task)
            results_dir = os.path.join(task_dir, 'results')
            zip_file = os.path.join(task_dir, 'results.zip')
            zf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
            for dirname, subdirs, files in os.walk(results_dir):
                for filename in files:
                    zf.write(os.path.join(dirname, filename),
                             os.path.join('results', filename))
            zf.close()
            if self.delete_directory:
                if confirm(None, 'Delete directory "results" after compression was selected.\nDo you want to delete it?') == YES:
                    shutil.rmtree(results_dir)
        print 'Results compressed'

    decompress = Button
    def _decompress_fired(self):
        for task in self.task_selector.evaluated_tasks:
            task_dir = os.path.join(self.project_info.project_dir, task)
            # results_dir = os.path.join(task_dir, 'results')
            zip_file = os.path.join(task_dir, 'results.zip')
            zf = zipfile.ZipFile(zip_file, 'r')
            zf.extractall(task_dir)
            zf.close()
            if self.delete_archive:
                if confirm(None, 'Delete zip-file after decompression was selected.\nDo you want to delete it?') == YES:
                    os.remove(zip_file)
        print 'Results decompressed'

    view = View(
                Item('delete_directory'),
                Item('delete_archive'),
                UItem('compress'),
                UItem('decompress')
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

    archiver = Instance(Archiver)
    def _archiver_default(self):
        return Archiver(project_info=self.project_info,
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
                          UItem('task_selector@'),
                          UItem('solver@'),
                          dock='tab',
                          label='Solver'
                          ),
                    Group(
                          UItem('task_selector@'),
                          UItem('postprocessor@'),
                          dock='tab',
                          label='Postprocessor'
                          ),
                    Group(
                          UItem('task_selector@'),
                          UItem('archiver@'),
                          dock='tab',
                          label='Archiver'
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
#    test_dir = os.path.join(os.getcwd(), 'test')
#    project_info = ProjectInfo(project_dir=test_dir,
#                               input_file=os.path.join(test_dir, 'input_final.inp'))

    pyatena = PyAtena()  #project_info=project_info)
    pyatena.configure_traits()

