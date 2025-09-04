from django.urls import reverse_lazy

from project.utils import StrAPITestCase
from .models import Label, PaymentMethodType, PaymentMethod

# Create your tests here.
class LabelTest(StrAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.label_1 = Label.objects.create(name="Test Label", colorHex="#ff5151", user=cls.user)
        cls.label_2 = Label.objects.create(name="Music", colorHex="#008115", user=cls.user)

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
        url = reverse_lazy('tax-label', kwargs={'pk': self.label_1.pk})

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_patch_label(self):
        self.authorize()
        url = reverse_lazy('tax-label', kwargs={'pk': self.label_2.pk})

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

class PaymentMethodTest(StrAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.paytype_pp = PaymentMethodType.objects.create(type="PayPal", icon="card-types/pp.png")
        cls.paytype_visa = PaymentMethodType.objects.create(type="VISA", icon="card-types/visa.png")
        cls.alt_bank_payment = PaymentMethod.objects.create(name="AltBank", type=cls.paytype_visa, user=cls.user)

    def test_add_payment(self):
        self.authorize()
        url = reverse_lazy('tax-pay-new')
        response = self.client.post(url, data={
            "name": "RameonBank",
            "type": self.paytype_visa.pk
        })

        self.assertEqual(response.status_code, 201)

    def test_search_payment(self):
        self.authorize()
        url = reverse_lazy('tax-pay-list')
        response = self.client.get(path=url, QUERY_STRING='search=alt')
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['count'], 1)

    def test_delete_payment(self):
        self.authorize()
        url = reverse_lazy('tax-pay', kwargs={'pk': self.alt_bank_payment.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_get_payment(self):
        self.authorize()
        url = reverse_lazy('tax-pay', kwargs={'pk': self.alt_bank_payment.pk})
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['name'], self.alt_bank_payment.name)