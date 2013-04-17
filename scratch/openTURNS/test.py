# Main OpenTURNS module
from openturns import *
# OpenTURNS viewer capability (since release 0.9.2)
# from openturns_viewer import ViewImage
# New syntax
from openturns.viewer import ViewImage

# Constant definition:
stochasticDimension = 2

# Random generator initialization:
RandomGenerator().SetSeed( 0 )

#Analytical model definition:

# Analytical construction : Input
inputFunction = Description( stochasticDimension )
inputFunction[0] = "R"
inputFunction[1] = "F"

# Analytical construction : Output
outputFunction = Description( 1 )
outputFunction[0] = "G"

formulas = Description( outputFunction.getSize() )
# Here, _pi is the built-in constant _pi=3.14159265....
formulas[0] = "R-F/(_pi*100.0)"

LimitState = NumericalMathFunction( inputFunction, outputFunction, formulas )

# Test of the limit state function:
x = NumericalPoint( stochasticDimension, 0 )
x[0] = 300.0
x[1] = 75000.0
print "x=" , x
print "G(x)=" , LimitState( x )

# Stochastic model definition:

# Mean
mean = NumericalPoint( stochasticDimension, 0.0 )
mean[0] = 300.0
mean[1] = 75000.0

# Standard deviation
sigma = NumericalPoint( stochasticDimension, 0.0 )
sigma[0] = 30.0
sigma[1] = 5000.0

# Additional parameters for the lognormal distribution:
component = Description( 1 )
BorneInf = 0.0

# Initialization of the distribution collection:
aCollection = DistributionCollection()

# Create a first marginal : LogNormal distribution 1D, parameterized by its mean and standard deviation
marginal = LogNormal( mean[0], sigma[0], BorneInf, LogNormal.MUSIGMA )
marginal.setName( "Yield strength" )
component[0] = "R"
marginal.setDescription( component )
# Graphical output of the PDF
pdfgraph1 = marginal.drawPDF()
# If the directory name is omitted, the graph will be produced in the current directory.
# If the dimensions are omitted, the default is 400x300 up to release 0.10.0, and 640x480 for the later releases
pdfgraph1.draw( "tmp/pdf_R", 640, 480 )
# Visualize the graph
ViewImage( pdfgraph1.getBitmap() )
# Fill the first marginal of aCollection
aCollection.add( Distribution( marginal, "Yield strength" ) )

# Create a second marginal : Normal distribution 1D
marginal = Normal( mean[1], sigma[1] )
marginal.setName( "Traction_load" )
component[0] = "F"
marginal.setDescription( component )
# Graphical output of the PDF
pdfgraph2 = marginal.drawPDF()
pdfgraph2.draw( "tmp/pdf_F", 640, 480 )
ViewImage( pdfgraph2.getBitmap() )
# Fill the second marginal of aCollection
aCollection.add( Distribution( marginal, "Traction_load" ) )

# Create a copula : IndependentCopula (no correlation)
aCopula = IndependentCopula( aCollection.getSize() )
aCopula.setName( "Independent copula" )

# Instanciate one distribution object
myDistribution = ComposedDistribution( aCollection, Copula( aCopula ) )
myDistribution.setName( "myDist" )

# We create a 'usual' RandomVector from the Distribution
vect = RandomVector( Distribution( myDistribution ) )

# We create a composite random vector
G = RandomVector( LimitState, vect )

# We create an Event from this RandomVector
myEvent = Event( G, ComparisonOperator( Less() ), 0.0, "Event 1" )

# Using Monte Carlo simulations

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
print "Number of calls to the limit state =" , LimitState.getEvaluationCallsNumber() - initialNumberOfCall
print "Pf = " , probability
print "CV =" , result.getCoefficientOfVariation()
MCcvgraph = algoMC.drawProbabilityConvergence()
MCcvgraph.draw( "tmp/montecarlo_convergence", 640, 480 )
ViewImage( MCcvgraph.getBitmap() )

# Using FORM analysis

# Resolution options:
eps = 1E-3

# We create a NearestPoint algorithm
myCobyla = Cobyla()
myCobyla.setSpecificParameters( CobylaSpecificParameters() )
myCobyla.setMaximumIterationsNumber( 100 )
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
result = algoFORM.getResult()
print "Number of calls to the limit state =" , LimitState.getEvaluationCallsNumber() - initialNumberOfCall
print "Pf =" , result.getEventProbability()

# Graphical result output
importanceFactorsGraph = result.drawImportanceFactors()
importanceFactorsGraph.draw( "tmp/importance_factors", 640, 480 )
ViewImage( importanceFactorsGraph.getBitmap() )

# Using Directional sampling

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
DScvgraph.draw( "tmp/directionalsampling_convergence", 640, 480 )
ViewImage( DScvgraph.getBitmap() )

