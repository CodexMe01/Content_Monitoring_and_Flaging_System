from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Keyword, ContentItem, Flag

class ContentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.keyword1 = Keyword.objects.create(name='badword')
        self.keyword2 = Keyword.objects.create(name='scam')

    def test_create_keyword(self):
        url = reverse('keyword-list-create')
        data = {'name': 'spam'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Keyword.objects.count(), 3)
        self.assertEqual(Keyword.objects.get(name='spam').name, 'spam')

    def test_scan_content_and_score(self):
        url = reverse('scan-content')
        data = [
            {
                "title": "A new badword appears",
                "source": "NewsSource",
                "body": "Nothing much here.",
                "last_updated": "2023-10-01T12:00:00Z"
            },
            {
                "title": "scam",
                "source": "DirectSource",
                "body": "This is a scam right here.",
                "last_updated": "2023-10-01T12:05:00Z"
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        
        
        flags = Flag.objects.all()
        self.assertEqual(flags.count(), 2)
        
        
        badword_flag = flags.get(keyword=self.keyword1)
        self.assertEqual(badword_flag.score, 70)
        
        
        scam_flag = flags.get(keyword=self.keyword2)
        self.assertEqual(scam_flag.score, 100)

    def test_suppression_logic(self):
        url = reverse('scan-content')
        data1 = {
            "title": "testing scam",
            "source": "Source1",
            "body": "this has a scam inside.",
            "last_updated": "2023-10-01T12:00:00Z"
        }
        self.client.post(url, [data1], format='json')
        
        flag = Flag.objects.get(keyword=self.keyword2)
        self.assertEqual(flag.status, 'pending')
        
       
        flag.status = 'irrelevant'
        flag.save()
        
        
        self.client.post(url, [data1], format='json')
        flag.refresh_from_db()
        self.assertEqual(flag.status, 'irrelevant') 
        
        data2 = {
            "title": "testing scam",
            "source": "Source1",
            "body": "this has a scam inside and more.",
            "last_updated": "2023-10-02T12:00:00Z"
        }
        self.client.post(url, [data2], format='json')
        flag.refresh_from_db()
        self.assertEqual(flag.status, 'pending') 
