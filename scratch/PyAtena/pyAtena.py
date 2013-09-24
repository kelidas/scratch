from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, HGroup, OKButton, CodeEditor
import numpy as np
import subprocess
import multiprocessing
import os
import shutil
import threading
import time
import datetime
import sys

DIR = r'C:\Users\Martina\Desktop\NOVA MORAVA\test'
CPU_NUM = 1  # multiprocessing.cpu_count()-1

STEP_STR = r'''STEP id {0} STATIC name "Load step No.{0}"
LOAD CASE  1 * 1.0000000  4 * 0.04875  65535 * 1.0000000
EXECUTE
STORE "results\result.{0:03d}"    
'''

def prepare_dir(d):
    '''Prepare directory if does not exist. If exist then delete it and create again.
    '''
    if os.path.exists(d):
        # for f in os.listdir(d):
            # os.remove(os.path.join(d, f))
        shutil.rmtree(d)
        os.mkdir(d)
    else:
        os.mkdir(d)

def execute_pool(func, arg_lst):
    try:
        pool = multiprocessing.Pool(processes=CPU_NUM)
        pool.map_async(func, arg_lst, chunksize=1)
        print 'pool map complete'
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

def run_mar(arg):
    with open('NULL', "w") as f:
        subprocess.call(arg[1], stdout=f)

    start_step = arg[2]

    # export
    infile = open(os.path.join(DIR, 'monitor_export.inp'), 'r')
    infile_data = infile.read()
    infile.close()
    prepare_dir(os.path.join(DIR, arg[0], 'exports'))
    # last_res = [int(v.split('.')[1]) for v in os.listdir(os.path.join(self.working_dir, task, 'results'))]
    outfile = open(os.path.join(DIR, arg[0], 'monitor_export.inp'), 'w')
    result_lst = os.listdir(os.path.join(DIR, arg[0], 'results'))
    result_lst.sort()
    last = result_lst[-1]
    outfile.write('RESTORE "results\{}"\n'.format(last))
    outfile.write(infile_data)
    outfile.close()
    DIR_ = os.path.join(DIR, arg[0])
    INP = 'monitor_export.inp'
    OUT = arg[0] + '.out'
    MSG = arg[0] + '.msg'
    ERR = arg[0] + '.err'
    cmd = 'AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}" "{}" "{}" "{}"'.format(DIR_, INP, OUT, MSG, ERR)
    with open('NULL', "w") as f:
        subprocess.call(cmd, stdout=f)
    # # end export


    print 'start', arg[0]
    sys.stdout.flush()

    import time
    time.sleep(5)

    displacement = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'displacement.txt'), skip_header=13, skip_footer=5)
#    reaction_left = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'reaction_left.txt'), skip_header=13, skip_footer=5)
#    reaction_right = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'reaction_right.txt'), skip_header=13, skip_footer=5)
#    iteration = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'iteration.txt'), skip_header=13, skip_footer=5)

    number_of_steps = int(displacement[:, 0].max())

    steps_to_save = [5, 10, 11]

#    tmp = np.round((iteration[:, 1] - np.floor(iteration[:, 1])), 10)
#    max_it = np.round(49. / 50., 10)

    # last step for delete
    last_step = number_of_steps
    steps_to_save.append(last_step)
    print 'last step', last_step

#    if tmp.max() == max_it:
#        print 'Number of iteration exceeded!'
#        step_ex = np.floor(iteration[:, 1][tmp == max_it])[0]
#        steps_to_save += [step_ex]
#        last_step = step_ex

    for i in range(int(start_step), int(last_step) + 1, 10):
        steps_to_save.append(i)

    print 'steps to save', steps_to_save
    print 'afds'

    file_lst = os.listdir(os.path.join(DIR, arg[0], 'results'))
    step_num = [int(os.path.splitext(f)[1][1:]) for f in file_lst]
    print step_num
    for idx, step in enumerate(step_num):
        if step in steps_to_save:
            pass
        else:
            print 'mazu', os.path.join(DIR, arg[0], 'results', file_lst[idx])
            try:
                os.remove(os.path.join(DIR, arg[0], 'results', file_lst[idx]))
            except:
                print 'nejde'
    sys.stdout.flush()

    time.sleep(60)


