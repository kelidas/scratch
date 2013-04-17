

# Main OpenTURNS module
from openturns import *
# OpenTURNS viewer capability (since release 0.9.2)
# from openturns_viewer import ViewImage
# New syntax
from openturns.viewer import ViewImage
import re
import numpy as np



# Constant definition:
stochasticDimension = 4

# Random generator initialization:
RandomGenerator().SetSeed( 0 )

#Analytical model definition:

# Analytical construction : Input
inputFunction = Description( stochasticDimension )
inputFunction[0] = "x1"
inputFunction[1] = "x2"
inputFunction[2] = "x3"
inputFunction[3] = "x4"

# Analytical construction : Output
outputFunction = Description( 1 )
outputFunction[0] = "G1"

formulas = Description( outputFunction.getSize() )
# Here, _pi is the built-in constant _pi=3.14159265....
#formulas[0] = "x1 * x1 - 4 * x2 - 2 * x3 * x4"
formulas[0] = "2 * x1 * x4 - x2 * x3"
#formulas[0] = "x1 * x2 * x4 -  2 * x3"

LimitState = NumericalMathFunction( inputFunction, outputFunction, formulas )

# Test of the limit state function:
x = NumericalPoint( stochasticDimension, 0 )
x[0] = 6.0
x[1] = 3.4718
x[2] = 2.356
x[3] = 1.0
print "x=" , x
print "G1(x)=" , LimitState( x )


# Stochastic model definition:

# Mean
mean = NumericalPoint( stochasticDimension, 0.0 )
mean[0] = x[0]
mean[1] = x[1]
mean[2] = x[2]
mean[3] = x[3]

# Standard deviation
sigma = NumericalPoint( stochasticDimension, 0.0 )
sigma[0] = .77479
sigma[1] = 0.2 * mean[1]
sigma[2] = 0.1 * mean[2]
sigma[3] = .1



# Additional parameters for the lognormal distribution:
component = Description( 1 )
BorneInf = 0.0

# Initialization of the distribution collection:
aCollection = DistributionCollection()

# Create a first marginal : Normal distribution 1D
marginal = Normal( mean[0], sigma[0] )
marginal.setName( "x1" )
component[0] = "x1"
marginal.setDescription( component )
# Graphical output of the PDF
pdfgraph1 = marginal.drawPDF()
pdfgraph1.draw( "korel_paper/pdf_x1", 640, 480 )

#ViewImage( pdfgraph2.getBitmap() )
# Fill the second marginal of aCollection
aCollection.add( Distribution( marginal, "x1" ) )

# Create a second marginal : LogNormal distribution 1D, parameterized by its mean and standard deviation
marginal = LogNormal( mean[1], sigma[1], BorneInf, LogNormal.MUSIGMA )
marginal.setName( "x2" )
component[0] = "x2"
marginal.setDescription( component )
# Graphical output of the PDF
pdfgraph2 = marginal.drawPDF()

# If the directory name is omitted, the graph will be produced in the current directory.
# If the dimensions are omitted, the default is 400x300 up to release 0.10.0, and 640x480 for the later releases
pdfgraph2.draw( "korel_paper/x2", 640, 480 )
# Visualize the graph
#ViewImage( pdfgraph1.getBitmap() )
# Fill the first marginal of aCollection
aCollection.add( Distribution( marginal, "x2" ) )

# Create a third marginal : LogNormal distribution 1D, parameterized by its mean and standard deviation
marginal = LogNormal( mean[2], sigma[2], BorneInf, LogNormal.MUSIGMA )
marginal.setName( "x3" )
component[0] = "x3"
marginal.setDescription( component )
# Graphical output of the PDF
pdfgraph3 = marginal.drawPDF()

# If the directory name is omitted, the graph will be produced in the current directory.
# If the dimensions are omitted, the default is 400x300 up to release 0.10.0, and 640x480 for the later releases
pdfgraph3.draw( "korel_paper/x3", 640, 480 )
# Visualize the graph
#ViewImage( pdfgraph1.getBitmap() )
# Fill the first marginal of aCollection
aCollection.add( Distribution( marginal, "x3" ) )


# Create a fourth marginal : Gumbel Max distribution 1D
marginal = Gumbel( mean[3], sigma[3], Gumbel.MUSIGMA )
marginal.setName( "x4" )
component[0] = "x4"
marginal.setDescription( component )
# Graphical output of the PDF
pdfgraph4 = marginal.drawPDF()
pdfgraph4.draw( "korel_paper/x4", 640, 480 )

#ViewImage( pdfgraph4.getBitmap() )
# Fill the second marginal of aCollection
aCollection.add( Distribution( marginal, "Section modulus -- plastic" ) )

# Visualize all graphs
ViewImage( pdfgraph1.getBitmap() )
ViewImage( pdfgraph2.getBitmap() )
ViewImage( pdfgraph3.getBitmap() )
ViewImage( pdfgraph4.getBitmap() )






# Create t h e Spearman c o r r e l a t i o n m a t r i x o f t h e i n p u t random v e c t o r
RS = CorrelationMatrix( 4 )
RS [ 0, 1 ] = .8
# E v a l u a t e t h e c o r r e l a t i o n m a t r i x o f t h e Normal c o p u l a from RS
R = NormalCopula.GetCorrelationFromSpearmanCorrelation( RS )
# Create t h e Normal c o p u l a p a r a m e t r i z e d by R
aCopula = NormalCopula ( R ) #copuleNormal





# Create a copula : IndependentCopula (no correlation)
#aCopula = IndependentCopula( aCollection.getSize() )
aCopula.setName( "Gaussian copula 0.8" )

# Instanciate one distribution object
myDistribution = ComposedDistribution( aCollection, Copula( aCopula ) )
myDistribution.setName( "myDist" )

