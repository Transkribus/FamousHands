'''
Created on Aug 20, 2017

@author: albert
'''

import requests
#workaround for insecure platform warnings...
#http://stackoverflow.com/questions/29099404/ssl-insecureplatform-error-when-using-requests-package
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import xmltodict


# class TranskribusUser:
#     def __init__(self, xmlStr):
#         dic = xmltodict.parse(xmlStr)
#         self.user = dic.get('trpUserLogin')
#         self.isAdmin = dic.get('isAdmin')

        
class Services:
    
    BASE_URL = "https://transkribus.eu/TrpServer/rest"
    
    def __init__(self):
        self.s = requests.Session()
     
     
    def Logout(self):
        url = self.BASE_URL +'/auth/logout'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.s.post(url, verify=False, headers=headers)
        try: self.cleanPersistentSession()
        except: pass
        
    def Login(self, user, pw):
        url = self.BASE_URL +'/auth/login' 
        t_id = "user_data" # note we are using the same t_id as for t_register... This is OK because the data response will be the same... I think
        params = {'user': user, 'pw': pw}
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        r = self.s.post(url, params=params, verify=False, headers=headers)
        print("RES:" + str(r.text))
        if r.status_code != 200: #ok
            raise Exception("NO 200")
        
        
        return xmltodict.parse(r.text)