'''
Created on Jun 8, 2017

@author: albert
'''
#import unittest
from django.test import TestCase
from .. import models as m

class FHUSERTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)

    def testFHUSERCreate(self):
        m.FHUSER.objects.create(first_name='Albert', last_name = 'Greinöcker', email = 'albert@xyz.com', password='1234')


