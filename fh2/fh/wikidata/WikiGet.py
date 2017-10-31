'''
Created on Mar 21, 2017

@author: albert
'''

import json

from urllib.request import urlopen 
import fh.models as m
import fh.wikidata.WikiUtils as wu
import datetime
#import wikipedia
from dateutil.relativedelta import relativedelta
#from wikidata.client import Client as wdCl 


class WikiGet:

    BASE_URL = "https://query.wikidata.org/sparql?query=";
    #QUERY_PATTERN = """SELECT ?gender ?genderLabel ?spouse ?spouseLabel ?genreLabel ?birthLabel ?birthPlLabel ?deathLabel ?deathPlLabel WHERE { wd:%id wdt:P21 ?gender. wd:%id wdt:P26 ?spouse. wd:%id wdt:P136 ?genre. wd:%id wdt:P569 ?birth. wd:%id wdt:P19 ?birthPl.wd:%id wdt:P570 ?death.wd:%id wdt:P20 ?deathPl. SERVICE wikibase:label { bd:serviceParam wikibase:language %22en%22. }"""
    #https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q354542&props=labels|descriptions|claims|sitelinks/urls&languages=en&languagefallback=&sitefilter=azwiki&formatversion=2
    #https://www.wikidata.org/wiki/Special:EntityData/Q5879.json
    #url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q354542&format=json&sitefilter=enwiki'
    #url = "https://query.wikidata.org/sparql?query=SELECT%20?spouseLabel%20WHERE%20{wd:Q1744%20wdt:P26%20?spouse.SERVICE%20wikibase:label%20{bd:serviceParam%20wikibase:language%20%22en%22%20.}}&format=json"


    def WikiGet(self):
        pass
      
    
    def GetLocation(self, wiki_id):
        QUERY_PATTERN = "SELECT ?label ?location WHERE { wd:%id wdt:P625 ?location. wd:%id rdfs:label ?label . FILTER (langMatches( lang(?label), \"EN\" ) ) }"    
        url = self.BASE_URL  + QUERY_PATTERN.replace("%id", wiki_id).replace(" ","%20") + "&format=json" # %7B%

        response = urlopen(url)
        data = response.read().decode("utf-8")
        j = json.loads(data)
        b = j['results']['bindings'][0]
        label = b['label']['value']
        loc = b['location']['value'];
        loc = loc.replace("Point(", "")
        loc = loc.replace(")", "")
        locs = loc.split(' ')
        return m.LOCATION.objects.create(lat=locs[1], lng=locs[0], label=label)
    
    
    
#     def IsHuman(self, q_id):
#         client = wdCl() 
#         d = client.get(q_id)
#         try:
#             g = client.get('P21') #gender
#             d[g] #try to access gender
#             return True
#         except:
#             return False
#     
    
    
#     def GetHumansContainingRegex(self, name_part):
#         QUERY_PATTERN =  "SELECT ?human ?label WHERE { ?human wdt:P31 wd:Q5; rdfs:label ?label. FILTER(LANG(?label) = \"en\"). FILTER REGEX(str(?label), '"+ name_part + "','i'). } LIMIT 5"
#         print(QUERY_PATTERN)
#         response = urlopen(self.BASE_URL + QUERY_PATTERN.replace(" ","%20") + "&format=json")
#         data = response.read().decode("utf-8")
#         j = json.loads(data)
#         print(json.dumps(j, indent=4, sort_keys=True))
    
    def GetItemsContaining(self,name_part):  
        QUERY_PATTERN = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + name_part + "&language=en&format=json&limit=50" 
        response = urlopen(QUERY_PATTERN.replace(" ","%20") + "&format=json")
        data = response.read().decode("utf-8")
        j = json.loads(data)
        
        b = j["search"]
        
        #print("------------\n")
        #print(json.dumps(j, indent=4, sort_keys=True))

        return b
                
    def GetHumansContaining(self, name_part):
        it = self.GetItemsContaining(name_part)
       
        qids = ""
        for i in it:
            qids += " wd:" + i["id"]
                            
        QUERY_PATTERN =  "SELECT ?human ?label WHERE { ?human wdt:P31 wd:Q5; rdfs:label ?label. values ?human {%ids} FILTER(LANG(?label) = \"en\"). }"
        url = self.BASE_URL  + QUERY_PATTERN.replace("%ids", qids).replace(" ","%20") + "&format=json" # %7B%
        response = urlopen(url)
        data = response.read().decode("utf-8")
        j = json.loads(data)
        
        b = j['results']['bindings'] 
        
        idLab = {}
        
        for bi in b:
            l = bi["label"]["value"]
            qid =  bi["human"]["value"].rsplit("/",1)[1]
           
            idLab[qid] = l
            
        return idLab
    
    def GetEntry(self,wiki_id, description = ""):
        #print ("WIKI_ID",wiki_id)
        #QUERY_PATTERN = "SELECT ?langSpokenLabel ?image ?gender ?genderLabel ?birthLabel ?birthPl ?deathLabel ?deathPl WHERE {wd:%id wdt:P1412 ?langSpoken.wd:%id wdt:P18 ?image.wd:%id wdt:P21 ?gender.wd:%id wdt:P569 ?birth.wd:%id wdt:P19 ?birthPl. wd:%id wdt:P570 ?death.wd:%id wdt:P20 ?deathPl. SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". } }"
        QUERY_PATTERN = "SELECT ?label ?itemLabel ?langSpokenLabel ?image ?gender ?genderLabel ?birthLabel ?birthPl ?deathLabel ?deathPl WHERE {{wd:%id wdt:P103 ?langSpoken}UNION{wd:%id rdfs:label ?item}UNION{wd:%id wdt:P18 ?image}UNION{wd:%id wdt:P21 ?gender}UNION{wd:%id wdt:P569 ?birth}UNION{wd:%id wdt:P19 ?birthPl}UNION{wd:%id wdt:P570 ?death.wd:%id wdt:P20 ?deathPl} SERVICE wikibase:label { bd:serviceParam wikibase:language \"en,de\". } }"
        url = self.BASE_URL  + QUERY_PATTERN.replace("%id", wiki_id).replace(" ","%20") + "&format=json" # %7B%

        response = urlopen(url)
        data = response.read().decode("utf-8")
        j = json.loads(data)
        b = j['results']['bindings'] 
        
        dic = {}
        for bi in b:
            for k in bi.keys():
                dic[k] = bi[k]
            
        #print(json.dumps(b, indent=4, sort_keys=True))
        
        #gender = dic['genderLabel']['value']
        #print (dic)
        
        image = ""
        if 'image' in dic:
            image = dic['image']['value']
            image = image.replace('http://', 'https://')
        
        place_of_birth = None
        if 'birthPl' in dic:
            place_of_birth_id = dic['birthPl']['value'].rsplit('/', 1)[1] #we just want the id
            place_of_birth = self.GetLocation(place_of_birth_id)
        else:
            print('birthplace not valid')
        

        bunknown = False
        birth = None
        if 'birthLabel' in dic:
            birth = dic['birthLabel']['value']
            
            if str(birth).startswith('t'):
                birth = None
                byear = None
                bmonth = None
                bday = None
                bunknown = True
            elif str(birth).startswith('-'):
                birth = dic['birthLabel']['value']
                byear = '-' + str(birth).split(sep='-')[1]   
                bmonth = str(birth).split(sep='-')[2]
                bday = str(str(birth).split(sep='-')[2]).split(sep='T')[0]
            else:
                birth = wu.WikiDate(dic['birthLabel']['value'])   
                byear = str(birth).split(sep='-')[0] 
                bmonth = str(birth).split(sep='-')[1]
                bday = str(str(birth).split(sep='-')[2]).split(sep=' ')[0]
