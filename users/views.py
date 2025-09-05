from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from project.settings_context import ACTIVATION_PATTERN_URL_FRONTEND, RESET_PASS_PATTERN_URL_FRONTEND
from project.serializers import DetailSerializer, EmptySerializer
from .models import User
from .serializers import *
from .utils import *
from .filters import *

@extend_schema(tags=["Auth"])
class MyTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=["Auth"])
class MyTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=["Auth"])
class MyTokenVerifyView(TokenVerifyView):
    pass

@extend_schema(tags=["Auth"],
               description="Authenticate using email and password to receive Access and Refresh tokens",
               responses=TokenObtainPairSerializer,
               request=EmailTokenObtainPairSerializer)
class LoginView(APIView):
    def post(self, request: Request, format=None):
        serializer = EmailTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if not email or not password:
            return Response({'detail': 'Email and password required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'User is not found'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            activationCode = VerificationCode.generate_code(user, 'registration_confirm')
            send_activation_user_email(activationCode, ACTIVATION_PATTERN_URL_FRONTEND)

            return Response({'detail': 'The user has not been activated. A new activation link has been sent to email.'},status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({'detail': 'Incorrect password entered.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

@extend_schema(tags=["Auth"],
               description="Allows new users to sign up by providing their details.",
               responses=DetailSerializer,
               request=UserRegistrationSerializer)
class RegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = serializer.save()

        verificationCode = VerificationCode.generate_code(user, 'registration_confirm')

        send_activation_user_email(verificationCode, ACTIVATION_PATTERN_URL_FRONTEND)

        return Response(
            {"detail": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )

@extend_schema(tags=["Auth"],
               description="Activation of a new user using a verification code.",
               responses=DetailSerializer,
               request=ActivateUserSerializer)
class ActivateUserView(APIView):
    def post(self, request: Request, format=None):
        serializer = ActivateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['verification_code']
        verificationCode = VerificationCode.objects.select_related('user').get(code=code)
        user = verificationCode.user

        user.is_active = True
        user.save()
        verificationCode.is_used = True
        verificationCode.save()

        return Response({'detail': 'The user has been successfully activated.'})

@extend_schema(tags=["Auth"],
               description="Generate a verification code for reset password and send on user email.",
               responses={201: DetailSerializer},
               request=ForgotPasswordSerializer)
class ForgotPasswordView(APIView):
    def post(self, request: Request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_code: VerificationCode = serializer.save()

        send_forgot_passwoord_email(verification_code, RESET_PASS_PATTERN_URL_FRONTEND)

        return Response(
            {"detail": "Verification code was registered successfully."},
            status=status.HTTP_201_CREATED
        )

@extend_schema(tags=['Auth'], 
               description='Resets the user\'s password using a valid verification code.',
               responses=DetailSerializer,
               request=ResetPasswordSerializer)
class ResetPasswordView(APIView):
    def post(self, request: Request, format=None):
        resetPassword = ResetPasswordSerializer(data=request.data)
        resetPassword.is_valid(raise_exception=True)

        password = resetPassword.validated_data['new_password']
        code = resetPassword.validated_data['verification_code']

        verificationCode = VerificationCode.objects.filter(code=code).select_related('user').first()
        verificationCode.is_used = True
        verificationCode.save()

        user = verificationCode.user
        user.set_password(password)
        user.save()

        send_reset_password_complete_email(user)

        return Response({'detail': 'The password has been successfully changed.'})

    
@extend_schema(tags=['Auth'], 
               description='Checks whether the provided verification code is valid and can be used.',
               responses={200: DetailSerializer, 404: DetailSerializer, 400: DetailSerializer},
               request=VerificationCodeVerifySerializer)
class VerificationCodeVerify(APIView):
    def post(self, request: Request, format=None):
        serializer = VerificationCodeVerifySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        return Response({'detail': 'The verification code is valid'})


@extend_schema(tags=["Users"], 
               description="Retrieve or update the current user's profile.",
               responses=UserSerializer)
class UserInfoView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

@extend_schema(tags=['Users'],
               description="Allows an authenticated user to change their e-mail. Requires the password to confirm and new email",
               request=ChangeEmailSerializer,
               responses=DetailSerializer)
class ChangeEmailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request: Request, format=None):
        user: User = request.user
        serializer = ChangeEmailSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user.email = serializer.validated_data['new_email']
        user.save()

        return Response({"detail": "The e-mail was changed successfully."})

@extend_schema(tags=['Users'], 
               description="Allows an authenticated user to change their password. Requires the old, repeat old and new passwords.",
               request=ChangePasswordSerializer,
               responses=DetailSerializer)
class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request, format=None):
        user: User = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "The password was changed successfully."})

@extend_schema(tags=['Admin'],
               description="Create, Read, Update, and Delete operations for user management")
class AdminUserInfo(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAdminSerializer
    queryset = User.objects.all()
    permission_classes = [ permissions.IsAdminUser ]

@extend_schema(tags=['Admin'],
               description="Retrieve a paginated list of all registered users")
class AdminUserList(ListAPIView):
    serializer_class = UserAdminSerializer
    permission_classes = [ permissions.IsAdminUser ]
    search_fields = ['username', 'email']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']

    def get_queryset(self):
        return User.objects.all()

@extend_schema(tags=['Admin'],
               description="Change password of user without restrictions",
               request=ChangeAdminPasswordSerializer,
               responses=DetailSerializer)
class AdminChangePassword(APIView):
    permission_classes = [ permissions.IsAdminUser ]

    def post(self, request: Request, pk=None, format=None):
        new_pass = request.data.get('new_password')
        user = get_object_or_404(User, pk=pk)

        user.set_password(new_pass)
        user.save()
        return Response({'detail': 'The password was changed successfully.'})

@extend_schema(tags=["Admin"],
               description="Authorization using user ID for admin panel access",
               responses=TokenObtainPairSerializer,
               request=EmptySerializer)
class AdminLoginAsUser(APIView):
    permission_classes = [ permissions.IsAdminUser ]

    def post(self, request: Request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })