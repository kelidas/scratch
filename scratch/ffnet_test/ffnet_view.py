
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List, Interface, implements, \
    Either, Enum, String, PythonValue, Any, Dict, Code, Long
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, HGroup, OKButton, CodeEditor, UItem, \
        VGroup, HSplit, EnumEditor, Handler, SetEditor, EnumEditor, InstanceEditor, \
        HTMLEditor, ShellEditor, CheckListEditor, VFlow, Label, Tabbed, FileEditor, \
        TextEditor, spring, VSplit, ListEditor

from traitsui.file_dialog import open_file

import numpy as np
import networkx as nx
import ffnet
import os
import scipy
import ast


class FFnetHelp(HasTraits):

    training_algorithm = Str

    help_string = Code
    @on_trait_change('training_algorithm')
    def _help_string_update(self):
        self.help_string = 'Help for parameters of the training algorithm\n'
        self.help_string += '----------------------------------------------'
        self.help_string += getattr(ffnet.ffnet, self.training_algorithm).__doc__ + '\n'
        if self.training_algorithm == 'train_tnc':
            self.help_string += 'Help for parameters of the oprimatization method\n'
            self.help_string += '-------------------------------------------------'
            self.help_string += scipy.optimize.fmin_tnc.__doc__
        elif self.training_algorithm == 'train_momentum':
            pass
        elif self.training_algorithm == 'train_rprop':
            pass
        elif self.training_algorithm == 'train_cg':
            self.help_string += 'Help for parameters of the oprimatization method\n'
            self.help_string += '-------------------------------------------------'
            self.help_string += scipy.optimize.fmin_cg.__doc__
        elif self.training_algorithm == 'train_bfgs':
            self.help_string += 'Help for parameters of the oprimatization method\n'
            self.help_string += '-------------------------------------------------'
            self.help_string += scipy.optimize.fmin_l_bfgs_b.__doc__
        elif self.training_algorithm == 'train_genetic':
            self.help_string += 'Help for parameters of the oprimatization method\n'
            self.help_string += '-------------------------------------------------'
            self.help_string += ffnet.pikaia.__doc__

    view = View(
                UItem('help_string', editor=CodeEditor()),
                width=.5,
                height=.5,
                resizable=True)


