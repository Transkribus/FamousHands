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


# def test(request): 
#     wi = w.WikiGet()
#     #wi.GetEntry("Q7346")
#     l = wi.GetLocation("Q1885566")
#     #print(l)
#     print(l)
#     logger.info('x')
#     template = loader.get_template('fh/login.html')    
#     context = {
#         'x': 'y',
#     }
# 
#     return HttpResponse(template.render(context, request))
#     
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
    context = {
        #'locs': m.LOCATION.objects.all(),
        'entries' : m.ENTRY.objects.all(),
        'lat' : lat,  #the center lat, lng, to be set as parameter
        'lng' : long
    }

    return HttpResponse(template.render(context, request))


'''
def register(request):
    template = loader.get_template('fh/register.html')
#    two_days_ago = datetime.utcnow() - timedelta(days=2)
#    recent_posts = m.Post.objects.filter(created_at__gt=two_days_ago).all()

    context = {
        'x': 'y',
    }

    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('fh/login.html')    
    context = {
        'x': 'y',
    }

    return HttpResponse(template.render(context, request))
'''

# def upload(request):
#     template = loader.get_template('fh/upload.html')    
#     context = {
#         'x': 'y',
#     }
# 
#     return HttpResponse(template.render(context, request))


# def images(request):
#     template = loader.get_template('fh/images.html')   
#     #loc = m.LOCATION.objects.create(lat=0, lng=0, label='loc1')
#     #e = m.ENTRY.objects.create(description='entry', date_of_birth=datetime.date(2007, 12, 5), date_of_death=datetime.date(2007, 12, 5), lifespan=2, place_of_birth= loc, place_of_death=loc)
#     #imgs = []
#     #for i in range(3):
#     #    imgs.append(m.HANDWRITTENIMAGE.objects.create(entry = e, title = 'Bild' + str(i), description = 'Desc Bild ' + str(i), date = datetime.date(2007, 12, 5), link = 'fh/img/upload/img' + str(i) + '.png'))  
#     context = {
#         'imgs': 'imgs'
#     }
# 
#     return HttpResponse(template.render(context, request))

def timeline(request):
    n = request.POST.get('filterName', '')
    la = request.POST.get('filterLang', '')
    lo = request.POST.get('filterLoc', '')
    template = loader.get_template('fh/timeline.html')    
    #entries = []
    entries = m.ENTRY.objects.all().order_by('year_of_birth').filter(Q(description__icontains=n)&Q(country_citizenship__icontains=lo))
    
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
            if a[0].year_of_birth == be.year_of_birth:
                same_entries.append(be)
                count += 1
            else:
                break
        different_entries.append(same_entries[:])
        while i < count:
            b = b[1:]
            a = a[1:]
            i+=1
    
    
    #get handwritings for all entries
    hws = {}
    for e in entries:
        hw = m.HANDWRITTENIMAGE.objects.filter(entry=e)
        hws[e.pk] = hw
    
    context = {
        'entries': different_entries,
        'hws' : hws,
        'from' : 'timeline'
    }

    return HttpResponse(template.render(context, request))

def timeline_k(request):
    n = request.POST.get('filterName', '')
    la = request.POST.get('filterLang', '')
    lo = request.POST.get('filterLoc', '')
    template = loader.get_template('fh/timeline_k.html')    
    entries = []
    entries = m.ENTRY.objects.all().order_by('year_of_birth').filter(Q(description__icontains=n)&Q(country_citizenship__icontains=lo))
    
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
                ia = math.ceil(float(a[0].year_of_birth)/1000)
                ib = math.ceil(float(be.year_of_birth)/1000)
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
    
    context = {
        'entries': different_entries,
        'from' : 'timeline_k'
    }

    return HttpResponse(template.render(context, request))
    
