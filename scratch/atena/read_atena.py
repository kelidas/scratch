import numpy as np
import re

sourceEncoding = "cp1250"
targetEncoding = "utf-8"

def _locate_line(file_object, info_pattern):
    '''
    Reads lines from file_object until it reaches a line which matches the RegEx pattern
    given in 'info_pattern'. Used to position file cursor to the correct place for 
    reading in arbitraty order.
    '''
    info_matcher = re.compile(info_pattern)
    info_line = ' '
    while not info_matcher.search(info_line) and info_line != '':
        info_line = file_object.readline()
    return info_line

def _extract_monitors(atena_file):
    # extract monitor data to separate files
    infile = open(atena_file, 'r')
    monitor_num = 0
    while 1:
        line = _locate_line(infile, r'Specifikace monitoru')
        if not line:
            monitor_num -= 1
            break
        outfile = open('monitor_%02i.txt' % monitor_num, 'w')
        while 1:
            if line.split() != []:
                outfile.write(unicode(line, sourceEncoding).encode(targetEncoding))
                line = infile.readline()
            else:
                monitor_num += 1
                break
        outfile.close()
    infile.close()
    return monitor_num

def _list_to_array(inlist):
    res_lengths = [len(item) for item in inlist]
    res_y = np.max(res_lengths)
    res_x = len(res_lengths)
    out_arr = np.array([])
    out_arr.resize((res_y, res_x))
    for idx, item in enumerate(inlist):
        out_arr[:len(item), idx] = item
    return out_arr

# monitor_num = _extract_monitors('atena_out.txt')
# atena_excel = []
# for i in range(monitor_num + 1):
#    steps, vals = np.loadtxt('monitor_%02i.txt' % i, skiprows=10).T
#    if i == 0:
#        atena_excel.append(steps)
#        atena_excel.append(vals)
#    else:
#        atena_excel.append(vals)


atena_excel = []
for file_i in range(3):
    # specielne pro dany pripad (steps, mon1, mon2, mon3) -> (steps,mon2,mon1,mon3)
    monitor_num = _extract_monitors('atena_out_%i.txt' % (file_i + 1))
    for i in [1, 0, 2]:
        steps, vals = np.loadtxt('monitor_%02i.txt' % i, skiprows=10).T
        if i == 1:
            atena_excel.append(steps)
            atena_excel.append(vals)
            atena_excel.append(np.array([0]))
        elif i == 0:
            atena_excel.append(vals)
        else:
            atena_excel.append(vals)
            atena_excel.append(np.array([0]))

excel_arr = _list_to_array(atena_excel)


# np.savetxt('excel_data.txt', excel_arr)

outfile = open('excel_data.txt', 'w')
for row in excel_arr:
    temp = 0
    for item in row:
        if temp == 0:
            outfile.write('%i;' % item)
            temp += 1
        elif temp == 1:
            outfile.write('%.4e;' % item)
            temp += 1
        elif temp == 2:
            outfile.write(';')
            temp += 1
        elif temp == 3:
            outfile.write('%.4e;' % item)
            temp += 1
        elif temp == 4:
            outfile.write('%.4e;' % item)
            temp += 1
        elif temp == 5:
            outfile.write(';')
            temp = 0
    outfile.write('\n')
outfile.close()

# zlepseni
outfile = open('excel_data.txt', 'r')
data = outfile.read()
outfile.close()
infile = open('excel_data.txt', 'w')
data = data.replace(';0;', ';;')
data = data.replace(';0.0000e+00;', ';;')
data = data.replace(';%.4e;' % 0, ';;')
infile.write(data)
infile.close()


print 'END!'
