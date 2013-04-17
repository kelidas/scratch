'''
Created on 20.10.2010

@author: Vasek
'''
#
# Simple example which uses a pool of workers to carry out some tasks.
#
# Notice that the results will probably not come out of the output
# queue in the same in the same order as the corresponding tasks were
# put on the input queue.  If it is important to get the results back
# in the original order then consider using `Pool.map()` or
# `Pool.imap()` (which will save on the amount of code needed anyway).
#
# Copyright (c) 2006-2008, R Oudkerk
# All rights reserved.
#

import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

#
# Function run by worker processes
#

def worker( input, output ):
    for func, args in iter( input.get, 'STOP' ):
        result = calculate( func, args )
        output.put( result )

#
# Function used to calculate result
#

def calculate( func, args ):
    result = func( *args )
    return '%s says that %s%s = %s' % \
        ( current_process().name, func.__name__, args, result )

#
# Functions referenced by tasks
#

def mul( a, b ):
    time.sleep( 0.5 * random.random() )
    return a * b

def plus( a, b ):
    time.sleep( 0.5 * random.random() )
    return a + b

#
#
#

def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [( mul, ( i, 7 ) ) for i in range( 20 )]
    TASKS2 = [( plus, ( i, 8 ) ) for i in range( 10 )]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        task_queue.put( task )

    # Start worker processes
    for i in range( NUMBER_OF_PROCESSES ):
        Process( target=worker, args=( task_queue, done_queue ) ).start()

    # Get and print results
    print 'Unordered results:'
    for i in range( len( TASKS1 ) ):
        print '\t', done_queue.get()

    # Add more tasks using `put()`
    for task in TASKS2:
        task_queue.put( task )

    # Get and print some more results
    for i in range( len( TASKS2 ) ):
        print '\t', done_queue.get()

    # Tell child processes to stop
    for i in range( NUMBER_OF_PROCESSES ):
        task_queue.put( 'STOP' )


if __name__ == '__main__':
    freeze_support()
    test()

#An example of how a pool of worker processes can each run a SimpleHTTPServer.HttpServer instance while sharing a single listening socket.

#
# Example where a pool of http servers share a single listening socket
#
# On Windows this module depends on the ability to pickle a socket
# object so that the worker processes can inherit a copy of the server
# object.  (We import `multiprocessing.reduction` to enable this pickling.)
#
# Not sure if we should synchronize access to `socket.accept()` method by
# using a process-shared lock -- does not seem to be necessary.
#
# Copyright (c) 2006-2008, R Oudkerk
# All rights reserved.
#

import os
import sys

from multiprocessing import Process, current_process, freeze_support
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

if sys.platform == 'win32':
    import multiprocessing.reduction    # make sockets pickable/inheritable


def note( format, *args ):
    sys.stderr.write( '[%s]\t%s\n' % ( current_process().name, format % args ) )


class RequestHandler( SimpleHTTPRequestHandler ):
    # we override log_message() to show which process is handling the request
    def log_message( self, format, *args ):
        note( format, *args )

def serve_forever( server ):
    note( 'starting server' )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def runpool( address, number_of_processes ):
    # create a single server object -- children will each inherit a copy
    server = HTTPServer( address, RequestHandler )

    # create child processes to act as workers
    for i in range( number_of_processes - 1 ):
        Process( target=serve_forever, args=( server, ) ).start()

    # main process also acts as a worker
    serve_forever( server )


def test():
    DIR = os.path.join( os.path.dirname( __file__ ), '..' )
    ADDRESS = ( 'localhost', 8000 )
    NUMBER_OF_PROCESSES = 4

    print 'Serving at http://%s:%d using %d worker processes' % \
          ( ADDRESS[0], ADDRESS[1], NUMBER_OF_PROCESSES )
    print 'To exit press Ctrl-' + ['C', 'Break'][sys.platform == 'win32']

    os.chdir( DIR )
    runpool( ADDRESS, NUMBER_OF_PROCESSES )


if __name__ == '__main__':
    freeze_support()
    test()

