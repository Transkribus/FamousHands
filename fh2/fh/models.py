from django.db import models


class FHUSER(models.Model):
    '''
    Storage of user-data taken from Transcribus
    '''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30) #TODO: use as PK or at least unique key 
    password = models.CharField(max_length=30)


class LOCATION(models.Model):
    '''
    Storage of a certain map position
    '''
    lat= models.DecimalField(decimal_places=4, max_digits=12) 
    lng= models.DecimalField(decimal_places=4, max_digits=12)
    label=models.CharField(max_length=30)


class ENTRY(models.Model):
    '''
    Storage of a Wikidata-Entry
    '''
    wiki_link = models.CharField(max_length=128, null=True) #saves just the wiki-id (Q-id) of the entry
    description = models.CharField(max_length=128)
    image = models.FilePathField(max_length=512) #Stored in file system
    country_citizenship = models.CharField(max_length=128)
    place_of_birth = models.ForeignKey(LOCATION, related_name='%(class)s_requests_created', on_delete=models.CASCADE)  # models.CharField(max_length=255) no location, just the name
    #date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    day_of_birth = models.IntegerField(null=True)
    month_of_birth = models.IntegerField(null=True)
    year_of_birth = models.IntegerField(null=True)
    place_of_death = models.ForeignKey(LOCATION, on_delete=models.CASCADE, blank=True, null=True)  # models.CharField(max_length=255) no location, just the name
    #date_of_death = models.DateField(auto_now=False, auto_now_add=False, null=True)
    day_of_death = models.IntegerField(null=True)
    month_of_death = models.IntegerField(null=True)
    year_of_death = models.IntegerField(null=True)
    native_lang = models.CharField(max_length=10) #TODO limit size?
    lifespan = models.IntegerField()
    unknown_date_of_death = models.BooleanField(blank=False)
    unknown_date_of_birth = models.BooleanField(blank=False)
    on = models.BooleanField(blank=False, default=True) # if false, items will not be displayed
    
class NAMEVARIANT(models.Model):
    '''
    Used by entry
    '''
    
    entry =models.ForeignKey(ENTRY, on_delete=models.CASCADE)
    lng_code = models.CharField(max_length=10) #TODO limit size?
    variant = models.CharField(max_length=128)

class HANDWRITTENIMAGE(models.Model):
    '''
    The images assigned to an entry
    '''

    entry = models.ForeignKey(ENTRY, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=128, null=True)
    date = models.DateField(auto_now_add=True)
    link = models.CharField(max_length=512, null=False) #the link to the image
    origin = models.CharField(max_length=512, null=True) #who uploaded the image
    on = models.BooleanField(blank=False, default=True) # if false, items will not be displayed
    
# class Contact(models.Model):
# 
#     first_name = models.CharField(
#         max_length=255,
#     )
#     last_name = models.CharField(
#         max_length=255,
# 
#     )
# 
#     email = models.EmailField()
# 
#     def __str__(self):
# 
#         return ' '.join([
#             self.first_name,
#             self.last_name,
#         ])

