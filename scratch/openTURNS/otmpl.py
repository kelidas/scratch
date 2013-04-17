#! /usr/bin/env python
#
#  @file  otmpl.py
#  @brief Script to plot OpenTURNS graphs
#
#  (C) Copyright 2005-2012 EDF-EADS-Phimeca
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This program is distributed in the hope that it will be useful
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#

"""
=============================
 openturns-matplotlib
=============================
  
 A module that implements OpenTURNS graph viewing using matplotlib
"""

import openturns as ot
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import re

class View:
    # filter the dictionary 'orig 'for valid keywords 'keys'
    @staticmethod
    def FilterDict(orig, keys):
        result = dict()
        for key in keys:
            if key in orig:
                result[key] = orig[key]
        return result
        
    # constructor    
    def __init__(self, graph, **kwargs):
        try:
            graph = ot.Graph(graph)
        except:
            print "-- The given object cannot be converted into an OpenTURNS Graph."
            return
            
        listDrawables = graph.getDrawables()
        size = len(listDrawables)
        if size == 0:
            print "-- Nothing to draw"
            return
            
        axesparams = View.FilterDict(kwargs, ('adjustable', 'agg_filter', 'alpha', 'anchor', 'animated', 'aspect', 'autoscale_on', 'autoscalex_on', 'autoscaley_on',  'axes','axes_locator', 'axis_bgcolor', 'axis_on', 'axis_off', 'axisbelow', 'clip_box', 'clip_on', 'clip_path', 'color_cycle', 'contains', 'cursor_props', 'figure', 'frame_on', 'gid', 'label', 'lod', 'navigate', 'navigate_mode', 'picker', 'position', 'rasterization_zorder', 'rasterized', 'snap', 'title', 'transform', 'style', 'url', 'visible', 'xbound', 'xlabel', 'xlim', 'xmargin', 'xscale', 'xtickslabels', 'xticks', 'ybound', 'ylabel', 'ylim', 'ymargin', 'yscale', 'ytickslabels', 'yticks', 'zorder'))

        # set title
        if not 'title' in axesparams:   
            axesparams['title'] = graph.getTitle()
            
        # set scale    
        if not 'xscale' in axesparams:   
            if (graph.getLogScale() == ot.GraphImplementation.LOGX) or (graph.getLogScale() == ot.GraphImplementation.LOGXY):
                axesparams['xscale'] = 'log'
        if not 'yscale' in axesparams:   
            if (graph.getLogScale() == ot.GraphImplementation.LOGY) or (graph.getLogScale() == ot.GraphImplementation.LOGXY):
                axesparams['yscale'] = 'log'
                
        # set bounding box
        if not 'xlim' in axesparams:   
            axesparams['xlim'] = [ graph.getBoundingBox()[0], graph.getBoundingBox()[1] ]
        if not 'ylim' in axesparams:   
            axesparams['ylim'] = [ graph.getBoundingBox()[2], graph.getBoundingBox()[3] ]
            
        self.fig = plt.figure()
        self.ax = [ self.fig.add_subplot(111, **axesparams) ]
        self.ax[0].grid()
                
        # set legend position
        if not 'legendposition' in kwargs:            
            try:
                legendPositionDict = {'bottomright':'lower right', 'bottom':'lower center', 'bottomleft':'lower left', 'left':'center left', 'topleft':'upper left', 'topright':'upper right', 'right':'center right', 'center':'center'}
                legendposition = legendPositionDict[ graph.getLegendPosition() ]
            except:
                print "-- Unknown legend position"           
            
        for i in range(size):
            drawable = listDrawables[i]
            drawableKind = re.search('(?<=implementation\=class\=)\w+', re.sub('implementation=\s?class', 'implementation=class', repr(drawable)[:70])).group(0)
            plotparams = View.FilterDict(kwargs, ('agg_filter', 'alpha', 'animated', 'antialiased', 'aa', 'axes', 'clip_box', 'clip_on', 'clip_path', 'color', 'c', 'contains', 'dash_capstyle', 'dash_joinstyle', 'dashes', 'data','drawstyle', 'figure', 'fillstyle', 'gid', 'label', 'linestyle', 'ls', 'linewidth', 'lw', 'lod', 'marker', 'markeredgecolor','mec', 'markeredgewidth', 'mew', 'markerfacecolor', 'mfc', 'markerfacecolor', 'mfcalt', 'markersize', 'markevery', 'picker', 'pickradius', 'rasterized', 'snap', 'solid_capstyle', 'solid_joinstyle', 'transform', 'url', 'visible','xdata', 'ydata', 'zorder'))
            
            # set color
            if (not 'color' in plotparams) and (not 'c' in plotparams):
                colorKind = drawable.getColor()
                plotparams['color'] = colorKind
                
            # set marker
            if not 'marker' in plotparams:
                try:
                    pointStyleDict = {'square':'s', 'circle':'o', 'triangleup':'2', 'plus':'+', 'times':'+', 'diamond':'+', 'triangledown':'v', 'star':'*', 'fsquare':'s', 'fcircle':'o', 'ftriangleup':'2', 'fdiamond':'D', 'bullet':'+', 'dot':'.'}
                    plotparams['marker'] = pointStyleDict[ drawable.getPointStyle() ]
                except:
                    print "-- Unknown marker"
                
            # set line style 
            if (not 'linestyle' in plotparams) and (not 'ls' in plotparams):
                try:
                    lineStyleDict = {'solid':'-', 'dashed':'--', 'dotted':':', 'dotdash':'-.', 'longdash':'--', 'twodash':'--'}   
                    plotparams['linestyle'] = lineStyleDict[ drawable.getLineStyle() ]
                except:
                    print "-- Unknown line style"
                
            # set line width
            if (not 'linewidth' in plotparams) and (not 'lw' in plotparams):
                plotparams['linewidth'] = drawable.getLineWidth()

            #fillstyle = drawable.getFillStyle()
            
            # retrieve data
            data = drawable.getData()
            x = data.getMarginal(0)
            if data.getDimension()>1:
                y = data.getMarginal(1)

            # add legend, title
            if drawableKind != 'Pie':
                self.ax[0].set_xlabel( graph.getXTitle() )
                self.ax[0].set_ylabel( graph.getYTitle() )

                if len(drawable.getLegendName()) == 0:
                    plotparams['label'] = '_nolegend_'
                else:
                    plotparams['label'] = drawable.getLegendName()
                

            if drawableKind == 'BarPlot':
                barparams = View.FilterDict(plotparams, ('agg_filter', 'alpha', 'animated', 'antialiased', 'aa', 'axes', 'clip_box', 'clip_on', 'clip_path', 'color', 'contains', 'edgecolor','ec','facecolor','fc', 'figure', 'fill', 'gid', 'hatch', 'label', 'linestyle', 'linewidth', 'lod', 'path_effects', 'picker', 'rasterized', 'snap', 'transform', 'url', 'zorder'))
                
                # linestyle for bar() is different than the one for plot()
                if 'linestyle' in barparams:
                    barparams.pop('linestyle')
                if (not 'linestyle' in plotparams) and (not 'ls' in plotparams):
                    lineStyleDict = {'solid':'solid', 'dashed':'dashed', 'dotted':'dotted', 'dotdash':'dashdot', 'longdash':'dashed', 'twodash':'dashed'}
                    if drawable.getLineStyle() in lineStyleDict:
                        barparams['linestyle'] = lineStyleDict[ drawable.getLineStyle() ]
                    else:
                        print "-- Unknown line style"
                    
                xi = drawable.getOrigin()
                for i in range(x.getSize()):
                    # label only the first bar to avoid getting several legend items
                    if (i == 1) and ('label' in barparams):
                        barparams.pop('label')
                    plt.bar( xi, height=y[i][0], width=x[i][0], **barparams )
                    xi += x[i][0]
                    
            elif drawableKind == 'Cloud':
                plotparams['linestyle']='None'
                self.ax[0].plot(x, y, **plotparams)                   
                
            elif drawableKind == 'Curve':
                if plotparams['linestyle'] == '-':
                    plotparams['marker'] = ''
                self.ax[0].plot( x, y, **plotparams ) 
                
            elif drawableKind == 'Pie':
                pieparams = View.FilterDict(kwargs, ('explode', 'colors', 'labels', 'autopct', 'pctdistance', 'labeldistance', 'shadow'))
                if not 'labels' in pieparams:
                    pieparams['labels'] = drawable.getLabels()
                if not 'colors' in pieparams:
                    pieparams['colors'] = drawable.getPalette()
                plt.gca().set_aspect('equal')
                plt.pie( x, **pieparams )
                
            elif drawableKind == 'Contour':
                X, Y = np.meshgrid( drawable.getX(), drawable.getY() )
                Z = np.reshape(drawable.getData(), (drawable.getX().getSize(), drawable.getY().getSize()) )
                contourparams = View.FilterDict(plotparams, ('colors', 'alpha', 'cmap', 'norm', 'levels', 'origin', 'extent', 'locator', 'extend', 'xunits', 'yunits', 'antialiased', 'linewidths', 'linestyles'))
                if not 'levels' in contourparams:
                    contourparams['levels'] = drawable.getLevels()
                contourset = plt.contour(X, Y, Z, **contourparams)
                
                labelsparams = View.FilterDict(plotparams, ('fontsize', 'colors', 'inline', 'inline_spacing', 'fmt', 'manual', 'rightside_up', 'use_clabeltext'))
                if not 'fontsize' in labelsparams:
                    labelsparams['fontsize'] = 8
                if not 'fmt' in labelsparams:
                    labelsparams['fmt'] = '%g'
                plt.clabel( contourset, **labelsparams )
                
            elif drawableKind == 'Staircase':
                if plotparams['linestyle'] == '-':
                    plotparams['marker']=''
                stepparams = plotparams
                if 'hold' in kwargs:
                    stepparams['hold'] = kwargs['hold']
                plt.step( x, y, **stepparams )

            elif drawableKind == 'Pairs':
                if 'title' in axesparams:
                    axesparams.pop('title')
                axesparams['xticks'] = []
                axesparams['yticks'] = []
                annotateparams = View.FilterDict(kwargs, ('agg_filter', 'alpha', 'animated', 'axes', 'backgroundcolor', 'bbox', 'clip_box', 'clip_on', 'clip_path', 'color', 'contains', 'family', 'fontfamily', 'fontname', 'name', 'figure', 'fontproperties', 'font_properties', 'gid', 'horizontalalignement', 'ha', 'label', 'linespacing', 'lod', 'multialignement', 'path_effects', 'picker', 'position', 'rasterized', 'rotation', 'rotation_mode', 'size', 'fontsize', 'snap', 'stretch', 'fontstretch', 'style', 'fontstyle', 'text', 'transform', 'url', 'variant', 'verticalalignment', 'va', 'visible', 'weight', 'fontweight', 'x', 'y', 'zorder'))
                annotateparams['color'] = 'black'
                plotparams['linestyle'] = 'None'

                self.ax[0].grid(False)
                dim = drawable.getData().getDimension()
                for i in range(dim):
                    for j in range(dim):
                      
                        self.ax.append( self.fig.add_subplot(dim, dim, 1+i*dim+j, **axesparams) ) 
                        if i != j:
                            x = drawable.getData().getMarginal(i)
                            y = drawable.getData().getMarginal(j)
                            plotparams['linestyle']='None'
                            self.ax[1+i*dim+j].plot(x, y, **plotparams)
                            #if i==0:
                                #self.ax[1+i*dim+j].xaxis.set_ticks_position('top')

                        else:
                            self.ax[1+i*dim+j].annotate('marginal'+' '+str(i+1),(-15,-4), **annotateparams)

        # Add legend
        if drawableKind != 'Pie':
            legendparams = View.FilterDict(kwargs, ('prop', 'numpoints', 'scatterpoints', 'scatteroffsets', 'markerscale', 'frameon', 'fancybox', 'shadow', 'ncol', 'mode', 'bbox_to_anchor', 'bbox_transform', 'title'))
            if not 'loc' in legendparams:
                legendparams['loc'] = legendposition
            if not 'shadow' in legendparams:
                legendparams['shadow'] = True
            if not 'fancybox' in legendparams:
                legendparams['fancybox'] = True   
            if not 'numpoints' in legendparams:
                legendparams['numpoints'] = 1   
            self.ax[0].legend( **legendparams )
                
    # Draw the graph on the screen
    def show(self):
        plt.show()

    # Save the current view to a file according to extension (default=png, pdf, eps, ...)
    def save(self, fname):
        self.fig.savefig(fname)
        

        
        
