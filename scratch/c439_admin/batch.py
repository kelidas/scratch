
import os
import sys
import subprocess


PC_LIST = [101, 102, 103, 104, 105, 106, 40, 108, 109, 110, 111, 112, 113, 114,
           115, 116, 117, 118, 119, 121, 122, 123, 124, 125, 126]
# PC_LIST = [40]
for i in PC_LIST:
    print '#' * 10, i, '#' * 30
    # IPCONFIG
    # os.system('ssh Teacher@147.229.29.%i ipconfig' % i)

    # LIST DIR
    # os.system('ssh Teacher@147.229.29.%i dir /cygdrive/d/StudentsData/' % i)

    # REBOOT
    # os.system('ssh Teacher@147.229.29.%i reboot -r now' % i)

    # SHUTDOWN
    # subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'shutdown -s'])

    # REMOTE DESKTOP
    # rdesktop -u Teacher -p 2bD318xM -g 95% -PKD 147.229.29.101 -r clipboard:PRIMARYCLIPBOARD
    # subprocess.call(['rdesktop', '-uTeacher', '-p2bD318xM', '-g90%', '-PKD', '-rclipboard:PRIMARYCLIPBOARD', '147.229.29.%i' % i])

    # UPLOAD DESKTOP WALLPAPER
    # os.system('scp gen_wallpaper/wallpaper.jpg Teacher@147.229.29.%i:/cygdrive/c/Windows/Web/Wallpaper/Windows/wallpaper.jpg' % i)

    # UPLOAD iTalc public key
#     if i != 101:
#         os.system('scp -r "iTALC" Teacher@147.229.29.%i:/cygdrive/c/ProgramData/' % i)

    # CLEAN DISK D ON STUDENT MACHINES
#     if i != 101:
#         subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'rm -r /cygdrive/d/*'])

    # Create Student directory on DISK D ON STUDENT MACHINES
#     if i != 101:
#         subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'mkdir /cygdrive/d/StudentsData'])

    # fix desktop icons (logout all computers)
    # subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'rm /cygdrive/c/Users/Student/AppData/Local/IconCache.db'])
    # subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'rm /cygdrive/c/Users/Teacher/AppData/Local/IconCache.db'])
    # subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'rm /cygdrive/c/Users/Remote/AppData/Local/IconCache.db'])



#     my_process = subprocess.Popen(['rdesktop', '-uTeacher', '-p2bD318xM', '-g90%',
#                                    '-PKD', '-r clipboard:PRIMARYCLIPBOARD',
#                                    '147.229.29.%i' % i])
#     my_process.wait()  # wait for process to end
#     if my_process.returncode != 0:
#         print "Something went wrong!"

if __name__ == '__main__':
    pass
