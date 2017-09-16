'''
Created on Mar 19, 2017

@author: albert
'''

#from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
#from django.contrib.auth import authenticate
import logging
import math
import wikipedia
import uuid
import os


from . import models as m
from django.db.models import Q
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core import serializers
from fh.wikidata import WikiGet as w
from fh.tools import EntryUploader as eu
from fh.transkribus import Services as serv 
 
import json 

 
# Get an instance of a logger
logger = logging.getLogger(__name__)
   
def index(request):
    template = loader.get_template('fh/index.html')
#    two_days_ago = datetime.utcnow() - timedelta(days=2)
#    recent_posts = m.Post.objects.filter(created_at__gt=two_days_ago).all()
    
    context = {
        'rnd_hw': (m.HANDWRITTENIMAGE.objects.order_by('?')[:10]),
        'cnt_entity' : m.ENTRY.objects.all(),
        'cnt_hw' : m.HANDWRITTENIMAGE.objects.all()
    }

    return HttpResponse(template.render(context, request))


def maps(request):
    template = loader.get_template('fh/maps.html')
    lat =  request.GET.get('lat', '47.26').replace(',','.') #IBK as default
    long = request.GET.get('lng', '11.39').replace(',','.')
    slider_km = request.GET.get('km', 50)
    
    context = {
        'entries' : m.ENTRY.objects.filter(on=True),
        'lat' : lat,  #the center lat, lng, to be set as parameter
        'lng' : long,
        'km' : slider_km
    }

    return HttpResponse(template.render(context, request))

def timeline(request):
    n = request.GET.get('filterName', '')
    la = request.GET.get('filterLang', '')
    lo = request.GET.get('filterLoc', '')
    agg = int(request.GET.get('agg','1')) #1...year, 10...decade, 100...mill, ...
    template = loader.get_template('fh/timeline.html')    
    entries = []
    entries = m.ENTRY.objects.filter(on=True).order_by('year_of_birth').filter(Q(description__icontains=n)&Q(country_citizenship__icontains=lo))
    
    a = entries[:]
    b = entries[:]
    same_entries = []
    different_entries = []
    count = 0
    
    while len(a) > 0:
        same_entries.clear()
        count = 0
        i = 0
        
        for be in b:
            try:
                ia = math.ceil(float(a[0].year_of_birth)/agg)
                ib = math.ceil(float(be.year_of_birth)/agg)
            except:
                ia = None
                ib = None
            if ia == ib:
                same_entries.append(be)
                count += 1
            else:
                break
        different_entries.append(same_entries[:])
        while i < count:
            b = b[1:]
            a = a[1:]
            i+=1
    for de in different_entries:
        i = 0
        while i < len(de):
            i += 1

    #get handwritings for all entries
    hws = {}
    for e in entries:
        hw = m.HANDWRITTENIMAGE.objects.filter(entry=e,on=True)
        hws[e.pk] = hw
        
    context = {
        'entries': different_entries,
        'agg' : agg,
        'hws' : hws
    }
    
    return HttpResponse(template.render(context, request))


