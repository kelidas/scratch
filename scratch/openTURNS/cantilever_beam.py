
from openturns import *
from math import *

#===============================================================================
#  Function 'deviation'
#===============================================================================
# Create here the python lines to define the implementation of the function

# In order to be able to use that function with the openturns library, 
# it is necessary to define a class which derives from OpenTURNSPythonFunction

class modelePYTHON( OpenTURNSPythonFunction ):
    # that following method defines the input size (4) and the output size (1)
    def __init__( self ):
        OpenTURNSPythonFunction.__init__( self, 4, 1 )

    # that following method gives the implementation of modelePYTHON
    def f( self, x ):
        E = x[0]
        F = x[1]
        L = x[2]
        I = x[3]
        return [( F * L * L * L ) / ( 3. * E * I )]

# Use that function defined in the script python
# with the openturns library
# Create a NumericalMathFunction from modelePYTHON
deviation = NumericalMathFunction( modelePYTHON() )


#===============================================================================
# Input random vector
#===============================================================================

# Create the marginal distributions of the input random vector
distributionE = Beta( 0.93, 3.2, 2.8e7, 4.8e7 )
distributionF = LogNormal( 30000, 9000, 15000, LogNormal.MUSIGMA )
distributionL = Uniform( 250, 260 )
distributionI = Beta( 2.5, 4.0, 3.1e2, 4.5e2 )

# Visualize the probability density function

pdfLoiE = distributionE.drawPDF()
# Change the legend
draw_E = pdfLoiE.getDrawable( 0 )
draw_E.setLegendName( 'Beta( 0.93, 3.2, 2.8e7, 4.8e7 )' )
pdfLoiE.setDrawable( draw_E, 0 )
# Change the title
pdfLoiE.setTitle( 'PDF of E' )

pdfLoiE.draw( 'cantilever_beam/distributionE_pdf', 640, 480 )
#Show( pdfLoiE )


pdfLoiF = distributionF.drawPDF()
# Change the legend
draw_F = pdfLoiF.getDrawable( 0 )
draw_F.setLegendName( 'LogNormal( 30000, 9000, 15000 )' )
pdfLoiF.setDrawable( draw_F, 0 )
# Change the title
pdfLoiF.setTitle( 'PDF of F' )

pdfLoiF.draw( 'cantilever_beam/distributionF_pdf', 640, 480 )
#Show( pdfLoiF )


pdfLoiL = distributionL.drawPDF()
# Change the legend
draw_L = pdfLoiL.getDrawable( 0 )
draw_L.setLegendName( 'Uniform( 250, 260 )' )
pdfLoiL.setDrawable( draw_L, 0 )
# Change the title
pdfLoiL.setTitle( 'PDF of L' )

pdfLoiL.draw( 'cantilever_beam/distributionL_pdf', 640, 480 )
#Show( pdfLoiL )


pdfLoiI = distributionI.drawPDF()
# Change the legend
draw_I = pdfLoiI.getDrawable( 0 )
draw_I.setLegendName( 'Beta( 2.5, 4.0, 3.1e2, 4.5e2 )' )
pdfLoiI.setDrawable( draw_I, 0 )
# Change the title
pdfLoiI.setTitle( 'PDF of I' )

pdfLoiI.draw( 'cantilever_beam/distributionI_pdf', 640, 480 )
#Show( pdfLoiI )


# Create the Spearman correlation matrix of the input random vector
RS = CorrelationMatrix( 4 )
RS[2, 3] = -.2

# Evaluate the correlation matrix of the Normal copula from RS
R = NormalCopula.GetCorrelationFromSpearmanCorrelation( RS )

# Create the Normal copula parametrized by R
copuleNormal = NormalCopula( R )

# Create collection of the marginal distributions
collectionMarginals = DistributionCollection( 4 )
collectionMarginals[0] = Distribution( distributionE )
collectionMarginals[1] = Distribution( distributionF )
collectionMarginals[2] = Distribution( distributionL )
collectionMarginals[3] = Distribution( distributionI )

# Create the input probability distribution of dimension 4
inputDistribution = ComposedDistribution( collectionMarginals,
                                         Copula( copuleNormal ) )

# Give a description of each component of the input distribution
inputDescription = Description( 4 )
inputDescription[0] = 'E'
inputDescription[1] = 'F'
inputDescription[2] = 'L'
inputDescription[3] = 'I'
inputDistribution.setDescription( inputDescription )

# Create the input random vector
inputRandomVector = RandomVector( inputDistribution )

# Create the output variable of interest
outputVariableOfInterest = RandomVector( deviation, inputRandomVector )


#===============================================================================
# Min/Max approach Study
#===============================================================================

print '##################################################'
print 'Min/Max study with deterministic experiment plane'
print '##################################################'

dim = deviation.getInputDimension()

# Create the structure of the experiment plane: Composite type

# On each direction separately, several levels are evaluated
# here, 3 levels: +/- 0.5, +/-1., +/-3. from the center
levelsNumber = 3
levels = NumericalPoint( levelsNumber, 0.0 )
levels[0] = 0.5
levels[1] = 1.0
levels[2] = 3.0
# Creation of the composite plane
myPlane = Composite( dim, levels )

# Generation of points according the structure of the experiment plane
# (in a reduced centered space)
inputSample = myPlane.generate()

# Scaling of the structure of the experiment plane
# scaling vector for each dimension of the levels of the structure
# to take into account the dimension of each component
# for example: the standard deviation of each component of 'inputRandomVector'
# in case of a RandomVector
scaling = NumericalPoint( dim )
scaling[0] = sqrt( inputRandomVector.getCovariance()[0, 0] )
scaling[1] = sqrt( inputRandomVector.getCovariance()[1, 1] )
scaling[2] = sqrt( inputRandomVector.getCovariance()[2, 2] )
scaling[3] = sqrt( inputRandomVector.getCovariance()[3, 3] )

inputSample.scale( scaling )

# Translation of the nonReducedSample onto the center of the experiment plane
# center = mean point of the inputRandomVector distribution
center = inputRandomVector.getMean()
inputSample.translate( center )

# Get the number of points in the experiment plane
pointNumber = inputSample.getSize()

# Evaluate the output variable of interes on the experiment plane
outputSample = deviation( inputSample )


# Evaluate the range of the output variable of interest on that experiment plane
minValue = outputSample.getMin()
maxValue = outputSample.getMax()

print 'From composite experiment plane of size = ', pointNumber
print 'Levels = ', levels[0], ', ', levels[1], ', ', levels[2]
print 'Min Value = ', minValue[0]
print 'Max Value = ', maxValue[0]
print ''


#===============================================================================
# Min/Max study by random sampling
#===============================================================================

print '################################'
print 'Min/Max study by random sampling'
print '################################'

pointNumber = 10000
print 'From random sampling = ', pointNumber
outputSample2 = outputVariableOfInterest.getNumericalSample( pointNumber )

minValue2 = outputSample2.getMin()
maxValue2 = outputSample2.getMax()

print 'Min Value = ', minValue2[0]
print 'Max Value = ', maxValue2[0]
print ''





print ''
#####################################################
### Random Study : central tendance of
### the output variable of interest
#####################################################

print '#########################################'
print 'Random Study : central tendance of'
print 'the output variable of interest'
print '#########################################'
print ''


#===============================================================================
# Taylor variance decomposition
#===============================================================================

print '###################################'
print 'Taylor variance decomposition'
print '###################################'
print ''

# We create a quadraticCumul algorithm
myQuadraticCumul = QuadraticCumul( outputVariableOfInterest )

# We compute the several elements provided by the quadratic cumul algorithm
# and evaluate the number of calculus needed
nbBefr = deviation.getEvaluationCallsNumber()

# Mean first order
meanFirstOrder = myQuadraticCumul.getMeanFirstOrder()[0]
nbAfter1 = deviation.getEvaluationCallsNumber()

# Mean second order
meanSecondOrder = myQuadraticCumul.getMeanSecondOrder()[0]
nbAfter2 = deviation.getEvaluationCallsNumber()

# Standard deviation
stdDeviation = sqrt( myQuadraticCumul.getCovariance()[0, 0] )
nbAfter3 = deviation.getEvaluationCallsNumber()

print 'First order mean = ', myQuadraticCumul.getMeanFirstOrder()[0]
print 'Evaluation calls number = ', nbAfter1 - nbBefr
print 'Second order mean = ', myQuadraticCumul.getMeanSecondOrder()[0]
print 'Evaluation calls number = ', nbAfter2 - nbAfter1
print 'Standard deviation = ', sqrt( myQuadraticCumul.getCovariance()[0, 0] )
print 'Evaluation calls number = ', nbAfter3 - nbAfter2

print 'Importance factors = '
for i in range( inputRandomVector.getDimension() ):
    print inputDistribution.getDescription()[i], ' = ', myQuadraticCumul.getImportanceFactors()[i]
print ''


#===============================================================================
# Random sampling
#===============================================================================

print '#####################'
print 'Random sampling'
print '#####################'

size1 = 10000
output_Sample1 = outputVariableOfInterest.getNumericalSample( size1 )
outputMean = output_Sample1.computeMean()
outputCovariance = output_Sample1.computeCovariance()

