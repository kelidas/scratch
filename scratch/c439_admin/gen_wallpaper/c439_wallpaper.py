# coding: utf-8
import Image, ImageDraw, ImageFont
from os import chdir, path


import textwrap

def text_block(text, width, x, y, fill):
    lines = textwrap.wrap(text, width=width)
    print lines
    y_text = y
    for line in lines:
        width, height = fnt.getsize(line)
        draw.text(((x + width) / 2, y_text), line, font=fnt, fill=fill)
        y_text += height





font_dir = "/usr/share/fonts/truetype/msttcorefonts/"
font_size = 30
font = "Arial.ttf"
bg = "#ffffff"
fg = "#000000"
fnt = ImageFont.truetype(font_dir + font, font_size)
lineWidth = 20


img = Image.open('Win7 LtBlue 1600x1200.jpg')
# imgbg = Image.new('RGBA', img.size, "#000000") # make an entirely black image
# mask = Image.new('L',img.size,"#000000")       # make a mask that masks out all
draw = ImageDraw.Draw(img)  # setup to draw on the main image
# drawmask = ImageDraw.Draw(mask)                # setup to draw on the mask
# drawmask.line((0, lineWidth/2, img.size[0],lineWidth/2),
#              fill="#999999", width=10)        # draw a line on the mask to allow some bg through
# img.paste(imgbg, mask=mask)                    # put the (somewhat) transparent bg on the main

x = 350
y = 100
dy = 15
draw.text((x, y),
          ur'- Data ukládejte do složky D:\StudentsData\<jméno v informačním systému FAST>',
          font=fnt, fill=bg)  # add some text to the main
y = y + dy + font_size
draw.text((x, y),
          ur'    - např. D:\StudentsData\novakj21\ ',
          font=fnt, fill=bg)  # add some text to the main
y = y + dy + font_size
draw.text((x, y),
          ur'    - data mimo tuto složku mohou být odstraněna',
          font=fnt, fill=bg)  # add some text to the main
y = y + dy + font_size + 60

draw.text((x, y),
          ur'- Plocha se při odhlášení / vypnutí počítače automaticky maže!',
          font=fnt, fill='#ff0000')
draw.text((x + 1, y + 1),
          ur'- Plocha se při odhlášení / vypnutí počítače automaticky maže!',
          font=fnt, fill='#ff0000')
y += dy + font_size
draw.text((x, y),
          ur'- Svá data si zálohujte, disk D může být kdykoliv smazán a data nejsou zálohována.',
          font=fnt, fill='#00ff00')
y += dy + font_size
draw.text((x, y),
          ur'    - (konec semestru, porucha počítače/systému)',
          font=fnt, fill='#00ff00')

y += dy + font_size + 60
draw.text((x, y),
          ur'- O případných problémech s počítačem informujte vyučujícího.',
          font=fnt, fill=bg)



del draw

img_name = "wallpaper.jpg"
img.save(img_name, "JPEG", quality=100)
del img
