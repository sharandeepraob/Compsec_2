from cryptography.fernet import Fernet
import os
from exeapp.models import AttackData
from exeapp.SSH_Paramiko import ssh_connector

changed_file_list=[]
def decryption(decrypt_key,Org_file_list,hostname,port,username,password):

    ssh = ssh_connector(hostname,port,username,password)
    i=0
    commands = ["pwd","find /home/kali/Documents -type f  -name '*.lazarus'"]
    stdin, stdout, stderr = ssh.exec_command(commands[0])
    curr_dir = stdout.read().decode('utf-8')
    # print(username)
    remote_dir = os.path.join(curr_dir.strip(),'Documents')
    stdin, stdout, stderr = ssh.exec_command(commands[1])
    changed_file_list = stdout.read().decode().splitlines()
    print(changed_file_list)
    for changed_file in changed_file_list:

        if i<=(len(changed_file_list)-1):
            
            stdin, stdout, stderr = ssh.exec_command(f"cat {changed_file}")
            file_content = stdout.read().decode()
            key = decrypt_key
            fernet = Fernet(key)
            decrypted_content = fernet.decrypt(file_content)
            new_file = Org_file_list[i]
            ssh.exec_command(f"echo '{decrypted_content.decode()}' > {changed_file}")
            ssh.exec_command(f"mv {changed_file} {new_file}" )
            i+=1

        else:
            break
    AttackData.objects.all().delete()