# We create a 'usual' RandomVector from the Distribution
vect = RandomVector( Distribution( myDistribution ) )

# We create a composite random vector
Z = RandomVector( LimitState, vect )

# We create an Event from this RandomVector
myEvent = Event( Z, ComparisonOperator( Less() ), 0.0, "Event 1" )


#-------------------------------------------------------------------------------
# Using Monte Carlo simulations
#-------------------------------------------------------------------------------

# Resolution options:
cv = 0.05
NbSim = 100000

algoMC = MonteCarlo( myEvent )
algoMC.setMaximumOuterSampling( NbSim )
algoMC.setBlockSize( 1 )
algoMC.setMaximumCoefficientOfVariation( cv )
# For statistics about the algorithm
initialNumberOfCall = LimitState.getEvaluationCallsNumber()

# Perform the analysis:
algoMC.run()

# Results:
result = algoMC.getResult()
probability = result.getProbabilityEstimate()
print "MonteCarlo result=" , result
print "Number of executed iterations =" , result.getOuterSampling()
print "Number of calls to the limit state =" , \
                LimitState.getEvaluationCallsNumber() - initialNumberOfCall
print "Pf = " , probability
print "CV =" , result.getCoefficientOfVariation()
MCcvgraph = algoMC.drawProbabilityConvergence()
MCcvgraph.draw( "beam_fig/montecarlo_convergence", 640, 480 )
ViewImage( MCcvgraph.getBitmap() )

#-------------------------------------------------------------------------------
# Using FORM analysis
#-------------------------------------------------------------------------------


# Resolution options:
eps = 1E-6
maxiter = 100

# We create a NearestPoint algorithm
myCobyla = Cobyla()
myCobyla.setSpecificParameters( CobylaSpecificParameters() )
myCobyla.setMaximumIterationsNumber( maxiter )
myCobyla.setMaximumAbsoluteError( eps )
myCobyla.setMaximumRelativeError( eps )
myCobyla.setMaximumResidualError( eps )
myCobyla.setMaximumConstraintError( eps )

# For statistics about the algorithm
initialNumberOfCall = LimitState.getEvaluationCallsNumber()

# We create a FORM algorithm
# The first parameter is a NearestPointAlgorithm
# The second parameter is an event
# The third parameter is a starting point for the design point research

algoFORM = FORM( NearestPointAlgorithm( myCobyla ), myEvent, mean )

# Perform the analysis:
algoFORM.run()

# Results:
resultFORM = algoFORM.getResult()
print "Number of calls to the limit state FORM =", \
            LimitState.getEvaluationCallsNumber() - initialNumberOfCall
print "FORM Pf =", resultFORM.getEventProbability()
print "FORM Beta =", resultFORM.getGeneralisedReliabilityIndex()


# Graphical resultFORM output
importanceFactorsGraph = resultFORM.drawImportanceFactors()
importanceFactorsGraph.draw( "beam_fig/importance_factors", 640, 480 )
ViewImage( importanceFactorsGraph.getBitmap() )

#-------------------------------------------------------------------------------
# Using SORM analysis
#-------------------------------------------------------------------------------

# Resolution options:
eps = 1E-6
maxiter = 100

# We create a NearestPoint algorithm
myCobyla = Cobyla()
myCobyla.setSpecificParameters( CobylaSpecificParameters() )
myCobyla.setMaximumIterationsNumber( maxiter )
myCobyla.setMaximumAbsoluteError( eps )
myCobyla.setMaximumRelativeError( eps )
myCobyla.setMaximumResidualError( eps )
myCobyla.setMaximumConstraintError( eps )

# For statistics about the algorithm
initialNumberOfCall = LimitState.getEvaluationCallsNumber()

# We create a SORM algorithm
# The first parameter is a NearestPointAlgorithm
# The second parameter is an event
# The third parameter is a starting point for the design point research

algoSORM = SORM( NearestPointAlgorithm( myCobyla ), myEvent, mean )

# Perform the analysis:
algoSORM.run()

# Results:
resultSORM = algoSORM.getResult()
print "Number of calls to the limit state SORM =", \
                LimitState.getEvaluationCallsNumber() - initialNumberOfCall
print "SORM Pf =", resultSORM.getEventProbabilityBreitung()
print "SORM Beta =", resultSORM.getGeneralisedReliabilityIndexBreitung()


# Graphical resultSORM output
importanceFactorsGraph = resultSORM.drawImportanceFactors()
importanceFactorsGraph.draw( "beam_fig/importance_factors", 640, 480 )
ViewImage( importanceFactorsGraph.getBitmap() )


#-------------------------------------------------------------------------------
# Using Directional sampling
#-------------------------------------------------------------------------------

# Resolution options:
cv = 0.05
NbSim = 100000

algoDS = DirectionalSampling( myEvent )
algoDS.setMaximumOuterSampling( NbSim )
algoDS.setBlockSize( 1 )
algoDS.setMaximumCoefficientOfVariation( cv )
# For statistics about the algorithm
initialNumberOfCall = LimitState.getEvaluationCallsNumber()

# Perform the analysis:
algoDS.run()

# Results:
result = algoDS.getResult()
probability = result.getProbabilityEstimate()
print "Number of executed iterations =" , result.getOuterSampling()
print "Number of calls to the limit state =" , LimitState.getEvaluationCallsNumber() - initialNumberOfCall
print "Pf = " , probability
print "CV =" , result.getCoefficientOfVariation()
DScvgraph = algoDS.drawProbabilityConvergence()
DScvgraph.draw( "beam_fig/directionalsampling_convergence", 640, 480 )
ViewImage( DScvgraph.getBitmap() )

