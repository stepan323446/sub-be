from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from currency.serializers import CurrencySerializer
from .models import User, VerificationCode
from .validators import validate_verification_code

class EmailTokenObtainPairSerializer(serializers.Serializer):
    email               = serializers.EmailField()
    password            = serializers.CharField(max_length=100)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password            = serializers.CharField(write_only=True, validators=[validate_password])
    password2           = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(is_active=False, **validated_data)
        return user
    
    
class VerificationCodeVerifySerializer(serializers.Serializer):
    verification_code    = serializers.CharField(max_length=150)
    purpose              = serializers.ChoiceField(choices=VerificationCode.PURPOSE_CHOICES)
    
    def validate(self, attrs):
        validate_verification_code(attrs['verification_code'], attrs['purpose'])
        return attrs
        
    
class ForgotPasswordSerializer(serializers.Serializer):
    email               = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError({"email": "User is not exists."})
        self.user = user
        
        return value
    
    def create(self, validated_data):
        purpose = 'password_reset'
        if not self.user.is_active:
            raise serializers.ValidationError({"non_field_errors": ["User is not active."]})

        verificationCode = VerificationCode.generate_code(self.user, purpose)
        return verificationCode
    
class ResetPasswordSerializer(serializers.Serializer):
    verification_code    = serializers.CharField(max_length=150)
    new_password         = serializers.CharField(max_length=50, validators=[validate_password])

    def validate(self, attrs):
        validate_verification_code(attrs['verification_code'], 'password_reset')
        return attrs
    
class ActivateUserSerializer(serializers.Serializer):
    verification_code    = serializers.CharField(max_length=150)

    def validate(self, attrs):
        validate_verification_code(attrs['verification_code'], 'registration_confirm')
        return attrs

class UserSerializer(serializers.ModelSerializer):
    username            = serializers.CharField()
    email               = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'limit', 'currency', 'is_monday_first', 'notification_email_enable', 'news_email_enable')

class UserAdminSerializer(serializers.ModelSerializer):
    username            = serializers.CharField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'limit', 'currency', 'is_monday_first', 'notification_email_enable', 'news_email_enable')

class ChangePasswordSerializer(serializers.Serializer):
    old_password            = serializers.CharField(write_only=True, max_length=100)
    new_password            = serializers.CharField(write_only=True, max_length=100)
    repeat_new_password     = serializers.CharField(write_only=True, max_length=100)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['repeat_new_password']:
            raise serializers.ValidationError({"repeat_new_password": "The passwords do not match the original"})
        return attrs

    def validate_old_password(self, value):
        user: User = self.context['request'].user
        
        if not user.check_password(value):
            raise serializers.ValidationError("You have entered an incorrect old password")
        
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value
    
class ChangeAdminPasswordSerializer(serializers.Serializer):
    new_password            = serializers.CharField(write_only=True, max_length=100)

class ChangeEmailSerializer(serializers.Serializer):
    new_email               = serializers.EmailField(write_only=True)
    password                = serializers.CharField(write_only=True, max_length=100)

    def validate_password(self, value):
        user: User = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("You have entered an incorrect password")
        
        return value