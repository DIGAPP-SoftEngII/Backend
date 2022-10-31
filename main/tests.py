from rest_framework.test import RequestsClient
from django.test import TestCase
from .models import Business
import datetime

# Django Testing on Model Functions
class BusinessTest(TestCase):
 """ Test module for Business model """

def setUp(self):
    Business.objects.create(
        name='WeWork Calle 11b', opening_time=datetime.time(8, 0, 0), 
            closing_time=datetime.time(8, 0, 0), city=1, 
            type='Co-working', address='Calle 11b #99-72',
            capacity = 450, internet_quality = 4.8,
            rating = 4.3, description = 'Most visited WeWork in Bogota',
            telephone_number=None, cover_picture = None)
    

def test_puppy_breed(self):
    weWork11b = Business.objects.get(name='WeWork Calle 11b')
    
    self.assertEqual(
        weWork11b.city, 1)
       


# client = RequestsClient()
# response = client.get('http://testserver/users/')
# assert response.status_code == 200