#    pythonequations is a collection of equations expressed as Python classes
#    Copyright (C) 2008 James R. Phillips
#    2548 Vera Cruz Drive
#    Birmingham, AL 35235 USA
#    email: zunzun@zunzun.com
#
#    License: BSD-style (see LICENSE.txt in main source directory)
#    Version info: $Id: EquationBaseClasses.py 276 2010-10-07 18:57:33Z zunzun.com $

import math, StringIO, string, new, sys, inspect, types, parser
try:
    import scipy.weave as weave
except:
    import weave
import numpy
numpy.seterr( all='raise' ) # numpy raises warnings, convert to exceptions to trap them

import ExtraCodeForEquationBaseClasses


class Equation( object ):

    # lower case "e" is removed so it is not mistaken for Euler's constant "e"
    # lower case "l" is removed so it is not mistaken for the number "1" - some fonts make these appear the same
    # upper case "O" is removed so it is not mistaken for the number "0" - some fonts make these appear the same
    ascii = 'abcdfghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ' # used in polynomials and polyfunctionals
    
    FittingTargetDict = {'SSQABS':['Fitting target is lowest sum of squared (SSQ) absolute error (traditional)', 'sum of squared absolute error'],
                         'ODR':['Fitting target is lowest sum of orthogonal distance (ODR) (robust, slow)', 'sum of orthogonal distance (ODR)'],
                         'SSQREL':['Fitting target is lowest sum of squared (SSQ) relative error (robust, slow)', 'sum of squared relative error'],
                         'ABSABS':['Fitting target is lowest sum of absolute value of absolute error (robust, slow)', 'sum of absolute value of absolute error'],
                         'ABSREL':['Fitting target is lowest sum of absolute value of relative error (robust, slow)', 'sum of absolute value of relative error'],
                         'PEAKABS':['Fitting target is lowest peak absolute value of absolute error (robust, slow)', 'peak absolute value of absolute error'],
                         'PEAKREL':['Fitting target is lowest peak absolute value of relative error (robust, slow)', 'peak absolute value of relative error'],
                         'AIC':['Fitting target is lowest AIC (robust, slow)', 'AIC'],
                         'BIC':['Fitting target is lowest BIC (robust, slow)', 'BIC']
                        }

    ExtendedFormsDict = {'':                              0,
                         'Offset':                        1,
                         'Reciprocal':                    2,
                         'ReciprocalWithOffset':          3,
                         'InverseX':                      4,
                         'InverseXWithOffset':            5,
                         'X_LinearDecay':                 6,
                         'X_LinearDecayAndOffset':        7,
                         'X_ExponentialDecay':            8,
                         'X_ExponentialDecayAndOffset':   9,
                         'X_LinearGrowth':                10,
                         'X_LinearGrowthAndOffset':       11,
                         'X_ExponentialGrowth':           12,
                         'X_ExponentialGrowthAndOffset':  13,
                         'InverseXY':                     14,
                         'InverseXYWithOffset':           15,
                         'XY_LinearDecay':                16,
                         'XY_LinearDecayAndOffset':       17,
                         'XY_ExponentialDecay':           18,
                         'XY_ExponentialDecayAndOffset':  19,
                         'XY_LinearGrowth':               20,
                         'XY_LinearGrowthAndOffset':      21,
                         'XY_ExponentialGrowth':          22,
                         'XY_ExponentialGrowthAndOffset': 23
                         }
                         
    # for weave.inline() C++ compilation, change as needed for your CPU and compiler
    if sys.platform == 'win32': # try to pre-detect MSVC++, MinGW32 or GCC and optimize appropriately.
        if weave.platform_info.msvc_exists():
            compiler_name = 'mingw32'
            compiler_flags_for_weave_inline = ['-O2']
        else:
            compiler_name = 'mingw32'
            compiler_flags_for_weave_inline = ['-O2']
    else:
        compiler_name = 'gcc'
        compiler_flags_for_weave_inline = ['-march=native', '-O2']
        
    nonlinearSolver = 1 # 1 = fmin, 2 = fmin_bfgs, 3 = fmin_cg, 4 = fmin_ncq, 5 = fmin_powell

    splineFlag = False
    userDefinedFunctionFlag = False
    polyfunctionalFlag = False
    polynomialFlag = False
    polyrationalFlag = False
    LinearSSQSolverFlag = False
    
    CannotAcceptDataWithZeroX = False
    CannotAcceptDataWithZeroY = False
    CannotAcceptDataWithPositiveX = False
    CannotAcceptDataWithPositiveY = False
    CannotAcceptDataWithNegativeX = False
    CannotAcceptDataWithNegativeY = False

    coefficientArray = []
    fixedCoefficientArray = []
    weightsArray = []
    Polyrat2DNumeratorFlags = []
    Polyrat2DDenominatorFlags = []
    
    # let the C++ in weave know if the equation needs a bounds check on coefficients
    requiresCoefficientBoundsCheckWhenFitting = False

    # having these empty/zero defaults makes saving equation parameters easier
    # in the function finders, even though most equations do not use them
    Polyfun2DFlags = []
    Polyrat2DNumeratorFlags = []
    Polyrat2DDenominatorFlags = []
    Polyfun3DFlags = []
    xPolynomialOrder = 0
    yPolynomialOrder = 0

    DependentDataContainsZeroFlag = False

    # for decoupling weave cache length from coefficient array length
    CacheGenerationList = []

    # default GA parameters
    fmin_xtol = 1.0E-16
    fmin_ftol = 1.0E-16
    fminIterationLimit = 2500
    fminFunctionLimit = 2500
    guessDivisor = 10.0
    diffScale = 0.7
    crossoverProb = 0.7
    maxparamvalue = 100.0
    minparamvalue = -100.0

    # for use in the user defined functions
    # based on http://lybniz2.sourceforge.net/safeeval.html
    functionDict = {}
    functionDict['Arithmetic Operations'] = ['power', 'mod']
    functionDict['Exponents And Logarithms'] = ['exp', 'log', 'log10', 'log2']
    functionDict['Trigonometric Functions'] = ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'hypot', 'arctan2', 'deg2rad', 'rad2deg']
    functionDict['Hyperbolic Trig Functions'] = ['arcsinh', 'arccosh', 'arctanh', 'sinh', 'cosh', 'tanh']
    functionDict['Other Special Functions'] = ['sinc']
    functionDict['Miscellaneous'] = ['sqrt', 'square', 'fabs', 'sign', 'maximum', 'minimum']

    constantsDict = {}
    constantsDict['Constants'] = ['pi', 'e']
    
    swapXYFlag = 0

    webCitationLink = ''


    def __init__( self, inExtendedName='' ):
                
        # this special, default, case is always OK
        if inExtendedName == '':
            self.extendedName = inExtendedName
            return

        createExtendedForm = False # until proven otherwise below
        
        if self.RequiresAutoGeneratedOffsetForm and inExtendedName == 'Offset':
            createExtendedForm = True
            
        if self.RequiresAutoGeneratedReciprocalForm and inExtendedName == 'Reciprocal':
            createExtendedForm = True
                
        if self.RequiresAutoGeneratedReciprocalForm and self.RequiresAutoGeneratedOffsetForm and inExtendedName == 'ReciprocalWithOffset':
            createExtendedForm = True
            
        if self.dimensionality == 2 and self.RequiresAutoGeneratedInverseForms and inExtendedName == 'InverseX':
            createExtendedForm = True
                
        if self.dimensionality == 2 and self.RequiresAutoGeneratedInverseForms and inExtendedName == 'InverseXWithOffset':
            createExtendedForm = True
                
        if self.dimensionality == 3 and self.RequiresAutoGeneratedInverseForms and inExtendedName == 'InverseXY':
            createExtendedForm = True
                
        if self.dimensionality == 3 and self.RequiresAutoGeneratedInverseForms and inExtendedName == 'InverseXYWithOffset':
            createExtendedForm = True
                
        if self.RequiresAutoGeneratedGrowthAndDecayForms:
            if self.dimensionality == 2 and inExtendedName.startswith( 'X_' ):
                createExtendedForm = True
            if self.dimensionality == 3 and inExtendedName.startswith( 'XY_' ):
                createExtendedForm = True
            
        if createExtendedForm:
            self.extendedName = inExtendedName
        else:
            raise Exception( 'Cannot create ' + inExtendedName + ' version of ' + self._name )


    def Initialize( self ):
        
        if 0 != self.requiresCoefficientBoundsCheckWhenFitting:
            self.upperCoefficientBoundsArray = numpy.ones( len( self.coefficientDesignatorTuple ) ) * 1.0E300
            self.lowerCoefficientBoundsArray = numpy.ones( len( self.coefficientDesignatorTuple ) ) * -1.0E300
        self.CreateCacheGenerationList()
        self.CreateExtendedCacheGenerationListIfNeeded()

        self.additionalDesignatorList = []

        if not self.splineFlag:
            self.numberOfCoefficientsForNonExtendedVersion = len( self.coefficientDesignatorTuple )

        if self.extendedName == '':
            pass
            
        # force nonlinear solver flag if needed
        if self.extendedName not in ['', 'Offset']:
            self.LinearSSQSolverFlag = 0

        if self.extendedName == 'Offset': # special case, one extra coefficient named offset
            clist = list( self.coefficientDesignatorTuple )
            self.additionalDesignatorList.append( 'Offset' )
            clist.append( 'Offset' )
            self.coefficientDesignatorTuple = tuple( clist )
        
        if self.extendedName == 'Reciprocal':
            pass

        if self.extendedName == 'ReciprocalWithOffset':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'InverseX':
            pass

        if self.extendedName == 'InverseXWithOffset':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'X_LinearDecay':
            self.SetAdditionalCoefficients( 1 )
            self.CannotAcceptDataWithZeroX = True

        if self.extendedName == 'X_LinearDecayAndOffset':
            self.SetAdditionalCoefficients( 2 )
            self.CannotAcceptDataWithZeroX = True

        if self.extendedName == 'X_ExponentialDecay':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'X_ExponentialDecayAndOffset':
            self.SetAdditionalCoefficients( 2 )

        if self.extendedName == 'X_LinearGrowth':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'X_LinearGrowthAndOffset':
            self.SetAdditionalCoefficients( 2 )

        if self.extendedName == 'X_ExponentialGrowth':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'X_ExponentialGrowthAndOffset':
            self.SetAdditionalCoefficients( 2 )

        if self.extendedName == 'InverseXY':
            pass

        if self.extendedName == 'InverseXYWithOffset':
            self.SetAdditionalCoefficients( 1 )
            
        if self.extendedName == 'XY_LinearDecay':
            self.SetAdditionalCoefficients( 1 )
            self.CannotAcceptDataWithZeroX = True
            self.CannotAcceptDataWithZeroY = True

        if self.extendedName == 'XY_LinearDecayAndOffset':
            self.SetAdditionalCoefficients( 2 )
            self.CannotAcceptDataWithZeroX = True
            self.CannotAcceptDataWithZeroY = True

        if self.extendedName == 'XY_ExponentialDecay':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'XY_ExponentialDecayAndOffset':
            self.SetAdditionalCoefficients( 2 )

        if self.extendedName == 'XY_LinearGrowth':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'XY_LinearGrowthAndOffset':
            self.SetAdditionalCoefficients( 2 )

        if self.extendedName == 'XY_ExponentialGrowth':
            self.SetAdditionalCoefficients( 1 )

        if self.extendedName == 'XY_ExponentialGrowthAndOffset':
            self.SetAdditionalCoefficients( 2 )


    # for use in the user defined functions
    def GetTokensFromTuple( self, tup, list=None ):
        if list is None:
            list = []
        if type( tup ) is types.TupleType:
            tupleLength = len( tup )
            if tupleLength > 1 and type( tup[0] ) is not types.TupleType:
                if tup[0] == 1:
                    list.append( tup[1] )
            if tupleLength == 2: # so a caret character can be trapped later
                if tup[0] == 33:
                    if tup[1] == '^':
                        list.append( '^' )
            for i in tup:
                list = self.GetTokensFromTuple( i, list )
        return list

    
    # for use in the user defined functions    
    def ParseVerifyCreateSafeDictAndCompileUserFunctionString( self ):
        
        # shift user functions into numpy namespace at run time, not import time
        numpySafeTokenList = []
        for key in self.functionDict.keys():
            numpySafeTokenList += self.functionDict[key]
        for key in self.constantsDict.keys():
            numpySafeTokenList += self.constantsDict[key]
            
        # to shift user functions such as "power" into the numpy namespace "numpy.power" for evaluation
        for token in numpySafeTokenList:
            exec( token + ' = numpy.' + token )
        
        # no blank lines of text, StringIO.StringIO() allows using file methods on text
        stringToConvert = ''
        rawData = StringIO.StringIO( self.userDefinedFunctionText ).readlines()
        for line in rawData:
            stripped = line.strip()
            if len( stripped ) > 0: # no empty strings
                if stripped[0] != '#': # no comment-only lines
                    stringToConvert += stripped + '\n'

        if stringToConvert == '':
            raise Exception( 'You must enter some function text for the software to use.' )

        if - 1 != stringToConvert.find( '=' ):
            raise Exception( 'Please do not use an equals sign "=" in your text.' )

        st = parser.expr( stringToConvert )
        tup = st.totuple()
        tokens = self.GetTokensFromTuple( tup ) # inherited method

        if '^' in tokens:
            raise Exception( 'The caret symbol "^" is not recognized by the parser, please substitute double asterisks "**" for "^".' )
            
        if 'ln' in tokens:
            raise Exception( "The parser uses log() for the natural log function, not ln(). Please use log() in your text." )

        if 'abs' in tokens:
            raise Exception( "The parser uses fabs() for the absolute value, not abs(). Please use fabs() in your text." )

        if 'EXP' in tokens:
            raise Exception( "The parser uses lower case exp(), not upper case EXP(). Please use lower case exp() in your text." )

        if 'LOG' in tokens:
            raise Exception( "The parser uses lower case log(), not upper case LOG(). Please use lower case log() in your text." )

        # test for required reserved tokens
        tokenNames = list( set( tokens ) - set( numpySafeTokenList ) )
        if 'X' not in tokenNames:
            raise Exception( 'You must use a separate upper case "X" in your function to enter a valid function of X.' )
        if self.dimensionality == 3:
            if 'Y' not in tokenNames:
                raise Exception( 'You must use a separate upper case "Y" in your function to enter a valid function of Y.' )

        if self.dimensionality == 2:
            self.coefficientDesignatorTuple = sorted( list( set( tokenNames ) - set( ['X'] ) ) )
        else:
            self.coefficientDesignatorTuple = sorted( list( set( tokenNames ) - set( ['X', 'Y'] ) ) )
                
        if len( self.coefficientDesignatorTuple ) == 0:
            raise Exception( 'I could not find any equation parameter or coefficient names, please check the function text' )

        # now compile code object using safe tokens
        self.safe_dict = dict( [ ( k, locals().get( k, None ) ) for k in numpySafeTokenList ] )
            
        # later evals re-use this compiled code for improved performance in EvaluateCachedData() methods
        self.userFunctionCodeObject = compile( stringToConvert, '<string>', 'eval' )


    def ShouldDataBeRejectedByThisEquation( self ):
        if self.IndependentData1ContainsZeroFlag and self.CannotAcceptDataWithZeroX:
            return 'The data contains at least one X value of zero, but this equation cannot use zero values of X.'
        if self.IndependentData2ContainsZeroFlag and self.CannotAcceptDataWithZeroY:
            return 'The data contains at least one Y value of zero, but this equation cannot use zero values of Y.'
        if self.IndependentData1ContainsPositiveFlag and self.CannotAcceptDataWithPositiveX:
            return 'The data contains at least one positive X value, but this equation cannot use positive values of X.'
        if self.IndependentData2ContainsPositiveFlag and self.CannotAcceptDataWithPositiveY:
            return 'The data contains at least one positive Y value, but this equation cannot use positive values of Y.'
        if self.IndependentData1ContainsNegativeFlag and self.CannotAcceptDataWithNegativeX:
            return 'The data contains at least one negative X value, but this equation cannot use negative values of X.'
        if self.IndependentData2ContainsNegativeFlag and self.CannotAcceptDataWithNegativeY:
            return 'The data contains at least one negative Y value, but this equation cannot use negative values of Y.'
        return 0


    def ConvertTextToData( self, dataText, useWeights=0 ):

        # you should first process commas before calling this method,
        # as it uses the default token delimiters in string.split()
        #
        # For example, convert $1,234.56 to 1234.56 or 1,23 to 1.23
        # Different number systems have commas in different places
        # and the Python built-in float() method uses decimal notation
        # or scientific notation only

        # cache some data set characteristics for later use,
        # these are for the data domains of individual equations
        self.IndependentData1ContainsZeroFlag = False
        self.IndependentData2ContainsZeroFlag = False
        self.IndependentData1ContainsPositiveFlag = False
        self.IndependentData2ContainsPositiveFlag = False
        self.IndependentData1ContainsNegativeFlag = False
        self.IndependentData2ContainsNegativeFlag = False

        # used in calculation of relative error to prevent divide-by-zero exceptions
        self.DependentDataContainsZeroFlag = False

        # StringIO.StringIO() allows using file methods on text
        rawData = StringIO.StringIO( dataText ).readlines()

        if useWeights:
            minimumNumberOfTokens = self.dimensionality + 1
        else:
            minimumNumberOfTokens = self.dimensionality

        # OK, now load in the data
        dataLists = [[], [], []]
        weightsList = []
        for line in rawData:

            # split the line into string tokens using the default string.split() delimiters
            tokenlist = string.split( line )

            # test this line for minimum required number of string tokens
            if len( tokenlist ) < minimumNumberOfTokens:
                continue

            # use the python built-in float() conversion and discard if any exceptions
            if self.dimensionality == 1:
                try:
                    a = float( tokenlist[0] )
                except:
                    continue
                if a > 1.0E300 or a < -1.0E300:
                    continue
                if a < 0.0:
                    self.IndependentData1ContainsNegativeFlag = True
                elif a > 0.0:
                    self.IndependentData1ContainsPositiveFlag = True
                else:
                    self.IndependentData1ContainsZeroFlag = True

                dataLists[0].append( a )

            if self.dimensionality == 2:
                try:
                    a = float( tokenlist[0] )
                    b = float( tokenlist[1] )
                    if useWeights:
                        c = float( tokenlist[2] )
                except:
                    continue
                if a > 1.0E300 or a < -1.0E300:
                    continue
                if b > 1.0E300 or b < -1.0E300:
                    continue
                if b == 0.0:
                    self.DependentDataContainsZeroFlag = True
                if a < 0.0:
                    self.IndependentData1ContainsNegativeFlag = True
                elif a > 0.0:
                    self.IndependentData1ContainsPositiveFlag = True
                else:
                    self.IndependentData1ContainsZeroFlag = True
                
                dataLists[0].append( a )
                dataLists[1].append( b )
                if useWeights:
                    weightsList.append( c )

            if self.dimensionality == 3:
                try:
                    a = float( tokenlist[0] )
                    b = float( tokenlist[1] )
                    c = float( tokenlist[2] )
                    if useWeights:
                        d = float( tokenlist[3] )
                except:
                    continue
                if a > 1.0E300 or a < -1.0E300:
                    continue
                if b > 1.0E300 or b < -1.0E300:
                    continue
                if c > 1.0E300 or c < -1.0E300:
                    continue
                if c == 0.0:
                    self.DependentDataContainsZeroFlag = True
                if a < 0.0:
                    self.IndependentData1ContainsNegativeFlag = True
                elif a > 0.0:
                    self.IndependentData1ContainsPositiveFlag = True
                else:
                    self.IndependentData1ContainsZeroFlag = True
                if b < 0.0:
                    self.IndependentData2ContainsNegativeFlag = True
                elif b > 0.0:
                    self.IndependentData2ContainsPositiveFlag = True
                else:
                    self.IndependentData2ContainsZeroFlag = True

                dataLists[0].append( a )
                dataLists[1].append( b )
                dataLists[2].append( c )
                if useWeights:
                    weightsList.append( d )

        if self.dimensionality == 1:
            self.IndependentDataArray = numpy.array( [dataLists[0]] )
        if self.dimensionality == 2:
            unused = [1.0] * len( dataLists[0] )
            self.IndependentDataArray = numpy.array( [dataLists[0], unused] ) # the second  _unused_  list is for a bug in scipy.odr, which is used to calculate standard errors on parameters
            self.DependentDataArray = numpy.array( dataLists[1] )
            if useWeights:
                self.weightsArray = numpy.array( weightsList )
        if self.dimensionality == 3:
            self.IndependentDataArray = numpy.array( [dataLists[0], dataLists[1]] )
            self.DependentDataArray = numpy.array( dataLists[2] )
            if useWeights:
                self.weightsArray = numpy.array( weightsList )


    def CalculatePredictedValuesUsingPassedInCoefficientsAndData( self, B, x ):
        try:
            self.cacheDict
        except:
            self.cacheDict = None
        if self.cacheDict is None:
            self.cacheDict = {}

        #any fixed coefficients?
        if self.fixedCoefficientArray != []:
            for i in range( len( self.fixedCoefficientArray ) ):
                if self.fixedCoefficientArray[i] > -1.0E300:
                    B[i] = self.fixedCoefficientArray[i]
                    
        tempCacheDict = self.cacheDict
        tempDataArray = self.IndependentDataArray
        
        self.cacheDict = {}
        self.IndependentDataArray = x
        self.FindOrCreateCache()
        predictedArray = self.EvaluateCachedData( B, self.cache )
        
        self.cacheDict = tempCacheDict
        self.IndependentDataArray = tempDataArray
        
        return predictedArray


    def CalculateParameterStatistics( self ):

        import scipy.stats
        
        # ensure integers are promoted to floating point with "1.0 * var"
        self.nobs = 1.0 * len( self.DependentDataArray )  # number of observations
        self.ncoef = 1.0 * len( self.coefficientArray )          # number of coef.
        self.df_e = self.nobs - self.ncoef                 # degrees of freedom, error
        self.df_r = self.ncoef - 1.0                              # degrees of freedom, regression

        try:
            self.r2 = 1.0 - self.AbsoluteErrorArray.var() / self.DependentDataArray.var()
        except:
            self.r2 = None

        try:
            self.rmse = numpy.sqrt( numpy.sum( self.AbsoluteErrorArray * self.AbsoluteErrorArray ) / self.nobs )
        except:
            self.rmse = None

        try:
            self.r2adj = 1.0 - ( 1.0 - self.r2 ) * ( ( self.nobs - 1.0 ) / ( self.nobs - self.ncoef ) )   # adjusted R-square
        except:
            self.r2adj = None


        try:
            self.Fstat = ( self.r2 / self.df_r ) / ( ( 1.0 - self.r2 ) / self.df_e )  # model F-statistic
        except:
            self.Fstat = None

        try:
            self.Fpv = 1.0 - scipy.stats.f.cdf( self.Fstat, self.df_r, self.df_e )  # F-statistic p-value
        except:
            self.Fpv = None

        # Model log-likelihood, AIC, and BIC criterion values
        try:
            self.ll = -( self.nobs * 0.5 ) * ( 1.0 + numpy.log( 2.0 * numpy.pi ) ) - ( self.nobs * 0.5 ) * numpy.log( numpy.dot( self.AbsoluteErrorArray, self.AbsoluteErrorArray ) / self.nobs )
        except:
            self.ll = None

        try:
            self.aic = -2.0 * self.ll / self.nobs + ( 2.0 * self.ncoef / self.nobs )
        except:
            self.aic = None

        try:
            self.bic = -2.0 * self.ll / self.nobs + ( self.ncoef * numpy.log( self.nobs ) ) / self.nobs
        except:
            self.bic = None

        if self.splineFlag != 0: # not appicable to splines
            self.cov_beta = None
            self.sd_beta = None
            self.tstat_beta = None
            self.pstat_beta = None
        else:
            # see both scipy.odr.odrpack and http://www.scipy.org/Cookbook/OLS
            # this is inefficient but works for every possible case
            import scipy.odr.odrpack
            model = scipy.odr.odrpack.Model( self.CalculatePredictedValuesUsingPassedInCoefficientsAndData )
            data = scipy.odr.odrpack.Data( self.IndependentDataArray, self.DependentDataArray )
            myodr = scipy.odr.odrpack.ODR( data, model, beta0=self.coefficientArray, maxit=0 )
            myodr.set_job( var_calc=0 )
            parameterStatistics = myodr.run()
            self.cov_beta = parameterStatistics.cov_beta # parameter covariance matrix
            self.sd_beta = parameterStatistics.sd_beta    # parameter standard errors

            try:
                self.tstat_beta = self.coefficientArray / self.sd_beta # coeff t-statistics
            except:
                self.tstat_beta = None

            try:
                self.pstat_beta = ( 1.0 - scipy.stats.t.cdf( numpy.abs( self.tstat_beta ), self.df_e ) ) * 2.0    # coef. p-values
            except:
                self.pstat_beta = None


    def VerifyCoefficientsAreWithinBounds( self, in_coeffArray ):
        # have this method return false if outside any desired bounds
        # note that for standard sum-of-squared fitting, the LinearSSQSolverFlag may
        # need to be set to false.  See SetGAParametersAndGuessInitialCoefficientsIfNeeded() for why this is needed.
        return True


    def SetGAParametersAndGuessInitialCoefficientsIfNeeded( self ):
        if self.splineFlag != 0: # not appicable to splines
            return
           
        if self.fixedCoefficientArray != []: # user has requested at least one fixed coefficient, must use nonlinear solver
            self.LinearSSQSolverFlag = 0
            
        if self.LinearSSQSolverFlag == 1 and self.fittingTarget == "SSQABS":
            return
            
        # make sure we are not over maximum possible number of points
        # FindOrCreateReducedDataCache() will usually add one to this to be safe
        self.numberOfDecimatedRawDataPoints = 3 * len( self.coefficientDesignatorTuple ) * self.dimensionality # seems to work OK, each equation can override
        if self.numberOfDecimatedRawDataPoints > len( self.DependentDataArray ):
            self.numberOfDecimatedRawDataPoints = len( self.DependentDataArray )

        #TODO: change these maximums when more CPU is available
        self.popSize = 100 * len( self.coefficientDesignatorTuple ) * self.dimensionality # seems to work OK, each equation can override
        if self.popSize > 500:
            self.popSize = 500

        #TODO: change these maximums when more CPU is available
        self.maxGenerations = 500 * len( self.coefficientDesignatorTuple ) * self.dimensionality # seems to work OK, each equation can override
        if self.maxGenerations > 5000:
            self.maxGenerations = 5000
        
        # Values in the existing coefficientArray will be placed into the initial DE population
        self.FindOrCreateReducedDataCache()

        if len( self.coefficientDesignatorTuple ) != len( self.coefficientArray ):
            self.coefficientArray = numpy.ones( len( self.coefficientDesignatorTuple ) )

        deltaZ = self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName][1].max() - self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName][1].min()
        self.sufficientSolution = deltaZ / self.guessDivisor

        if self.userDefinedFunctionFlag:
            self.EstimateInitialCoefficientsUsingPython() # seems very slow, profiling shows numpy.random's permutation() use in diffev.py is the problem
        else:
            self.EstimateInitialCoefficientsUsingCPP()


    def EstimateInitialCoefficientsUsingPython( self ):
        
        import diffev
        
        numpy.random.seed( 3 ) # yield repeatable results
        delta = self.maxparamvalue - self.minparamvalue
        pop0 = numpy.random.random( ( self.popSize, len( self.coefficientArray ) ) ) * delta + ( self.minparamvalue + delta / 2.0 )
        pop0[0] = self.coefficientArray
 
        de = diffev.DiffEvolver( self.CalculateReducedDataFittingTarget, pop0, crossover_rate=self.crossoverProb / 2.0, scale=self.diffScale, strategy=( 'best', 1, 'bin' ), prng=ExtraCodeForEquationBaseClasses.custom_prng_for_diffev() )
        de.solve( self.sufficientSolution, self.maxGenerations )
        self.coefficientArray = de.best_vector


    def EvaluateCachedData( self, coeff, indep_data ):

        # based on the weave array3d.py example function 'pure_inline'
        code = '''
initializeFunctionPointerArray();
// see __init__.py
(*functionArray[equationIndex])(len_cgl, extFormFlag, numberOfDataPoints, _nc, _cwoArray, coeff, indep_data, resultArray, _pndia);
'''

        # aliases to make the C++ names match the Python names
        parameterNameList = []
        
        len_cgl = len( self.CacheGenerationList )
        parameterNameList.append( 'len_cgl' )
        
        extFormFlag = self.ExtendedFormsDict[self.extendedName]
        parameterNameList.append( 'extFormFlag' )

        # these are passed in
        parameterNameList.append( 'coeff' )
        parameterNameList.append( 'indep_data' )

        equationIndex = self.equationIndex
        parameterNameList.append( 'equationIndex' )

        # this offset array is to speed weave's array access, reducing the number of required
        # multiplications in C/C++ loops - in effect partially caching C/C++ data access.
        _cwoArray = numpy.array( range( 0, len( self.CacheGenerationList ) * len( indep_data[0] ), len( indep_data[0] ) ), dtype='intc' ) # "long to int" compiler errors without specifying the underlying C data type here
        parameterNameList.append( '_cwoArray' )

        # quickly make an uninitialized numpy array to hold the results
        resultArray = numpy.empty( len( indep_data[0] ) )
        parameterNameList.append( 'resultArray' )

        numberOfDataPoints = len( indep_data[0] )
        parameterNameList.append( 'numberOfDataPoints' )

        _nc = self.numberOfCoefficientsForNonExtendedVersion
        parameterNameList.append( '_nc' )

        _pndia = numpy.array( [len( self.Polyrat2DNumeratorFlags ), len( self.Polyrat2DNumeratorFlags ) + len( self.Polyrat2DDenominatorFlags )], dtype='intc' ) # "long to int" compiler errors without specifying the underlying C data type here
        parameterNameList.append( '_pndia' )

        weave.inline( code, parameterNameList, support_code=ExtraCodeForEquationBaseClasses.cppCodeForEvaluate, extra_compile_args=Equation.compiler_flags_for_weave_inline, compiler=Equation.compiler_name )

        return resultArray


    def CalculateErrors( self ):
        self.FindOrCreateCache()
        self.PredictedArray = self.EvaluateCachedData( self.coefficientArray, self.cache )
        self.AbsoluteErrorArray = self.PredictedArray - self.DependentDataArray

        try:
            if self.DependentDataContainsZeroFlag == False:
                self.RelativeErrorArray = self.AbsoluteErrorArray / self.DependentDataArray
                self.PercentErrorArray = self.RelativeErrorArray * 100.0
        except:
            self.DependentDataContainsZeroFlag = True # in effect, yes...
            self.RelativeErrorArray = None
            self.PercentErrorArray = None


    def FindOrCreateCache( self ):
        try:
            self.cacheDict
        except:
            self.cacheDict = None
        if self.cacheDict is None:
            self.cacheDict = {}
            
        # if the thread's cache dictionary does not exist, create it
        if 'AllDataCache' not in self.cacheDict.keys():
            self.cacheDict['AllDataCache'] = {} # create an empty dictionary to fill

        # check each item in the equation's cache generation list
        cacheList = []
        for i in self.CacheGenerationList:
            # if this item is not in the cache, create it and add it to the cache
            if i[0] not in self.cacheDict['AllDataCache'].keys():
                # strip any numbers from the end of the string
                s = i[0]
                found = 1
                while found:
                    found = 0
                    lastchar = s[len( s ) - 1]
                    if lastchar.isdigit() or lastchar == '_' or lastchar == '.' or lastchar == '-' or lastchar == '[' or lastchar == ']' or lastchar == ',' or lastchar == ' ':
                        found = 1
                        s = s[:-1]
                cacheItem = eval( 'ExtraCodeForEquationBaseClasses.CG_' + s + "(self.IndependentDataArray, i[1], self)" )
                self.cacheDict['AllDataCache'][i[0]] = cacheItem
            cacheList.append( self.cacheDict['AllDataCache'][i[0]] )
        self.cache = numpy.array( cacheList )


    def CreateDecimatedRawData( self ):
        try:
            self.cacheDict
        except:
            self.cacheDict = None
        if self.cacheDict is None:
            self.cacheDict = {}

        # create a reduced subset of data, checking along each data dimension
        # to attempt selection of representative data.  This is done by getting indices
        # on the main data set, then drawing from the main data set using those indices

        # if the number of data points in the full data set is not ~1.5 times greater than the desired
        # number of data points in the reduced data set, just use the full data set directly
        if ( 1.5 * self.numberOfDecimatedRawDataPoints ) >= len( self.DependentDataArray ):
            self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName] = [self.IndependentDataArray, self.DependentDataArray]
            return

        # find the array indices for the max and min values of each data dimension in the full data set
        minXindex = 0
        maxXindex = 0
        minYindex = 0
        maxYindex = 0
        minZindex = 0
        maxZindex = 0
        for i in range( len( self.DependentDataArray ) ):
            if self.IndependentDataArray[0][i] < self.IndependentDataArray[0][minXindex]:
                minXindex = i
            if self.IndependentDataArray[0][i] > self.IndependentDataArray[0][maxXindex]:
                maxXindex = i
            if self.dimensionality == 3:
                if self.IndependentDataArray[1][i] < self.IndependentDataArray[1][minYindex]:
                    minYindex = i
                if self.IndependentDataArray[1][i] > self.IndependentDataArray[1][maxYindex]:
                    maxYindex = i
            if self.DependentDataArray[i] < self.DependentDataArray[minZindex]:
                minZindex = i
            if self.DependentDataArray[i] > self.DependentDataArray[maxZindex]:
                maxZindex = i

        # now make an array of the *indices* we will use in the reduced data set.
        # NO duplicate entries desired, so use "if value X not in list Y" logic
        indexList = []
        if minXindex not in indexList:
            indexList += minXindex,
        if maxXindex not in indexList:
            indexList += maxXindex,
        if self.dimensionality == 3:
            if minYindex not in indexList:
                indexList += minYindex,
            if maxYindex not in indexList:
                indexList += maxYindex,
        if minZindex not in indexList:
            indexList += minZindex,
        if maxZindex not in indexList:
            indexList += maxZindex,

        # if we have have not selected all data points, draw more data point indices
        if len( self.DependentDataArray ) > len( indexList ):
            #create a list of indices sorted by value of dependent variable
            sortedIndexList = range( len( self.DependentDataArray ) )
            sortedIndexList.sort( self.ReducedDataComparisonFunctionUsedForSorting )

            for i in range( self.numberOfDecimatedRawDataPoints ):
                index = i * len( self.DependentDataArray ) / self.numberOfDecimatedRawDataPoints
                if index not in indexList:
                    indexList += ( index ),

        # now that we have all the locations (indices) of the data points in the reduced
        # data set, draw those points from the full data set and make our reduced data cache
        reducedData = [[], [], []]
        for i in indexList:
            reducedData[0].append( self.IndependentDataArray[0][i] )
            if self.dimensionality == 3:
                reducedData[1].append( self.IndependentDataArray[1][i] )
            reducedData[2].append( self.DependentDataArray[i] )

        if self.dimensionality == 2:
            independentDataArray = numpy.array( [reducedData[0]] )
            dependentDataArray = numpy.array( reducedData[2] )
        else:
            independentDataArray = numpy.array( [reducedData[0], reducedData[1]] )
            dependentDataArray = numpy.array( reducedData[2] )

        self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName] = [independentDataArray, dependentDataArray]


    def ReducedDataComparisonFunctionUsedForSorting( self, int1, int2 ):
        if self.DependentDataArray[int1] < self.DependentDataArray[int2]:
            return - 1
        if self.DependentDataArray[int1] > self.DependentDataArray[int2]:
            return 1
        return 0


    def FindOrCreateReducedDataCache( self ):
        try:
            self.cacheDict
        except:
            self.cacheDict = None
        if self.cacheDict is None:
            self.cacheDict = {}

        # these are for looking up values in the Reduced Data cache
        self.decimatedRawDataCacheName = 'DecimatedRawDataCache' + str( self.numberOfDecimatedRawDataPoints ) + '_' + str( self.dimensionality ) + 'D'
        self.reducedDataName = 'ReducedDataCache' + str( self.numberOfDecimatedRawDataPoints ) + '_' + str( self.dimensionality ) + 'D'

        # if the Decimated Raw Data cache dictionaries do not exist, create them
        if 'DecimatedRawDataCache' not in self.cacheDict.keys():
            self.cacheDict['DecimatedRawDataCache'] = {}

        # if the Reduced Data cache dictionaries do not exist, create them
        if 'ReducedDataCache' not in self.cacheDict.keys():
            self.cacheDict['ReducedDataCache'] = {}

        # if we don't have a reduced data set for [this number of points], first
        # check if there is one for [this number +1].  If not a +1 to use, then make this set
        if self.decimatedRawDataCacheName not in self.cacheDict['DecimatedRawDataCache'].keys():
            nextSetName = 'DecimatedRawDataCache' + str( self.numberOfDecimatedRawDataPoints + 1 ) + '_' + str( self.dimensionality ) + 'D' # +1 is OK for estimation
            if nextSetName not in self.cacheDict['DecimatedRawDataCache'].keys():
                self.CreateDecimatedRawData() # create the Decimated Raw Data cache for this number of Reduced Data points
            else:
                self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName] = self.cacheDict['DecimatedRawDataCache'][nextSetName]

        # check each item in the equation's cache generation list
        if self.reducedDataName not in self.cacheDict['ReducedDataCache'].keys(): # if a cache for this number of points does not exist, create it
            self.cacheDict['ReducedDataCache'][self.reducedDataName] = {}
        tempReducedDataCacheList = []
        for i in self.CacheGenerationList:
            # if this item is not in the Reduced Data cache, create it and add it to the cache
            if i[0] not in self.cacheDict['ReducedDataCache'][self.reducedDataName].keys():
                # strip any numbers from the end of the string
                s = i[0]
                found = 1
                while found:
                    found = 0
                    lastchar = s[len( s ) - 1]
                    if lastchar.isdigit() or lastchar == '_' or lastchar == '.' or lastchar == '-' or lastchar == '[' or lastchar == ']' or lastchar == ',' or lastchar == ' ':
                        found = 1
                        s = s[:-1]
                cacheItem = eval( 'ExtraCodeForEquationBaseClasses.CG_' + s + "(self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName][0], i[1], self)" ),
                self.cacheDict['ReducedDataCache'][self.reducedDataName][i[0]] = cacheItem
            tempReducedDataCacheList.append( self.cacheDict['ReducedDataCache'][self.reducedDataName][i[0]][0] )

        # now store this cache and associated dependent data conveniently for later retrieval
        self.reducedCache = numpy.array( tempReducedDataCacheList )
        self.reducedDependentData = self.cacheDict['DecimatedRawDataCache'][self.decimatedRawDataCacheName][1]


    def CalculateFittingTarget( self, in_coeffArray ):
        #save time by checking constraints and bounds first
        if not self.VerifyCoefficientsAreWithinBounds( in_coeffArray ):
            return 1.0E300

        try:
            #any fixed coefficients?
            if self.fixedCoefficientArray != []:
                for i in range( len( self.fixedCoefficientArray ) ):
                    if self.fixedCoefficientArray[i] > -1.0E300:
                        in_coeffArray[i] = self.fixedCoefficientArray[i]
                        
            error = self.EvaluateCachedData( in_coeffArray, self.cache ) - self.DependentDataArray
            
            if 0 != len( self.weightsArray ):
                error = error * self.weightsArray
                
            if self.fittingTarget == "SSQABS":
                val = numpy.sum( error * error )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "SSQREL":
                error = error / self.DependentDataArray
                val = numpy.sum( error * error )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "ABSABS":
                val = numpy.sum( numpy.abs( error ) )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "ABSREL":
                val = numpy.sum( numpy.abs( error / self.DependentDataArray ) )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "PEAKABS":
                val = numpy.max( numpy.abs( error ) )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "PEAKREL":
                val = numpy.max( numpy.abs( error / self.DependentDataArray ) )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300

            ncoef = 1.0 * len( in_coeffArray )          # number of coef.
            nobs = 1.0 * len( self.DependentDataArray )  # number of observations
            ll = -( nobs * 0.5 ) * ( 1.0 + numpy.log( 2.0 * numpy.pi ) ) - ( nobs * 0.5 ) * numpy.log( numpy.dot( error, error ) / nobs )

            if self.fittingTarget == "AIC":
                val = -2.0 * ll / nobs + ( 2.0 * ncoef / nobs )
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "BIC":
                val = -2.0 * ll / nobs + ( ncoef * numpy.log( nobs ) ) / nobs
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
            if self.fittingTarget == "ODR": # this is inefficient but works for every possible case
                import scipy.odr.odrpack
                model = scipy.odr.odrpack.Model( self.CalculatePredictedValuesUsingPassedInCoefficientsAndData )
                if 0 != len( self.weightsArray ):
                    data = scipy.odr.odrpack.Data( self.IndependentDataArray, self.DependentDataArray, we=self.weightsArray )
                else:
                    data = scipy.odr.odrpack.Data( self.IndependentDataArray, self.DependentDataArray )
                myodr = scipy.odr.odrpack.ODR( data, model, beta0=self.coefficientArray, maxit=len( self.coefficientArray ) * self.fminIterationLimit )
                myodr.set_job( var_calc=0 )
                out = myodr.run()
                val = out.sum_square
                if numpy.isfinite( val ):
                    return val
                else:
                    return 1.0E300
        except:
            return 1.0E300


    def CalculateReducedDataFittingTarget( self, in_coeffArray ):
        #save time by checking constraints and bounds first
        if not self.VerifyCoefficientsAreWithinBounds( in_coeffArray ):
            return 1.0E300

        # just return SSQ, as we are only using this method for guessing initial coefficients
        try:
            #any fixed coefficients?
            if self.fixedCoefficientArray != []:
                for i in range( len( self.fixedCoefficientArray ) ):
                    if self.fixedCoefficientArray[i] > 1.0E300:
                        in_coeffArray[i] = self.fixedCoefficientArray[i]
                        
            error = self.EvaluateCachedData( in_coeffArray, self.reducedCache ) - self.reducedDependentData
            ssq = numpy.sum( error * error )
        except:
            ssq = 1.0E300
        if numpy.isfinite( ssq ):
            return ssq
        else:
            return 1.0E300


    def FitToCacheData( self ):
        self.FindOrCreateCache()

        # linear fits - this may have been set to zero in SetGAParametersAndGuessInitialCoefficientsIfNeeded()
        # if there are fixed coefficients
        if self.LinearSSQSolverFlag != 0: # can we linear fit?
            if self.fittingTarget == "SSQABS":
                self.coefficientArray = numpy.linalg.lstsq( self.cache.T, self.DependentDataArray )[0]
                if 0 == len( self.weightsArray ):
                    return

        #nonlinear fits
        if self.fittingTarget == "ODR":
                import scipy.odr.odrpack
                model = scipy.odr.odrpack.Model( self.CalculatePredictedValuesUsingPassedInCoefficientsAndData )
                if 0 != len( self.weightsArray ):
                    data = scipy.odr.odrpack.Data( self.IndependentDataArray, self.DependentDataArray, we=self.weightsArray )
                else:
                    data = scipy.odr.odrpack.Data( self.IndependentDataArray, self.DependentDataArray )
                myodr = scipy.odr.odrpack.ODR( data, model, beta0=self.coefficientArray, maxit=len( self.coefficientArray ) * self.fminIterationLimit )
                myodr.set_job( fit_type=0, deriv=0 ) # explicit ODR, faster forward-only finite differences for derivatives
                out = myodr.run()
                self.coefficientArray = out.beta
        else:
            import scipy.optimize
            if self.nonlinearSolver == 1: # 1 = fmin, 2 = fmin_bfgs, 3 = fmin_cg, 4 = fmin_ncq, 5 = fmin_powell
                self.coefficientArray = scipy.optimize.fmin( self.CalculateFittingTarget, self.coefficientArray, maxiter=len( self.coefficientArray ) * self.fminIterationLimit, maxfun=len( self.coefficientArray ) * self.fminFunctionLimit, disp=0, xtol=self.fmin_xtol, ftol=self.fmin_ftol )
            elif self.nonlinearSolver == 2:
                self.coefficientArray = scipy.optimize.fmin_bfgs( self.CalculateFittingTarget, self.coefficientArray, maxiter=len( self.coefficientArray ) * self.fminIterationLimit, disp=0 )
            elif self.nonlinearSolver == 3:
                self.coefficientArray = scipy.optimize.fmin_cg( self.CalculateFittingTarget, self.coefficientArray, maxiter=len( self.coefficientArray ) * self.fminIterationLimit, disp=0 )
            elif self.nonlinearSolver == 4:
                self.coefficientArray = scipy.optimize.fmin_ncg( self.CalculateFittingTarget, self.coefficientArray, maxiter=len( self.coefficientArray ) * self.fminIterationLimit, disp=0 )
            elif self.nonlinearSolver == 5:
                self.coefficientArray = scipy.optimize.fmin_powell( self.CalculateFittingTarget, self.coefficientArray, maxiter=len( self.coefficientArray ) * self.fminIterationLimit, disp=0, xtol=1e-10, ftol=1e-10 )

            #any fixed coefficients?
            if self.fixedCoefficientArray != []:
                for i in range( len( self.fixedCoefficientArray ) ):
                    if self.fixedCoefficientArray[i] > -1.0E300:
                        self.coefficientArray[i] = self.fixedCoefficientArray[i]


    def EstimateInitialCoefficientsUsingCPP( self ):

        # based on the weave array3d.py example function 'pure_inline'
        supportCode = '''
// adapted for scipy.weave by James Phillips http://zunzun.com April 2008
// from Differential Evolution Program: de.c  Version: 3.6
// DE homepage: http://www.icsi.berkeley.edu/~storn/code.html

/*------Constants for rnd_uni()--------------------------------------------*/
#define IM1 2147483563
#define IM2 2147483399
#define AM (1.0/IM1)
#define IMM1 (IM1-1)
#define IA1 40014
#define IA2 40692
#define IQ1 53668
#define IQ2 52774
#define IR1 12211
#define IR2 3791
#define NTAB 32
#define NDIV (1+IMM1/NTAB)
#define EPS 1.2e-7
#define RNMX (1.0-EPS)


void  assignd(int D, double *a, double *b)
// Assigns D-dimensional vector b to vector a.
{
	for (int j=0; j<D; j++)
	a[j] = b[j];
}

double rnd_uni(long *idum)
// generates an equally distributed random number in the interval [0,1]
{
	long j;
	long k;
	static long idum2=123456789;
	static long iy=0;
	static long iv[NTAB];
	double temp;

	if (*idum <= 0)
	{
		if (-(*idum) < 1) *idum=1;
		else *idum = -(*idum);
		idum2=(*idum);
		for (j=NTAB+7;j>=0;j--)
		{
			k=(*idum)/IQ1;
			*idum=IA1*(*idum-k*IQ1)-k*IR1;
			if (*idum < 0) *idum += IM1;
			if (j < NTAB) iv[j] = *idum;
		}
		iy=iv[0];
	}
	k=(*idum)/IQ1;
	*idum=IA1*(*idum-k*IQ1)-k*IR1;
	if (*idum < 0) *idum += IM1;
	k=idum2/IQ2;
	idum2=IA2*(idum2-k*IQ2)-k*IR2;
	if (idum2 < 0) idum2 += IM2;
	j=iy/NDIV;
	iy=iv[j]-idum2;
	iv[j] = *idum;
	if (iy < 1) iy += IMM1;
	if ((temp=AM*iy) > RNMX) return RNMX;
	else return temp;
}

''' + ExtraCodeForEquationBaseClasses.cppCodeForGA


        # aliases to make the C++ names match the Python names
        parameterNameList = []

        len_cgl = len( self.CacheGenerationList )
        parameterNameList.append( 'len_cgl' )
        
        total_ncoeff = len( self.additionalDesignatorList ) + self.numberOfCoefficientsForNonExtendedVersion
        parameterNameList.append( 'total_ncoeff' )
        
        extFormFlag = self.ExtendedFormsDict[self.extendedName]
        parameterNameList.append( 'extFormFlag' )

        sufficientSolution = self.sufficientSolution
        parameterNameList.append( 'sufficientSolution' )

        # this offset array is to speed weave's array access, reducing the number of required
        # multiplications in C/C++ loops - in effect partially caching C/C++ data access.
        _cwoArray = numpy.array( range( 0, len( self.CacheGenerationList ) * len( self.reducedCache[0] ), len( self.reducedCache[0] ) ), dtype='intc' )
        parameterNameList.append( '_cwoArray' )

        equationIndex = self.equationIndex
        parameterNameList.append( 'equationIndex' )

        indep_data = self.reducedCache
        parameterNameList.append( 'indep_data' )

        dep_data = self.reducedDependentData
        parameterNameList.append( 'dep_data' )

        numberOfDataPoints = len( self.reducedDependentData )
        parameterNameList.append( 'numberOfDataPoints' )

        inibound_h = self.maxparamvalue
        parameterNameList.append( 'inibound_h' )

        inibound_l = self.minparamvalue
        parameterNameList.append( 'inibound_l' )

        genmax = self.maxGenerations
        parameterNameList.append( 'genmax' )

        F = self.diffScale
        parameterNameList.append( 'F' )

        CR = self.crossoverProb
        parameterNameList.append( 'CR' )

        populationSize = self.popSize
        parameterNameList.append( 'populationSize' )

        coeffs = self.coefficientArray
        parameterNameList.append( 'coeffs' )

        _nc = self.numberOfCoefficientsForNonExtendedVersion
        parameterNameList.append( '_nc' )

        useFixedCoefficientArrayFlag = 0
        if self.fixedCoefficientArray != []:
            useFixedCoefficientArrayFlag = 1
        parameterNameList.append( 'useFixedCoefficientArrayFlag' )

        fixedCoefficientArray = self.fixedCoefficientArray
        parameterNameList.append( 'fixedCoefficientArray' )

        shouldBoundsBeChecked = self.requiresCoefficientBoundsCheckWhenFitting
        if 0 != self.requiresCoefficientBoundsCheckWhenFitting:
            upperConstraints = self.upperCoefficientBoundsArray
            lowerConstraints = self.lowerCoefficientBoundsArray
        else:
            upperConstraints = self.reducedDependentData # unused, give something that stops compiler warnings
            lowerConstraints = self.reducedDependentData # unused, give something that stops compiler warnings
        parameterNameList.append( 'shouldBoundsBeChecked' )
        parameterNameList.append( 'upperConstraints' )
        parameterNameList.append( 'lowerConstraints' )

        seed = 3  # yield repeatable results
        parameterNameList.append( 'seed' )

        target = 1
        parameterNameList.append( 'target' )

        _pndia = numpy.array( [len( self.Polyrat2DNumeratorFlags ), len( self.Polyrat2DNumeratorFlags ) + len( self.Polyrat2DDenominatorFlags )], dtype='intc' ) # "long to int" compiler errors without specifying the underlying C data type here
        parameterNameList.append( '_pndia' )
        
        code = '''
    initializeFunctionPointerArray();

    // adapted for scipy.weave by James Phillips http://zunzun.com April 2008
    // from Differential Evolution Program: de.c  Version: 3.6
    // DE homepage: http://www.icsi.berkeley.edu/~storn/code.html

    int D = total_ncoeff;

    long  rnd_uni_init;    // serves as a seed for rnd_uni()

    int   i, j, L, n;      // counting variables
    int   r1, r2, r3, r4;  // placeholders for random indexes
    int   r5;              // placeholders for random indexes
    int   imin;            // index to member with lowest energy
    int   gen;

    double trial_cost;      // buffer variable
    double *tmp, *best;     // internal members
    double *bestit;         // internal members
    double *cost;           // obj. funct. values
    double **c, **d;        // internal members
    double **pold, **pnew;  // internal members
    double **pswap;         // internal members
    double cmin;            // help variables

    int ndatapoints = numberOfDataPoints;

    /*-----Initialize random number generator-----------------------------*/

    rnd_uni_init = -(long)seed;  /* initialization of rnd_uni() */

    c = new double* [populationSize];
    for (i=0; i<populationSize; i++)
        c[i] = new double[D];

    d = new double* [populationSize];
    for (i=0; i<populationSize; i++)
        d[i] = new double[D];

    tmp = new double[D];
    best = new double[D];
    bestit = new double[D];
    cost = new double[populationSize];

    // random initial population
    for (i=0; i<populationSize; i++)
        for (j=0; j<D; j++)
            c[i][j] = inibound_l + rnd_uni(&rnd_uni_init)*(inibound_h - inibound_l);

    // pre-seed the first generation's list with passed-in parameter values
    for (j=0; j<D; j++)
        c[0][j] = coeffs[j];

    double * coeff;

    for (j=0; j<populationSize; j++)
    {
        coeff = c[j];
        cost[j] = 0.0;
        int boundsTestOK = 1;

        // check for parameter constraints
        if(0 != (int)shouldBoundsBeChecked)
        {
            for(i=0; i<total_ncoeff; i++)
                if ((coeff[i] < lowerConstraints[i]) || (coeff[i]  > upperConstraints[i]))
                {
                    cost[j] = 1.0E300;
                    boundsTestOK = 0;
                }
        }

        if(0 != boundsTestOK)
        {
            // see __init__.py
            cost[j] = (*functionArray[equationIndex])(len_cgl, extFormFlag, ndatapoints, _nc, _cwoArray, coeff, indep_data, dep_data, _pndia);
        }
    }

    cmin = cost[0];
    imin = 0;
    for (i=1; i<populationSize; i++)
    {
        if (cost[i]<cmin)
        {
            cmin = cost[i];
            imin = i;
        }
    }

    assignd(D,best,c[imin]);            /* save best member ever          */

    assignd(D,bestit,c[imin]);          /* save best member of generation */

    pold = c; /* old population (generation G)   */
    pnew = d; /* new population (generation G+1) */


    /*=======================================================================*/
    /*=========Iteration loop================================================*/
    /*=======================================================================*/

    gen = 0;                          /* generation counter reset */

    while ((gen < genmax) && (sufficientSolution < cmin))
    {
        for (j=0; j<populationSize; j++)         /* Start of loop through ensemble  */
        {
            do                        /* Pick a random population member */
            {                         /* endless loop for populationSize < 2 !!!     */
                r1 = (int)(rnd_uni(&rnd_uni_init)*populationSize);
            }while(r1==j);

            do                        /* Pick a random population member */
            {                         /* endless loop for populationSize < 3 !!!     */
                r2 = (int)(rnd_uni(&rnd_uni_init)*populationSize);
            }while((r2==j) || (r2==r1));

            do                        /* Pick a random population member */
            {                         /* endless loop for populationSize < 4 !!!     */
                r3 = (int)(rnd_uni(&rnd_uni_init)*populationSize);
            }while((r3==j) || (r3==r1) || (r3==r2));

            do                        /* Pick a random population member */
            {                         /* endless loop for populationSize < 5 !!!     */
                r4 = (int)(rnd_uni(&rnd_uni_init)*populationSize);
            }while((r4==j) || (r4==r1) || (r4==r2) || (r4==r3));

            do                        /* Pick a random population member */
            {                         /* endless loop for populationSize < 6 !!!     */
                r5 = (int)(rnd_uni(&rnd_uni_init)*populationSize);
            }while((r5==j) || (r5==r1) || (r5==r2) || (r5==r3) || (r5==r4));

            /*-------DE/best/1/bin--------------------------------------------------------------------*/
            assignd(D,tmp,pold[j]);
            n = (int)(rnd_uni(&rnd_uni_init)*D);
            for (L=0; L<D; L++) /* perform D binomial trials */
            {
                if ((rnd_uni(&rnd_uni_init) < CR) || L == (D-1)) /* change at least one parameter */
                {
                    tmp[n] = bestit[n] + F*(pold[r2][n]-pold[r3][n]);
                }
                n = (n+1)%D;
            }


            /*=======Trial mutation now in tmp[]. Test how good this choice really was.==================*/

            double * coeff;
            coeff = tmp;
            double temp, temp_x_sq, temp_y_sq, s_sq, s_over_r, s_sq_b, s_over_r_b;

            trial_cost = 0.0;

            int boundsTestOK = 1;

            // check for parameter constraints
            if(0 != (int)shouldBoundsBeChecked)
            {
                for(i=0; i<total_ncoeff; i++)
                {
                    if ((coeff[i] < lowerConstraints[i]) || (coeff[i]  > upperConstraints[i]))
                    {
                        trial_cost = 1.0E300;
                        boundsTestOK = 0;
                    }
                }
            }

            if(0 != boundsTestOK)
            {
                if(0 != useFixedCoefficientArrayFlag) // for performance, use flag to enter this code section
                {
                    for (int fixedIndex = 0; fixedIndex < total_ncoeff; fixedIndex++)
                    {
                        if (fixedCoefficientArray[fixedIndex] > -1.0E300)
                        {
                            coeff[fixedIndex] = fixedCoefficientArray[fixedIndex];
                        }
                    }
                }
                
                // see __init__.py
                trial_cost = (*functionArray[equationIndex])(len_cgl, extFormFlag, ndatapoints, _nc, _cwoArray, coeff, indep_data, dep_data, _pndia);
            }

            if (trial_cost <= cost[j])   /* improved objective function value ? */
            {
                cost[j]=trial_cost;
                assignd(D,pnew[j],tmp);
                if (trial_cost<cmin)          /* Was this a new minimum? */
                {                               /* if so...*/
                    cmin=trial_cost;           /* reset cmin to new low...*/
                    imin=j;
                    assignd(D,best,tmp);
                }
            }
            else
            {
                assignd(D,pnew[j],pold[j]); /* replace target with old value */
            }
        }   /* End mutation loop through pop. */

            assignd(D,bestit,best);  /* Save best population member of current iteration */

            /* swap population arrays. New generation becomes old one */

            pswap = pold;
            pold  = pnew;
            pnew  = pswap;

            gen++;

        /*=======================================================================*/
        /*=========End of iteration loop=========================================*/
        /*=======================================================================*/
    }

    for(i=0; i<D; i++)
        coeffs[i] = best[i];

    delete cost;
    delete bestit;
    delete best;
    delete tmp;

    for (i=0; i<populationSize; i++)
        delete d[i];
    delete d;
    for (i=0; i<populationSize; i++)
        delete c[i];
    delete c;
'''

        weave.inline( code, parameterNameList, support_code=supportCode, extra_compile_args=Equation.compiler_flags_for_weave_inline, compiler=Equation.compiler_name )


    def GetAdditionalDesignator( self, n ):
        return Equation.ascii[n]


    def CodeCPP( self ):
        s = """// To the best of my knowledge this code is correct.
// If you find any errors or problems please contact
// me at zunzun@zunzun.com.
//      James


#include <math.h>

"""
        s += "// " + self.FittingTargetDict[self.fittingTarget][1] + "\n\n"
        if self.dimensionality == 2:
            s += "double " + self.__class__.__name__ + "_model(double x_in)\n{\n"
        else:
            s += "double " + self.__class__.__name__ + "_model(double x_in, double y_in)\n{\n"
        s += "\tdouble temp;\n\ttemp = 0.0;\n\n"

        s += "\t// coefficients\n"
        for i in range( len( self.coefficientArray ) ):
            s += "\tdouble " + self.coefficientDesignatorTuple[i] + " = %-.16E" % ( self.coefficientArray[i] ) + ";\n"
        s += "\n"
        
        s += self.GetSpecificCodeCPP_WithExtendedCodeIfNeeded()
        
        s += "\treturn temp;\n}\n"
        return s


    def ConvertCppToAnotherLanguage( self, languageString, inString ):
        if languageString == 'PYTHON':
            newString = inString.replace( ';', '' )

            newString = newString.replace( 'double ', '' )
            
            newString = newString.replace( 'pow(', 'math.pow(' )
            newString = newString.replace( 'log(', 'math.log(' )
            newString = newString.replace( 'exp(', 'math.exp(' )
            
            newString = newString.replace( 'sin(', 'math.sin(' )
            newString = newString.replace( 'cos(', 'math.cos(' )
            newString = newString.replace( 'tan(', 'math.tan(' )
            newString = newString.replace( 'cosh(', 'math.cosh(' )

            newString = newString.replace( '//', '#' )
            
        if languageString == 'JAVA':
            newString = inString.replace( 'pow(', 'Math.pow(' )
            newString = newString.replace( 'log(', 'Math.log(' )
            newString = newString.replace( 'exp(', 'Math.exp(' )
            
            newString = newString.replace( 'sin(', 'Math.sin(' )
            newString = newString.replace( 'cos(', 'Math.cos(' )
            newString = newString.replace( 'tan(', 'Math.tan(' )
            newString = newString.replace( 'cosh(', 'Math.cosh(' )

            if newString[0] == '\t':
                newString = '\t' + newString
            newString = newString.replace( '\n\t', '\n\t\t' )
                
        if languageString == 'CSHARP':
            newString = inString.replace( 'pow(', 'Math.Pow(' )
            newString = newString.replace( 'log(', 'Math.Log(' )
            newString = newString.replace( 'exp(', 'Math.Exp(' )
            
            newString = newString.replace( 'sin(', 'Math.Sin(' )
            newString = newString.replace( 'cos(', 'Math.Cos(' )
            newString = newString.replace( 'tan(', 'Math.Tan(' )
            newString = newString.replace( 'cosh(', 'Math.Cosh(' )

            if newString[0] == '\t':
                newString = '\t' + newString
            newString = newString.replace( '\n\t', '\n\t\t' )
                
        if languageString == 'SCILAB':
            newString = inString.replace( ';', '' )

            newString = newString.replace( 'double ', '' )

            newString = newString.replace( 'pow(', 'power(' )
                
            newString = newString.replace( '//', '%' )

        if languageString == 'MATLAB':
            newString = inString.replace( 'pow(', 'power(' )

            newString = newString.replace( 'double ', '' )

            newString = newString.replace( '^', '.^' )
            newString = newString.replace( '*', '.*' )
            newString = newString.replace( '/', './' )
                
            newString = newString.replace( '//', '%' )

        return newString


    def CodePYTHON( self ):
        s = """# To the best of my knowledge this code is correct.
# If you find any errors or problems please contact
# me at zunzun@zunzun.com.
#      James


import math

"""
        s += "# " + self.FittingTargetDict[self.fittingTarget][1] + "\n\n"
        if self.dimensionality == 2:
            s += "def " + self.__class__.__name__ + "_model(x_in):\n"
        else:
            s += "def " + self.__class__.__name__ + "_model(x_in, y_in):\n"
        s += "\ttemp = 0.0\n\n"

        s += "\t# coefficients\n"
        for i in range( len( self.coefficientArray ) ):
            s += "\t" + self.coefficientDesignatorTuple[i] + " = %-.16E" % ( self.coefficientArray[i] ) + "\n"
        s += "\n"

        s += self.ConvertCppToAnotherLanguage( 'PYTHON', self.GetSpecificCodeCPP_WithExtendedCodeIfNeeded() )

        s += "\treturn temp\n"
        return s


    def CodeJAVA( self ):
        s = """// To the best of my knowledge this code is correct.
// If you find any errors or problems please contact
// me at zunzun@zunzun.com.
//      James


import java.lang.Math;

"""
        s += "// " + self.FittingTargetDict[self.fittingTarget][1] + "\n\n"
        s += "class " + self.__class__.__name__ + "\n{\n"
        if self.dimensionality == 2:
            s += "\tdouble " + self.__class__.__name__ + "_model(double x_in)\n\t{\n"
        else:
            s += "\tdouble " + self.__class__.__name__ + "_model(double x_in, double y_in)\n\t{\n"
        s += "\t\tdouble temp;\n\t\ttemp = 0.0;\n\n"

        s += "\t\t// coefficients\n"
        for i in range( len( self.coefficientArray ) ):
            s += "\t\tdouble " + self.coefficientDesignatorTuple[i] + " = %-.16E" % ( self.coefficientArray[i] ) + ";\n"
        s += "\n"
        
        s += self.ConvertCppToAnotherLanguage( 'JAVA', self.GetSpecificCodeCPP_WithExtendedCodeIfNeeded() )
        
        s += "\t\treturn temp;\n\t}\n}\n"
        return s


    def CodeCS( self ):
        s = """// To the best of my knowledge this code is correct.
// If you find any errors or problems please contact
// me at zunzun@zunzun.com.
//      James


using System;

"""
        s += "// " + self.FittingTargetDict[self.fittingTarget][1] + "\n\n"
        s += "class " + self.__class__.__name__ + "\n{\n"
        if self.dimensionality == 2:
            s += "\tdouble " + self.__class__.__name__ + "_model(double x_in)\n\t{\n"
        else:
            s += "\tdouble " + self.__class__.__name__ + "_model(double x_in, double y_in)\n\t{\n"
        s += "\t\tdouble temp;\n\t\ttemp = 0.0;\n\n"

        s += "\t\t// coefficients\n"
        for i in range( len( self.coefficientArray ) ):
            s += "\t\tdouble " + self.coefficientDesignatorTuple[i] + " = %-.16E" % ( self.coefficientArray[i] ) + ";\n"
        s += "\n"
        
        s += self.ConvertCppToAnotherLanguage( 'CSHARP', self.GetSpecificCodeCPP_WithExtendedCodeIfNeeded() )
        
        s += "\t\treturn temp;\n\t}\n}\n"
        return s


    def CodeSCILAB( self ):
        s = """// To the best of my knowledge this code is correct.
// If you find any errors or problems please contact
// me at zunzun@zunzun.com.
//      James

"""
        s += "// " + self.FittingTargetDict[self.fittingTarget][1] + "\n\n"
        if self.dimensionality == 2:
            s += "function y=" + self.__class__.__name__ + "_model(x_in)\n"
        else:
            s += "function z=" + self.__class__.__name__ + "_model(x_in, y_in)\n"
        s += "\ttemp = 0.0\n\n"

        s += "\t// coefficients\n"
        for i in range( len( self.coefficientArray ) ):
            s += "\t" + self.coefficientDesignatorTuple[i] + " = %-.16E" % ( self.coefficientArray[i] ) + "\n"
        s += "\n"
        
        s += self.ConvertCppToAnotherLanguage( 'SCILAB', self.GetSpecificCodeCPP_WithExtendedCodeIfNeeded() )
        
        if self.dimensionality == 2:
            s += "\n\ty = temp\n"
        else:
            s += "\n\tz = temp\n"
        s += "endfunction\n"
        return s


    def CodeMATLAB( self ):
        s = """% To the best of my knowledge this code is correct.
% If you find any errors or problems please contact
% me at zunzun@zunzun.com.
%      James

"""
        s += "% " + self.FittingTargetDict[self.fittingTarget][1] + "\n\n"
        if self.dimensionality == 2:
            s += "function y=" + self.__class__.__name__ + "_model(x_in)\n"
        else:
            s += "function z=" + self.__class__.__name__ + "_model(x_in, y_in)\n"
        s += "\ttemp = 0.0;\n\n"

        s += "\t% coefficients\n"
        for i in range( len( self.coefficientArray ) ):
            s += "\t" + self.coefficientDesignatorTuple[i] + " = %-.16E" % ( self.coefficientArray[i] ) + ";\n"
        s += "\n"

        # semicolons on lines internal to functions
        #  comment designators
        #  replace "^" with ".^"
        s += self.ConvertCppToAnotherLanguage( 'MATLAB', self.GetSpecificCodeCPP_WithExtendedCodeIfNeeded() )

        if self.dimensionality == 2:
            s += "\n\ty = temp;\n"
        else:
            s += "\n\tz = temp;\n"
        return s


    def GetSpecificCodeCPP_WithExtendedCodeIfNeeded( self ):
        
        code = self.SpecificCodeCPP()
        
        if self.extendedName == '':
            return code
            
        if self.extendedName == 'Offset':
            return code + '\ttemp = temp + ' + self.additionalDesignatorList[0] + ';\n'

        if self.extendedName == 'Reciprocal':
            return code + '\ttemp = 1.0 / temp;\n'

        if self.extendedName == 'ReciprocalWithOffset':
            return code + '\ttemp = 1.0 / temp + ' + self.additionalDesignatorList[0] + ';\n'

        if self.extendedName == 'InverseX':
            return code + '\ttemp = x_in / temp;\n'

        if self.extendedName == 'InverseXWithOffset':
            return code + '\ttemp = x_in / temp + ' + self.additionalDesignatorList[0] + ';\n'

        if self.extendedName == 'InverseXY':
            return code + '\ttemp = (x_in * y_in) / temp;\n'

        if self.extendedName == 'InverseXYWithOffset':
            return code + '\ttemp = (x_in * y_in) / temp + ' + self.additionalDesignatorList[0] + ';\n'

        if self.extendedName == 'X_LinearDecay':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * x_in);\n'

        if self.extendedName == 'XY_LinearDecay':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * x_in * y_in);\n'

        if self.extendedName == 'X_LinearDecayAndOffset':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * x_in) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'XY_LinearDecayAndOffset':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * x_in * y_in) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'X_ExponentialDecay':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * exp(x_in));\n'

        if self.extendedName == 'XY_ExponentialDecay':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * exp(x_in * y_in));\n'

        if self.extendedName == 'X_ExponentialDecayAndOffset':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * exp(x_in)) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'XY_ExponentialDecayAndOffset':
            return code + '\ttemp = temp / (' + self.additionalDesignatorList[0] + ' * exp(x_in * y_in)) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'X_LinearGrowth':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * x_in);\n'

        if self.extendedName == 'XY_LinearGrowth':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * x_in * y_in);\n'

        if self.extendedName == 'X_LinearGrowthAndOffset':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * x_in) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'XY_LinearGrowthAndOffset':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * x_in * y_in) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'X_ExponentialGrowth':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * exp(x_in));\n'

        if self.extendedName == 'XY_ExponentialGrowth':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * exp(x_in * y_in));\n'

        if self.extendedName == 'X_ExponentialGrowthAndOffset':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * exp(x_in)) + ' + self.additionalDesignatorList[1] + ';\n'

        if self.extendedName == 'XY_ExponentialGrowthAndOffset':
            return code + '\ttemp = temp * (' + self.additionalDesignatorList[0] + ' * exp(x_in * y_in)) + ' + self.additionalDesignatorList[1] + ';\n'


    def get_name( self ):
        if self.extendedName == '':
            return self._name

        if self.extendedName == 'Offset':
            return self._name + " With Offset"

        if self.extendedName == 'Reciprocal':
            return "Reciprocal " + self._name

        if self.extendedName == 'ReciprocalWithOffset':
            return "Reciprocal " + self._name + " With Offset"

        if self.extendedName == 'InverseX':
            return "Inverse " + self._name

        if self.extendedName == 'InverseXWithOffset':
            return "Inverse " + self._name + " With Offset"

        if self.extendedName == 'X_LinearDecay':
            if self.dimensionality == 2:
                return self._name + " With Linear Decay"
            else:
                return self._name + " With X Linear Decay"

        if self.extendedName == 'X_LinearDecayAndOffset':
            if self.dimensionality == 2:
                return self._name + " With Linear Decay And Offset"
            else:
                return self._name + " With X Linear Decay And Offset"

        if self.extendedName == 'X_ExponentialDecay':
            if self.dimensionality == 2:
                return self._name + " With Exponential Decay"
            else:
                return self._name + " With X Exponential Decay"

        if self.extendedName == 'X_ExponentialDecayAndOffset':
            if self.dimensionality == 2:
                return self._name + " With Exponential Decay And Offset"
            else:
                return self._name + " With X Exponential Decay And Offset"

        if self.extendedName == 'X_LinearGrowth':
            if self.dimensionality == 2:
                return self._name + " With Linear Growth"
            else:
                return self._name + " With X Linear Growth"

        if self.extendedName == 'X_LinearGrowthAndOffset':
            if self.dimensionality == 2:
                return self._name + " With Linear Growth And Offset"
            else:
                return self._name + " With X Linear Growth And Offset"

        if self.extendedName == 'X_ExponentialGrowth':
            if self.dimensionality == 2:
                return self._name + " With Exponential Growth"
            else:
                return self._name + " With X Exponential Growth"

        if self.extendedName == 'X_ExponentialGrowthAndOffset':
            if self.dimensionality == 2:
                return self._name + " With Exponential Growth And Offset"
            else:
                return self._name + " With X Exponential Growth And Offset"

        if self.extendedName == 'InverseXY':
            return "Inverse " + self._name

        if self.extendedName == 'InverseXYWithOffset':
            return "Inverse " + self._name + " With Offset"
            
        if self.extendedName == 'XY_LinearDecay':
            return self._name + " With XY Linear Decay"

        if self.extendedName == 'XY_LinearDecayAndOffset':
            return self._name + " With XY Linear Decay And Offset"

        if self.extendedName == 'XY_ExponentialDecay':
            return self._name + " With XY Exponential Decay"

        if self.extendedName == 'XY_ExponentialDecayAndOffset':
            return self._name + " With XY Exponential Decay And Offset"

        if self.extendedName == 'XY_LinearGrowth':
            return self._name + " With XY Linear Growth"

        if self.extendedName == 'XY_LinearGrowthAndOffset':
            return self._name + " With XY Linear Growth And Offset"

        if self.extendedName == 'XY_ExponentialGrowth':
            return self._name + " With XY Exponential Growth"

        if self.extendedName == 'XY_ExponentialGrowthAndOffset':
            return self._name + " With XY Exponential Growth And Offset"


    def get_HTML( self ):

        index = self._HTML.rfind( '= ' ) # the index of the rightmost '=' sign plus a space

        if self.extendedName == '':
            return self._HTML

        if self.extendedName == 'Offset':
            return self._HTML + " + " + self.additionalDesignatorList[0]

        if self.extendedName == 'Reciprocal':
            return self._HTML[:index] + "= 1.0 / (" + self._HTML[index + 1:] + ")"

        if self.extendedName == 'ReciprocalWithOffset':
            return self._HTML[:index] + "= 1.0 / (" + self._HTML[index + 1:] + ") + " + self.additionalDesignatorList[0]

        if self.extendedName == 'InverseX':
            return self._HTML[:index] + "= x / (" + self._HTML[index + 1:] + ")"

        if self.extendedName == 'InverseXWithOffset':
            return self._HTML[:index] + "= x / (" + self._HTML[index + 1:] + ") + " + self.additionalDesignatorList[0]

        if self.extendedName == 'X_LinearDecay':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * x)"

        if self.extendedName == 'X_LinearDecayAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * x) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'X_ExponentialDecay':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * exp(x))"

        if self.extendedName == 'X_ExponentialDecayAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * exp(x)) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'X_LinearGrowth':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * x)"

        if self.extendedName == 'X_LinearGrowthAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * x) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'X_ExponentialGrowth':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * exp(x))"

        if self.extendedName == 'X_ExponentialGrowthAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * exp(x)) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'InverseXY':
            return self._HTML[:index] + "= xy / (" + self._HTML[index + 1:] + ")"

        if self.extendedName == 'InverseXYWithOffset':
            return self._HTML[:index] + "= xy / (" + self._HTML[index + 1:] + ") + " + self.additionalDesignatorList[0]
            
        if self.extendedName == 'XY_LinearDecay':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * x * y)"

        if self.extendedName == 'XY_LinearDecayAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * x * y) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'XY_ExponentialDecay':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * exp(x*y))"

        if self.extendedName == 'XY_ExponentialDecayAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") / (" + self.additionalDesignatorList[0] + " * exp(x*y)) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'XY_LinearGrowth':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * x * y)"

        if self.extendedName == 'XY_LinearGrowthAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * x * y) + " + self.additionalDesignatorList[1]

        if self.extendedName == 'XY_ExponentialGrowth':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * exp(x*y))"

        if self.extendedName == 'XY_ExponentialGrowthAndOffset':
            return self._HTML[:index] + "= (" + self._HTML[index + 1:] + ") * (" + self.additionalDesignatorList[0] + " * exp(x*y)) + " + self.additionalDesignatorList[1]


    # properties associated with get_X() accessor above
    name = property( get_name )
    HTML = property( get_HTML )

    def CreateExtendedCacheGenerationListIfNeeded( self ):
        
        if self.extendedName == '':
            return

        if self.extendedName == 'Offset':
            return

        if self.extendedName == 'Reciprocal':
            return

        if self.extendedName == 'ReciprocalWithOffset':
            return

        if self.extendedName == 'InverseX':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_X( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'InverseXWithOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_X( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'InverseXY':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_XY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'InverseXYWithOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_XY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_LinearDecay':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_X( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_LinearDecay':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_XY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_LinearDecayAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_X( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_LinearDecayAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_XY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_ExponentialDecay':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpX( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_ExponentialDecay':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpXY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_ExponentialDecayAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpX( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_ExponentialDecayAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpXY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_LinearGrowth':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_X( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_LinearGrowth':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_XY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_LinearGrowthAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_X( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_LinearGrowthAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_XY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_ExponentialGrowth':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpX( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_ExponentialGrowth':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpXY( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'X_ExponentialGrowthAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpX( NameOrValueFlag=1 ), []] )
            return

        if self.extendedName == 'XY_ExponentialGrowthAndOffset':
            self.CacheGenerationList.append( [ExtraCodeForEquationBaseClasses.CG_ExpXY( NameOrValueFlag=1 ), []] )
            return


    def SetAdditionalCoefficients( self, inNumberOfAdditionalCoefficients ):

        clist = list( self.coefficientDesignatorTuple )

        if inNumberOfAdditionalCoefficients == 1:
            if - 1 != self.extendedName.find( 'Offset' ):
                self.additionalDesignatorList.append( 'Offset' )
                clist.append( 'Offset' )
            else:
                self.additionalDesignatorList.append( self.GetAdditionalDesignator( self.numberOfCoefficientsForNonExtendedVersion ) )
                clist.append( self.GetAdditionalDesignator( self.numberOfCoefficientsForNonExtendedVersion ) )
        
        if inNumberOfAdditionalCoefficients == 2:
            self.additionalDesignatorList.append( self.GetAdditionalDesignator( self.numberOfCoefficientsForNonExtendedVersion ) )
            clist.append( self.GetAdditionalDesignator( self.numberOfCoefficientsForNonExtendedVersion ) )
            if - 1 != self.extendedName.find( 'Offset' ):
                self.additionalDesignatorList.append( 'Offset' )
                clist.append( 'Offset' )
            else:
                self.additionalDesignatorList.append( self.GetAdditionalDesignator( self.numberOfCoefficientsForNonExtendedVersion + 1 ) )
                clist.append( self.GetAdditionalDesignator( self.numberOfCoefficientsForNonExtendedVersion + 1 ) )
            
        self.coefficientDesignatorTuple = tuple( clist )



class Equation2D( Equation ):
    dimensionality = 2
    exampleData = """
   X        Y
 5.357    0.376
 5.457    0.489
 5.797    0.874
 5.936    1.049
 6.161    1.327
 6.697    2.054
 6.731    2.077
 6.775    2.138
 8.442    4.744
 9.769    7.068
 9.861    7.104
 """



class Equation3D( Equation2D ):
    dimensionality = 3
    exampleData = """
   X      Y       Z
 3.017  2.175   0.320
 2.822  2.624   0.629
 2.632  2.839   0.950
 2.287  3.030   1.574
 2.207  3.057   1.725
 2.048  3.098   2.035
 1.963  3.115   2.204
 1.784  3.144   2.570
 1.712  3.153   2.721
 2.972  2.106   0.313
 2.719  2.542   0.643
 2.495  2.721   0.956
 2.070  2.878   1.597
 1.969  2.899   1.758
 1.768  2.929   2.088
 1.677  2.939   2.240
 1.479  2.957   2.583
 1.387  2.963   2.744
 2.843  1.984   0.315
 2.485  2.320   0.639
 2.163  2.444   0.954
 1.687  2.525   1.459
 1.408  2.547   1.775
 1.279  2.554   1.927
 1.016  2.564   2.243
 0.742  2.568   2.581
 0.607  2.571   2.753
 """
 
