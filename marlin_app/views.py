from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

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
