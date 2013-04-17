# -*- coding: cp1250 -*-
######################################
#Author: Václav Sadílek
#E-mail: vaclav.sadilek@klikni.cz
######################################
from Tkinter import *
from ScrolledText import *
from string import *
import Image, ImageEnhance
#from types import UnicodeType


# tady bude náš celý program  
def vyberSouboruu():
    #print u"tak jsem uvnitř funkce infilea právě tisknu tuto větu :-)"
    import tkFileDialog
    nazev = tkFileDialog.askopenfilenames( filetypes = ( ( 'image files', '*.jpg *.png *.gif' ), ( 'all files', '*.*' ) ) )
    #print nazev
    vstup.delete( 0, END )
    vstup.insert( 0, nazev )
    #print "Obsah vstupniho pole: ", vstup.get()

def vyberSouboru():
    #print u"tak jsem uvnitř funkce a právě tisknu tuto větu :-)"
    import tkFileDialog
    nazev_logo = tkFileDialog.askopenfilename( filetypes = ( ( 'image files', '*.png *.gif' ), ( 'all files', '*.*' ) ) )
    #print nazev_logo
    vstup_logo.delete( 0, END )
    vstup_logo.insert( 0, nazev_logo )
    #print "Obsah vstupniho pole: ", vstup.get()


def nazvySouboru():
    nazev = vstup.get()
    #print nazev
    #podokno=Toplevel(hlavni)  # Toplevel je udelátko nového podokna
    #textout = ScrolledText(podokno)
    #textout.pack()
    #textout.tag_config("hlavicka", foreground="blue", underline=0, font="Arial 15 bold")
    #textout.insert(END, nazev, 'hlavicka')
    #podokno.mainloop()
    pocet = 1
    predletter = ''
    num = 0
    if nazev[0] != '{':
        switch = 1
    for letter in nazev:
        if letter == '{':
            switch = 0;
            continue
        elif letter == '}':
            switch = 1
            continue
        elif switch == 1:
            if letter == ' ':
                pocet += 1
            elif letter == ' ' and nazev[num - 1] == '}':
                continue
    num += 1

    i = 0
    soubor = pocet * [""]
    #print soubor

    if nazev[0] != '{':
        switch = 1
    for letter in nazev:
        if letter == '{':
            switch = 0;
            continue
        elif switch == 0:
            if letter == '}':
                switch = 1
                continue
            if letter != '}':
                soubor[i] = soubor[i] + letter
        elif switch == 1:
            if letter == ' ':
                i += 1
            elif letter != ' ':
                soubor[i] = soubor[i] + letter
            elif letter == ' ' and nazev[num - 1] == '}':
                continue
        num += 1

    return soubor

def vynechRadky( n ):
    n = 10  #pocet vynechanych radku
    for i in range( 0, n - 1 ):
        infile.readline()

def nactiData():
    pocet = len( nazvySouboru() )
    text = pocet * ['']
    soubor = pocet * [""]
    soubor = nazvySouboru()
    mnoz = 0
    for i in range( 0, pocet ):
        infile = open( soubor[i], 'r' )
        for j in infile.readlines():
            mnoz += 1
        infile.close()
    seznam = [''] * ( mnoz )
    mnoz = 0
    for i in range( 0, pocet ):
        infile = open( soubor[i], 'r' )
        for j in infile.readlines():
            seznam[mnoz] = j.split()
            mnoz += 1
        infile.close()
    #print mnoz 
    #print seznam     
    for i in range( 0, mnoz - 1 ):
        for j in range( 0, len( seznam[i] ) ):
            print seznam[i][j], '\t',
        print '\n',


def reduce_opacity( im, opacity ):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert( 'RGBA' )
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness( alpha ).enhance( opacity )
    im.putalpha( alpha )
    return im

def watermark( im, mark, position, opacity = 1 ):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity( mark, opacity )
    if im.mode != 'RGBA':
        im = im.convert( 'RGBA' )
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new( 'RGBA', im.size, ( 0, 0, 0, 0 ) )
    if position == 'tile':
        w = int( mark.size[0] / float( vstup_ratio.get() ) )
        h = int( mark.size[1] / float( vstup_ratio.get() ) )
        mark = mark.resize( ( w, h ) )
        xx = int( vstup_x.get() )
        yy = int( vstup_y.get() )
        for y in range( 0, im.size[1], mark.size[1] + yy ):
            for x in range( 0, im.size[0], mark.size[0] + xx ):
                layer.paste( mark, ( x, y ) )
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min( 
            float( im.size[0] ) / mark.size[0], float( im.size[1] ) / mark.size[1] )
        w = int( mark.size[0] * ratio / float( vstup_ratio.get() ) )
        h = int( mark.size[1] * ratio / float( vstup_ratio.get() ) )
        mark = mark.resize( ( w, h ) )
        layer.paste( mark, ( ( im.size[0] - w ) / 2, ( im.size[1] - h ) / 2 ) )
    #elif position == 'bottom_right':
        #ww, hw = mark.size
        #wi, hi = im.size
        #print ww, hw, wi, hi
        #mark = mark.resize((w, h))
        #layer.paste(mark, (wi-ww, hi-hw))
    elif position == 'bottom_right_zoom':
        ww, hw = mark.size
        wi, hi = im.size
        #print ww, hw, wi, hi
        h = int( hi / float( vstup_ratio.get() ) )
        w = int( ww * h / hw )
        x = int( vstup_x.get() )
        y = int( vstup_y.get() )
        #print x,y
        mark = mark.resize( ( w, h ) )
        layer.paste( mark, ( wi - w + x, hi - h + y ) )
    else:
        layer.paste( mark, position )
    # composite the watermark with the layer
    return Image.composite( layer, im, layer )