def timeline_cent(request):
    n = request.POST.get('filterName', '')
    la = request.POST.get('filterLang', '')
    lo = request.POST.get('filterLoc', '')
    template = loader.get_template('fh/timeline_cent.html')    
    entries = []
    entries = m.ENTRY.objects.all().order_by('year_of_birth').filter(Q(description__icontains=n)&Q(country_citizenship__icontains=lo))
    
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
                ia = math.ceil(float(a[0].year_of_birth)/100)
                ib = math.ceil(float(be.year_of_birth)/100)
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

    context = {
        'entries': different_entries,
        'from' : 'timeline_cent'
    }
    
    return HttpResponse(template.render(context, request))

def timeline_dec(request):
    n = request.POST.get('filterName', '')
    la = request.POST.get('filterLang', '')
    lo = request.POST.get('filterLoc', '')
    template = loader.get_template('fh/timeline_dec.html')    
    entries = []
    entries = m.ENTRY.objects.all().order_by('year_of_birth').filter(Q(description__icontains=n)&Q(country_citizenship__icontains=lo))
    
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
                ia = math.floor(float(a[0].year_of_birth)/10)
                ib = math.floor(float(be.year_of_birth)/10)
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

    context = {
        'entries': different_entries,
        'from': 'timeline_dec'
    }

    return HttpResponse(template.render(context, request))
    
# def create_entry(request):
#     template = loader.get_template('fh/create_entry.html')
#     context = {}
#     return HttpResponse(template.render(context, request))

def upload_handwriting(request):
    template = loader.get_template('fh/upload_handwriting.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
    
def admin(request):
    template = loader.get_template('fh/admin.html')
    context = {
        'entries' : m.ENTRY.objects.all(),
        }
    return HttpResponse(template.render(context, request))

def longsearch(request):
    template = loader.get_template('fh/longsearch.html')
    s = request.POST.get('search', '')
    context = {
        'entries' : m.ENTRY.objects.filter(Q(description__icontains=s)|Q(description__icontains=s))
       # 'users' : User.objects.all()
        }
    return HttpResponse(template.render(context, request))

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
        'handwritings' : m.HANDWRITTENIMAGE.objects.filter(entry=e) #TODO: better way
        }
    
    return HttpResponse(template.render(context, request))


def search(request):
    template = loader.get_template('fh/search.html')
    template1 = loader.get_template('fh/longsearch.html')

    s = request.POST.get('search', '')
    p = s.split('/')
    if len(p)==2:
        entries = m.ENTRY.objects.all().order_by('description').filter(Q(month_of_birth__icontains=p[0])&Q(year_of_birth__icontains=p[1])|Q(day_of_birth__icontains=p[0])&Q(month_of_birth__icontains=p[1])|Q(month_of_death__icontains=p[0])&Q(year_of_death__icontains=p[1])|Q(day_of_death__icontains=p[0])&Q(month_of_death__icontains=p[1]))
    elif len(p)==3:
        entries = m.ENTRY.objects.all().order_by('description').filter(Q(day_of_birth__icontains=p[0])|Q(month_of_birth__icontains=p[1])|Q(day_of_death__icontains=p[0])|Q(month_of_death__icontains=p[1])| Q(year_of_death__icontains=p[2])|Q(year_of_birth__icontains=p[2]))
    else  :
        entries = m.ENTRY.objects.all().order_by('description').filter(Q(description__icontains=s)|Q(month_of_birth__icontains=s)|Q(year_of_birth__icontains=s)|Q(day_of_birth__icontains=s)|Q(day_of_death__icontains=s)| Q(month_of_death__icontains=s)| Q(year_of_death__icontains=s)|Q(wiki_link__icontains=s)|Q(place_of_birth__label__icontains=s)|Q(place_of_death__label__icontains=s))
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
    request.session['user'] = None;
    return HttpResponseRedirect("index")
 
def login_process(request):
    e = request.POST.get('email','')
    p = request.POST.get('password','')
    #user = authenticate(username=e, password=p)
    #if user is not None:
    #    return HttpResponseRedirect("user")
    #else:
    #    return HttpResponseRedirect("index")
    
    if (e == 'admin' and p == 'admin123'):
        request.session['user'] = 'admin';
        request.session.modified = True
        return HttpResponseRedirect("index")
    
    s = serv.Services();
    try:
        res = s.Login(e,p)
        request.session['user'] = res;
        request.session.modified = True 
    except:
        messages.warning(request, "login_failed")
    
    return HttpResponseRedirect("index")

