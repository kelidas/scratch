#------------------------------------------------------------------------------#
#----- up-dated for "use_header" ----------------------------------------------#
#----- Uhersky Ostroh ---------------------------------------------------------#

from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES, ProgressDialog
from traitsui.api import View, Item, UItem, Group, HGroup, OKButton, CodeEditor, Tabbed, SetEditor
import numpy as np
import subprocess
import multiprocessing
import os
import shutil
import threading
import time
import datetime
import re
import sys
import zipfile
import shutil
from email.mime.multipart import MIMEMultipart
import smtplib
import base64
import socket


def send_email_smtp(sender, receiver, email):
    # Send the message via local SMTP server.
    s = smtplib.SMTP('ex07.fce.vutbr.cz', 587)
    # s.set_debuglevel( 1 )
    s.starttls()
    s.login('sadilek.v', 'passw')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, receiver, email)
    s.quit()

def generate_email(sender, receiver, subject):
    frame = MIMEMultipart(u'related')
    frame['From'] = sender
    frame['To'] = receiver
    frame['Subject'] = subject
    msg = MIMEMultipart(u'alternative')
    frame.attach(msg)
    return frame

def execute_pool(func, cpu_num, args_lst, kwds, send_msg=False):
    try:
        pool = multiprocessing.Pool(processes=cpu_num)
        for arg in args_lst:
            arg=[arg]
            pool.apply_async(func, args=arg, kwds=kwds)
        print 'pool apply complete'
    except (KeyboardInterrupt, SystemExit):
        print 'got ^C while pool mapping, terminating the pool'
        pool.terminate()
        print 'pool is terminated'
    except Exception, e:
        print 'got exception: %r, terminating the pool' % (e,)
        pool.terminate()
        print 'pool is terminated'
    finally:
        print 'joining pool processes'
        pool.close()
        pool.join()
        print 'join complete'
    if send_msg:
        email = generate_email('sadilek.v@fce.vutbr.cz',
                               'martina.som@seznam.cz',
                               'Pool finished, %s' % socket.gethostname())
        try:
            send_email_smtp('sadilek.v@fce.vutbr.cz',
                            'martina.som@seznam.cz',
                            email.as_string())
        except:
            print 'E-mail wasn\'t sent.'
    print 'the end'

def run_cmd(cmd, **kwds):
    print cmd, 'running ...'
    sys.stdout.flush()
    with open(os.devnull, "w") as fnull:
        # p = subprocess.Popen('konsole -e ls -la', stdout=fnull, shell=True)
        p = subprocess.Popen('start /WAIT ' + cmd, stdout=fnull, shell=True)
        p.communicate()
    print cmd, 'finished'
    sys.stdout.flush()

if __name__ == '__main__':
    CPU_NUM =  multiprocessing.cpu_count()-1
    cmd_lst = []
    ns = 100
    name = 'beamA'
    for i in range(0,ns):        
        cmd_lst.append(('ParticleModel.exe {} {}'.format(name,i)))
    arg_lst = cmd_lst
    #run_cmd(arg_lst[0])
    kwds = {}
    execute_pool(run_cmd, CPU_NUM, arg_lst, kwds, send_msg=False)
    print 'END!'
