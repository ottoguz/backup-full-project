#

import subprocess
import time
from sys import platform


def select_os():
    if platform == 'linux' or 'linux2':
        return 'linux'
    elif platform == 'win32':
        return 'windows'
    #elif platform == 'darwin':
        #return 'OS X'


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
                 FULL BACKUP FROM THE FILE SERVER BEGAN AT {}s
  ===========================================================================
    '''.format(start_time)
    return start


def footer(st_day, st_time, path_log, bkp_name):
    today = time.strftime('%d-%m-%y')
    end_time = time.strftime('%H:%M:%S')
    bkp_name = bkp_name.replace('tar cvf', '')
    final = '''
    ===========================================================================
                            ENDED FULL BACKUP
                STARTING TIME:    {}  -  {}
                ENDING TIME  :    {}  -  {}
                LOG FILE     :    {}
                BKP FILE     :    {}
    ===========================================================================
    '''.format(st_day, st_time, today, end_time, path_log, bkp_name)
    return final


def unmount_disk(disk):
    try:
        umount = 'umount {} /mnt'.format(disk)
        subprocess.call(umount, shell=True)
        return True
    except OSError:
        return False


def generate_log_linux():
    date = time.strftime('%d-%m-%y')
    file_log = '{}-backup-full.txt'.format(date)
    path_log = '/var/log/backup/backup-full/{}'.format(file_log)
    return path_log


def generate_log_windows():
    #date = time.strftime('%y-%m-%d')
    time_bkp = time.strftime('%H:%M:%S')
    file_log = '{}-backup-full.zip'.format(time_bkp)
    path_log = 'E:\\backup\\backup_full_logs {}'.format(file_log)
    return path_log


def log_file_windows(bkp_start_time, file_list, final):
    file = 'backupfull_log_{}.txt' .format(time.strftime('%d-%m-%y'))
    f = open(file, 'w')
    f.write(bkp_start_time)
    f.write(file_list)
    f.write(final)
    f.close()
    return file


def gen_list_windows():
    files = 'cd /d C:\\Users\\55359\\Desktop\\Software_Engineering\\Python 3\\LPA && dir /s /b'
    files_out = subprocess.getoutput(files)
    return files_out


def gen_backup_linux():
    date = time.strftime('%d-%m-%y')
    bkp_file_name = '{}_backup-full.tar.gz'.format(date)
    bkp_destination = '/mnt/backup/{}'.format(bkp_file_name)
    source_path = '/home/gustavo/Documents/Pycharm/LPA'
    backup = 'tar cvf {} {}'.format(bkp_destination, source_path)
    return backup


def gen_backup_windows():
    date = time.strftime('%d-%m-%y')
    backup_file_name = '{}-backupfull.zip'.format(date)
    #backup_destination = 'E:\\backup\\backup_full'
    backup_source = 'C:\\Users\\55359\\Desktop\\Software_Engineering\\Python 3\\LPA'
    backup = 'cd /d F:\\backup && tar -cf {} "{}" '.format(backup_file_name, backup_source)
    return backup


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
    final = footer(start_day, bkp_start_time, path_log, backup[8:20] + backup[20:47])

    r = open(path_log, 'r')
    content = r.readlines()
    content.append(final)
    r = open(path_log, 'w')
    r.writelines(content)
    r.close()
    for i in range(len(content)):
        print(content[i], end="")

    unmount_disk(disk)


def full_backup_windows():
    bkp_start_time = time.strftime('%H:%M:%S')
    start_time = header(bkp_start_time)
    print(start_time)

    backup = gen_backup_windows()
    path_log = generate_log_windows()
    file_list = gen_list_windows()
    print(file_list)

    subprocess.call(backup, shell=True)

    start_day = time.strftime('%d-%m-%y')
    final = footer(start_day, bkp_start_time, path_log, backup[27:51])
    print(final)

    log_file_windows(start_time, file_list, final)

    log_to_folder = 'move C:\\Users\\55359\\Desktop\\Software_Engineering\\Atividade_extensionista_1\\backup-full-project-main\\backupfull_log_{}.txt E:\\backup\\backup_full_logs' .format(start_day)
    subprocess.call(log_to_folder, shell=True)


op_sys = select_os()
try:
    if op_sys == 'linux':
        full_backup_linux()
except OSError:
    full_backup_windows()
