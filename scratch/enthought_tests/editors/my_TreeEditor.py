#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.

"""
Demonstrates using the TreeEditor to display a hierarchically organized data
structure. 

In this case, the tree has the following hierarchy:
  - Partner
    - Company
      - Department
        - Employee
"""

# Imports:
from traits.api \
    import HasTraits, Str, Regex, List, Instance
    
from traitsui.api \
    import Item, View, TreeEditor, TreeNode

class Employee ( HasTraits ):
    """ Defines a company employee. """
    
    name = Str( '<unknown>' )
    title = Str
    phone = Regex( regex=r'\d\d\d-\d\d\d\d' )
    
    def default_title ( self ):
        self.title = 'Senior Engineer'

class Department ( HasTraits ):
    """ Defines a department with employees. """
    
    name = Str( '<unknown>' )
    employees = List( Employee )

class Stochastic_model ( HasTraits ):
    """ Defines a company with departments and employees. """
    
    name = Str( '<unknown>' )
    departments = List( Department )
    employees = List( Employee )

class Random_variable( HasTraits ):
    pass
class Statistical_correlation( HasTraits ):
    pass
class Sampling_simulation( HasTraits ):
    pass
class General_data( HasTraits ):
    pass
class Simulation_results( HasTraits ):
    pass

# Create an empty view for objects that have no data to display:    
no_view = View()

# Define the TreeEditor used to display the hierarchy:
tree_editor = TreeEditor( 
    nodes=[
        TreeNode( node_for=[ Stochastic_model ],
                  auto_open=True,
                  children='',
                  label='=Stochastic model',
                  view=View( [ 'name' ] ),
        ),
        TreeNode( node_for=[ Stochastic_model ],
                  auto_open=True,
                  #children='Random_variable',
                  label='=Random variable',
        ),
        TreeNode( node_for=[ Stochastic_model ],
                  auto_open=True,
                  #children='Statistical_correlation',
                  label='=Statistical correlation',
        ),
        TreeNode( node_for=[ Sampling_simulation ],
                  auto_open=True,
                  children='',
                  label='=Sampling/Simulation',
                  view=View( [ 'name' ] )
        ),
        TreeNode( node_for=[ Sampling_simulation ],
                  auto_open=True,
                  #children='General_data',
                  label='=General data',
        ),
        TreeNode( node_for=[ Sampling_simulation ],
                  auto_open=True,
                  #children='Check_samples',
                  label='=Check samples',
        ),
        TreeNode( node_for=[ Sampling_simulation ],
                  auto_open=True,
                  #children='Check_varibles_data',
                  label='=Check variables data',
        ),
        TreeNode( node_for=[ Sampling_simulation ],
                  auto_open=True,
                  #children='Model_analysis',
                  label='=Model analysis',
        ),
        TreeNode( node_for=[ Sampling_simulation ],
                  auto_open=True,
                  #children='FORM',
                  label='=FORM',
        ),
        TreeNode( node_for=[ Simulation_results ],
                  auto_open=True,
                  children='',
                  label='=Simulation results',
                  view=View( [ 'name' ] )
        ),
        TreeNode( node_for=[ Simulation_results ],
                  auto_open=True,
                  #children='Histograms',
                  label='=Histograms',
        ),
        TreeNode( node_for=[ Simulation_results ],
                  auto_open=True,
                  #children='Sensitivity_analysis',
                  label='=Sensitivity analysis',
        ),
        TreeNode( node_for=[ Simulation_results ],
                  auto_open=True,
                  #children='Reliability',
                  label='=Reliability',
        ),
        TreeNode( node_for=[ Simulation_results ],
                  auto_open=True,
                  #children='LSF_definition',
                  label='=LSF definition',
        ),
        TreeNode( node_for=[ Employee ],
                  auto_open=True,
                  label='name',
                  view=View( [ 'name', 'title', 'phone' ] )
        )
    ]
 )

class Partner ( HasTraits ):
    """ Defines a business partner."""
    
    name = Str( '<unknown>' )
    company = Instance( Stochastic_model )

    view = View( 
        Item( name='company',
              editor=tree_editor,
              show_label=False
        ),
        title='Company Structure',
        buttons=[ 'OK' ],
        resizable=True,
        style='custom',
        width=.3,
        height=.3
    )

# Create an example data structure:    
jason = Employee( name='Jason',
                   title='Senior Engineer',
                   phone='536-1057' )
mike = Employee( name='Mike',
                   title='Senior Engineer',
                   phone='536-1057' )
dave = Employee( name='Dave',
                   title='Senior Software Developer',
                   phone='536-1057' )
martin = Employee( name='Martin',
                   title='Senior Engineer',
                   phone='536-1057' )
duncan = Employee( name='Duncan',
                   title='Consultant',
                   phone='526-1057' )

# Create the demo:                   
demo = Partner( 
    name='Enthought, Inc.',
    company=Stochastic_model( 
        name='Enthought',
        employees=[ dave, martin, duncan, jason, mike ],
        departments=[ 
            Department( 
                name='Business',
                employees=[ jason, mike ]
            ),
            Department( 
                name='Scientific',
                employees=[ dave, martin, duncan ]
            )
        ]
    )
 )

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
