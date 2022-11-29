# Bibliotecas utilizadas para criar o backup e arquivo de log
import subprocess
import time
import platform

# Bibliotécas e módulos utilizados para criar a função enviar o log por Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Módulos utilizados para criar a interface gráfica
from tkinter import *
from tkinter import filedialog


# Função criada para reconhecer o Sistema operacional
def select_os():
    os = platform.system()
    return os


source_dir = ""


# Função para atualizar o caminho para o diretório de origem do backup(GUI)
def source_dir_func():
    global source_dir
    source_dir = filedialog.askdirectory()
    source_search_txt.config(text=source_dir)
    return source_dir


dest_dir = ""


# Função para atualizar o caminho para o diretório de destino do backup(GUI)
def dest_dir_func():
    global dest_dir
    dest_dir = filedialog.askdirectory()
    destination_search_txt.config(text=dest_dir)
    return dest_dir


# Função para mostrar a mensagem de aguarde enquanto faz o backup
def put_message(e):
    message_label.config(text="Full backup is running, please wait...")


# Função para remover a mensagem de aguarde após o término do backup
def remove_message():
    message_label.config(text="")


# Função para chamar a tela de envio de email
def email_window():
    # Função para mostrar a mensagem de envio do email
    def show_message(e):
        email_message.config(text="Email sent! Please check your inbox!")

    # Configurações da tela de email
    window = Tk()
    window.title("Terminal X - Full Backup - Send Email")
    window.geometry("400x300")
    window.configure(bg="#FFFFFF")

    # Cabeçalho da tela
    email_label = Label(window,
                        text="Send backup log file via Email:",
                        bg="#FFFFFF", fg="#000000",
                        font="Arial 14 bold")
    email_label.place(x=54, y=30)

    # Indicação de rementente do email
    from_email_label = Label(window,
                             text="From: ",
                             bg="#FFFFFF",
                             fg="#000000",
                             font="Arial 12 bold")
    from_email_label.place(x=20, y=80)

    # Entrada do endereço de email do remetente
    from_email = Entry(window,
                       bg="#008AC1",
                       fg="#FFFFFF",
                       width=36,
                       font="Arial 11 bold")
    from_email.place(x=75, y=82)

    # Indicação de email do destinatário
    to_email_label = Label(window,
                           text="To: ",
                           bg="#FFFFFF",
                           fg="#000000",
                           font="Arial 12 bold")
    to_email_label.place(x=20, y=125)

    # Entrada do endereço de email do destinatário
    to_email = Entry(window,
                     bg="#008AC1",
                     fg="#FFFFFF", width
                     =36, font="Arial 11 bold")
    to_email.place(x=75, y=127)

    # Indicação da senha do email do rementente
    pass_email_label = Label(window,
                             text="Password: ",
                             bg="#FFFFFF",
                             fg="#000000",
                             font="Arial 12 bold")
    pass_email_label.place(x=20, y=170)

    # Entrada da senha de email do remetente
    pass_email = Entry(window,
                       bg="#008AC1",
                       fg="#FFFFFF",
                       width=20,
                       font="Arial 11 bold", show="*")
    pass_email.place(x=120, y=173)

    # Chamada das funções que criam o log e atualiza os dados do log
    backup.generate_log()
    backup.subscribe_log(backup.header(), backup.gen_list(), backup.footer())

    # Botão de enviar (Chama o método que envia email da classe backup)
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

    # Espaço para a mensagem de email enviado
    email_message = Label(window,
                          text="",
                          font="Arial 12 bold",
                          bg="#ffffff")
    email_message.place(x=55, y=262)

    # Remove a mensagem de aguarde do termino do backup na tela principal
    remove_message()


# Tela principal(GUI)
root = Tk()

# Configurações da tela
root.title("Terminal X - Full Backup")
root.geometry("800x600")

# Plano de fundo da tela principal
frame = PhotoImage(file="background.png")