print 'Sample size = ', size1
print 'Mean from sample = ', outputMean[0]
print 'Standard deviation from sample = ', sqrt( outputCovariance[0, 0] )

#===============================================================================
# Kernel Smoothing Fitting
#===============================================================================

print '##########################'
print '# Kernel Smoothing Fitting'
print '##########################'

# We generate a sample of the output variable
size = 10000
output_sample = outputVariableOfInterest.getNumericalSample( size )

# We build the kernel smoothing distribution
kernel = KernelSmoothing()
bw = kernel.computeSilvermanBandwidth( output_sample )
smoothed = kernel.buildImplementation( output_sample, bw )
print 'Sample size = ', size
print 'Kernel bandwidth = ', kernel.getBandwidth()[0]

# We draw the pdf and cdf from kernel smoothing
# Evaluate at best the range of the graph
mean_sample = output_sample.computeMean()[0]
standardDeviation_sample = sqrt( output_sample.computeCovariance()[0, 0] )
xmin = mean_sample - 4 * standardDeviation_sample
xmax = mean_sample + 4 * standardDeviation_sample

# Draw the PDF
smoothedPDF = smoothed.drawPDF( xmin, xmax, 251 )
# Change the title
smoothedPDF.setTitle( 'Kernel smoothing of the deviation - PDF' )
# Change the legend
smoothedPDF_draw = smoothedPDF.getDrawable( 0 )
title = 'PDF from Normal kernel (' + str( size ) + ' data)'
smoothedPDF_draw.setLegendName( title )
smoothedPDF.setDrawable( smoothedPDF_draw, 0 )
smoothedPDF.draw( 'cantilever_beam/smoothedPDF', 640, 480 )

# Draw the CDF
smoothedCDF = smoothed.drawCDF( xmin, xmax, 251 )
# Change the title
smoothedCDF.setTitle( 'Kernel smoothing of the deviation - CDF' )
# Change the legend
smoothedCDF_draw = smoothedCDF.getDrawable( 0 )
title = 'CDF from Normal kernel (' + str( size ) + ' data)'
smoothedCDF_draw.setLegendName( title )
smoothedCDF.setDrawable( smoothedCDF_draw, 0 )
# Change the legend position
smoothedCDF.setLegendPosition( 'bottomright' )
smoothedCDF.draw( 'cantilever_beam/smoothedCDF', 640, 480 )

# In order to see the graph without creating the associated files
#Show(smoothedPDF)
#Show(smoothedCDF)

# Mean of the output variable of interest
print 'Mean from kernel smoothing = ', smoothed.getMean()[0]
print ''

# Superposition of the kernel smoothing pdf and the gaussian one
# which mean and standard deviation are those of the output_sample
normalDist = NormalFactory().buildImplementation( output_sample )
normalDistPDF = normalDist.drawPDF( xmin, xmax, 251 )
normalDistPDFDrawable = normalDistPDF.getDrawable( 0 )
normalDistPDFDrawable.setColor( 'blue' )
smoothedPDF.addDrawable( normalDistPDFDrawable )
smoothedPDF.draw( 'cantilever_beam/smoothedPDF_and_NormalPDF', 640, 480 )

# In order to see the graph without creating the associated files
#Show(smoothedPDF)


#===============================================================================
# Probabilistic Study: treshold exceedance: deviation > 30 cm
#===============================================================================

print ''
print '###########################################################'
print 'Probabilistic Study: treshold exceedance: deviation > 30 cm'
print '###########################################################'
print ''


######
# FORM
######

print '####'
print 'FORM'
print '####'

# We create an Event from this RandomVector
# treshold has been defined in the kernel smoothing section
treshold = 30
myEvent = Event( outputVariableOfInterest, ComparisonOperator( Greater() ),
                 treshold )
myEvent.setName( 'Deviation > 30 cm' )

# We create a NearestPoint algorithm
myCobyla = Cobyla()
myCobyla.setMaximumIterationsNumber( 1000 )
myCobyla.setMaximumAbsoluteError( 1.0e-10 )
myCobyla.setMaximumRelativeError( 1.0e-10 )
myCobyla.setMaximumResidualError( 1.0e-10 )
myCobyla.setMaximumConstraintError( 1.0e-10 )

# We create a FORM algorithm
# The first parameter is a NearestPointAlgorithm
# The second parameter is an event
# The third parameter is a starting point for the design point research
meanVector = inputRandomVector.getMean()
myAlgoFORM = FORM( NearestPointAlgorithm( myCobyla ), myEvent, meanVector )

# Get the number of times the limit state function has been evaluated so far
deviationCallNumberBeforeFORM = deviation.getEvaluationCallsNumber()

# Perform the simulation
myAlgoFORM.run()

