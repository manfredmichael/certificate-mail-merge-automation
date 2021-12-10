from datetime import datetime

def get_certificate_info(name, code, type, url,\
    date_published=None, valid_until='Forever'):
    if not date_published:
        date_published = datetime.now().strftime('%d %B %Y')
    return [code, date_published, name, type, valid_until, url]
