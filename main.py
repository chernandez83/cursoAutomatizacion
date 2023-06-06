import paramiko
import scp
import time
from getpass import getpass

HOST = '10.0.0.101'
USER = 'batman'

if __name__ =='__main__':
    try:
        password = getpass('Password: ')
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
        client.connect(HOST, username=USER, password=password)
        
        # stdin, stdout, sterr = client.exec_command('ls -a')
        # time.sleep(1)
        # result = stdout.read().decode()
        # print(result)
        
        # # SFTP
        sftp_client = client.open_sftp()
        
        # # Cargar arhivo por SFTP
        sftp_client.put(
            localpath='paramiko.txt', 
            remotepath='prueba/archivo_destino.txt'
        )
        
        # # Descargar arhivo por SFTP
        sftp_client.get(
            remotepath='prueba/archivo.txt', 
            localpath='archivo_destino.txt'
        )
        
        # # SCP
        scp_client = scp.SCPClient(client.get_transport())
        
        # # Cargar arhivo por SCP
        scp_client.put(
            'paramiko.txt',
            remote_path='prueba/archivo_scp.txt'
        )
        
        # # Descargar arhivo por SCP
        scp_client.get(
            remote_path='prueba/archivo.txt', 
            local_path='archivo_scp.txt'
        )
        
        # Canales        
        session = client.get_transport().open_session()
        if session.active:
            session.exec_command('cd prueba && ls -la') # solo se puede ejecutar una vez, cierra el canal
            result = session.recv(1024).decode()
            print(result)
            # session.exec_command('ls -la') # marcaría error
        
        # Ejecutar como root
        session = client.get_transport().open_session()
        if session.active:
            # combinar stderr con stdout
            session.set_combine_stderr(True)
            # obtener pseudo terminal para pasar la contraseña de sudo
            session.get_pty()
            session.exec_command('sudo ls -l')
            
            stdin = session.makefile('wb')
            stdout = session.makefile('rb')
            
            stdin.write(password + '\n')
            
            result = stdout.read().decode()
            print(result)
        
        
        # Ejecutar como root (alternativo)
        session = client.get_transport().open_session()
        if session.active:
            # combinar stderr con stdout
            session.set_combine_stderr(True)
            
            # Pasar contaseña con un pipe
            session.exec_command(f'echo {password} | sudo -S ls -la')
            
            stdout = session.makefile('rb')
           
            result = stdout.read().decode()
            print(result)
            
        
        # sftp_client.close()
        # scp_client.close()
        client.close()
        
    except paramiko.ssh_exception.AuthenticationException as e:
        print('Authenticación fallida')
        print(e)