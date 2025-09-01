from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .settings_context import DEFAULT_FROM_EMAIL

User = get_user_model()

class StrAPITestCase(APITestCase):
    url = None

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.setUpUser()
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)

    @classmethod
    def setUpUser(cls):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def get_user_info(self):
        user_info_url = reverse('user-info')
        response = self.client.get(user_info_url)
        return response.data
    
    def authorize(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


def send_email_template(subject, to, html_content, html_content_alt, context):
    html_content = render_to_string(html_content, context)
    html_content_alt = render_to_string(html_content_alt, context)

    email = EmailMultiAlternatives(subject, html_content_alt, DEFAULT_FROM_EMAIL, [to])
    email.attach_alternative(html_content, "text/html")
    email.send()