#            if not str(birth).startswith('-') and not bunknown: 
        else:
            birth = None
            byear = None
            bmonth = None
            bday = None

        place_of_death = None
        if 'deathPl' in dic:
            place_of_death_id = dic['deathPl']['value'].rsplit('/', 1)[1] #we just want the id
            place_of_death = self.GetLocation(place_of_death_id)

        dunknown = False
        death = None
        if 'deathLabel' in dic:
            death = dic['deathLabel']['value']
            
            if str(death).startswith('t'):
                death = None
                dyear = None
                dmonth = None
                dday = None
                dunknown = True
            elif str(death).startswith('-'):
                death = dic['deathLabel']['value']
                dyear = '-' + str(death).split(sep='-')[1]   
                dmonth = None
                dday = None
            else:
                death = wu.WikiDate(dic['deathLabel']['value'])    
                dyear = str(death).split(sep='-')[0] 
                dmonth = str(death).split(sep='-')[1]
                dday = str(str(death).split(sep='-')[2]).split(sep=' ')[0]
        else:
                death = None
                dyear = None
                dmonth = None
                dday = None
        #print('death:' + str(death))
            
        native_lang = None
        
        if 'langSpokenLabel' in dic:
            native_lang = dic['langSpokenLabel']['value'][:9] #Abbr?
            
        lifespan = 1
            
        if dunknown or bunknown:
            lifespan = -1
        elif dyear == None:
            lifespan = relativedelta(datetime.datetime.now(), birth).years
        elif str(byear).startswith('-') and str(dyear).startswith('-'):
            birthy = str(byear).split('-')[1]
            deathy = str(dyear).split('-')[1]
            lifespan = int(birthy) - int(deathy)
        elif str(byear).startswith('-') or str(dyear).startswith('-'):
            lifespan = abs(float(byear)) + abs(float(dyear))
        else:
            lifespan = int(dyear) - int(byear)
        
        return m.ENTRY.objects.create(country_citizenship=place_of_birth, image= image, wiki_link=wiki_id, native_lang=native_lang, description=description, day_of_birth=bday, month_of_birth=bmonth, year_of_birth=byear, day_of_death=dday, month_of_death=dmonth, year_of_death=dyear, lifespan=lifespan, place_of_birth= place_of_birth, place_of_death=place_of_death, unknown_date_of_death=dunknown, unknown_date_of_birth=bunknown)
        
    def GetHandwriting(self, wiki_id):
        #Hier sollen die Entries von der Handwriting tabelle geholt werden.
        QUERY_PATTERN = "SELECT ?label ?itemLabel ?langSpokenLabel ?image ?gender ?genderLabel ?birthLabel ?birthPl ?deathLabel ?deathPl WHERE {{wd:%id wdt:P1412 ?langSpoken}UNION{wd:%id rdfs:label ?item}UNION{wd:%id wdt:P18 ?image}UNION{wd:%id wdt:P21 ?gender}UNION{wd:%id wdt:P569 ?birth}UNION{wd:%id wdt:P19 ?birthPl}UNION{wd:%id wdt:P570 ?death.wd:%id wdt:P20 ?deathPl} SERVICE wikibase:label { bd:serviceParam wikibase:language \"en,de\". } }"
        url = self.BASE_URL  + QUERY_PATTERN.replace("%id", wiki_id).replace(" ","%20") + "&format=json" # %7B%

        response = urlopen(url)
        data = response.read().decode("utf-8")
        j = json.loads(data)
        
        #print(json.dumps(j, indent=4, sort_keys=True))
        
        b = j['results']['bindings'] #[0]
        
        dic = {}
        for bi in b:
            for k in bi.keys():
                dic[k] = bi[k]