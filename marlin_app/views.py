from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail

class RegisterUserAPIView(APIView):
    #permite a los no logeados usar esto
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            #llama al metodo necesario dentro del serializer y se guarda el usuario creado
            user = serializer.save()
            #se genera el refresh token con el usuario creado
            # refresh  = RefreshToken.for_user(user)
            token_serializer = CustomTokenObtainPairSerializer()
            token_data = token_serializer.get_token(user)
            #Se envia la respuesta positiva y los tokens del usuario creado
            return Response({"message": "Usuario creado correctamente",
                             "refresh": str(token_data),
                             "access": str(token_data.access_token),
                            #  "username": user.username,
                            #  "email": user.email
                             }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Recover password 
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

            reset_url = f"marlin-app://reset-password/{uid}/{token}/"

            # Send email to the user
            send_mail(
                'Restablecer contraseña',
                f'Usa el siguiente enlace para restablecer tu contraseña: {reset_url}',
                'tu-email@gmail.com',  # De
                [user.email],  # Para
                fail_silently=False,
            )
            return Response({"message": "Se ha enviado un correo para restablecer la contraseña"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = {
            'uidb64': kwargs['uidb64'],
            'token': kwargs['token'],
            'new_password': request.data.get('new_password')  # Cambia 'password' a 'new_password'
        }
        serializer = PasswordResetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Aquí no es necesario pasar validated_data, ya que se guarda internamente.
            return Response({"message": "Contraseña restablecida correctamente"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
