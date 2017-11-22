import urllib
import requests
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
import datetime

base_url = 'https://nakup.itesco.cz/groceries/cs-CZ/search?query='
search = {'pampers3': 'pampers+midi+dry',
          'pampers4': 'pampers+maxi+dry',
          'hami_kase': 'hami+mlecna+kase'}
directory = 'data'

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
    print(name, p_last, p, p_last > p)

    fig, ax = plt.subplots(figsize=(6, 2), tight_layout=True)
    ax.plot(time_new, p_new)
    ax.set_title(srch)
    ax.set_ylabel('price')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    fig.savefig(fname + '.png')

    body += '<h3>old={}, new={}, {}</h3>'.format(p_last, p, p_last > p)
    body += '<img src={}.png><br>'.format(name)

with open(os.path.join(directory, 'prices.html'), 'w') as f:
    f.write(html.format(body))
