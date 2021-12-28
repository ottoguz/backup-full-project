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


def start(start_time):
    start = '''
  ===========================================================================
||   ____          _____ _  ___    _ _____    ______ _    _ _      _         ||
||  |  _ \   /\   / ____| |/ / |  | |  __ \  |  ____| |  | | |    | |        ||
||  | |_) | /  \ | |    | ' /| |  | | |__) | | |__  | |  | | |    | |        ||
||  |  _ < / /\ \| |    |  < | |  | |  ___/  |  __| | |  | | |    | |        ||
||  | |_) / ____ \ |____| . \| |__| | |      | |    | |__| | |____| |____    ||
||  |____/_/    \_\_____|_|\_ \____/|_|      |_|     \____/|______|______|   ||
||                                                                           ||
||                    FULL BACKUP FROM THE FILE SERVER                       ||
||                                                                           ||
  ===========================================================================
  ===========================================================================
                 FULL BACKUP FROM THE FILE SERVER BEGAN AT {}s
  ===========================================================================
    '''.format(start_time)
    return start


def finish(st_day, st_time, path_log, bkp_name):
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
    date = time.strftime('%H:%M:%S')
    file_log = '{}-backup-full.txt.tar.gz'.format(date)
    path_log = '/var/log/backup/backup-full/{}'.format(file_log)
    return path_log


def generate_log_windows():
    #date = time.strftime('%y-%m-%d')
    time_bkp = time.strftime('%H:r%M:%S')
    file_log = '{}-backup-full.zip'.format(time_bkp)
    path_log = 'E:\\backup\\backup_full_logs {}'.format(file_log)
    return path_log


def gen_backup_linux():
    date = time.strftime('%y-%m-%d')
    bkp_file_name = '{}-backup-full.tar.gz'.format(date)
    bkp_destination = '/mnt/backup/{}'.format(bkp_file_name)
    source_path = '/home/gustavo/Documents/Pycharm/LPA'
    backup = 'tar cvf {} {}'.format(bkp_destination, source_path)
    return backup


def gen_backup_windows():
    date = time.strftime('%d-%m-%y')
    backup_file_name = '{}-backupfull.zip'.format(date)
    #backup_destination = 'E:\\backup\\backup_full'
    backup_source = 'C:\\files'
    backup = 'cd /d F:\\backup && tar -cvf {} "{}" '.format(backup_file_name, backup_source)
    return backup


def backup_full_linux():
    disk = '/dev/sdb1'
    bkp_start_time = time.strftime('%H:%M:%S')
    start_time = start(bkp_start_time)
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
    final = finish(start_day, bkp_start_time, path_log, backup)

    r = open(path_log, 'r')
    content = r.readlines()
    content.append(final)
    r = open(path_log, 'w')
    r.writelines(content)
    r.close()
    for i in range(len(content)):
        print(content[i], end="")

    unmount_disk(disk)


def backup_full_windows():
    bkp_start_time = time.strftime('%H:%M:%S')
    start_time = start(bkp_start_time)
    print(start_time)

    backup = gen_backup_windows()

    path_log = generate_log_windows()
    log = 'cd /d E:\\backup\\backup_full_logs && echo {}>>backupfull_log.txt'.format(path_log)

    '''
    x = open(path_log, 'w')
    x.write(start_time)
    x.close()
    '''
    subprocess.call(log, shell=True)
    subprocess.call(backup, shell=True)

    start_day = time.strftime('%d-%m-%y')
    final = finish(start_day, bkp_start_time, path_log, backup[28:51])
    print(final)
    '''
    r = open(path_log, 'r')
    content = r.readlines()
    content.append(final)
    r = open(path_log, 'w')
    r.writelines(content)
    r.close()
    for i in range(len(content)):
        print(content[i], end="")
    '''


op_sys = select_os()
try:
    if op_sys == 'linux':
        backup_full_linux()
except OSError:
    backup_full_windows()
