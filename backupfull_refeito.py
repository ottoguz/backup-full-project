def backupfull():
    disk = '/dev/sdb'  # Define onde está a partição que será usada para guardar o backup
    horaInicio = time.strftime('%H:%M:%S')
    pathlog = geralog()
    backup = gerabackup()
    log = ' >> %s' % pathlog
    start = inicio(horaInicio)
    # print(log) #Printa o Banner

    x = open(pathlog, 'w')
    x.write(start)
    x.close()

    # Monta o hd de backup
    mount = 'mount ' + disk + ' /backup'
    subprocess.call(mount, shell=True)

    # RODA O BACKUP
    subprocess.call(backup + log, shell=True)
    # r = open(pathlog, 'w')

    # Printa o final e relatório
    diaInicio = (time.strftime("%d-%m-%Y"))
    final = termino(diaInicio, horaInicio, backup, pathlog)

    r = open(pathlog, 'r')  # Abra o arquivo (leitura)
    conteudo = r.readlines()
    conteudo.append(final)  # insira seu conteúdo
    r = open(pathlog, 'w')  # Abre novamente o arquivo (escrita)
    r.writelines(conteudo)  # escreva o conteúdo criado anteriormente nele.
    r.close()
    # Descomente essa função para desmontar a partição que será utilizada para armazenar o backup
    desmonta_hd(disk)
    send_email(pathlog)