# def register_process(request):
#     first_name = request.POST['first_name']
#     last_name = request.POST['last_name']
#     email = request.POST['email']
#     password = request.POST['password']
#     password2 = request.POST['password2']
#     if password == password2:
#         m.FHUSER.objects.create(first_name=first_name, last_name = last_name, email = email, password=password) #TODO remove
#         user = User.objects.create_user(username= email, first_name=first_name, last_name = last_name, email = email, password=password)
#         user.save()
#         return HttpResponseRedirect("user")
#     else:
#         return HttpResponseRedirect("register")

# def create_entry_process(request):
#     wiki_id = request.POST['wikidata_id']
#     desc = request.POST['desc']
#     print("WID:" + wiki_id)
#     wi = w.WikiGet()
#     #wi.GetEntry("Q7346")
#     entry = wi.GetEntry(wiki_id, desc)
#     #print(entry)
#     return HttpResponseRedirect("index")


#TODO
def upload_handwriting_process(request):
    
    qids = request.session["fnames"] # the file names uploaded stored within the session
    
    qid = request.POST.get("wikidata_id","")
    qtitle = request.POST.get("title","")
    
    if not m.ENTRY.objects.filter(wiki_link=qid).exists():
        wi = w.WikiGet()
        #wi.GetEntry("Q7346")
        entry = wi.GetEntry(qid, qtitle)
    else:
        entry = m.ENTRY.objects.get(wiki_link=qid)
        
    print("REQ:" + str(request))
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
            
            hwi = m.HANDWRITTENIMAGE.objects.create(entry=entry, title=title, description=desc, link= qid + "/" + fname, origin=origin)
    
    request.session["fnames"] = [];
    request.session.modified = True
    return HttpResponseRedirect("upload_handwriting")


@csrf_exempt
def upload_handwriting_process_imgs(request):
    file = request.FILES['file']
    #file.save()
    #file.save_as('/home/albert/Dropbox/my/workspaces/liclipse/fh/fh/static/fh/img/tmp/' + str(file));
    fname = str(uuid.uuid4()) + "." + os.path.splitext(str(file))[1][1:].strip() 
    
    fnames = []
    if 'up_file_names' in request.session:
        print("fnames found in session")
        fnames = request.session["up_file_names"]
    
    fnames.append(fname)
    request.session["fnames"] = fnames

    default_storage.save('fh/static/fh/img/tmp/' + fname, ContentFile(file.read()))
    #path = "/" + path.split("/", 1)[1]; 
    return HttpResponse(json.dumps(fname), content_type="application/json") 


def long_view(request):
    template = loader.get_template('fh/long_view.html')
    context = {
        'x': 'y',
    }
    return HttpResponse(template.render(context, request))

#-------------------------------------------
def script(request):
    #eup = eu.EntryUploader()
    #eup.upload()
    #eup.uploadHandwriting()
    #wg = w.WikiGet()
    #hc = wg.GetHumansContaining("Einstein")
    #return HttpResponse(str(hc))

    m.ENTRY.objects.get(pk=955).delete()
    return HttpResponse("ok")


#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
def search_name_service(request):
    name_part = request.GET.get("name_part")
    
    wg = w.WikiGet()
    hc = wg.GetHumansContaining(name_part)
    print(hc)
    
    
    print("-----------------------------------------")
    entries = m.ENTRY.objects.all().order_by('pk').filter(Q(description__icontains=name_part))
    wlDesc = list(entries.values_list('wiki_link', 'description'))
    print( wlDesc)
    
    mrg = hc.copy()
    mrg.update(wlDesc)
    print("-----------------------------------------")
    print(mrg) 
    return HttpResponse(json.dumps(mrg), content_type="application/json")

