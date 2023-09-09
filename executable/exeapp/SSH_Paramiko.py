import paramiko

def ssh_connector(hostname, port, username, password):

    # Initialize an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        client.connect(hostname, port=port, username=username, password=password)
        return client
  
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None  # Return None on error

    



# ssh_client = establish_ssh_connection(hostname, port, username, password)
# if ssh_client:
#     print("SSH connection established successfully.")
#     # Perform your SSH operations here
#     # Remember to close the connection when done: ssh_client.close()
# else:
#     print("SSH connection could not be established.")
