from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton, CodeEditor
import numpy as np
import subprocess
import multiprocessing
import os
import shutil
import threading

DIR = r'E:\Documents\python\workspace\AtenaScience\test'
CPU_NUM = multiprocessing.cpu_count()

def _prepare_dir(d):
    if os.path.exists(d):
        # for f in os.listdir(d):
            # os.remove(os.path.join(d, f))
        shutil.rmtree(d)
        os.mkdir(d)
    else:
        os.mkdir(d)

def run_mar(arg):
    print arg[0], arg[1]
    subprocess.call(arg[1])
    print 'jkhklkh', arg[0], arg[1]

    # export
    infile = open(os.path.join(DIR, 'monitor_export.inp'), 'r')
    infile_data = infile.read()
    infile.close()
    _prepare_dir(os.path.join(DIR, arg[0], 'exports'))
    # last_res = [int(v.split('.')[1]) for v in os.listdir(os.path.join(self.working_dir, task, 'results'))]
    outfile = open(os.path.join(DIR, arg[0], 'monitor_export.inp'), 'w')
    last = os.listdir(os.path.join(DIR, arg[0], 'results'))[-1]
    outfile.write('RESTORE "results\{}"\n'.format(last))
    outfile.write(infile_data)
    outfile.close()
    DIR_ = os.path.join(DIR, arg[0])
    INP = 'monitor_export.inp'
    subprocess.call('AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}"'.format(DIR_, INP))
    # # end export

    displacement = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'displacement.txt'), skip_header=13, skip_footer=5)
    reaction_1 = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'reaction_1.txt'), skip_header=13, skip_footer=5)
    reaction_2 = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'reaction_2.txt'), skip_header=13, skip_footer=5)
    stress = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'stress.txt'), skip_header=13, skip_footer=5)
    crack = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'crack.txt'), skip_header=13, skip_footer=5)
    iteration = np.genfromtxt(os.path.join(DIR, arg[0], 'exports', 'iteration.txt'), skip_header=13, skip_footer=5)

    number_of_steps = int(displacement[:, 0].max())

    steps_to_save = [1, 2, 3]
    decomp = stress[np.sum(stress[:, 1] < 0), 0]
    steps_to_save.append(decomp - 1)
    steps_to_save.append(decomp)

    cracks = crack[np.sum(crack[:, 1] != 1.0), 0]
    steps_to_save.append(cracks - 1)
    steps_to_save.append(cracks)

    steps_to_save.append(number_of_steps)

    print steps_to_save

    int_steps = (np.int64(iteration[:, 1]) - iteration[:, 1]) == 0
    num_iter = iteration[:, 0][int_steps][1:] - iteration[:, 0][int_steps][:-1]
    if num_iter.max() == 100:
        print 'Number of iteration exceeded!'

    file_lst = os.listdir(os.path.join(DIR, arg[0], 'results'))
    for step, name in enumerate(file_lst):
        if (step + 1) in steps_to_save:
            pass
        else:
            os.remove(os.path.join(DIR, arg[0], 'results', name))

class Preprocessor(HasTraits):

    working_dir = Directory(os.path.join(DIR), auto_set=False)

    random_fields_on = Bool(True)

    random_variables_on = Bool(False)

    random_fields_dir = Directory()
    def _random_fields_dir_default(self):
        return os.path.join(self.working_dir, 'random_fields')

