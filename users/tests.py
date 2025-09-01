from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from project.settings_context import CODE_PATTERN_PLACEHOLDER
from project.utils import StrAPITestCase
from .models import VerificationCode

User = get_user_model()

class UserInfoTest(StrAPITestCase):
    url = reverse_lazy('user-info')

    def test_user_info_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_user_info_authorized(self):
        self.authorize()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_info_disable_is_monday_first(self):
        self.authorize()
        response = self.client.patch(self.url, data={
            'is_monday_first': False
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.is_monday_first)


class ChangeEmailTest(StrAPITestCase):
    url = reverse_lazy('change-email')

    def test_invalid_pass(self):
        self.authorize()
        response = self.client.post(path=self.url, data={
            'new_email': 'new@example.com',
            'password': 'invalid_password'
        })

        self.assertEqual(response.status_code, 400)

    def test_successful_change(self):
        self.authorize()
        response = self.client.post(path=self.url, data={
            'new_email': 'new@example.com',
            'password': 'testpassword123'
        })
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.email, 'new@example.com')

class ChangePasswordTest(StrAPITestCase):
    url = reverse_lazy('change-password')

    NEW_PASSWORD = 'NSej2pF64anb'

    def test_invalid_old_pass(self):
        self.authorize()
        response = self.client.post(path=self.url, data={
            'old_password': 'invalid_password',
            'new_password': self.NEW_PASSWORD,
            'repeat_new_password': self.NEW_PASSWORD,
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_easy_pass(self):
        self.authorize()
        response = self.client.post(path=self.url, data={
            'old_password': 'testpassword123',
            'new_password': '123456789',
            'repeat_new_password': '123456789',
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_repeated_pass(self):
        self.authorize()
        response = self.client.post(path=self.url, data={
            'old_password': 'testpassword123',
            'new_password': self.NEW_PASSWORD,
            'repeat_new_password': 'something_else',
        })
        self.assertEqual(response.status_code, 400)

    def test_successful_change(self):
        self.authorize()
        response = self.client.post(path=self.url, data={
            'old_password': 'testpassword123',
            'new_password': self.NEW_PASSWORD,
            'repeat_new_password': self.NEW_PASSWORD,
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password(self.NEW_PASSWORD))

class LoginTest(StrAPITestCase):
    url = reverse_lazy('login')

    def test_invalid_email(self):
        response = self.client.post(path=self.url, data={
            'email': 'invalid@example.com',
            'password': '1234'
        })
        self.assertEqual(response.status_code, 401)

    def test_invalid_password(self):
        response = self.client.post(path=self.url, data={
            'email': 'test@example.com',
            'password': '1234'
        })
        self.assertEqual(response.status_code, 401)

    def test_success_authorization(self):
        response = self.client.post(path=self.url, data={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 200)

class RegisterTest(StrAPITestCase):
    url = reverse_lazy('register')

    USERNAME = 'olaf'
    EMAIL = 'olaf@gmail.com'
    PASSWORD = 'NSej2pF64anb'

    def test_exist_user(self):
        response = self.client.post(path=self.url, data={
            "username": "testuser",
            "email": "test@example.com",
            "password": self.PASSWORD,
            "password2": self.PASSWORD,
        })
        self.assertEqual(response.status_code, 400)

    def test_easy_password(self):
        response = self.client.post(path=self.url, data={
            "username": self.USERNAME,
            "email": self.PASSWORD,
            "password": "1234",
            "password2": "1234",
        })
        self.assertEqual(response.status_code, 400)

    def test_successful_registration(self):
        response = self.client.post(path=self.url, data={
            "username": self.USERNAME,
            "email": self.EMAIL,
            "password": self.PASSWORD,
            "password2": self.PASSWORD,
        })
        user = User.objects.filter(username=self.USERNAME).first()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(user.check_password(self.PASSWORD))

        
class ForgotPasswordTest(StrAPITestCase):
    url = reverse_lazy('forgot-password')

    def test_invalid_email(self):
        response = self.client.post(path=self.url, data={
            "email": "invalid@example.com"
        })

        self.assertEqual(response.status_code, 400)
    
    def test_success_email(self):
        response = self.client.post(path=self.url, data={
            "email": "test@example.com"
        })

        self.assertEqual(response.status_code, 201)

class ResetPasswordTest(StrAPITestCase):
    url = reverse_lazy('reset-password')
    NEW_PASSWORD = 'NSej2pF64anb'

    def setUp(self):
        forgot_password = reverse_lazy('forgot-password')
        self.client.post(path=forgot_password, data={
            "email": "test@example.com",
        })
        self.reset_code = VerificationCode.objects.first().code

    def test_invalid_reset_code(self):
        response = self.client.post(path=self.url, data={
            "verification_code": '12345',
            "new_password": self.NEW_PASSWORD
        })
        
        self.assertEqual(response.status_code, 400)

    def test_simple_password(self):
        response = self.client.post(path=self.url, data={
            "verification_code": self.reset_code,
            "new_password": '12345'
        })
        
        self.assertEqual(response.status_code, 400)

    def test_successful_change(self):
        response = self.client.post(path=self.url, data={
            "verification_code": self.reset_code,
            "new_password": self.NEW_PASSWORD
        })
        self.user.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password(self.NEW_PASSWORD))
