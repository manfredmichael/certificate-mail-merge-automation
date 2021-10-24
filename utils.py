from datetime import datetime

def create_code(date_time, cert_type, cert_no, base):
    dd = date_time.strftime('%d')
    mm = date_time.strftime('%m')
    yy = date_time.strftime('%y')
    code = base.replace('[DATE]', dd)\
                           .replace('[MONTH]', mm)\
                           .replace('[YEAR]', yy)\
                           .replace('[TYPE]', cert_type)\
                           .replace('[NO]', str(cert_no).zfill(3))\

    return code

def add_email_log(email):
    with open('data/log.txt', 'a+') as f:
        f.write('\n{} : Email sent to {}'.format(datetime.now().strftime('%d/%m/%y %H/%M/%S'), email))
