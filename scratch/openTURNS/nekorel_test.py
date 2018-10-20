# Main OpenTURNS module
from openturns import *
# optional matplotlib viewer
from openturns.viewer import View

# dimension
dim = 2

# RandomGenerator.SetSeed(0)

limitState = NumericalMathFunction(['X', 'Y'], ['G'], ['Y+1-X*X'])

x = [0., 4.]
print 'x=', x
print 'G(x)=', limitState(x)

# Create a first marginal : LogNormal distribution 1D, parameterized by
# its mean and standard deviation
R_dist = Normal(0., 1.)
R_dist.setName('X')
R_dist.setDescription('X')
# Graphical output of the PDF
R_pdf = R_dist.drawPDF()
# View(R_pdf).save('pdf_X.png')
View(R_pdf).show()

# Create a second marginal : Normal distribution 1D
F_dist = Normal(4., 2.)
F_dist.setName('Y')
F_dist.setDescription('Y')
# Graphical output of the PDF
F_pdf = F_dist.drawPDF()
# View(F_pdf).save('pdf_Y.png')
View(F_pdf).show()

# Create a copula : IndependentCopula (no correlation)
aCopula = IndependentCopula(dim)
aCopula.setName('Independent copula')

# Instanciate one distribution object
myDistribution = ComposedDistribution([R_dist, F_dist], aCopula)
myDistribution.setName('myDist')

# We create a 'usual' RandomVector from the Distribution
vect = RandomVector(myDistribution)

# We create a composite random vector
G = RandomVector(limitState, vect)

# We create an Event from this RandomVector
myEvent = Event(G, Less(), 0.0, 'Event 1')

cv = 0.05
NbSim = 100000

algoMC = MonteCarlo(myEvent)
algoMC.setMaximumOuterSampling(NbSim)
algoMC.setBlockSize(1)
algoMC.setMaximumCoefficientOfVariation(cv)
# For statistics about the algorithm
initialNumberOfCall = limitState.getEvaluationCallsNumber()

algoMC.run()

result = algoMC.getResult()
probability = result.getProbabilityEstimate()
print 'MonteCarlo result=', result
print 'Number of executed iterations =', result.getOuterSampling()
print 'Number of calls to the limit state =', limitState.getEvaluationCallsNumber() - initialNumberOfCall
print 'Pf = ', probability
print 'CV =', result.getCoefficientOfVariation()
MCcvgraph = algoMC.drawProbabilityConvergence()
# View(MCcvgraph).save('montecarlo_convergence.png')
View(MCcvgraph).show()


myCobyla = Cobyla()
# Resolution options:
eps = 1e-3
myCobyla.setMaximumIterationsNumber(1000)
myCobyla.setMaximumAbsoluteError(eps)
myCobyla.setMaximumRelativeError(eps)
myCobyla.setMaximumResidualError(eps)
myCobyla.setMaximumConstraintError(eps)

# For statistics about the algorithm
initialNumberOfCall = limitState.getEvaluationCallsNumber()

# We create a FORM algorithm
# The first parameter is a NearestPointAlgorithm
# The second parameter is an event
# The third parameter is a starting point for the design point research

algoFORM = FORM(myCobyla, myEvent, myDistribution.getMean())

algoFORM.run()

result = algoFORM.getResult()
print 'Number of calls to the limit state =', limitState.getEvaluationCallsNumber() - initialNumberOfCall
print 'Beta =', result.getGeneralisedReliabilityIndex()
print 'Pf =', result.getEventProbability()

# Graphical result output
importanceFactorsGraph = result.drawImportanceFactors()
# View(importanceFactorsGraph).save('importance_factors.png')
View(importanceFactorsGraph).show()


cv = 0.05
NbSim = 100000

algoDS = DirectionalSampling(myEvent)
algoDS.setMaximumOuterSampling(NbSim)
algoDS.setBlockSize(1)
algoDS.setMaximumCoefficientOfVariation(cv)
# For statistics about the algorithm
initialNumberOfCall = limitState.getEvaluationCallsNumber()

algoDS.run()

result = algoDS.getResult()
probability = result.getProbabilityEstimate()
print 'Number of executed iterations =', result.getOuterSampling()
print 'Number of calls to the limit state =', limitState.getEvaluationCallsNumber() - initialNumberOfCall
print 'Pf = ', probability
print 'CV =', result.getCoefficientOfVariation()
DScvgraph = algoDS.drawProbabilityConvergence()
# View(DScvgraph).save('directionalsampling_convergence.png')
View(DScvgraph).show()
