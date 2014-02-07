import Image, ImageDraw, ImageFont
from os import chdir, path

def txt2img(text,x=10,y=10,bg="#ffffff",fg="#000000",font="Verdana.ttf",FontSize=14):
    font_dir = "/usr/share/fonts/truetype/msttcorefonts/"
    img_name = "Win7 LtBlue 1920x1200_new.jpg"
    font_size = FontSize
    fnt = ImageFont.truetype(font_dir+font, font_size)
    lineWidth = 20
    img = Image.open("Win7 LtBlue 1920x1200.jpg")
    #imgbg = Image.new('RGBA', img.size, "#000000") # make an entirely black image
    #mask = Image.new('L',img.size,"#000000")       # make a mask that masks out all
    draw = ImageDraw.Draw(img)                     # setup to draw on the main image
    #drawmask = ImageDraw.Draw(mask)                # setup to draw on the mask
    #drawmask.line((0, lineWidth/2, img.size[0],lineWidth/2),
    #              fill="#999999", width=10)        # draw a line on the mask to allow some bg through
    #img.paste(imgbg, mask=mask)                    # put the (somewhat) transparent bg on the main
    draw.text((x,y), text, font=fnt, fill=bg)      # add some text to the main
    del draw 
    img.save(img_name,"JPEG",quality=100)  

#txt2img('Ahoj')



font_dir = "/usr/share/fonts/truetype/msttcorefonts/"
font_size = 30
font = "Verdana.ttf"
bg="#ffffff"
fg="#000000"
fnt = ImageFont.truetype(font_dir+font, font_size)
lineWidth = 20

for i in range(8):
    img = Image.open("Win7 LtBlue 1920x1200.jpg")
    #imgbg = Image.new('RGBA', img.size, "#000000") # make an entirely black image
    #mask = Image.new('L',img.size,"#000000")       # make a mask that masks out all
    draw = ImageDraw.Draw(img)                     # setup to draw on the main image
    #drawmask = ImageDraw.Draw(mask)                # setup to draw on the mask
    #drawmask.line((0, lineWidth/2, img.size[0],lineWidth/2),
    #              fill="#999999", width=10)        # draw a line on the mask to allow some bg through
    #img.paste(imgbg, mask=mask)                    # put the (somewhat) transparent bg on the main

    x = 100
    y = 100
    dy = 15
    draw.text((x,y), 'Save your data to disk D:', font=fnt, fill=bg)      # add some text to the main
    y = y+dy+font_size
    draw.text((x,y), 'All data on the Desktop will be deleted!', font=fnt, fill='#ff0000')
    y += dy+font_size+60
    draw.text((x,y), 'When leaving switch the computer', font=fnt, fill='#00ff00')
    y += dy+font_size
    draw.text((x,y), 'into Standby (Sleep) mode.', font=fnt, fill='#00ff00')

    x = 1000
    y = 100
    dy = 15
    draw.text((x,y), 'Remote Desktop Acces:', font=fnt, fill=bg)
    y += dy+font_size
    draw.text((x,y), 'address: stm-%i.stm.fce.vutbr.cz'%(i+1), font=fnt, fill=bg)
    y += (dy+font_size)
    draw.text((x,y), 'login: student%i'%(i+1), font=fnt, fill=bg)
    y += (dy+font_size)
    draw.text((x,y), 'access from home: http://wifigw.cis.vutbr.cz#vpn', font=fnt, fill=bg)
    y += (dy+font_size) + 45
    draw.text((x,y), 'Wake on lan:', font=fnt, fill=bg)
    y += (dy+font_size)
    draw.text((x,y), 'http://ws_cheetah.stm.fce.vutbr.cz/wakeonlan/', font=fnt, fill=bg)
    y += (dy+font_size) + 45
    draw.text((x,y), u'Standby (Sleep) mode, reboot: Ctrl+Alt+End', font=fnt, fill=bg)

    del draw 
    
    img_name = "Win7 LtBlue 1920x1200_new_%i.jpg"%(i+1)
    img.save(img_name,"JPEG",quality=100)  
    del img