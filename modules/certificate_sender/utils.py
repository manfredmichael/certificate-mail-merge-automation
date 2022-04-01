import re

# remove class in participant names
def remove_class(name):
  return ' '.join([name for name in name.lower().replace('_',' ')\
                   .split(' ') if not isclass(name) and len(name)>1])

def isclass(x): 
    return re.search('[0-9][A-Za-z][A-Za-z][0-9][0-9]', x)
