
import os
import sys
import subprocess


PC_LIST = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
           115, 116, 117, 118, 119, 121, 122, 123, 124, 125, 126]

for i in PC_LIST:
    print '#' * 10, i, '#' * 30
    # IPCONFIG
    # os.system('ssh Teacher@147.229.29.%i ipconfig' % i)

    # RESTART
    # os.system('ssh Teacher@147.229.29.%i restart -r now' % i)

    # SHUTDOWN
    # os.system('ssh Teacher@147.229.29.%i shutdown -s now' % i)

    # REMOTE DESKTOP
    # subprocess.call(['rdesktop', '-uTeacher', '-p2bD318xM', '-g90%', '-PKD', '-rclipboard:PRIMARYCLIPBOARD', '147.229.29.%i' % i])

    # UPLOAD DESKTOP WALLPAPER
    # os.system('scp gen_wallpaper/wallpaper.jpg Teacher@147.229.29.%i:/cygdrive/c/Windows/Web/Wallpaper/Windows/wallpaper.jpg' % i)

    # CLEAN DISK D ON STUDENT MACHINES
#     if i != 101:
#         subprocess.call(['ssh', 'Teacher@147.229.29.%i' % i, 'rm -r /cygdrive/d/*'])



#     my_process = subprocess.Popen(['rdesktop', '-uTeacher', '-p2bD318xM', '-g90%',
#                                    '-PKD', '-r clipboard:PRIMARYCLIPBOARD',
#                                    '147.229.29.%i' % i])
#     my_process.wait()  # wait for process to end
#     if my_process.returncode != 0:
#         print "Something went wrong!"

if __name__ == '__main__':
    pass
