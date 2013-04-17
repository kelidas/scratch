import os
import re
import sys
import urllib

start_html = '''
<html>
<head>
<meta charset="windows-1250" />
<title></title>
</head>
<body>
'''

end_html = '''
</body>
</html>
'''

def index():
    infile = open('/var/www/gen_photo/index.html', 'r')
    html = infile.read()
    infile.close()
    return html


def gen(req):
    group = req.form['group']
    f = urllib.urlopen('https://intranet.fce.vutbr.cz/pedagog/rozvrh/studSkupTisk.asp?skupina=%s' % group) 
    html = f.read()
    f.close()
    names = re.findall(r'<TD><B>(.*?)</B>', html)
    nicknames = re.findall(r'<TD align=\'left\'>(.*?)<TD>', html)

    text = '' 
    text += start_html
    for name, nick in zip(names, nicknames):
        text += '<img src=http://www.fce.vutbr.cz/images/fotky/studenti/%s.jpg title=\'%s\'>' % (nick, name)
        text += '\n'

    text += end_html

    return text
