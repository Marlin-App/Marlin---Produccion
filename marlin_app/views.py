import threading
import pytz
from datetime import datetime
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DeliveryOrder, DeliveryProfile, Order, Store
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os
import asyncio
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
import googlemaps
load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('API_KEY_GOOGLE'))

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
    
def redirect_view (request, *args, **kwargs):
    data = {
            'uid': kwargs['uidb64'],
            'token': kwargs['token'],
        }
    return render(request, 'redirect.html', data)
    
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

            reset_url = f"https://marlin-desarrollo.vercel.app/api/redirect/{uid}/{token}/"

            html_message = render_to_string('reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })

            subject = 'Restablecer contraseña'
            from_email = 'marlin.aplicacion@gmail.com'
            to = [user.email]

            msg = EmailMultiAlternatives(subject, '', from_email, to)
            msg.attach_alternative(html_message, "text/html")  # Adjuntar el contenido HTML
            
            msg.send()
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
    
class DeleteAccount(APIView):

    def delete(self, request):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        user.delete()
        return Response({"message": "Cuenta eliminada correctamente"}, status=status.HTTP_200_OK)
    
class AcceptOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        print("--------------realizo la fundin-------------------")
        try:
            order_id = request.data.get('order_id')
            order = Order.objects.get(id=order_id)
            order.status = 'Buscando repartidor'
            order.save()
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

        store = order.store_id        

        deliveries = DeliveryProfile.objects.all()

        delivery_coords = []
        for delivery in deliveries:

            coords = tuple(float(value) for value in delivery.coordinates.split(","))
            delivery_coords.append(coords)

        store_coords = [float(value) for value in store.coodernates.split(",")]

        matrix_result = gmaps.distance_matrix(
            origins=[store_coords],
            destinations=delivery_coords,
            mode="driving"
        )
        distances = matrix_result["rows"][0]["elements"]
        deliveries_with_distance = [
            (delivery, distances[i]["distance"]["value"] / 1000)
            for i, delivery in enumerate(deliveries)
                if distances[i]["status"] == "OK"
        ]
        deliveries_with_distance.sort(key=lambda x: x[1])
        deliveries_organized = [delivery[0] for delivery in deliveries_with_distance[:10]]
        # deliveries_organized = [
        #     {"id": delivery.id, "name": delivery.user_id.first_name}  # Incluye los atributos necesarios
        #     for delivery, _ in deliveries_with_distance[:10]
        # ]
        thread = threading.Thread(target=self.assign_order_to_deliveries, args=(order, deliveries_organized))
        thread.start()
        return Response({"message": "Orden lista, buscando repartidor"}, status=status.HTTP_200_OK)
       
    def assign_order_to_deliveries(self, order, deliveries):
        for delivery in deliveries:
            assigned = asyncio.run(self.try_assing_order(order, delivery))
            if assigned:
                print('si se asigno')
                break
            else:
                print('no se asigno')

    async def try_assing_order(self, order, delivery):
        print('entro a try')
        delivery_order = await sync_to_async(DeliveryOrder.objects.create, thread_sensitive=True)(
            delivery_id=delivery,
            order_id=order,
            assigned_at=datetime.now(pytz.timezone("America/Costa_Rica")),
            status='Pendiente'
        )
        print('creo el resto')

        accepted = await self.wait_for_acceptance(delivery_order, timeout=120)
        return accepted
        
    async def wait_for_acceptance(self, delivery_order, timeout):
        print('continuo')
        for _ in range(int(timeout / 5)):
            print('espero')
            await asyncio.sleep(5)
            await sync_to_async(delivery_order.refresh_from_db, thread_sensitive=True)()
            if delivery_order.status == 'Aceptada':
                return True
        await sync_to_async(delivery_order.delete, thread_sensitive=True)()
        return False

class AcceptDeliveryOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            delivery_order_id = request.data.get('delivery_order_id')
            delivery_order = DeliveryOrder.objects.get(id=delivery_order_id)
            if delivery_order.status == 'Pendiente':
                delivery_order.status = 'Aceptada'
                delivery_order.save()
                delivery_order.order_id.status = 'En camino'
                delivery_order.order_id.delivery_id = delivery_order.delivery_id.user_id
                delivery_order.order_id.save()
                return Response({"message": "Orden de reparto aceptada"}, status=status.HTTP_200_OK)
        except DeliveryOrder.DoesNotExist:
            return Response({'error': 'Delivery Order not found'}, status=404)
        return Response({"message": "algo ha salido mal"}, status=status.HTTP_200_OK)
        
