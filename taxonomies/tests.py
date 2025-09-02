from django.urls import reverse_lazy

from project.utils import StrAPITestCase
from .models import Label

# Create your tests here.
class LabelTest(StrAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.label = Label.objects.create(name="Test Label", colorHex="#ff5151", user=cls.user) # 1
        cls.label = Label.objects.create(name="Music", colorHex="#008115", user=cls.user) # 2

    def test_create_label_incorrect_color(self):
        self.authorize()
        url = reverse_lazy('tax-label-new')

        response = self.client.post(path=url, data={
            'name': 'IT',
            'colorHex': 'blue'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_label_success(self):
        self.authorize()
        url = reverse_lazy('tax-label-new')

        response = self.client.post(path=url, data={
            'name': 'IT',
            'colorHex': "#230aff"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_label(self):
        self.authorize()
        url = reverse_lazy('tax-label', kwargs={'pk': 2})

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_patch_label(self):
        self.authorize()
        url = reverse_lazy('tax-label', kwargs={'pk': 2})

        response = self.client.patch(path=url, data={
            'name': 'Games'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_search_list(self):
        self.authorize()
        url = reverse_lazy('tax-label-list')
        response = self.client.get(path=url, QUERY_STRING='search=music')
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['count'], 1)