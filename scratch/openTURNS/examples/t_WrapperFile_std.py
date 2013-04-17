#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :

  # Read the wrapper file named 'poutre'
  wrapper = WrapperFile.FindWrapperByName( "poutre" )

  # Show where the wrapper was found
  #print wrapper.getDescriptionFilePath()

  # Get the content of the wrapper file
  data       = WrapperData(wrapper.getWrapperData())
  filelist   = data.getFileList()
  varlist    = data.getVariableList()
  parameters = data.getParameters()

  # Show the content
  # replace dll suffix on windows
  libraryPath = data.getLibraryPath().replace("-0.dll", ".so")
  print "library path =", libraryPath
  print "function =", data.getFunctionDescription()
  print "gradient =", data.getGradientDescription()
  print "hessian  =", data.getHessianDescription()
  print "Files:"
  for f in filelist:
      print "file ->", f
  print "Variables:"
  for v in varlist:
      print "variable ->", v
  print "parameters =", parameters

  # Add an (useless) new variable to the description
  V = WrapperDataVariable()
  V.id_      = "V"
  V.comment_ = "Useless variable"
  V.unit_    = "None"
  V.regexp_  = "V=.*"
  V.format_  = "V=%10.5g"
  V.type_    = 0 # 0: in, 1:out
  varlist.add( V )
  print "New variables:"
  for v in varlist:
      print "variable ->", v
  data.setVariableList( varlist )
  
  # Add an (useless) new file to the description
  F = WrapperDataFile()
  F.id_    = "Fich"
  F.name_  = "Useless file"
#  F.path_  = "c:/uselessFile"
  F.path_  = "/tmp/uselessFile"
  F.type_  = 1 # 0:in, 1:out
  F.subst_ = "V"
  filelist.add( F )
  print "New files:"
  for f in filelist:
      print "file ->", f
  data.setFileList( filelist )

  # Update the wrapper description with the new data and
  # write it out to disk
  if (data.isValid()):
      wrapper.setWrapperData( data )
      print "data =", data.__str__().replace("-0.dll", ".so")
      wrapper.writeFile( "wrp.xml" )
  
  deviation = NumericalMathFunction( wrapper )
  outPoint = deviation( (210.e9, 1000, 1.5, 2.e-6, 77777) )
  print "deviation =", outPoint

except :
  import sys
  print "t_NumericalMathFunction_exec.py", sys.exc_type, sys.exc_value