# Get the number of times the limit state function has been evaluated so far
deviationCallNumberAfterFORM = deviation.getEvaluationCallsNumber()

# Stream out the results
resultFORM = myAlgoFORM.getResult()
print 'FORM event probability = ', resultFORM.getEventProbability()
print 'Number of evaluations of the limit state function = ', \
        deviationCallNumberAfterFORM - deviationCallNumberBeforeFORM

print 'Generalized reliability index = ', resultFORM.getGeneralisedReliabilityIndex()
print 'Standard space design point = '
for i in range( inputRandomVector.getDimension() ):
    print inputDistribution.getDescription()[i], ' = ', resultFORM.getStandardSpaceDesignPoint()[i]

print 'Physical space design point = '
for i in range( inputRandomVector.getDimension() ):
    print inputDistribution.getDescription()[i], ' = ', resultFORM.getPhysicalSpaceDesignPoint()[i]

print 'Importance factors = '
for i in range( inputRandomVector.getDimension() ):
    print inputDistribution.getDescription()[i], ' = ', resultFORM.getImportanceFactors()[i]

print 'Hasofer reliability index = ', resultFORM.getHasoferReliabilityIndex()
# resultFORM.getGeneralisedReliabilityIndex()
print ''

# Graph 1 : Importance Factors graph
importanceFactorsGraph = resultFORM.drawImportanceFactors()
title = 'FORM Importance factors - ' + myEvent.getName()
importanceFactorsGraph.setTitle( title )
importanceFactorsGraph.draw( 'cantilever_beam/ImportanceFactorsDrawingFORM', 640, 480 )

# In order to see the graph without creating the associated files
#Show(importanceFactorsGraph)


######
# MC
######

print '#############'
print 'Monte Carlo'
print '#############'
print ''


maximumOuterSampling = 40000
blockSize = 100
coefficientOfVariation = .1

# We create a Monte Carlo algorithm
myAlgoMonteCarlo = MonteCarlo( myEvent )
myAlgoMonteCarlo.setMaximumOuterSampling( maximumOuterSampling )
myAlgoMonteCarlo.setBlockSize( blockSize )
myAlgoMonteCarlo.setMaximumCoefficientOfVariation( coefficientOfVariation )

# Define the HistoryStrategy to store the numerical samples generated
# both for the input random vector and the output random vector
# Full strategy
myAlgoMonteCarlo.setInputOutputStrategy( HistoryStrategy( Full() ) )

# Define the HistoryStrategy to store the values of the probability estimator
# and the variance estimator
# used to draw the convergence graph
# Full strategy
myAlgoMonteCarlo.setConvergenceStrategy( HistoryStrategy( Full() ) )

# Perform the simulation
myAlgoMonteCarlo.run()

# Display number of iterations and number of evaluations
# of the limit state function
print 'Number of evaluations of the limit state function = ', \
    myAlgoMonteCarlo.getResult().getOuterSampling()*myAlgoMonteCarlo.getResult().getBlockSize()

# Display the Monte Carlo probability of 'myEvent'
print 'Monte Carlo probability estimation = ', myAlgoMonteCarlo.getResult().getProbabilityEstimate()

# Display the variance of the Monte Carlo probability estimator
print 'Variance of the Monte Carlo probability estimator = ', \
        myAlgoMonteCarlo.getResult().getVarianceEstimate()

# Display the confidence interval length centered around
# the MonteCarlo probability MCProb
# IC = [MCProb - 0.5 * length, MCProb + 0.5 * length ]
# level 0.95
print '0.95 Confidence Interval = [', myAlgoMonteCarlo.getResult().\
        getProbabilityEstimate() - 0.5 * myAlgoMonteCarlo.getResult().\
        getConfidenceLength( 0.95 ), ', ', myAlgoMonteCarlo.getResult().\
        getProbabilityEstimate() + 0.5 * myAlgoMonteCarlo.getResult().\
        getConfidenceLength( 0.95 ), ']'

# Draw the convergence graph and the confidence intervalle of level alpha
alpha = 0.9
convergenceGraphMonteCarlo = myAlgoMonteCarlo.drawProbabilityConvergence( alpha )
# In order to see the graph without creating the associated files
#Show(convergenceGraphMonteCarlo)

# Create the file .EPS
convergenceGraphMonteCarlo.draw( 'cantilever_beam/convergenceGraphMonteCarlo', 640, 480 )
#Show(convergenceGraphMonteCarlo)



#===============================================================================
# Directional Sampling
#===============================================================================

print '######################'
print 'Directional Sampling'
print '######################'
print ''

# Directional sampling from an event (slow and safe strategy by default)

