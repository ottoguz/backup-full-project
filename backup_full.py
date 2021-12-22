#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import subprocess
import time

#Essa função gera um banner com a hora inicial do Backup
def inicio(horaInicio):

    inicio = '''
  ===========================================================================
||   ____          _____ _  ___    _ _____    ______ _    _ _      _         ||
||  |  _ \   /\   / ____| |/ / |  | |  __ \  |  ____| |  | | |    | |        ||
||  | |_) | /  \ | |    | ' /| |  | | |__) | | |__  | |  | | |    | |        ||
||  |  _ < / /\ \| |    |  < | |  | |  ___/  |  __| | |  | | |    | |        ||
||  | |_) / ____ \ |____| . \| |__| | |      | |    | |__| | |____| |____    ||
||  |____/_/    \_\_____|_|\_ \____/|_|      |_|     \____/|______|______|   ||
||                                                                           ||
||                       BACKUP FULL DO FILESERVER                           ||
||                                                                           ||
  ===========================================================================
  ===========================================================================
                 BACKUP FULL DO FILESERVER INICIADO ÀS %s
  ===========================================================================
''' % horaInicio
    return inicio

#Termino e calculos
def termino(diaInicio, horaInicio, backup, pathlog):
    hoje = (time.strftime("%d-%m-%Y"))
    horaFinal   = time.strftime('%H:%M:%S')
    backup = backup.replace('tar cvf', '')
    final = '''
  ===========================================================================
                            BACKUP FULL FINALIZADO
                HORA INICIAL:    %s  -  %s
                HORA FINAL  :    %s  -  %s
                LOG FILE    :    %s
                BAK FILE    :    %s
  ===========================================================================
    ''' % (diaInicio, horaInicio, hoje, horaFinal, pathlog, backup)
    return final


#ESSA FUNÇÃO DESMONTA O HD DE BACKUP POR SEGURANÇA.
#DESCOMENTE A LINHA desmonta_hd() DENTRO DE backupfull() PARA UTILIZÁ-LA
def desmonta_hd(disk):
    try:
        umount = 'umount %s' % disk
        subprocess.call(umount, shell=True)
        return True
    except:
        return False


#CONSTROI OS LOGS DO SISTEMA - Aqui selecionamos o nome do backup e o arquivo de logs que iremos criar.
def geralog():
    date = (time.strftime("%Y-%m-%d"))              #
    logfile     = '%s-backup-full.txt' % date       # Cria o arquivo de Log
    pathlog     = '/var/log/backup/backup-full/%s' % logfile    # Arquivo de log
    return pathlog


#CONSTROI O ARQUIVO E PATH DE BACKUP E RETORNA
def gerabackup():
    date = (time.strftime("%Y-%m-%d"))
    backupfile  = '%s-backup-full.tar.gz' % date    # Cria o nome do arquivo de Backup
    pathdestino = '/backup/home/%s' % backupfile # Destino onde será gravado o Backup
    pathorigem  = '/home/'                 # pasta que será 'backupeada'
    backup      = 'tar cvf %s %s' % (pathdestino, pathorigem) # Comando de execução
    return backup

##FUNCAO QUE ENVIA OS LOGS DE BACKUP PARA O ADMIN
def send_email(pathlog):
   try:
    fromaddr = "bruno@terminalx.net.br"
    toaddr = 'bruno@terminalx.net.br'
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Logs de backup Xterm"

    body = "\nEm anexo logs de backup"

    msg.attach(MIMEText(body, 'plain'))

   # filename = 'teste.pdf'

    attachment = open(pathlog,'rb')


    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    attachment.close()

    server = smtplib.SMTP('smtp.hostinger.com.br', 587)
    server.starttls()
    server.login(fromaddr, "bmed2007#")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print('\nEmail enviado com sucesso!')
   except:
    print("\nErro ao enviar email")


#CRIA OS BACKUPs
def backupfull():
    disk = '/dev/sdb'        #Define onde está a partição que será usada para guardar o backup
    horaInicio = time.strftime('%H:%M:%S')
    pathlog = geralog()
    backup = gerabackup()
    log = ' >> %s' % pathlog
    start = inicio(horaInicio)
    print(start) #Printa o Banner

    l = open(pathlog, 'w')
    l.write(start)
    l.close()

    #Monta o hd de backup
    mount = 'mount '+ disk + ' /backup'
    subprocess.call(mount, shell=True)

    #RODA O BACKUP
    subprocess.call(backup + log, shell=True)

    #Printa o final e relatório
    diaInicio = (time.strftime("%d-%m-%Y"))
    final = termino(diaInicio, horaInicio, backup, pathlog)
    r = open(pathlog, 'w')
    r.write(final)
    r.close()

    #Descomente essa função para desmontar a partição que será utilizada para armazenar o backup
    desmonta_hd(disk)
    send_email(pathlog)

##########################################################################MAIN########################################################################

backupfull()