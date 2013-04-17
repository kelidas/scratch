#! /usr/bin/python
#    Version info: $Id: FitStatistics.py 230 2010-06-30 20:20:14Z zunzun.com $

# the pythonequations base is located up one directory from the top-level examples
# directory, go up one directory in the path from there for the import to work properly
import sys, os;
if os.path.join(sys.path[0][:sys.path[0].rfind(os.sep)], '../..') not in sys.path:
    sys.path.append(os.path.join(sys.path[0][:sys.path[0].rfind(os.sep)], '../..'))
import pythonequations


equation = pythonequations.Equations3D.Polynomial.Linear3D() # Simple surface

equation.fittingTarget = 'SSQABS' # see the Equation base class for a list of fitting targets
equation.ConvertTextToData(equation.exampleData) # Equations have ASCII text data for testing and examples

equation.Initialize() # now that the equation has data, set up the cache

# If performing a nonlinear fit and you have parameter estimates, set them
# instead of calling this method.  This call is harmless for linear fits
equation.SetGAParametersAndGuessInitialCoefficientsIfNeeded() # estimate initial parameters if needed

equation.FitToCacheData() # perform the fit

equation.CalculateErrors() # so we can calculate parameter statistics
equation.CalculateParameterStatistics() # so we can print the parameter statistics

print equation.name, str(equation.dimensionality) + "D"
print equation.fittingTarget + ":", equation.CalculateFittingTarget(equation.coefficientArray)

print 'Degress of freedom error',  equation.df_e
print 'Degress of freedom regression',  equation.df_r

if equation.rmse == None:
    print 'Root Mean Squared Error (RMSE): n/a'
else:
    print 'Root Mean Squared Error (RMSE):',  equation.rmse

if equation.r2 == None:
    print 'R-squared: n/a'
else:
    print 'R-squared:',  equation.r2

if equation.r2adj == None:
    print 'R-squared adjusted: n/a'
else:
    print 'R-squared adjusted:',  equation.r2adj

if equation.Fstat == None:
    print 'Model F-statistic: n/a'
else:
    print 'Model F-statistic:',  equation.Fstat

if equation.Fpv == None:
    print 'Model F-statistic p-value: n/a'
else:
    print 'Model F-statistic p-value:',  equation.Fpv

if equation.ll == None:
    print 'Model log-likelihood: n/a'
else:
    print 'Model log-likelihood:',  equation.ll

if equation.aic == None:
    print 'Model AIC: n/a'
else:
    print 'Model AIC:',  equation.aic

if equation.bic == None:
    print 'Model BIC: n/a'
else:
    print 'Model BIC:',  equation.bic


print
for i in range(len(equation.coefficientArray)):
    if equation.tstat_beta == None:
        tstat = 'n/a'
    else:
        tstat = '%-.5E' %  ( equation.tstat_beta[i])

    if equation.pstat_beta == None:
        pstat = 'n/a'
    else:
        pstat = '%-.5E' %  ( equation.pstat_beta[i])

    print "Coefficient %s = %-.16E, std error: %-.5E, t-stat: %s, p-stat: %s" % (equation.coefficientDesignatorTuple[i], equation.coefficientArray[i],  equation.sd_beta[i], tstat,  pstat)


print
print "Coefficient Covariance Matrix"
for i in  equation.cov_beta:
    print i