# We create a Directional Sampling algorithm
myAlgoDirectionalSim = DirectionalSampling( myEvent )
myAlgoDirectionalSim.setMaximumOuterSampling( maximumOuterSampling * blockSize )
myAlgoDirectionalSim.setBlockSize( 1 )
myAlgoDirectionalSim.setMaximumCoefficientOfVariation( coefficientOfVariation )

# Define the HistoryStrategy to store the numerical samples generated
# both for the input random vector and the output random vector
# Full strategy
myAlgoDirectionalSim.setInputOutputStrategy( HistoryStrategy( Full() ) )

# Define the HistoryStrategy to store the values of the probability estimator
# and the variance estimator
# used to draw the convergence graph
# Full strategy
myAlgoDirectionalSim.setConvergenceStrategy( HistoryStrategy( Full() ) )

# Save the number of calls of the limit state function, 
# its gradient and hessian already done
deviationCallNumberBefore = deviation.getEvaluationCallsNumber()
deviationGradientCallNumberBefore = deviation.getGradientCallsNumber()
deviationHessianCallNumberBefore = deviation.getHessianCallsNumber()

# Perform the simulation
myAlgoDirectionalSim.run()

# Save the number of calls of the limit state function, 
# its gradient and hessian already done
deviationCallNumberAfter = deviation.getEvaluationCallsNumber()
deviationGradientCallNumberAfter = deviation.getGradientCallsNumber()
deviationHessianCallNumberAfter = deviation.getHessianCallsNumber()

# Display number of iterations and number of evaluations
# of the limit state function
print 'Number of evaluations of the limit state function = ', \
    deviationCallNumberAfter - deviationCallNumberBefore

# Display the Directional Simulation probability of 'myEvent'
print 'Directional Sampling probability estimation = ', \
    myAlgoDirectionalSim.getResult().getProbabilityEstimate()

# Display the variance of the Directional Simulation probability estimator
print 'Variance of the Directional Sampling probability estimator = ', \
    myAlgoDirectionalSim.getResult().getVarianceEstimate()

# Display the confidence interval length centered around
# the MonteCarlo probability MCProb
# IC = [MCProb - 0.5 * length, MCProb + 0.5 * length ]
# level 0.95
print '0.95 Confidence Interval = [', myAlgoDirectionalSim.getResult().\
        getProbabilityEstimate() - 0.5 * myAlgoDirectionalSim.getResult().\
        getConfidenceLength( 0.95 ), ', ', myAlgoDirectionalSim.getResult().\
        getProbabilityEstimate() + 0.5 * myAlgoDirectionalSim.getResult().\
        getConfidenceLength( 0.95 ), ']'

# Draw the convergence graph and the confidence intervalle of level alpha
alpha = 0.9
convergenceGraphDS = myAlgoDirectionalSim.drawProbabilityConvergence( alpha )
# In order to see the graph without creating the associated files
#Show(convergenceGraphDS)

# Create the file .EPS
convergenceGraphDS.draw( 'cantilever_beam/convergenceDS', 640, 480 )
#Show(convergenceGraphDS)



#===============================================================================
# Latin Hypercube Sampling
#===============================================================================

print '##########################'
print 'Latin Hypercube Sampling'
print '##########################'
print ''

# We create a LHS algorithm
myAlgoLHS = LHS( myEvent )
myAlgoLHS.setMaximumOuterSampling( maximumOuterSampling )
myAlgoLHS.setBlockSize( blockSize )
myAlgoLHS.setMaximumCoefficientOfVariation( coefficientOfVariation )

# Define the HistoryStrategy to store the numerical samples generated
# both for the input random vector and the output random vector
# Full strategy
myAlgoLHS.setInputOutputStrategy( HistoryStrategy( Full() ) )

# Define the HistoryStrategy to store the values of the probability estimator
# and the variance estimator
# used to draw the convergence graph
# Full strategy
myAlgoLHS.setConvergenceStrategy( HistoryStrategy( Full() ) )

# Perform the simulation
myAlgoLHS.run()

# Display number of iterations and number of evaluations
# of the limit state function
print 'Number of evaluations of the limit state function = ', \
    myAlgoLHS.getResult().getOuterSampling()*myAlgoLHS.getResult().getBlockSize()

# Display the Directional Simulation probability of 'myEvent'
print 'Directional Sampling probability estimation = ', \
    myAlgoLHS.getResult().getProbabilityEstimate()

# Display the variance of the Directional Simulation probability estimator
print 'Variance of the Directional Sampling probability estimator = ', \
    myAlgoLHS.getResult().getVarianceEstimate()

