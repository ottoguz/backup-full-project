from sys import platform


def select_os():
    if platform == 'linux' or 'linux2':
        return 'linux'
    elif platform == 'win32':
        return 'windows'


print(select_os())


