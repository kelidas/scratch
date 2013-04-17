# -*- coding: cp1250 -*-
######################################
#Author: Václav Sadílek
#E-mail: vaclav.sadilek@klikni.cz
######################################
from Tkinter import *
from ScrolledText import *
from string import *
import Image, ImageEnhance

def vyberSouboruu():  
    #print u"tak jsem uvnitř funkce a právě tisknu tuto větu :-)"
    import tkFileDialog  
    nazev=tkFileDialog.askopenfilenames(filetypes=(('image files', '*.jpg *.png *.gif'), ('all files', '*.*')))
    #print nazev
    vstup.delete(0, END)
    vstup.insert(0, nazev)  
    #print "Obsah vstupniho pole: ", vstup.get()

def vyberSouboru():  
    #print u"tak jsem uvnitř funkce a právě tisknu tuto větu :-)"
    import tkFileDialog  
    nazev_logo=tkFileDialog.askopenfilename(filetypes=(('image files', '*.png *.gif'), ('all files', '*.*')))
    #print nazev_logo
    vstup_logo.delete(0, END)
    vstup_logo.insert(0, nazev_logo)  
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
            elif letter == ' ' and nazev[num-1] == '}':
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
            elif letter == ' ' and nazev[num-1] == '}':
                continue
        num += 1 
        
    return soubor

def spoj():
    soubor = nazvySouboru()
    for i in range(0,len(soubor)):
        infile = Image.open(soubor[i],'r')
        rawExif = infile.info['exif']
        h1 = infile.size[0]
        v1 = infile.size[1]
        pom = float(v1)/float(h1)
        print 'Obrázek má poměr stran ' and pom
        new = Image.new( "RGB", (h1-432,v1),'white')
        new.paste(infile,(0-216,0))
        new.save(soubor[i][:len(soubor[i])-4]+'_res.jpg','JPEG', exif = rawExif)
    print 'Vse OK'

hlavni=Tk()
hlavni.title(u"Kelidas watermarker")

stitek=Label(hlavni, text=u"Vyber soubory pro vložení watermarku:")

vstup=Entry(hlavni)

prochazej=Button(hlavni, text='...', command=vyberSouboruu)  
prochazej_logo=Button(hlavni, text='...', command=vyberSouboru)

stitek.grid(row=0, sticky=W)
vstup.grid(row=0,column=1)
prochazej.grid(row=0,column=2)

tlOK=Button(hlavni, text='OK',command=spoj)   #numberLetters
tlOK.grid(row=1,column=1, sticky=W+E)
tlEXIT=Button(hlavni, text='EXIT',command=hlavni.destroy)
tlEXIT.grid(row=1, column=2,sticky = W+E)


hlavni.mainloop()  #  spustíme/zobrazíme celý program
