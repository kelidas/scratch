from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton

STEP_STR = r'''STEP id {0} STATIC name "Load step No.{0}"
LOAD CASE  1 * 1.0000000  2 * 10.0000000  65535 * 1.0000000
EXECUTE
STORE "results\result.{0:03d}"    
'''

class StepGen(HasTraits):
    start_step = Int(1)
    last_step = Int(5)
    step_str = Str(STEP_STR)

    generate = Button()
    def _generate_fired(self):
        self.steps = ''
        for i in range(self.start_step, self.last_step + 1):
            self.steps += self.step_str.format(i) + '\n'

    steps = Str

    traits_view = View(
                       Item('start_step'),
                       Item('last_step'),
                       Item('step_str', style='custom', tooltip='help'),
                       Item('generate'),
                       Item('steps', style='custom'),
                        title='StepGen',
                        id='',
                        dock='tab',
                        resizable=True,
                        width=.4,
                        height=.5,
                        buttons=[OKButton])


if __name__ == '__main__':
    stepgen = StepGen()
    stepgen.configure_traits()
