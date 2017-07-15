from lxml import etree
from PIL import Image

with open('main.html','r',encoding="utf-8") as f:
    html = f.read()
root = etree.HTML(html)
imgs = root.xpath('//img[@class="math"]')

s0 = 25
s = 18

for img in imgs:
    iname = img.get('src')
    im = Image.open(iname)
    dx, dy = im.size
    print(dx,dy)
    img.attrib['height'] = '{:.1f}pt'.format(dy/s0 * s)
    img.attrib['width'] = '{:.1f}pt'.format(dx/s0 * s)
    
imgs = root.xpath('//img[@class="math-display"]')
for img in imgs:
    iname = img.get('src')
    im = Image.open(iname)
    dx, dy = im.size
    img.attrib['height'] = '{:.1f}pt'.format(dy/s0 * s)
    img.attrib['width'] = '{:.1f}pt'.format(dx/s0 * s)
    
    
with open('main_fix.html', 'w', encoding='utf8') as f:
    f.write(etree.tostring(root).decode('utf8'))
