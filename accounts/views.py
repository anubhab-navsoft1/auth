from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
# from django_otp.plugins.otp_totp.models import TOTPDevice
from .serializers import LoginSerializer, CustomUserSerializers
from .custom_backend import CustomEmailBackend
from .models import CustomUser, OTP
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.conf import settings

class CreateRegistrationApiView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializers

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                password = request.data.get('password')
                user.set_password(password)
                user.save()

                return Response({
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginAPIView(GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            otp_instance = OTP.objects.create(user=user, otp=otp)

            send_mail(
                'Your OTP for login',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP has been sent to your email'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
class OTPVerifyApiView(GenericAPIView):
    
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            otp_obj = OTP.objects.filter(user=user).order_by('-created_at').first()
            if otp_obj and otp_obj.otp == otp_entered:
                # Delete OTP record as it's been verified
                user.is_logged_in = True
                otp_obj.delete()

                # Generate JWT token upon successful OTP verification
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                send_mail(
                    'OTP validation Successful',
                    f'{user.username} are successfully logged in',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                # custom_email_backend = CustomEmailBackend()
                # custom_email_backend.send_otp_verification_email(user.email, access_token)
                return Response({"message": "OTP verification successful", "access_token": access_token, "refresh_token" : str(refresh), "data" : user.is_logged_in}, status=status.HTTP_200_OK)
        
        # If OTP verification fails or user not found
        return Response({"error": "Invalid OTP or email"}, status=status.HTTP_400_BAD_REQUEST)
    

    

class DeleteAllUsersAPIView(GenericAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            num_deleted, _ = CustomUser.objects.all().delete()
            return Response({'message': f'{num_deleted} users deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)