def test():
    pocet = len( nazvySouboru() )
    soubor = pocet * [""]
    soubor = nazvySouboru()
    mark = Image.open( vstup_logo.get() )
    #print mark.size
    for i in range( 0, pocet ):
        im = Image.open( soubor[i] )
       #print im.size
        if c.var.get() == 1:
            watermark( im, mark, prom_position.get(), float( vstup_transparency.get() ) ).show()
            watermark( im, mark, prom_position.get(), float( vstup_transparency.get() ) ).save( soubor[i][:len( soubor[i] ) - 4] + "_water" + soubor[i][len( soubor[i] ) - 4:] )
        else:
            watermark( im, mark, prom_position.get(), float( vstup_transparency.get() ) ).save( soubor[i][:len( soubor[i] ) - 4] + "_water" + soubor[i][len( soubor[i] ) - 4:] )
        #watermark(im, mark, (10, 10), .5).show()
        #watermark(im, mark, (10, 10), .5).save(soubor[i][:len(soubor[i])-4]+"_water"+soubor[i][len(soubor[i])-4:])
    #watermark(im, mark, 'tile', 0.5).show()
    #watermark(im, mark, 'scale', 1.0).show()
    podokno = Toplevel( hlavni )  # Toplevel je udelátko nového podokna
    textout = Message( podokno, text = r"Hotovo!", width = 50 )
    textout.pack()
    tlacOK = Button( podokno, text = 'OK', command = podokno.destroy )   #numberLetters
    tlacOK.pack()
    podokno.mainloop()

#if __name__ == '__main__':
#    test()

def open_help():
    inputfile = open( 'help.txt', 'r' )
    helptext = Toplevel( hlavni )  # Toplevel je udelátko nového podokna
    helptext.title( u"Help" )
    texto = ScrolledText( helptext )
    texto.pack()
    texto.insert( END, unicode( inputfile.read(), 'cp1250' ) )
    helptext.mainloop()

hlavni = Tk()
hlavni.title( u"Kelidas watermarker" )


stitek = Label( hlavni, text = u"Vyber soubory pro vložení watermarku:" )
stitek_logo = Label( hlavni, text = u"Vyber soubor s obrazkem loga:" )
stitek_transparency = Label( hlavni, text = u"Zadej hodnotu průhlednosti 0-1:" )
stitek_position = Label( hlavni, text = u"Zadej pozici watermarku:" )
stitek_x = Label( hlavni, text = u"Posun ve smeru X:" )
stitek_y = Label( hlavni, text = u"Posun ve smeru Y:" )
stitek_ratio = Label( hlavni, text = u"Měřítko měnící velikost watermarku:" )

prom_position = StringVar( hlavni )  # tkinterovská proměnná
prom_position.set( u"tile" )      # počáteční hodnota

vstup = Entry( hlavni )
vstup_logo = Entry( hlavni )
vstup_transparency = Entry( hlavni )
vstup_transparency.insert( 0, "1" )
vstup_position = OptionMenu( hlavni, prom_position, u"tile", u"scale", u"bottom_right_zoom" )
#vstup_position.insert(0, 'bottom_right_zoom')
vstup_x = Entry( hlavni )
vstup_x.insert( 0, '0' )
vstup_y = Entry( hlavni )
vstup_y.insert( 0, '0' )
vstup_ratio = Entry( hlavni )
vstup_ratio.insert( 0, '1' )

prochazej = Button( hlavni, text = '...', command = vyberSouboruu )
prochazej_logo = Button( hlavni, text = '...', command = vyberSouboru )

stitek.grid( row = 0, sticky = W )
vstup.grid( row = 0, column = 1 )
prochazej.grid( row = 0, column = 2 )

stitek_logo.grid( row = 1, sticky = W )
vstup_logo.grid( row = 1, column = 1 )
prochazej_logo.grid( row = 1, column = 2 )

stitek_transparency.grid( row = 2, sticky = W )
vstup_transparency.grid( row = 2, column = 1 )

stitek_position.grid( row = 3, sticky = W )
vstup_position.grid( row = 3, column = 1, sticky = W + E )

stitek_x.grid( row = 4, sticky = W )
vstup_x.grid( row = 4, column = 1 )

stitek_y.grid( row = 5, sticky = W )
vstup_y.grid( row = 5, column = 1 )

stitek_ratio.grid( row = 6, sticky = W )
vstup_ratio.grid( row = 6, column = 1 )

v = IntVar()
c = Checkbutton( hlavni, text = "Zobrazit výsledek", variable = v )
c.var = v
#print c.var.get()
c.grid( row = 7, sticky = W )

tlHELP = Button( hlavni, text = 'HELP', command = open_help )
tlHELP.grid( row = 8, column = 0, sticky = W + E )
tlOK = Button( hlavni, text = 'OK', command = test )   #numberLetters
tlOK.grid( row = 8, column = 1, sticky = W + E )
tlEXIT = Button( hlavni, text = 'EXIT', command = hlavni.destroy )
tlEXIT.grid( row = 8, column = 2, sticky = W + E )


hlavni.mainloop()  #  spustíme/zobrazíme celý program












