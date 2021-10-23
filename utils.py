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
