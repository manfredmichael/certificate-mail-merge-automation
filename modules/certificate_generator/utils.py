from datetime import datetime
import time

def create_code(base, cert_no, digit_num=3):
    cert_no = str(cert_no).zfill(3)
    code = str(base) + cert_no
    return code

def wait(s):
    for i in range(s):
        print('sending in {} seconds '.format(s-i), end='\r', flush=True)
        time.sleep(1)
    print(' '.join([' ' for i in range(20)]), end='\r', flush=true)

