from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializers
from django.db import transaction
from django.contrib.auth import authenticate

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
        
class LogInView(GenericAPIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "data": {
                        "access_token": access_token,
                        "refresh_token": str(refresh),
                        "user_info": {"username": user.username} 
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"errors": "Incorrect username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"errors": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)


    

    