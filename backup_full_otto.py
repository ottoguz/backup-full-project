"""
This program (Full Backup) makes a full backup of contents from a specific folder and sends it to a destined backup
folder. It also creates a log file in order to keep track of backup occurrences displaying the date/time and files
backed up.
"""

import subprocess
import time
from sys import platform


# This function acknowledges which OS the program is running on
def select_os():
    if platform == 'linux' or 'linux2':
        return 'linux'
    elif platform == 'win32':
        return 'windows'
    # elif platform == 'darwin':
    # return 'OS X'


# Header of the Full Backup display
def header(start_time):
    start = '''
  ===========================================================================
||    ______ _    _ _      _       ____          _____ _  ___    _ _____     ||
||   |  ____| |  | | |    | |     |  _ \   /\   / ____| |/ / |  | |  __ \    ||
||   | |__  | |  | | |    | |     | |_)   /  \ | |    | ' /| |  | | |__) |   ||
||   |  __| | |  | | |    | |     |  _ < / /\ \| |    |  < | |  | |  ___/    ||
||   | |    | |__| | |____| |____ | |_) / ____ \ |____| . \| |__| | |        ||
||   |_|     \____/|______|______||____/_/    \_\_____|_|\_ \____/|_|        ||
||                                                                           ||
||                    FULL BACKUP FROM THE FILE SERVER                       ||
||                                                                           ||
  ===========================================================================
  ===========================================================================
                 FULL BACKUP FROM THE FILE SERVER BEGAN AT {}
  ===========================================================================
    '''.format(start_time)
    return start


# Footer of the Full Backup display
def footer(st_day, st_time, path_log, bkp_name):
    today = time.strftime('%d-%m-%y')
    end_time = time.strftime('%H:%M:%S')
    bkp_name = bkp_name.replace('tar cvf', '')
    final = '''
    ===========================================================================
                            ENDED FULL BACKUP
                STARTING DATE/TIME: {}  -  {}
                ENDING DATE/TIME  : {}  -  {}
                LOG FILE PATH     : {}
                BKP FILE PATH     : {}
    ===========================================================================
    '''.format(st_day, st_time, today, end_time, path_log, bkp_name)
    return final


# When running the program on linux OS this function is summoned to unmount the disk containing the backup
def unmount_disk_linux(disk):
    try:
        umount = 'umount {} /mnt'.format(disk)
        subprocess.call(umount, shell=True)
        return True
    except OSError:
        return False


# When running the program on windows OS this function is summoned to mount the disk to receive the backup
def mount_disk_windows():
    mount = 'mountvol F: \\\\?\\Volume{2ba99565-d610-11eb-8376-806e6f6e6963}\\'
    subprocess.call(mount, shell=True)


# When running the program on windows OS this function is summoned to unmount the disk to receive the backup
def unmount_disk_windows():
    unmount = 'mountvol F: /p'
    subprocess.call(unmount, shell=True)


# creates the log file (.txt) and its path for linux
def generate_log_linux():
    date = time.strftime('%d-%m-%y')
    file_log = '{}-backup-full.txt'.format(date)
    path_log = '/var/log/backup/backup-full/{}'.format(file_log)
    return path_log


# creates the log file (.txt) and its path for windows
def generate_log_windows():
    date = time.strftime('%d-%m-%y')
    # time_bkp = time.strftime('%H:%M:%S')
    file_log = '{}-backup-full.txt'.format(date)
    path_log = 'E:\\backup\\backup_full_logs\\{}'.format(file_log)
    return path_log


# subscribes the header(bkp_start_time), list of backed up files, and footer(final) on the log file for windows
def log_file_windows(bkp_start_time, file_list, final):
    file = 'backupfull_log_{}.txt'.format(time.strftime('%d-%m-%y'))
    f = open(file, 'w')
    f.write(bkp_start_time)
    f.write(file_list)
    f.write(final)
    f.close()
    return file


# generates a list with the files to be backed up on windows
def gen_list_windows():
    files = 'cd /d C:\\Users\\55359\\Desktop\\Software_Engineering\\Python 3\\LPA && dir /s /b'
    files_out = subprocess.getoutput(files)
    return files_out


# Creates the backup file, compacts it and sends it to the destination on linux
def gen_backup_linux():
    date = time.strftime('%d-%m-%y')
    bkp_file_name = '{}_backup-full.tar.gz'.format(date)
    bkp_destination = '/mnt/backup/{}'.format(bkp_file_name)
    source_path = '/home/gustavo/Documents/Pycharm/LPA'
    backup = 'tar cvf {} {}'.format(bkp_destination, source_path)
    return backup


# Creates the backup file, compacts it and sends it to the destination on windows
def gen_backup_windows():
    date = time.strftime('%d-%m-%y')
    backup_file_name = '{}-backupfull.zip'.format(date)
    # backup_destination = 'E:\\backup\\backup_full'
    backup_source = 'C:\\Users\\55359\\Desktop\\Software_Engineering\\Python 3\\LPA'
    backup = 'cd /d F:\\backup\\ && tar -cf {} "{}" '.format(backup_file_name, backup_source)
    return backup


# Main function for linux
def full_backup_linux():
    disk = '/dev/sdb1'
    bkp_start_time = time.strftime('%H:%M:%S')
    start_time = header(bkp_start_time)
    # print(start_time)

    backup = gen_backup_linux()

    path_log = generate_log_linux()
    log = '>> {}'.format(path_log)

    x = open(path_log, 'w')
    x.write(start_time)
    x.close()

    mount = 'mount ' + disk + ' /mnt'
    subprocess.call(mount, shell=True)

    subprocess.call(backup + log, shell=True)

    start_day = time.strftime('%d-%m-%y')
    final = footer(start_day, bkp_start_time, path_log, backup[20:47])

    r = open(path_log, 'r')
    content = r.readlines()
    content.append(final)
    r = open(path_log, 'w')
    r.writelines(content)
    r.close()
    for i in range(len(content)):
        print(content[i], end="")

    unmount_disk_linux(disk)


# Main function for windows
def full_backup_windows():
    mount_disk_windows()

    bkp_start_time = time.strftime('%H:%M:%S')
    start_time = header(bkp_start_time)
    print(start_time)

    backup = gen_backup_windows()
    path_log = generate_log_windows()
    file_list = gen_list_windows()
    print(file_list)

    subprocess.call(backup, shell=True)

    start_day = time.strftime('%d-%m-%y')
    final = footer(start_day, bkp_start_time, path_log, backup[6:16] + backup[27:51].lstrip())
    print(final)

    log_file_windows(start_time, file_list, final)

    log_to_folder = 'move C:\\Users\\55359\\Desktop\\Software_Engineering\\Atividade_extensionista_1\\backup-full' \
                    '-project-main\\backupfull_log_{}.txt E:\\backup\\backup_full_logs'.format(start_day)
    subprocess.call(log_to_folder, shell=True)

    unmount_disk_windows()


# Here the function select_os() is summoned to acknowledge the OS on which the program is running
op_sys = select_os()
try:
    if op_sys == 'linux':
        full_backup_linux()
except OSError:
    full_backup_windows()
