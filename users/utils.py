from .models import VerificationCode, User

from project.settings_context import CODE_PATTERN_PLACEHOLDER
from project.utils import send_email_template



def send_forgot_passwoord_email(verification_code: VerificationCode, url_pattern: str):
    subject = 'Reset password'
    user = verification_code.user
    url_to_recovery = url_pattern.replace(CODE_PATTERN_PLACEHOLDER, verification_code.code)

    template_context = {
        'username': user.username,
        'url_to_recovery': url_to_recovery
    }
    
    send_email_template(subject, 
                        user.email, 
                        "auth/email_reset_password.html",
                        "auth/email_reset_password_alt.html",
                        template_context)
    
def send_reset_password_complete_email(user: User):
    subject = 'Reset password completed'

    template_context = {
        'username': user.username
    }
    
    send_email_template(subject,
                        user.email,
                        'auth/email_reset_password_success.html',
                        'auth/email_reset_password_success_alt.html',
                        template_context
                        )
    
def send_activation_user_email(verification_code: VerificationCode, url_pattern: str):
    subject = 'Account activation'
    user = verification_code.user
    url_to_activate = url_pattern.replace(CODE_PATTERN_PLACEHOLDER, verification_code.code)

    template_context = {
        'username': user.username,
        'url_to_activate': url_to_activate
    }

    send_email_template(subject,
                        user.email,
                        'auth/email_account_activation.html',
                        'auth/email_account_activation_alt.html',
                        template_context
                        )