def upload_handwriting(request):
    template = loader.get_template('fh/upload_handwriting.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
    
def admin(request):
    
    if  'user' in request.session and request.session['user']['isAdmin']:
        template = loader.get_template('fh/admin.html')
        context = {
            'entries' : m.ENTRY.objects.all().order_by('description'),
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.warning(request, "insufficient_privileges")
        return HttpResponseRedirect("index")

    

# def longsearch(request):
#     template = loader.get_template('fh/longsearch.html')
#     s = request.POST.get('search', '')
#     context = {
#         'entries' : m.ENTRY.objects.filter(on=True).filter(Q(description__icontains=s)|Q(description__icontains=s))
#         }
#     return HttpResponse(template.render(context, request))

def detail(request):
    template = loader.get_template('fh/detail.html')
    s = request.GET.get('id', '')
    e = m.ENTRY.objects.get(pk=s)
    wikipedia.set_lang(translation.get_language())
    
    try:
        desc = wikipedia.summary(e.description, sentences=5).split("==")[0]

    except:
        desc = ""
        
    context = {
        'e' :  e,
        'description' : desc,
        'handwritings' : m.HANDWRITTENIMAGE.objects.filter(entry=e,on=True),
        'wiki_name' : wikipedia.search(e.description,1)[0]
        }
    
    return HttpResponse(template.render(context, request))


def search(request):
    template = loader.get_template('fh/search.html')
    template1 = loader.get_template('fh/longsearch.html')

    s = request.POST.get('search', '')
    p = s.split('/')
    if len(p)==2:
        entries = m.ENTRY.objects.filter(on=True).order_by('description').filter(Q(month_of_birth__icontains=p[0])&Q(year_of_birth__icontains=p[1])|Q(day_of_birth__icontains=p[0])&Q(month_of_birth__icontains=p[1])|Q(month_of_death__icontains=p[0])&Q(year_of_death__icontains=p[1])|Q(day_of_death__icontains=p[0])&Q(month_of_death__icontains=p[1]))
    elif len(p)==3:
        entries = m.ENTRY.objects.filter(on=True).order_by('description').filter(Q(day_of_birth__icontains=p[0])|Q(month_of_birth__icontains=p[1])|Q(day_of_death__icontains=p[0])|Q(month_of_death__icontains=p[1])| Q(year_of_death__icontains=p[2])|Q(year_of_birth__icontains=p[2]))
    else  :
        entries = m.ENTRY.objects.filter(on=True).order_by('description').filter(Q(description__icontains=s)|Q(month_of_birth__icontains=s)|Q(year_of_birth__icontains=s)|Q(day_of_birth__icontains=s)|Q(day_of_death__icontains=s)| Q(month_of_death__icontains=s)| Q(year_of_death__icontains=s)|Q(wiki_link__icontains=s)|Q(place_of_birth__label__icontains=s)|Q(place_of_death__label__icontains=s))
    context = {
        'entries' : entries,
        }
    if len(entries) < 10 and len(entries) > 1:                       
        return HttpResponse(template1.render(context, request))
    elif len(entries) == 1:
        return HttpResponseRedirect("detail?id=" + str(entries[0].id))
    else:
        return HttpResponse(template.render(context, request)) 


def image_gallery(request):
    template = loader.get_template('fh/image_gallery.html')
    s = request.GET.get('id', '')
    e = m.ENTRY.objects.get(pk=s)
    context = {
        'e' :  e,
        'handwritings' : m.HANDWRITTENIMAGE.objects.filter(entry=e) 
    }
    return HttpResponse(template.render(context, request))
################################################################

def logout_process(request):
    s = serv.Services();
    s.Logout()
    del request.session['user']
    request.session.modified = True
    return HttpResponseRedirect("index")
 
def login_process(request):
    e = request.POST.get('email','')
    p = request.POST.get('password','')
  
    s = serv.Services();
    try:
        request.session['user'] = s.Login(e,p)['trpUserLogin']
        request.session.modified = True 
    except:
        messages.warning(request, "login_failed")
    
    return HttpResponseRedirect("index")



'''
    always called after: upload_handwriting_process_imgs
'''
def upload_handwriting_process(request):
    
    qids = request.session["fnames"] # the file names uploaded stored within the session
    
    qid = request.POST.get("wikidata_id","")
    qtitle = request.POST.get("title","")
    
    #if entry does not exist, create one
    if not m.ENTRY.objects.filter(wiki_link=qid).exists():
        wi = w.WikiGet()
        entry = wi.GetEntry(qid, qtitle)
    else:
        entry = m.ENTRY.objects.get(wiki_link=qid)
        
    for fname in qids:
        src= 'fh/static/fh/img/tmp/' + fname
        dst = 'fh/static/fh/img/upload/' + qid + "/" + fname
        
        if os.path.isfile(src): 
            os.makedirs('fh/static/fh/img/upload/' + qid, exist_ok=True)
            #Move files from the tmp to the upload store, remove file afterwards
            os.rename(src, dst)
            title = request.POST.get("title__" + fname)
            desc =  request.POST.get("desc__" + fname) #link to the origin
            origin =  request.session['user'] #the logged in user
            
            m.HANDWRITTENIMAGE.objects.create(entry=entry, title=title, description=desc, link= qid + "/" + fname, origin=origin)
    
    request.session["fnames"] = [];
    request.session.modified = True
    return HttpResponseRedirect("upload_handwriting")


@csrf_exempt
def upload_handwriting_process_imgs(request):
    file = request.FILES['file']
    fname = str(uuid.uuid4()) + "." + os.path.splitext(str(file))[1][1:].strip() 
    
    fnames = []
    if 'up_file_names' in request.session:
        print("fnames found in session")
        fnames = request.session["up_file_names"]
    
    fnames.append(fname)
    request.session["fnames"] = fnames

    default_storage.save('fh/static/fh/img/tmp/' + fname, ContentFile(file.read()))
    return HttpResponse(json.dumps(fname), content_type="application/json") 


#-------------------------------------------
# Web Services
#-------------------------------------------

def search_name_service(request):
    name_part = request.GET.get("name_part")
    
    wg = w.WikiGet()
    hc = wg.GetHumansContaining(name_part)
    
    entries = m.ENTRY.objects.filter(on=True).order_by('pk').filter(Q(description__icontains=name_part))
    wlDesc = list(entries.values_list('wiki_link', 'description'))
    
    mrg = hc.copy()
    mrg.update(wlDesc)
    return HttpResponse(json.dumps(mrg), content_type="application/json")

def turn_onoff_service(request):
    if  'user' in request.session and request.session['user']['isAdmin']:
        what = request.GET.get("what") #entity or image
        iid = request.GET.get("id")
        on = request.GET.get("on") # should item be turned on?
        
        if (what == 'entity'):
            ent = m.ENTRY.objects.get(pk=iid)
            ent.on=(on == 'true')
            ent.save()
        else: 
            hwi = m.HANDWRITTENIMAGE.objects.get(pk=iid)
            hwi.on=(on == 'true')
            hwi.save()
        return HttpResponse('ok', content_type="text/plain")
    else:
        return HttpResponse('insufficient_privileges', content_type="text/plain")
    
    
#-------------------------------------------
'''
    This is just for starting batch processes
    not really part of the web application
'''
def script(request):
    eup = eu.EntryUploader()
    eup.upload()
    eup.uploadHandwriting()
    
    #wg = w.WikiGet()
    #hc = wg.GetEntry('Q567', 'description') #Merkel
    #hc = wg.GetHumansContaining("Einstein")
    #return HttpResponse(str(hc))

    #m.ENTRY.objects.get(pk=955).delete()
    return HttpResponse("ok")
    