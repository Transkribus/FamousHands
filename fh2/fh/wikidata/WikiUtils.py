'''
Created on Jun 22, 2017

@author: albert
'''

from datetime import datetime

 

def WikiDate(dt_str):
    f = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(dt_str, f)
