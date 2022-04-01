from modules.certificate_sender.sender import Sender

sender = Sender(folder_id='1JVDXhAUC92-Mx553sYWT5tPlbH5UwmIr',
                client_secret_path='secrets/client_secret.json')

sender.generate_all()
sender.send_all()
