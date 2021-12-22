import subprocess
import time


def select_os():
    op_sys = str(input('Enter the OS(linux/windows):'))
    if op_sys == 'linux':
        return op_sys
    elif op_sys == 'windows':
        return op_sys


def start(start_time):
    start_banner = '''
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
    return start_banner


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


def generate_log_linux():
    date = time.strftime('%H:%M:%S')
    file_log = '{}-backup-full.txt.tar.gz'.format(date)
    path_log = '/var/log/backup/backup-full/{}'.format(file_log)
    return path_log


def generate_log_windows():
    date = time.strftime('%d-%m-%y')
    time_bkp = time.strftime('%H:%M:%S')
    file_log = '{} {}-backup-full.zip'.format(date, time_bkp)
    path_log = 'E:\\backup\\backup_full_logs {}'.format(file_log)
    return path_log


def gen_backup_linux():
    date = time.strftime('%d-%m-%y')
    bkp_file_name = '{}-backup-full.tar.gz'.format(date)
    bkp_destination = '/home/gustavo/backup/{}'.format(bkp_file_name)
    source_path = '/home/gustavo/bkp_test/'
    backup = 'tar cvf {} {}'.format(bkp_destination, source_path)
    return backup


def gen_backup_windows():
    date = time.strftime('%d-%m-%y')
    backup_file_name = '{}-backupfull.zip'.format(date)
    backup_destination = 'E:\\backup\\backup_full'
    backup_source = 'C:\\files'
    backup = 'cd /d E:\\backup\\backup_full && tar -cvf {} "{}" '.format(backup_file_name, backup_source)
    return backup


#def format_log_windows(log_path, file_name):


def backup_full_linux():
    disk = '/dev/sdb'
    start_time_bkp = time.strftime('%H:%M:%S')
    start_time = start(start_time_bkp)
    print(start_time)

    backup = gen_backup_linux()

    path_log = generate_log_linux()
    log = '>> {}'.format(path_log)

    l = open(path_log, 'w')
    l.write(start_time)
    l.close()

    mount = 'mount ' + disk + ' /backup'
    subprocess.call(mount, shell=True)

    subprocess.call(backup + log, shell=True)

    start_day = time.strftime('%d-%m-%y')
    final = finish(start_day, start_time_bkp, path_log, backup, )
    print(final)
    r = open(path_log, 'w')
    r.write(final)
    r.close()


def backup_full_windows():
    start_time_bkp = time.strftime('%H:%M:%S')
    start_time = start(start_time_bkp)
    print(start_time)

    backup = gen_backup_windows()

    path_log = generate_log_windows()
    log = 'cd /d E:\\backup\\backup_full_logs && echo {}>>backupfull_log.txt'.format(path_log)

    subprocess.call(log, shell=True)
    subprocess.call(backup, shell=True)



    start_day = time.strftime('%d-%m-%y')
    final = finish(start_day, start_time_bkp, path_log, backup[39:63])
    print(final)


op_sys = select_os()
if op_sys == 'linux':
    backup_full_linux()
else:
    backup_full_windows()