class Preprocessor(HasTraits):

    working_dir = Directory(os.path.join(DIR), auto_set=False)

#    random_fields_on = Bool(True)
#
#    random_variables_on = Bool(False)
#
#    random_fields_dir = Directory()
#    def _random_fields_dir_default(self):
#        return os.path.join(self.working_dir, 'random_fields')

#    random_fields_dir = Property(Str, depends_on='working_dir')
#    @cached_property
#    def _get_random_fields_dir(self):
#        return os.path.join(self.working_dir, 'random_fields')

#    number_of_tasks = Property(Int)
#    @cached_property
#    def _get_number_of_tasks(self):
#        if os.path.exists(self.random_fields_dir):
#            return len([f for f in os.listdir(self.random_fields_dir) if os.path.splitext(f)[1] == ".ccp"])

    model_inp = File(os.path.join(DIR, 'input_normalni.inp'),
                     filter=['Atena input (*.inp)|*.inp', 'All files (*.*)|*.*'],
                     auto_set=False, enter_set=True)

    evaluated_start_sim = Int(1)

    evaluated_last_sim = Int(50)

    model_data = Property(Str, depends_on='model_inp')
    @cached_property
    def _get_model_data(self):
        infile = open(self.model_inp, 'r')
        return infile.read()

    number_of_rvs = Property(Int, depends_on='model_data')
    @cached_property
    def _get_number_of_rvs(self):
        return self.model_data.count('{v}')

#    number_of_fields = Property(Int, depends_on='model_data')
#    @cached_property
#    def _get_number_of_fields(self):
#        return self.model_data.count('{f}')

    task_name = Property(Str, depends_on='model_inp')
    @cached_property
    def _get_task_name(self):
        return os.path.splitext(os.path.basename(self.model_inp))[0] + '_{:03d}'

    last_steps = Property(Int)
    def _get_last_steps(self):
        last_steps = []
        for i in range(self.evaluated_start_sim, self.evaluated_last_sim + 1):  # self.number_of_tasks
            file_lst = os.listdir(os.path.join(self.working_dir, self.task_name.format(i), 'results'))
            step_nums = [int(os.path.splitext(f)[1][1:]) for f in file_lst]
            last_steps.append(np.max(step_nums))
        return last_steps

    task_lst = Property(List)
    @cached_property
    def _get_task_lst(self):
        task_lst = []
        for i in range(self.evaluated_start_sim, self.evaluated_last_sim + 1):  # self.number_of_tasks
            task_lst.append(self.task_name.format(i))
        return task_lst

    freet_txt = File(os.path.join(DIR, 'NovaMorava_inputs_all_0let.txt'),
                     filter=['Freet (*.txt)|*.txt', 'All files (*.*)|*.*'],
                     auto_set=False, enter_set=True)

    freet_data = Property(Str, depends_on='model_inp')
    @cached_property
    def _get_freet_data(self):
        return np.loadtxt(self.freet_txt, skiprows=1, delimiter='\t')

    def _insert_vars_to_inp(self, outfile, var_list):
        m_d = self.model_data.format(v='{}')
        outfile.write(m_d.format(*var_list))

    test = Button(label='test')
    def _test_fired(self):
        infile = open(os.path.join(DIR, self.freet_txt), 'r')
        line_1 = infile.readline().split('\t')
        vals = ['<' + l_1 + '>' for l_1 in line_1]
        if self.number_of_rvs > 0:
            outfile = open(os.path.join(DIR, 'test.inp'), 'w')
            self._insert_vars_to_inp(outfile, vals)
            outfile.close()
            print 'test'
#        if self.number_of_fields > 0:
#            pass

    generate = Button(label='generate')
    def _generate_fired(self):
        if confirm(None, 'All results will be deleted!') == YES:
            for idx, task in enumerate(self.task_lst):
                task_dir = os.path.join(self.working_dir, task)
                prepare_dir(task_dir)
                outfile = open(os.path.join(task_dir, task + '.inp'), 'w')
