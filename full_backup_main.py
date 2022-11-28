# FUNCTIONAL

# Libraries used to create the backup + log
import subprocess
import time
import platform

# Libraries used to create the function that sends the log through email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Library for the GUI
from tkinter import *
from tkinter import filedialog


# This function acknowledges which OS the program is running on
def select_os():
    os = platform.system()
    return os


source_dir = ""


def source_dir_func():
    global source_dir
    source_dir = filedialog.askdirectory()
    source_search_txt.config(text=source_dir)
    return source_dir


dest_dir = ""


def dest_dir_func():
    global dest_dir
    dest_dir = filedialog.askdirectory()
    destination_search_txt.config(text=dest_dir)
    return dest_dir


def put_message(e):
    message_label.config(text="Full backup is running, please wait...")


def remove_message():
    message_label.config(text="")


def email_window():
    def show_message(e):
        email_message.config(text="Email sent! Please check your inbox!")

    window = Tk()
    window.title("Terminal X - Full Backup - Send Email")
    window.geometry("400x300")
    window.configure(bg="#FFFFFF")

    email_label = Label(window,
                        text="Send backup log file via Email:",
                        bg="#FFFFFF", fg="#000000",
                        font="Arial 14 bold")
    email_label.place(x=54, y=30)

    from_email_label = Label(window,
                             text="From: ",
                             bg="#FFFFFF",
                             fg="#000000",
                             font="Arial 12 bold")
    from_email_label.place(x=20, y=80)

    from_email = Entry(window,
                       bg="#008AC1",
                       fg="#FFFFFF",
                       width=36,
                       font="Arial 11 bold")
    from_email.place(x=75, y=82)

    to_email_label = Label(window,
                           text="To: ",
                           bg="#FFFFFF",
                           fg="#000000",
                           font="Arial 12 bold")
    to_email_label.place(x=20, y=125)

    to_email = Entry(window,
                     bg="#008AC1",
                     fg="#FFFFFF", width
                     =36, font="Arial 11 bold")
    to_email.place(x=75, y=127)

    pass_email_label = Label(window,
                             text="Password: ",
                             bg="#FFFFFF",
                             fg="#000000",
                             font="Arial 12 bold")
    pass_email_label.place(x=20, y=170)

    pass_email = Entry(window,
                       bg="#008AC1",
                       fg="#FFFFFF",
                       width=20,
                       font="Arial 11 bold", show="*")
    pass_email.place(x=120, y=173)

    backup.generate_log()
    backup.subscribe_log(backup.header(), backup.gen_list(), backup.footer())

    send_button = Button(window,
                         command=lambda: backup.send_email(from_email.get(), to_email.get(), pass_email.get()),
                         text="SEND",
                         bg="#008AC1",
                         fg="#FFFFFF",
                         font="Arial 12 bold",
                         bd=1,
                         relief="solid")
    send_button.place(x=180, y=220)
    send_button.bind("<Button>", show_message)

    email_message = Label(window,
                          text="",
                          font="Arial 12 bold",
                          bg="#ffffff")
    email_message.place(x=55, y=262)
    remove_message()


root = Tk()
root.title("Terminal X - Full Backup")
root.geometry("800x600")
frame = PhotoImage(file="background.png")
frame_label = Label(root,
                    border=0,
                    bg='grey',
                    image=frame)
frame_label.place(x=0, y=0)

header_text = Label(root,
                    text=f'Full Backup started at: {time.strftime("%H:%M:%S")}',
                    font="Arial 12 bold",
                    bg="#ffffff")
header_text.place(x=210, y=100)

source_label = Label(root,
                     text=f'Select the backup source directory: ',
                     font="Arial 12 bold",
                     bg="#ffffff")
source_label.place(x=210, y=150)

source_button = Button(root,
                       command=lambda: source_dir_func(),
                       text="SELECT", bg="#008AC1",
                       fg="#FFFFFF",
                       font="Arial 8 bold",
                       bd=1,
                       relief="solid")
source_button.place(x=220, y=180)

source_search_txt = Label(root,
                          text=source_dir,
                          bg="#000000",
                          fg="#FFFFFF",
                          width=50,
                          font="Arial 10 bold")
source_search_txt.place(x=280, y=180)
os = select_os()
if os == "Linux":
    source_search_txt.place(x=300, y=183)

destination_label = Label(root,
                          text=f'Select the backup destination directory: ',
                          font="Arial 12 bold",
                          bg="#ffffff")
destination_label.place(x=210, y=220)

destination_button = Button(root,
                            command=lambda: dest_dir_func(),
                            text="SELECT",
                            bg="#008AC1",
                            fg="#FFFFFF",
                            font="Arial 8 bold",
                            bd=1,
                            relief="solid")
destination_button.place(x=220, y=250)

