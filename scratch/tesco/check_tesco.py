import urllib
import requests
import os
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from collections import OrderedDict
import datetime

base_url = 'https://nakup.itesco.cz/groceries/cs-CZ/search?query='
search = {'pampers2': 'pampers+mini+dry',
          'pampers2premium': 'pampers+mini+premium',
          'pampers3': 'pampers+midi+dry',
          'pampers3premium': 'pampers+midi+premium',
          'pampers4': 'pampers+maxi+dry',
          'pampers4premium': 'pampers+maxi+premium',
          'hami_kase': 'hami+mlecna+kase'}
directory = os.path.join(os.path.dirname(__file__), 'data')

html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title></title>
</head>
<body>
{}
</body>
</html>
'''

def get_price(search):
    #response = urllib.request.urlopen(base_url + search)
    response = requests.get(base_url + search)

    html = response.text
    p = re.findall('unitPrice&quot;,(\d*.[\d]*)', html)
    p = [float(i.replace(chr(44), '.')) for i in p]
    return np.min(p)


body = ''
for name, srch in search.items():
    p = get_price(srch)
    p_old = np.array([])
    time = np.array([])
    p_last = 0
    fname = os.path.join(directory, name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(fname + '.npy'):
        p_old = np.load(fname + '.npy')
        time = np.load(fname + '_time.npy')
        p_last = p_old[-1]
    p_new = p_old.tolist() + [p]
    time_new = time.tolist() + [datetime.datetime.now()]
    np.save(fname + '.npy', p_new)
    np.save(fname + '_time.npy', time_new)
    #print(name, p_last, p, p_last > p)

    fig, ax = plt.subplots(figsize=(6, 2), tight_layout=True)
    ax.plot(time_new, p_new)
    ax.set_title(srch)
    ax.set_ylabel('price')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    fig.savefig(fname + '.png')

    body += '<h3>min={}, new={}, {}</h3>'.format(min(p_new), p)
    body += '<img src={}.png><br>'.format(name)

with open(os.path.join(directory, 'prices.html'), 'w') as f:
    f.write(html.format(body))