#    random_fields_dir = Property(Str, depends_on='working_dir')
#    @cached_property
#    def _get_random_fields_dir(self):
#        return os.path.join(self.working_dir, 'random_fields')

    number_of_tasks = Property(Int)
    @cached_property
    def _get_number_of_tasks(self):
        if os.path.exists(self.random_fields_dir):
            return len([f for f in os.listdir(self.random_fields_dir) if os.path.splitext(f)[1] == ".ccp"])

    model_inp = File(os.path.join(DIR, 'task_rr.inp'), filter=['Atena input file (*.inp)|*.inp', 'All files (*.*)|*.*'], auto_set=False, enter_set=True)

    model_data = Property(Str, depends_on='model_inp')
    @cached_property
    def _get_model_data(self):
        infile = open(self.model_inp, 'r')
        return infile.read()

    number_of_rvs = Property(Int, depends_on='model_data')
    @cached_property
    def _get_number_of_rvs(self):
        return self.model_data.count('{v}')

    number_of_fields = Property(Int, depends_on='model_data')
    @cached_property
    def _get_number_of_fields(self):
        return self.model_data.count('{f}')

    task_name = Property(Str, depends_on='model_inp')
    @cached_property
    def _get_task_name(self):
        return os.path.splitext(os.path.basename(self.model_inp))[0] + '_{:03d}'

    task_lst = Property(List, depends_on='model_inp')
    @cached_property
    def _get_task_lst(self):
        task_lst = []
        for i in range(33, 97):  # self.number_of_tasks
            task_lst.append(self.task_name.format(i))
        return task_lst

    freet_txt = File(os.path.join(DIR, 'vyhradni.txt'),
                     filter=['Freet (*.txt)|*.txt', 'All files (*.*)|*.*'],
                     auto_set=False, enter_set=True)

    freet_data = Property(Str, depends_on='model_inp')
    @cached_property
    def _get_freet_data(self):
        return np.loadtxt(self.freet_txt, skiprows=2, delimiter='\t')

    test = Button(label='test')
    def _test_fired(self):
        infile = open(os.path.join(DIR, self.freet_txt), 'r')
        line_1 = infile.readline().split('\t')
        line_2 = infile.readline().split('\t')
        vals = ['<' + l_1 + '--' + l_2 + '>' for l_1, l_2 in zip(line_1, line_2)]
        if self.number_of_rvs > 0:
            m_d = self.model_data.format(v='{}')
            outfile = open(os.path.join(DIR, 'test.inp'), 'w')
            outfile.write(m_d.format(*vals))
            outfile.close()
            print 'test'
        if self.number_of_fields > 0:
            pass

    generate = Button(label='generate')
    def _generate_fired(self):
        if confirm(None, 'All results will be deleted!') == YES:
            for idx, task in enumerate(self.task_lst):
                task_dir = os.path.join(self.working_dir, task)
                self._prepare_dir(task_dir)
                outfile = open(os.path.join(task_dir, task + '.inp'), 'w')
                if self.number_of_fields > 0:
                    shutil.copy2(os.path.join(self.random_fields_dir, task + '.ccp'), task_dir)
                    field = task + '.ccp'
                    # outfile.write(m_d.format(field))
                if self.number_of_rvs > 0:
                    m_d = self.model_data.format(v='{}')
                    outfile.write(m_d.format(*self.freet_data[idx, :]))
                outfile.close()
                print 'TASK ' + task + ' created'
        else:
            pass

    run = Button(label='execute')
    def _run_fired(self):
        cmd_lst = []
        for task in self.task_lst:
            DIR = os.path.join(self.working_dir, task)
            INP = task + '.inp'
            OUT = task + '.out'
            MSG = task + '.msg'
            ERR = task + '.err'
            cmd_lst.append(('AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}" "{}" "{}" "{}"'.format(DIR, INP, OUT, MSG, ERR)))
            self._prepare_dir(os.path.join(self.working_dir, task, 'exports'))
            self._prepare_dir(os.path.join(self.working_dir, task, 'results'))
        arg_lst = zip(self.task_lst, cmd_lst)
        self._execute_pool(run_mar, arg_lst)

    export = Button(label='export')
    def _export_fired(self):
        infile = open(os.path.join(self.working_dir, 'monitor_export.inp'), 'r')
        infile_data = infile.read()
        infile.close()
        cmd_lst = []
        for task in self.task_lst:
            self._prepare_dir(os.path.join(self.working_dir, task, 'exports'))
            # last_res = [int(v.split('.')[1]) for v in os.listdir(os.path.join(self.working_dir, task, 'results'))]
            outfile = open(os.path.join(self.working_dir, task, 'monitor_export.inp'), 'w')
            last = os.listdir(os.path.join(self.working_dir, task, 'results'))[-1]
            outfile.write('RESTORE "results\{}"\n'.format(last))
            outfile.write(infile_data)
            outfile.close()
            DIR = os.path.join(self.working_dir, task)
            INP = 'monitor_export.inp'
            cmd_lst.append(('AtenaConsole64.exe /D "{}" /O /extend_real_output_width /execute "{}"'.format(DIR, INP)))
        self._execute_pool(subprocess.call, cmd_lst)

    def _prepare_dir(self, d):
        if os.path.exists(d):
            # for f in os.listdir(d):
                # os.remove(os.path.join(d, f))
            shutil.rmtree(d)
            os.mkdir(d)
        else:
            os.mkdir(d)

    def _execute_pool(self, func, arg_lst):
        try:
            pool = multiprocessing.Pool(processes=CPU_NUM)
            pool.map_async(func, arg_lst)
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





    # #threads = []
    # #for i in m:
    # #    t = threading.Thread(target=subprocess.call,args=(i,), daemon=True)
    # #    #threads.append(t)
    # #    t.start()
    # #t.join()



    traits_view = View(
                       Item('working_dir'),
                       Item('model_inp'),
                       Item('number_of_rvs', style='readonly'), Item('number_of_fields', style='readonly'),
                       Item('task_name', style='readonly'),
                       Item('random_fields_dir'),
                       Item('number_of_tasks', style='readonly'),
                       Item('test'),
                       Item('generate'),
                       Item('run'),
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