class FFnet(HasTraits):

    input = Array
    target = Array

    net_file = File('ffnet_net.pkl')

    mode = Enum('create', ['create', 'train', 'test', 'call'])

    n_inp = Long(enter_set=True, auto_set=False)
    @on_trait_change('input')
    def _n_inp_update(self):
        ndim = self.input.ndim
        if ndim == 1:
            self.n_inp = 1
        else:
            self.n_inp = self.input.shape[1]

    n_hid = List(Long, enter_set=True, auto_set=False)
    @on_trait_change('input')
    def _n_hid_update(self):
        ndim = self.input.ndim
        if ndim == 1:
            self.n_hid = [1]
        else:
            self.n_hid = [self.input.shape[1]]

    n_tar = Long(enter_set=True, auto_set=False)
    @on_trait_change('target')
    def _n_tar_update(self):
        ndim = self.target.ndim
        if ndim == 1:
            self.n_tar = 1
        else:
            self.n_tar = self.target.shape[1]

    bias_enabled = Bool(True)

    net_architecture = Trait('mlgraph',
                             {'mlgraph': ffnet.mlgraph,
                              'tmlgraph': ffnet.tmlgraph,
                              'imlgraph': ffnet.imlgraph,
                                         })

    conec = Array

    net = Instance(ffnet.ffnet)

    create_net = Button
    def _create_net_fired(self):
        self.conec = self.net_architecture_(tuple([self.n_inp] +
                                            self.n_hid +
                                            [self.n_tar]), biases=self.bias_enabled)
        self.net = ffnet.ffnet(self.conec)
        self.display_message('NETWORK CREATED')

    ffnet_plot = Button
    def _ffnet_plot_fired(self):
        import matplotlib.pyplot as plt
        nx.draw_graphviz(self.net.graph, prog='dot',
                         node_color='#A0CBE2', node_size=500,
                         edge_color='k')
        plt.show()

    training_algorithm = Enum('train_tnc', ['train_tnc',
                           'train_momentum',
                           'train_rprop',
                           'train_cg',
                           'train_bfgs',
                           'train_genetic'])

    train_config = Str(str({'nproc': 1,
                         'maxfun': None,
                         # 'bounds': (-100, 100),
                         'messages': 1}))
    @on_trait_change('training_algorithm')
    def _train_config_update(self):
        if self.training_algorithm == 'train_tnc':
            self.train_config = str({'nproc': 1,
                                 'maxfun': None,
                                 # 'bounds': (-100, 100),
                                 'messages': 1})
        elif self.training_algorithm == 'train_momentum':
            self.train_config = str({'eta': 0.2,
                                 'momentum': 0.8,
                                 'maxiter': 10000,
                                 'disp': True})
        elif self.training_algorithm == 'train_rprop':
            self.train_config = str({'a': 1.2,
                                 'b': 0.5,
                                 'mimin': 1e-6,
                                 'mimax': 50.0,
                                 'xmi': 0.1,
                                 'maxiter':10000,
                                 'disp':True})
        elif self.training_algorithm == 'train_cg':
            self.train_config = str({'maxiter': 10000,
                                 'disp': True})
        elif self.training_algorithm == 'train_bfgs':
            self.train_config = str({'maxfun': 15000,
                                 # 'bounds': (-100, 100),
                                 'iprint':0})
        elif self.training_algorithm == 'train_genetic':
            self.train_config = str({'lower':-25,
                                 'upper': 25,
                                 'individuals': 20,
                                 'generations': 500,
                                 'verbosity': 1})

    ffnet_train = Button('train / continue training')
    def _ffnet_train_fired(self):
        f = getattr(self.net, self.training_algorithm)
        self.display_message(self.train_config)
        f(self.input, self.target, **ast.literal_eval(self.train_config))
        self.display_message('NETWORK TRAINED...')

    ffnet_test = Button('test')
    def _ffnet_test_fired(self):
        self.display_message('TESTING NETWORK...')
        output, regression = self.net.test(self.input, self.target, iprint=1)
        Rsquared = regression[0][2]
        maxerr = abs(output - self.target).max()
        try:
            import matplotlib.pyplot as plt
            plt.plot(self.target, 'bx--', label='target')
            plt.plot(output, 'k-o', label='output')
            plt.xlabel('pattern')
            plt.legend(loc='best')
            plt.title('Outputs vs. target of trained network.')
            plt.grid(True)
            plt.show()
        except ImportError, e:
            print "Cannot make plots. For plotting install matplotlib.\n%s" % e

    help = Instance(FFnetHelp)
    def _help_default(self):
        return FFnetHelp(training_algorithm=self.training_algorithm)

    @on_trait_change('training_algorithm')
    def _help_update(self):
        self.help.training_algorithm = self.training_algorithm

    ffnet_call = Button()
    def _ffnet_call_fired(self):
        output = self.net.call(self.input)
        self.display_message('NETWORK OUTPUT...')
        self.display_message(output.__str__())

    ffnet_save = Button('save net')
    def _ffnet_save_fired(self):
        ffnet.savenet(self.net, self.net_file)
        self.display_message('NETWORK SAVED...')

    ffnet_load = Button('load net')
    def _ffnet_load_fired(self):
        self.net = ffnet.loadnet(self.net_file)
        self.display_message('NETWORK LOADED...')
        self.display_message(self.net)

    traits_view = View(
                       Item('mode', style='simple'),  # , editor=EnumEditor(values=mode.values, cols=4)
                       HGroup(
                              Item('net_file', springy=True),
                              UItem('ffnet_save'),
                              UItem('ffnet_load'),
                              visible_when='mode != "create"',
                       ),
                       '_',
                       Group(
                           Item('net_architecture',
                                tooltip=('imlgraph - multilayer architecture with independent outputs' +
                                         'mlgraph - standard multilayer network architecture\n' +
                                         'tmlgraph - multilayer network full connectivity list\n')
                                ),
                           Item('bias_enabled'),
                           Item('n_inp', style='readonly'),
                           '_',
                            Item('n_hid', style='custom'),
                            '_',
                            Item('n_tar', style='readonly'),
                            VGroup(
                                  UItem('create_net'),
                                  UItem('ffnet_plot'),
                                  ),
                            label='ffnet create',
                            visible_when='mode == "create"',
                            dock='tab',
                            show_border=True,
                            id='ffnet.configuration',
                            ),
                       Group(
                             Item('training_algorithm'),
                             HGroup(
                                 Item('train_config', style='custom',
                                      editor=TextEditor(multi_line=True), springy=True),
                                 UItem('help'),
                             ),
                             VGroup(
                                   UItem('ffnet_train'),
                                   ),
                             label='training configuration',
                             visible_when='mode == "train"',
                             dock='tab',
                             show_border=True,
                             id='ffnet.training'
                             ),
                        Group(
                              UItem('ffnet_test'),
                             label='test',
                             visible_when='mode == "test"',
                             dock='tab',
                             show_border=True,
                             id='ffnet.test'
                             ),
                        Group(
                             UItem('ffnet_call'),
                             label='ffnet call',
                             visible_when='mode == "call"',
                             dock='tab',
                             show_border=True,
                             id='ffnet.call'
                             ),
                       id='ffnet.view',
                       resizable=True,
                        )


class FFnetView(HasTraits):

    input_dir = Directory(os.path.split(__file__)[0])

    input_file = File(entries=10)
    def _input_file_default(self):
        return os.path.join(self.input_dir, 'input.txt')

    target_file = File(entries=10)
    def _target_file_default(self):
        return os.path.join(self.input_dir, 'target.txt')

    ffnet = Instance(FFnet, ())

    message = String('')

    load_data = Button
    def _load_data_fired(self):
        self.ffnet.display_message = self._add_line
        if self.input_file == '' or self.target_file == '':
            self._add_line('NO INPUT FILES SELECTED')
        else:
            self.ffnet.input = np.loadtxt(self.input_file, skiprows=1)
            self.ffnet.target = np.loadtxt(self.target_file, skiprows=1, ndmin=2)
            self._add_line('DATA LOADED...')

    def _add_line(self, string):
        """ Adds a line to the message window.
        """
        self.message += (string + '\n')  # + self.message)  # [0:1000]

    clear_message = Button('clear message window')
    def _clear_message_fired(self):
        self.message = ''

    traits_view = View(
                       HSplit(
                              VGroup(
                               Group(
                                    Item('input_file', id='ffnet_view.infile'),
                                    Item('target_file', id='ffnet_view.tarfile'),
                                    UItem('load_data'),
                                    show_border=True,
                                    label='Load data',
                                    id='ffnet_view.load',
                                    ),
                                UItem('ffnet@'),
                                ),
                              Group(
                                    UItem('clear_message'),
                                    UItem('message', style='simple', editor=CodeEditor()),
                              ),
                        ),
                       id='ffnet_view.view',
                       width=.8,
                       height=.6,
                       resizable=True
                    )


if __name__ == '__main__':
    FFnetView().configure_traits()
