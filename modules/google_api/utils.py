from datetime import datetime

def get_certificate_info(name, code,  url, type=None,\
    date_published=None, valid_until='Forever'):
    if not date_published:
        date_published = datetime.now().strftime('%d %B %Y')
    if not type:
        type_code = code[:-2]
        if type_code == 'PT':
            type = 'Participant'
        elif type_code == 'CM':
            type = 'Commitee'
        elif type_code == 'CP':
            type = 'Completed'
        elif type_code == 'SP':
            type = 'Speaker'
        elif type_code == 'AP':
            type = 'Appreciation'
        else:
            type = 'Unknown'
    return [code, date_published, name, type, valid_until, url]