# Display the confidence interval length centered around
# the MonteCarlo probability MCProb
# IC = [MCProb - 0.5 * length, MCProb + 0.5 * length ]
# level 0.95
print '0.95 Confidence Interval = [', myAlgoLHS.getResult().\
        getProbabilityEstimate() - 0.5 * myAlgoLHS.getResult().\
        getConfidenceLength( 0.95 ), ', ', myAlgoLHS.getResult().\
        getProbabilityEstimate() + 0.5 * myAlgoLHS.getResult().\
        getConfidenceLength( 0.95 ), ']'

# Draw the convergence graph and the confidence intervalle of level alpha
alpha = 0.9
convergenceGraphLHS = myAlgoLHS.drawProbabilityConvergence( alpha )
# In order to see the graph without creating the associated files
#Show(convergenceGraphLHS)

# Create the file .EPS
convergenceGraphLHS.draw( 'cantilever_beam/convergenceLHS', 640, 480 )
#Show(convergenceGraphLHS)


#===============================================================================
# Importance Sampling
#===============================================================================

print '##########################'
print 'Importance Sampling'
print '##########################'
print ''

maximumOuterSampling = 40000
blockSize = 1
standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
mean = standardSpaceDesignPoint
sigma = NumericalPoint( 4, 1.0 )
importanceDistribution = Normal( mean, sigma, CorrelationMatrix( 4 ) )

myStandardEvent = StandardEvent( myEvent )

myAlgoImportanceSampling = ImportanceSampling( myStandardEvent,
                                                Distribution( importanceDistribution ) )
myAlgoImportanceSampling.setMaximumOuterSampling( maximumOuterSampling )
myAlgoImportanceSampling.setBlockSize( blockSize )
myAlgoImportanceSampling.setMaximumCoefficientOfVariation( coefficientOfVariation )

# Define the HistoryStrategy to store the numerical samples generated
# both for the input random vector and the output random vector
# Full strategy
myAlgoImportanceSampling.setInputOutputStrategy( HistoryStrategy( Full() ) )

# Define the HistoryStrategy to store the values of the probability estimator
# and the variance estimator
# used to draw the convergence graph
# Full strategy
myAlgoImportanceSampling.setConvergenceStrategy( HistoryStrategy( Full() ) )

# Perform the simulation
myAlgoImportanceSampling.run()

# Display number of iterations and number of evaluations
# of the limit state function
print 'Number of evaluations of the limit state function = ', \
    myAlgoImportanceSampling.getResult().getOuterSampling()*myAlgoImportanceSampling.getResult().getBlockSize()

# Display the Directional Simulation probability of 'myEvent'
print 'Directional Sampling probability estimation = ', \
    myAlgoImportanceSampling.getResult().getProbabilityEstimate()

# Display the variance of the Directional Simulation probability estimator
print 'Variance of the Directional Sampling probability estimator = ', \
    myAlgoImportanceSampling.getResult().getVarianceEstimate()

# Display the confidence interval length centered around
# the MonteCarlo probability MCProb
# IC = [MCProb - 0.5 * length, MCProb + 0.5 * length ]
# level 0.95
print '0.95 Confidence Interval = [', myAlgoImportanceSampling.getResult().\
        getProbabilityEstimate() - 0.5 * myAlgoImportanceSampling.getResult().\
        getConfidenceLength( 0.95 ), ', ', myAlgoImportanceSampling.getResult().\
        getProbabilityEstimate() + 0.5 * myAlgoImportanceSampling.getResult().\
        getConfidenceLength( 0.95 ), ']'

# Draw the convergence graph and the confidence intervalle of level alpha
alpha = 0.9
convergenceGraphIS = myAlgoImportanceSampling.drawProbabilityConvergence( alpha )
# In order to see the graph without creating the associated files
#Show(convergenceGraphIS)

# Create the file .EPS
convergenceGraphIS.draw( 'cantilever_beam/convergenceIS', 640, 480 )
#Show(convergenceGraphIS)



#===============================================================================
# Response surface : Polynomial expansion chaos
#===============================================================================

print '##########################'
print 'Polynomial expansion chaos'
print '##########################'
print ''

#############################################################
# STEP 1 : Construction of the multivariate orthonormal basis

# Dimension of the input random vector
dim = 4

# Create the univariate polynomial family collection
# which regroups the polynomial families for each direction
polyColl = PolynomialFamilyCollection( dim )

# Variable E
# Jacobi(alpha, beta) <=> Beta(\beta + 1, \alpha + \beta + 2, -1, 1)
alphaJ = 1.27
betaJ = -0.07
jacobiFamily = JacobiFactory( alphaJ, betaJ )
polyColl[0] = OrthogonalUniVariatePolynomialFamily( jacobiFamily )


