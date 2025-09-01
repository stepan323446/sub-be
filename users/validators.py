from rest_framework import serializers

from project.settings_context import CODE_PATTERN_PLACEHOLDER
from .models import VerificationCode

def validate_url_code_pattern(value):
    if CODE_PATTERN_PLACEHOLDER not in value:
        raise serializers.ValidationError({'url_to_recovery': f'The line should have a space for inserting the verification code. For example: https://example.com/reset-password/{CODE_PATTERN_PLACEHOLDER}/'})
    
def validate_verification_code(code, purpose):
    verification_code = VerificationCode.objects.filter(code=code, purpose=purpose).first()
        
    if not verification_code:
        raise serializers.ValidationError({'verification_code': 'Verification code does not exists.'})
    
    if not verification_code.is_available:
        raise serializers.ValidationError({'verification_code': 'The verification code has expired.'})