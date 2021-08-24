from user.token_serializers import CustomTokenObtainPairSerializer
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, UserInfoSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .activation_token import account_activation_token
from django.core.mail import EmailMessage
import threading

User = get_user_model()


class ActivationEmailThread(threading.Thread):
    def __init__(self, mail_subject, message, to):
        self.mail_subject = mail_subject
        self.message = message
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMessage(self.mail_subject, self.message, to=self.to)
        email.send(fail_silently=False)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serialized_data = UserRegistrationSerializer(data=request.data)
        if serialized_data.is_valid():
            user = serialized_data.save()
            if user:
                send_user_activation_email(self, user)
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UserInfoSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserActivateSuccessTemplateView(TemplateView):
    template_name = "registration/user_activated.html"


class UserActivateInvalidTemplateView(TemplateView):
    template_name = "registration/invalid_activation.html"


def send_user_activation_email(self, user):
    domain = get_current_site(self.request).domain
    mail_subject = 'Activate your account.'
    token = account_activation_token.make_token(user)
    message = render_to_string(
        'registration/activate_user_email.html', {
            'first_name': user.first_name,
            'domain': domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
            'protocol': self.request.scheme
        })
    to_email = user.email
    ActivationEmailThread(mail_subject, message, [to_email]).start()


def activate_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('user_activated')
    else:
        return redirect('invalid_activation')
