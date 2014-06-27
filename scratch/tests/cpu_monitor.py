
try:
    import psutil
except:
    print 'You have to install <psutils>'

import time

process_list = psutil.get_process_list()
print '%-6s \t %-20s \t\t %-6s \t %-20s' % ('PID', 'Process name', 'PID', 'Process name')
for i in range(0, len(process_list), 2):
    print '%-6i \t %-20s' % (process_list[i].pid, process_list[i].name),
    try:
        print '\t\t %-6i \t %-20s' % (process_list[i + 1].pid, process_list[i + 1].name)
    except:
        continue

print '\n\n'
print 'This program monitor entered running process'
print 'and return start time, end time and running time.'
print 'The CPU-usage is averaged over test sequence and compared\n by test criterium.'

print 'ENTER THE FOLLOWING VALUES -- INTEGERS'
pid = int(raw_input('Enter the PROCESS number (PID) for monitoring: '))

def set_param():
    print 'Default values: 5, 2, 1, 60'
    try:
            n_test = int(raw_input('Enter the number of tests during sequence [-]: '))
    except:
            n_test = 5

    try:
            test_criterium = int(raw_input('Enter the average CPU-usage during sequence (this value will be imply that the process end) [-]: '))
    except:
            test_criterium = 2

    try:
            sequence_time = int(raw_input('Enter the time pause of testing sequence [s]: '))
    except:
            sequence_time = 1

    try:
            pause_interval = int(raw_input('Enter the time between testing sequence [s]: '))
    except:
            pause_interval = 60
    return n_test, test_criterium, sequence_time, pause_interval


if psutil.pid_exists(pid):
    n_test, test_criterium, sequence_time, pause_interval = set_param()
    p = psutil.Process(pid)
    print 'Process name is ', p.name
    start_time = time.time()
    print 'Monitoring start ', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    while 1:
        cpu_count = 0
        for i in range(0, n_test):
            cpu_count += p.get_cpu_percent()
            time.sleep(sequence_time)
        if cpu_count / float(n_test) < test_criterium:
            end_time = time.time()
            print 'Monitoring end ', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            break
        else:
            print '\t still running'
        time.sleep(pause_interval)
    print 'Process time = ', time.strftime("%H:%M:%S", time.gmtime(end_time - start_time - n_test * sequence_time))


else:
    print 'This process number doesn\'t exist'


exit_key = raw_input('Enter for exit: ')