destination_search_txt = Label(root,
                               text=dest_dir,
                               bg="#000000",
                               fg="#FFFFFF",
                               width=50,
                               font="Arial 10 bold")
destination_search_txt.place(x=280, y=250)
if os == "Linux":
    destination_search_txt.place(x=300, y=253)

start_button = Button(root,
                      command=lambda: backup.gen_backup() and email_window(),
                      text="START",
                      bg="#008AC1",
                      fg="#FFFFFF",
                      font="Arial 12 bold",
                      bd=1,
                      relief="solid")
start_button.place(x=440, y=300)
start_button.bind("<Button>", put_message)

message_label = Label(root,
                      text="",
                      font="Arial 12 bold",
                      bg="#ffffff")
message_label.place(x=332, y=350)


class Backup:
    def __init__(self, time_now=time.strftime('%H:%M:%S'), date_now=time.strftime('%d-%m-%y')):
        self.__backup_destination = ''
        self.__backup_source = ''
        self.__time_now = time_now
        self.__date_now = date_now

    def get_time_now(self):
        return self.__time_now

    def get_date_now(self):
        return self.__date_now

    def open_move_file(self):
        if os == "Windows":
            open_file = "notepad " + file
            subprocess.run(open_file)
            cd = 'cd'
            current_folder = subprocess.getoutput(cd)
            log_to_folder = "move " + current_folder + '\\' + file + ' ' + self.__backup_destination
            subprocess.run(log_to_folder, shell=True)
            return file
        elif os == "Linux":
            open_file = "gedit " + file
            subprocess.run(open_file, shell=True)
            pwd = "pwd"
            current_folder = subprocess.getoutput(pwd)
            log_to_folder = "mv " + current_folder + "/" + file + " " + self.__backup_destination + "/" + file
            subprocess.run(log_to_folder, shell=True)
            return file

    # Header of the Full Backup display
    def header(self):
        time_now = Backup.get_time_now(self)
        header = '''
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
                    >>> CLOSE THE FILE TO SEND IT VIA EMAIL! <<<
        '''.format(time_now)
        return header

    def gen_backup(self):
        date_now = Backup.get_date_now(self)
        os = select_os()
        backup_file_name = 'full_backup_{}.tar.gz'.format(date_now)
        backup_source = source_dir
        self.__backup_source = backup_source
        backup_destination = dest_dir
        self.__backup_destination = backup_destination
        if os == "Linux":
            backup = 'cd ' + str(backup_destination) + ' && tar -cf {} "{}" '.format(backup_file_name, backup_source)
            subprocess.run(backup, shell=True)
            return backup
        elif os == "Windows":
            backup = 'cd /d ' + str(backup_destination) + ' && tar -cf {} "{}" '.format(backup_file_name, backup_source)
            subprocess.run(backup, shell=True)
            return backup

    def gen_list(self):
        os = select_os()
        if os == "Windows":
            files = "cd /d " + self.__backup_source + " && dir /s"
            files_out = subprocess.getoutput(files)
            return files_out
        elif os == "Linux":
            files = "cd " + self.__backup_source + " && ls"
            files_out = subprocess.getoutput(files)
            return files_out

    def generate_log(self):
        date_now = Backup().get_date_now()
        os = select_os()
        file_log = 'full_backup_log_{}.txt'.format(date_now)
        path_log = self.__backup_destination
        if os == "Linux":
            path_log = path_log + "/" + file_log
            return path_log
        elif os == "Windows":
            path_log = path_log + "\\" + file_log
            return path_log

    def footer(self):
        footer = '''
        ===========================================================================
                                     ENDED FULL BACKUP
                ENDING DATE/TIME  : {}  -  {}
                LOG FILE PATH     : {}
                BKP FILE PATH     : {}
        ===========================================================================
        '''.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M:%S'), self.__backup_destination,
                   self.__backup_destination)
        return footer

    def subscribe_log(self, header, file_list, footer):
        file = 'full_backup_log_{}.txt'.format(time.strftime('%d-%m-%y'))
        f = open(file, 'w')
        f.write(header)
        f.write(file_list)
        f.write(footer)
        f.close()

    def send_email(self, from_email, to_email, pass_email):
        os = select_os()
        global file
        try:
            fromaddr = from_email
            toaddr = to_email
            password = pass_email

            msg = MIMEMultipart()

            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = 'Full backup logs to Xterm'

            body = '\n Please find attached the backup logs'

            msg.attach(MIMEText(body, 'plain'))

            file = 'full_backup_log_{}.txt'.format(time.strftime('%d-%m-%y'))
            attachment = open(file, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment.read()))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= {}'.format(file))

            msg.attach(part)

            attachment.close()

            server = smtplib.SMTP('smtp.hostinger.com.br', 587)
            server.starttls()
            server.login(fromaddr, password)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

            self.open_move_file()

        except:

            self.open_move_file()


backup = Backup()

root.mainloop()
