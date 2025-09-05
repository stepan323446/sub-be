from django.urls import reverse_lazy
from unittest.mock import Mock, patch
from project.utils import StrAPITestCase

from .models import Service

# Create your tests here.
class ServiceTest(StrAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Fake Storage
        cls.storage_save_patcher = patch("django.core.files.storage.FileSystemStorage.save")
        cls.mock_save = cls.storage_save_patcher.start()
        cls.mock_save.return_value = "fake.jpg"

        # Fake GET to google api
        cls.requests_get_patcher = patch("services.models.requests.get")
        mock_get = cls.requests_get_patcher.start()
        mock_get.return_value = Mock(status_code=200, content=b"fake image")

        cls.spotify = Service.objects.create(name="Spotify", url="https://spotify.com", user=cls.user)
    
    @classmethod
    def tearDown(cls):
        cls.storage_save_patcher.stop()
        cls.requests_get_patcher.stop()
        super().tearDown(cls)

    def test_create_service_success(self):
        self.authorize()
        url = reverse_lazy('service-new')
        
        response = self.client.post(url, data={
            "name": "Deezer",
            "url": "https://deezer.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_service(self):
        self.authorize()
        url = reverse_lazy('service', kwargs={'pk': self.spotify.pk})

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_patch_service(self):
        self.authorize()
        url = reverse_lazy('service', kwargs={'pk': self.spotify.pk})

        response = self.client.patch(path=url, data={
            'name': 'Deezer'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_search_services(self):
        self.authorize()
        url = reverse_lazy('service-list')
        response = self.client.get(path=url, QUERY_STRING='search=spot')
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['count'], 1)