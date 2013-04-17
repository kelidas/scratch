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


group = raw_input('Type the name of study group: ')

f = urllib.urlopen('https://intranet.fce.vutbr.cz/pedagog/rozvrh/studSkupTisk.asp?skupina=%s' % group) 
html = f.read()
f.close()
names = re.findall('<TD><B>(\S+ \S+)</B>', html)
nicknames = re.findall('<TD align=\'left\'>(\w+)<TD>', html)

infile = open('%s.html' % group, 'w')
infile.write( start_html )
for name, nick in zip(names, nicknames):
    infile.write('<img src=http://www.fce.vutbr.cz/images/fotky/studenti/%s.jpg title=\'%s\'>' % (nick, name))
    infile.write('\n')

infile.write( end_html )
infile.close()

os.system('firefox %s.html' % group)