# Variable F
# Laguerre(k) <=> Gamma( k+1, 1, 0) (parametrage ppal)
kLaguerre = 1.78
laguerreFamily = LaguerreFactory( kLaguerre )
polyColl[1] = OrthogonalUniVariatePolynomialFamily( laguerreFamily )

# Variable L
# Legendre <=> Unif(-1,1)
legendreFamily = LegendreFactory()
polyColl[2] = OrthogonalUniVariatePolynomialFamily( legendreFamily )


# Variable I
# Jacobi(alpha, beta) <=> Beta(\beta + 1, \alpha + \beta + 2, -1, 1)
alphaJ2 = 0.5
betaJ2 = 1.5
jacobiFamily2 = JacobiFactory( alphaJ2, betaJ2 )
polyColl[3] = OrthogonalUniVariatePolynomialFamily( jacobiFamily2 )


# Create the multivariate orthonormal basis
# which is the cartesian product of the univariate basis
multivariateBasis = OrthogonalProductPolynomialFactory( polyColl, EnumerateFunction( dim ) )

# Build a term of the basis as a NumericalMathFunction
# Generally, we do not need to construct manually any term,
# all terms are constructed automatically by a strategy of construction of the basis
i = 5
Psi_i = multivariateBasis.build( i )

# Get the measure mu associted to the multivariate basis
distributionMu = multivariateBasis.getMeasure()


###################################################################
# STEP 2 : Truncated strategy of the multivariate orthonormal basis

# CleaningStrategy:
# among the maximumCinsideredTerms = 500 first polynoms,
# those which have the mostSignificant = 50 most significant contributions
# with significance criterion significanceFactor = 10^(-4)
# The True boolean indicates if we are interested
# in the online monitoring of the current basis update
# (removed or added coefficients)
maximumConsideredTerms = 500
mostSignificant = 50
significanceFactor = 1.0e-4
truncatedBasisStrategy = CleaningStrategy( OrthogonalBasis( multivariateBasis ),
                                           maximumConsideredTerms, mostSignificant,
                                           significanceFactor, True )
truncatureBasisStrategy = FixedStrategy( OrthogonalBasis( multivariateBasis ), 481 )

###############################################################
# STEP 3 : Evaluation strategy of the aproximation coefficients

# The technique proposed is the Least Squares technique
# where the points come from an experiment plane
# Here: the Monte Carlo sampling technoque
sampleSize = 10000
evaluationCoeffStrategy = LeastSquaresStrategy( MonteCarloExperiment( sampleSize ) )

#####################################################
# STEP 4 : Creation of the Functional Chaos Algorithm

# FunctionalChaosAlgorithm:
# combination of the model : limitStateFunction
# the distribution of the input random vector: Xdistribution
# the trucature strategy of the multivariate basis
# and the evaluation strategy of the coefficients
polynomialChaosAlgorithm = FunctionalChaosAlgorithm( deviation, Distribution( inputDistribution ),
                                                    AdaptiveStrategy( truncatureBasisStrategy ),
                                                    ProjectionStrategy( evaluationCoeffStrategy ) )

#####################################################
# Run and results exploitation

# Perform the simulation
polynomialChaosAlgorithm.run()

# Stream out the results
polynomialChaosResult = polynomialChaosAlgorithm.getResult()

# Get the polynomial chaos coefficients
coefficients = polynomialChaosResult.getCoefficients()

# Get the meta model as a NumericalMathFunction
metaModel = polynomialChaosResult.getMetaModel()

# Get the indices of the selected polynomials : K
subsetK = polynomialChaosResult.getIndices()

# Get the composition of the polynomials
# of the truncated multivariate basis
for i in range( subsetK.getSize() ):
    print 'Polynomial number ', i, ' in truncated basis <-> polynomial number ', \
        subsetK[i], ' = ', EnumerateFunction( dim )( subsetK[i] ), ' in complete basis'
print ''

# Get multivariate basis
# as a collection of NumericalMathFunction
multivariateBasisCollection = polynomialChaosResult.getReducedBasis()

# Get the distribution of variables Z
mu = polynomialChaosResult.getDistribution()
print 'Distribution in the transformed variables = ', mu
print ''

# Get the composed model which is the model of the reduced variables Z
composedModel = polynomialChaosResult.getComposedModel()

# Define the new random vector
newOutputVariableOfInterest = RandomVector( polynomialChaosResult )

# Get the mean and variance of the meta model
print 'Mean = ', newOutputVariableOfInterest.getMean()
print 'Standard deviation = ', sqrt( newOutputVariableOfInterest.getCovariance()[0, 0] )
print ''


#####################################################
# Graphs validation

# Graph 1 : cloud
#================

