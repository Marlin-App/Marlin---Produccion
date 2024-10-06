from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Store, StoreItem, StoreType, ItemTag
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Registrar un usuario

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user = user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'picture']

    #sobreescribir el metodo update
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for arrt, value in user_data.items():
                setattr(instance.user, arrt, value)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.user.save()
        instance.save()
        return instance

    # def update(self, instance, validated_data):

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        #Datos extras al token
        token['username'] = user.username
        token['email'] = user.email
        token['userprofile'] = user.userprofile.id
        
        # Devuelve el token
        return token

#Serializador para comunicar datos por medio de json
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['picture'].startswith('image/upload/'):
            representation['picture'] = representation['picture'].replace('image/upload/', '')
        if representation['banner'].startswith('image/upload/'):
            representation['banner'] = representation['banner'].replace('image/upload/', '')
        return representation

class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['picture'].startswith('image/upload/'):
            representation['picture'] = representation['picture'].replace('image/upload/', '')
        return representation

class StoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreType
        fields = '__all__'

class StoreItemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTag
        fields = '__all__'