# Contorno da tela principal
frame_label = Label(root,
                    border=0,
                    bg='grey',
                    image=frame)
frame_label.place(x=0, y=0)

# Horário de início do backup na tela principal
header_text = Label(root,
                    text=f'Full Backup started at: {time.strftime("%H:%M:%S")}',
                    font="Arial 12 bold",
                    bg="#ffffff")
header_text.place(x=210, y=100)

# Label da entrada do diretório de origem do backup
source_label = Label(root,
                     text=f'Select the backup source directory: ',
                     font="Arial 12 bold",
                     bg="#ffffff")
source_label.place(x=210, y=150)

# Botão para abrir o explorer e buscar o caminho do diretório de origem do backup
source_button = Button(root,
                       command=lambda: source_dir_func(),
                       text="SELECT", bg="#008AC1",
                       fg="#FFFFFF",
                       font="Arial 8 bold",
                       bd=1,
                       relief="solid")
source_button.place(x=220, y=180)

# Espaço para subscrever o caminho do diretório de origem do backup
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

# Label da entrada do diretório de destino do backup
destination_label = Label(root,
                          text=f'Select the backup destination directory: ',
                          font="Arial 12 bold",
                          bg="#ffffff")
destination_label.place(x=210, y=220)

# Botão para abrir o explorer e buscar o caminho do diretório de destino do backup
destination_button = Button(root,
                            command=lambda: dest_dir_func(),
                            text="SELECT",
                            bg="#008AC1",
                            fg="#FFFFFF",
                            font="Arial 8 bold",
                            bd=1,
                            relief="solid")
destination_button.place(x=220, y=250)

# Espaço para subscrever o caminho do diretório de origem do backup
destination_search_txt = Label(root,
                               text=dest_dir,
                               bg="#000000",
                               fg="#FFFFFF",
                               width=50,
                               font="Arial 10 bold")
destination_search_txt.place(x=280, y=250)
if os == "Linux":
    destination_search_txt.place(x=300, y=253)

# Botão para iniciar o backup (Chama o método que realiza o backup na classe backup e a função com a tela de email)
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

# Espaço para a presentar a mensagem de backup em andamento para o usuario aguardar
message_label = Label(root,
                      text="",
                      font="Arial 12 bold",
                      bg="#ffffff")
message_label.place(x=332, y=350)


# Classe backup
class Backup:
    # Atributos da classe backup
    def __init__(self, time_now=time.strftime('%H:%M:%S'), date_now=time.strftime('%d-%m-%y')):
        self.__backup_destination = ''
        self.__backup_source = ''
        self.__time_now = time_now
        self.__date_now = date_now

    # Retorno do horário atual
    def get_time_now(self):
        return self.__time_now

    # Retorno da data atual
    def get_date_now(self):
        return self.__date_now

    # Método para mover o arquivo de log para a pasta de destino junto ao backup compactado
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

    # Método contendo o cabeçalho que é enviado no log com o horário de início do backup
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

    # Método que entra na pasta onde os arquivos do backup estão e compacta
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

    # Método que cria o arquivo de log(vazio)
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

    # Método que lista os arquivos a serem inclusos no backup para que sejam impressos no log
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

    # Método que cria o rodapé que é enviado no arquivo de log
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

    # Método que subscreve e atualiza os dados no arquivo de log
    def subscribe_log(self, header, file_list, footer):
        file = 'full_backup_log_{}.txt'.format(time.strftime('%d-%m-%y'))
        f = open(file, 'w')
        f.write(header)
        f.write(file_list)
        f.write(footer)
        f.close()

    # Método que envia o email ao destinatário
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
            # Chamamento do método que move o arquivo de log para a pasta de destino
            self.open_move_file()

        except:
            # Chamamento do método que move o arquivo de log para a pasta de destino
            self.open_move_file()


# Instância da classe Backup
backup = Backup()
# Loop da GUI
root.mainloop()
