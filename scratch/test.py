from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

import numpy as np
from etsproxy.traits.api import \
    HasTraits, Int, Array, Str, implements, Range, Property, cached_property, File, \
     Float, Instance, Any, Interface, Event, on_trait_change, Button, Bool, Callable, BaseFloat, Trait
from etsproxy.traits.ui.api import \
    View, Item, Group, VGroup, HGroup, HSplit, VSplit, Tabbed, ModelView, Controller
from math import pi, e
from mathkit.mfn.mfn_line.mfn_line import \
    MFnLineArray
from numpy import \
    sign, linspace, array, cos, sqrt, argmax, hstack, max, zeros_like, argwhere, loadtxt
from spirrid.i_rf import \
    IRF
from spirrid.rf import RF
from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

class PosFloat (BaseFloat):
    # : The function to use for evaluating strings to this type:
    evaluate = float

    # : The default value for the trait:
    default_value = 1.0

    # : A description of the type of value this trait accepts:
    info_text = 'positive float'

    def validate (self, object, name, value):
        """ Validates that a specified value is valid for this trait.

            Note: The 'fast validator' version performs this check in C.
        """
        if value >= 0:
            return value

        else:
            self.error(object, name, value)
            self.default_value = 0.0

class a(HasTraits):

    tl = PosFloat
    b = Trait([1, 2, 3])



aa = a()
aa.configure_traits()



#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.


#-- Imports ------------------------------------------------------------------

from traits.api \
    import HasPrivateTraits, List, Str, Property, on_trait_change

from traitsui.api \
    import View, HGroup, Item, TabularEditor

from traitsui.tabular_adapter \
    import TabularAdapter

from traitsui.ui_editor \
    import UIEditor

from traitsui.basic_editor_factory \
    import BasicEditorFactory

#-- Define the reusable StringListEditor class and its helper classes --------

# Define the tabular adapter used by the Traits UI string list editor:
class MultiSelectAdapter (TabularAdapter):

    # The columns in the table (just the string value):
    columns = [ ('Value', 'value') ]

    # The text property used for the 'value' column:
    value_text = Property

    def _get_value_text (self):
        return self.item

# Define the actual Traits UI string list editor:
class _StringListEditor (UIEditor):

    # Indicate that the editor is scrollable/resizable:
    scrollable = True

    # The list of available editor choices:
    choices = List(Str)

    # The list of currently selected items:
    selected = List(Str)

    border_size = Int

    layout_style = Int

    # The traits UI view used by the editor:
    view = View(
        Item('choices',
              show_label=False,
              editor=TabularEditor(
                               show_titles=False,
                               selected='selected',
                               editable=False,
                               multi_select=True,
                               adapter=MultiSelectAdapter())
        ),
        id='string_list_editor',
        resizable=True
    )

    def init_ui (self, parent):

        self.sync_value(self.factory.choices, 'choices', 'from',
                         is_list=True)
        self.selected = self.value

        return self.edit_traits(parent=parent, kind='subpanel')

    @on_trait_change(' selected')
    def _selected_modified (self):
        self.value = self.selected

# Define the StringListEditor class used by client code:
class StringListEditor (BasicEditorFactory):

    # The editor implementation class:
    klass = _StringListEditor

    # The extended trait name containing the editor's set of choices:
    choices = Str

#-- Define the demo class ----------------------------------------------------

class MultiSelect (HasPrivateTraits):
    """ This class demonstrates using the StringListEditor to select a set
        of string values from a set of choices.
    """

    # The list of choices to select from:
    choices = List(Str)

    # The currently selected list of choices:
    selected = List(Str)

    # A dummy result so that we can display the selection using the same
    # StringListEditor:
    result = List(Str)

    # A traits view showing the list of choices on the left-hand side, and
    # the currently selected choices on the right-hand side:
    view = View(
        HGroup(
            Item('selected',
                  show_label=False,
                  editor=StringListEditor(choices='choices')
            ),
            Item('result',
                  show_label=False,
                  editor=StringListEditor(choices='selected')
            )
        ),
        width=0.20,
        height=0.25
    )

# Create the demo:
demo = MultiSelect(choices=[ 'one', 'two', 'three', 'four', 'five', 'six',
                                 'seven', 'eight', 'nine', 'ten' ],
                    selected=[ 'two', 'five', 'nine' ])

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