#                if self.number_of_fields > 0:
#                    shutil.copy2(os.path.join(self.random_fields_dir, task + '.ccp'), task_dir)
#                    field = task + '.ccp'
                    # outfile.write(m_d.format(field))
                if self.number_of_rvs > 0:
                    self._insert_vars_to_inp(outfile, self.freet_data[idx, :])
                outfile.close()
                print 'TASK ' + task + ' created'
        else:
            pass

    run = Button(label='execute')
    def _run_fired(self):
        cmd_lst = []
        for task in self.task_lst:
            prepare_dir(os.path.join(self.working_dir, task, 'results'))
            DIR = os.path.join(self.working_dir, task)
            INP = task + '.inp'
            OUT = task + '.out'
            MSG = task + '.msg'
            ERR = task + '.err'
            cmd_lst.append(('AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}" "{}" "{}" "{}"'.format(DIR, INP, OUT, MSG, ERR)))
        arg_lst = zip(self.task_lst, cmd_lst, np.ones(len(cmd_lst)).tolist())
        # run_mar(arg_lst[0])
        execute_pool(run_mar, arg_lst)

    step_str = Str(STEP_STR)

    steps_to_add = Int(400)

    add_steps_and_continue = Button('add steps and continue')
    def _add_steps_and_continue_fired(self):
        cmd_lst = []
        for task, last_step in zip(self.task_lst, self.last_steps):
            steps = ''
            for i in range(last_step + 1, last_step + self.steps_to_add + 1):
                steps += self.step_str.format(i) + '\n'
            INP = 'continue_{0:%d}_{0:%m}_{0:%y}_{0:%H}_{0:%M}_{1:s}.inp'.format(datetime.datetime.now(), task)
            outfile = open(os.path.join(self.working_dir, task, INP), 'w')
            outfile.write('RESTORE "results\\result.{:03d}"\n\n'.format(last_step))
            outfile.write(steps)
            outfile.close()
            DIR = os.path.join(self.working_dir, task)
            OUT = task + '.out'
            MSG = task + '.msg'
            ERR = task + '.err'
            cmd_lst.append(('AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}" "{}" "{}" "{}"'.format(DIR, INP, OUT, MSG, ERR)))
        arg_lst = zip(self.task_lst, cmd_lst, self.last_steps)
        print self.task_lst
        print self.last_steps
        print cmd_lst
        # run_mar(arg_lst[0])
        execute_pool(run_mar, arg_lst)

    export = Button(label='export')
    def _export_fired(self):
        infile = open(os.path.join(self.working_dir, 'monitor_export.inp'), 'r')
        infile_data = infile.read()
        infile.close()
        cmd_lst = []
        for task in self.task_lst:
            prepare_dir(os.path.join(self.working_dir, task, 'exports'))
            # last_res = [int(v.split('.')[1]) for v in os.listdir(os.path.join(self.working_dir, task, 'results'))]
            outfile = open(os.path.join(self.working_dir, task, 'monitor_export.inp'), 'w')
            last = os.listdir(os.path.join(self.working_dir, task, 'results'))[-1]
            outfile.write('RESTORE "results\{}"\n'.format(last))
            outfile.write(infile_data)
            outfile.close()
            DIR = os.path.join(self.working_dir, task)
            INP = 'monitor_export.inp'
            cmd_lst.append(('AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}"'.format(DIR, INP)))
        execute_pool(subprocess.call, cmd_lst)


    # #threads = []
    # #for i in m:
    # #    t = threading.Thread(target=subprocess.call,args=(i,), daemon=True)
    # #    #threads.append(t)
    # #    t.start()
    # #t.join()


    traits_view = View(
                       Item('working_dir'),
                       Item('model_inp'),
                       Item('freet_txt'),
                       Item('number_of_rvs', style='readonly'),
                       Item('task_name', style='readonly'),
                       HGroup(
                              Item('evaluated_start_sim'),
                              Item('evaluated_last_sim'),
                              ),
                       Item('test'),
                       Item('generate'),
                       Item('run'),
                       Item('step_str', style='custom'),
                       Item('steps_to_add'),
                       Item('add_steps_and_continue'),
                       Item('export'),
                        title='PyATENA',
                        id='',
                        dock='tab',
                        resizable=True,
                        width=.5,
                        height=.5,
                        buttons=[OKButton])





if __name__ == '__main__':
    preprocessor = Preprocessor()
    preprocessor.configure_traits()
    # pool = multiprocessing.Pool(processes=1)
    # result = pool.map(subprocess.call, m)

    print 'END!'

