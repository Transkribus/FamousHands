import csv
import os

'''
Created on Aug 4, 2017

An import batch for entry data

@author: albert
'''

from fh.wikidata import WikiGet as w;
import fh.models as m
import datetime
from shutil import copyfile
import os

class EntryUploader:

    def setEntry(self, q, label):
        wi = w.WikiGet()
        #wi.GetEntry("Q7346")
        entry = wi.GetEntry(q, label)
    
    
    def upload(self):
        with open('/home/albert/tmp/fh/Famous Hands/tab2.csv', 'rt') as csvfile:
            f = csv.reader(csvfile, delimiter=',', quotechar='"')
            q_label = {};
            next(f) #ignore header
            for row in f:
                if  len(row[2]) > 0 and row[2].startswith('Q'):
                    print  (row[2]);
                    q_label[ row[2]] = row[0]
                    self.setEntry(row[2], row[0])
                    

    def uploadHandwriting(self):
        with open('/home/albert/tmp/fh/Famous Hands/q_folder.csv', 'rt') as csvfile:
            f = csv.reader(csvfile, delimiter='\t', quotechar='"')
            next(f) #ignore header
            for row in f:
                print (row[0])
                new_dir = '/home/albert/Dropbox/my/workspaces/liclipse/fh/fh/static/fh/img/upload/' + row[2];
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                i = 0
                for img in os.listdir('/home/albert/tmp/fh/Famous Hands/' + row[2]):
                    img_p = row[2] + '/' + img;
                    print(row[3])
                    en = m.ENTRY.objects.get(pk=row[3])                    
                    m.HANDWRITTENIMAGE.objects.create(entry = en, title = row[2]  + "_" + str(i), description = row[2]  + "_" + str(i), date = datetime.datetime.now(), link = img_p)
                    copyfile('/home/albert/tmp/fh/Famous Hands/' + img_p, '/home/albert/Dropbox/my/workspaces/liclipse/fh/fh/static/fh/img/upload/' + img_p)
                    i += 1