if __name__ == '__main__':
  
    # Curve
    graph = ot.Normal().drawCDF()
    #graph.draw('curve1')
    view = View(graph, color='blue')
    #view.save('normal.png')
    view.show()
    
    # Contour
    graph = ot.Normal([1,2],[3,5], ot.CorrelationMatrix(2)).drawPDF()
    #graph.draw('curve2')
    view = View(graph)
    view.show()
    
    # Histogram tests
    normal = ot.Normal(1)
    size = 100
    sample = normal.getNumericalSample(size)
    graph = ot.VisualTest.DrawHistogram(sample, 10)
    #graph.draw('curve3')
    view = View(graph)
    view.show()
    
    # QQPlot tests
    size = 100
    normal = ot.Normal(1)
    sample = normal.getNumericalSample(size)
    sample2 = ot.Gamma(3.0, 4.0, 0.0).getNumericalSample(size)
    graph = ot.VisualTest.DrawQQplot(sample, sample2, 100)
    #graph.draw('curve4')
    view = View(graph)
    view.show()
    
    # Clouds tests
    dimension = (2)
    R = ot.CorrelationMatrix(dimension)
    R[0, 1] = 0.8
    distribution = ot.Normal(ot.NumericalPoint(dimension, 3.0), ot.NumericalPoint(dimension, 2.0), R)
    size = 100
    sample2D = distribution.getNumericalSample(size)
    firstSample = ot.NumericalSample(size, 1)
    secondSample = ot.NumericalSample(size, 1)
    for i in range(size):
        firstSample[i] = ot.NumericalPoint(1, sample2D[i, 0])
        secondSample[i] = ot.NumericalPoint(1, sample2D[i, 1])
    graph = ot.VisualTest.DrawClouds(sample2D, ot.Normal(ot.NumericalPoint(dimension, 2.0), ot.NumericalPoint(dimension, 3.0), R).getNumericalSample(size / 2))
    #graph.draw('curve5')
    view = View(graph)
    view.show()
    
    # CobWeb tests
    size = 100
    inputDimension = 6
    inputSample = ot.Normal(inputDimension).getNumericalSample(size)
    inputVar = ot.Description(inputDimension)
    for i in range(inputDimension):
      inputVar[i] = "X" + str(i)
    formula = ot.Description(1)
    expression = ""
    for i in range(inputDimension):
      if i > 0:
        expression += "+"
      expression += "cos(" + str(i + 1) + "*" + inputVar[i] + ")"
    formula[0] = expression
    outputVar = ot.Description(1)
    outputVar[0] = "y"
    model = ot.NumericalMathFunction(inputVar, outputVar, formula)
    outputSample = model(inputSample)
    graph = ot.VisualTest.DrawCobWeb(inputSample, outputSample, 2.5, 3.0, "red", False)
    #graph.draw('curve6')
    view = View(graph)
    view.show()

    # Staircase
    distribution = ot.Poisson(10.0)
    graph = distribution.drawCDF()
    #graph.draw('curve7')
    view = View(graph)
    view.show()
    
    # Pie
    graph = ot.SensitivityAnalysis.DrawImportanceFactors([.4,.3,.2,.1],['a0', 'a1', 'a2', 'a3'],'Zou')
    #graph.draw('curve8')
    view = View(graph)
    view.show()
    
    # Pairs
    dim = 5
    meanPoint = ot.NumericalPoint(dim, 0.0)
    sigma = ot.NumericalPoint(dim, 5.0)
    R = ot.CorrelationMatrix(dim)
    distribution = ot.Normal(meanPoint, sigma, R)
    for i in range(1, dim):
        R[i, i - 1] = -0.25
    distribution2 = ot.Normal(meanPoint, sigma, R)
    size = 1000
    sample = distribution.getNumericalSample( size )
    graph = ot.Graph("Pairs", " ", " ", True, "topright")
    myPairs = ot.Pairs(sample, "Pairs example", sample.getDescription(), "green", "bullet")
    graph.add(ot.Drawable(myPairs))
    #graph.draw("Graph_Pairs_OT")
    view = View(graph)
    view.show()
    
    