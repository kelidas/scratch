
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
            self.help_string += ffnet.pikaia.pikaia.__doc__

    view = View(
                UItem('help_string', editor=CodeEditor()),
                width=.5,
                height=.5,
                resizable=True)


class FFnet(HasTraits):

    input_train = Array
    target = Array

    n_inp = Long(enter_set=True, auto_set=False)
    @on_trait_change('input_train')
    def _n_inp_update(self):
        ndim = self.input_train.ndim
        if ndim == 1:
            self.n_inp = 1
        else:
            self.n_inp = self.input_train.shape[1]

    n_hid = List(Long, enter_set=True, auto_set=False)
    @on_trait_change('input_train')
    def _n_hid_update(self):
        ndim = self.input_train.ndim
        if ndim == 1:
            self.n_hid = [1]
        else:
            self.n_hid = [self.input_train.shape[1]]

    n_tar = Long(enter_set=True, auto_set=False)
    @on_trait_change('target')
    def _n_tar_update(self):
        ndim = self.target.ndim
        if ndim == 1:
            self.n_tar = 1
        else:
            self.n_tar = self.target.shape[1]

    bias_enabled = Bool(True)

    net_architecture = Trait('mlgraph - standard multilayer network architecture',
                             {'mlgraph - standard multilayer network architecture': ffnet.mlgraph,
                              'tmlgraph - multilayer network full connectivity list': ffnet.tmlgraph,
                              'imlgraph - multilayer architecture with independent outputs': ffnet.imlgraph,
                                         })

    conec = Array

    net = Instance(ffnet.ffnet)

    create_net = Button
    def _create_net_fired(self):
        self.conec = self.net_architecture_(tuple([self.n_inp] +
                                            self.n_hid +
                                            [self.n_tar]), biases=self.bias_enabled)
        self.net = ffnet.ffnet(self.conec)
        print 'net created'

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

    train_config = Dict({'nproc': 1,
                         'maxfun': None,
                         # 'bounds': (-100, 100),
                         'messages': 1}, auto_set=False, enter_set=True)
    @on_trait_change('training_algorithm')
    def _train_config_update(self):
        if self.training_algorithm == 'train_tnc':
            self.train_config = {'nproc': 1,
                                 'maxfun': None,
                                 # 'bounds': (-100, 100),
                                 'messages': 1}
        elif self.training_algorithm == 'train_momentum':
            self.train_config = {'eta': 0.2,
                                 'momentum': 0.8,
                                 'maxiter': 10000,
                                 'disp': True}
        elif self.training_algorithm == 'train_rprop':
            self.train_config = {'a': 1.2,
                                 'b': 0.5,
                                 'mimin': 1e-6,
                                 'mimax': 50.0,
                                 'xmi': 0.1,
                                 'maxiter':10000,
                                 'disp':True}
        elif self.training_algorithm == 'train_cg':
            self.train_config = {'maxiter': 10000,
                                 'disp': True}
        elif self.training_algorithm == 'train_bfgs':
            self.train_config = {'maxfun': 15000,
                                 # 'bounds': (-100, 100),
                                 'disp':True}
        elif self.training_algorithm == 'train_genetic':
            self.train_config = {'lower':-25,
                                 'upper': 25,
                                 'individuals': 20,
                                 'generations': 500,
                                 'verbosity': 1}

    ffnet_train = Button('train / continue training')
    def _ffnet_train_fired(self):
        f = getattr(self.net, self.training_algorithm)
        import sys; sys.stdout.flush()
        f(self.input_train, self.target, **self.train_config)
        print 'net trained'

    ffnet_test = Button('test')
    def _ffnet_test_fired(self):
        print "TESTING NETWORK..."
        output, regression = self.net.test(self.input_train, self.target, iprint=1)
        Rsquared = regression[0][2]
        maxerr = abs(output - self.target).max()
        print output
        try:
            import matplotlib.pyplot as plt
            plt.plot(self.target.T, 'b--')
            plt.plot(output.T, 'k-')
            plt.legend(('target', 'output'))
            plt.xlabel('pattern')
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

    ffnet_save = Button()

    ffnet_load = Button()

    traits_view = View(
                       Group(
                           Item('net_architecture'),
                           Item('n_inp', style='readonly'),
                           '_',
                            Item('n_hid', style='custom'),
                            '_',
                            Item('n_tar', style='readonly'),
                            Item('bias_enabled'),
                            VGroup(
                                  UItem('create_net'),
                                  UItem('ffnet_plot'),
                                  ),
                            label='ffnet configuration',
                            id='ffnet.configuration',
                            ),
                       Group(
                             Item('training_algorithm'),
                             HGroup(
                                 Item('train_config', springy=True),
                                 UItem('help'),
                             ),
                             VGroup(
                                   UItem('ffnet_train'),
                                   UItem('ffnet_test'),
                                   ),
                             label='training configuration',
                             id='ffnet.training'
                             ),
                       id='ffnet.view',
                       resizable=True,
                        )


class FFnetView(HasTraits):

    input_train_file = File(entries=10)
    target_file = File(entries=10)

    input_file = File(entries=10)

    ffnet = Instance(FFnet, ())

    load_data = Button
    def _load_data_fired(self):
        self.ffnet.input_train = np.loadtxt(self.input_train_file, skiprows=1)
        self.ffnet.target = np.loadtxt(self.target_file, skiprows=1, ndmin=2)

    traits_view = View(
                       Group(
                            Item('input_train_file', id='ffnet_view.infile'),
                            Item('target_file', id='ffnet_view.tarfile'),
                            UItem('load_data'),
                            show_border=True,
                            label='Load data',
                            ),
                        UItem('ffnet@'),
                       id='ffnet_view.view',
                       resizable=True,
                       scrollable=True
                    )


if __name__ == '__main__':
    FFnetView().configure_traits()
