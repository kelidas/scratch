'''
Created on 24.3.2010

@author: Vasek
'''

#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.# Imports: 
from random \
    import randint, choice
    
from traits.api \
    import HasStrictTraits, Str, Int, Float, List, Bool, Property, Enum
    
from traitsui.api \
    import View, Item, TableEditor
    
from traitsui.table_column \
    import ObjectColumn
    
from traitsui.extras.checkbox_column \
    import CheckboxColumn
    

# Create a specialized column to set the text color differently based upon
# whether or not the player is in the lineup:
class TabColumn ( ObjectColumn ):
    
    # Override some default settings for the column:
    width = 0.1
    horizontal_alignment = 'center'

#    def get_text_color ( self, object ):
#        return [ 'light grey', 'black' ][ object.num ]
   
        
# The 'players' trait table editor:
tab_editor = TableEditor( 
    sortable=False,
    #configurable=False,
    auto_size=False,
    sort_model=False,
    selection_mode=( 'cells' ),
    columns=[ TabColumn( name='num', label='Num',
                                 width=0.08, editable=False ),
                 TabColumn( name='name', label='Name', width=0.15,
                               horizontal_alignment='left' ),
                 TabColumn( name='distrib', label='Distribution' , width=0.15, cell_color='wheat' ),
                 TabColumn( name='descript', label='Descriptors', width=0.2 ),
                 TabColumn( name='mean', label='Mean' ),
                 TabColumn( name='std', label='Std' ),
                 TabColumn( name='cov', label='COV' ),
                 TabColumn( name='skew', label='Skew' ),
                 TabColumn( name='kurt', label='Kurtosis' ),
                 TabColumn( name='status', label='Status' )
                     ] )

# 'Player' class:  
class RV ( HasStrictTraits ):
    
    # Trait definitions:  
    num = Int
    name = Str
    distrib = Enum( 'Normal', 'Uniform', 'Weibull', modified=True )
    descript = Enum( 'Moments', 'Parameters', 'Moments and parameters', modified=True )
    mean = Float
    std = Float
    cov = Float
    skew = Float
    kurt = Float
    status = Str
    #average = Property( Float )
    
    
    def _get_average ( self ):
        """ Computes the player's batting average from the current statistics.
        """
        if self.at_bats == 0:
            return 0.0
            
        return float( self.singles + self.doubles + 
                      self.triples + self.home_runs ) / self.at_bats

                      
class Team ( HasStrictTraits ):
    
    # Trait definitions:
    RVs = List( RV )
    
    # Trait view definitions:
    traits_view = View( 
        Item( 'RVs',
              show_label=False,
              editor=tab_editor
        ),
        title='Random variable',
        width=1,
        height=0.5,
        resizable=True
    )


def random_RV ( name ):    
    """ Generates and returns a random player.
    """
    p = RV( num=randint( 0, 10 ),
           name=name,
            distrib=choice( ['Normal', 'Uniform', 'Weibull'] ),
            descript=choice( ['Moments', 'Parameters', 'Moments and parameters'] ),
                mean=randint( 0, 50 ),
                std=randint( 0, 50 ),
                cov=randint( 0, 30 ),
                skew=randint( 0, 20 ),
                kurt=randint( 0, 5 ),
                status='OK' ) 
    return p
    
# Create the demo:  
demo = view = Team( RVs=[ random_RV( name ) for name in [
    'Dave', 'Mike', 'Joe', 'Tom', 'Dick', 'Harry', 'Dirk', 'Fields', 'Stretch'
]] )

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