# Generate a NumericalSample of the input random vector
# Evaluate the meta model and the real model
# draw the clouds (metamodel, real model)
# Verify points are on the first diagonal
sizeX = 500
Xsample = inputDistribution.getNumericalSample( sizeX )

modelSample = deviation( Xsample )
metaModelSample = metaModel( Xsample )

sampleMixed = NumericalSample( sizeX, 2 )
for i in range( sizeX ):
    sampleMixed[i][0] = modelSample[i][0]
    sampleMixed[i][1] = metaModelSample[i][0]

legend = str( sizeX ) + ' realisations'
comparisonCloud = Cloud( sampleMixed, 'blue', 'fsquare', legend )
graphCloud = Graph( 'Polynomial chaos expansion', 'model', 'meta model', True, 'topleft' )
graphCloud.addDrawable( comparisonCloud )

#Show(graphCloud)
graphCloud.draw( 'cantilever_beam/PCE_comparisonModels' )


# Graph 2 : polynoms family graphs
#=================================

degreeMax = 5
pointNumber = 101
colorList = Drawable.GetValidColors()

# Jacobi for E
xMinJacobi = -1
xMaxJacobi = 1
titleJacobi = 'Jacobi(' + str( alphaJ ) + ', ' + str( betaJ ) + ') polynomials'
graphJacobi = Graph( titleJacobi, 'z', 'polynomial values', True, 'topleft' )
for i in range( degreeMax ):
    graphJacobi_temp = jacobiFamily.build( i ).draw( xMinJacobi, xMaxJacobi, pointNumber )
    graphJacobi_temp_draw = graphJacobi_temp.getDrawable( 0 )
    legend = 'degree ' + str( i )
    graphJacobi_temp_draw.setLegendName( legend )
    graphJacobi_temp_draw.setColor( colorList[i] )
    graphJacobi.addDrawable( graphJacobi_temp_draw )

#Show(graphJacobi)
graphJacobi.draw( 'cantilever_beam/PCE_JacobiPolynomials_VariableE' )


# Laguerre for F
xMinLaguerre = 0
xMaxLaguerre = 10
titleLaguerre = 'Laguerre(' + str( kLaguerre ) + ') polynomials'
graphLaguerre = Graph( titleLaguerre, 'z', 'polynomial values', True, 'topleft' )
for i in range( degreeMax ) :
    graphLaguerre_temp = laguerreFamily.build( i ).draw( xMinLaguerre, xMaxLaguerre, pointNumber )
    graphLaguerre_temp_draw = graphLaguerre_temp . getDrawable ( 0 )
    legend = 'degree ' + str( i )
    graphLaguerre_temp_draw.setLegendName ( legend )
    graphLaguerre_temp_draw.setColor( colorList[ i ] )
    graphLaguerre.addDrawable ( graphLaguerre_temp_draw )

#Show(graphLaguerre)
graphLaguerre.draw( 'cantilever_beam/PCE_LaguerrePolynomials_VariableF' )


# Legendre for L
xMinLegendre = -1
xMaxLegendre = 1
titleLegendre = 'Legendre polynomials'
graphLegendre = Graph( titleLegendre, 'z', 'polynomial values', True, 'topright' )
for i in range( degreeMax ):
    graphLegendre_temp = legendreFamily.build( i ).draw( xMinLegendre, xMaxLegendre, pointNumber )
    graphLegendre_temp_draw = graphLegendre_temp.getDrawable( 0 )
    legend = 'degree ' + str( i )
    graphLegendre_temp_draw.setLegendName( legend )
    graphLegendre_temp_draw.setColor( colorList[i] )
    graphLegendre.addDrawable( graphLegendre_temp_draw )

#Show(graphLegendre)
graphLegendre.draw( 'cantilever_beam/PCE_LegendrePolynomials_VariableL' )


# Jacobi for I
xMinJacobi2 = -1
xMaxJacobi2 = 1
titleJacobi2 = 'Jacobi(' + str( alphaJ2 ) + ', ' + str( betaJ2 ) + ') polynomials'
graphJacobi2 = Graph( titleJacobi2, 'z', 'polynomial values', True, 'topright' )
for i in range( degreeMax ):
    graphJacobi2_temp = jacobiFamily2.build( i ).draw( xMinJacobi2, xMaxJacobi2, pointNumber )
    graphJacobi2_temp_draw = graphJacobi2_temp.getDrawable( 0 )
    legend = 'degree ' + str( i )
    graphJacobi2_temp_draw.setLegendName( legend )
    graphJacobi2_temp_draw.setColor( colorList[i] )
    graphJacobi2.addDrawable( graphJacobi2_temp_draw )

#Show(graphJacobi2)
graphJacobi2.draw( 'cantilever_beam/PCE_JacobiPolynomials_VariableI' )






