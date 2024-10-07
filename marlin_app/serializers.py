import json
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Store, StoreItem, StoreType, ItemTag, AtributeValue, Atribute
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
    def create(self, validated_data):

        print(validated_data)

        #obtener el objeto atributos y quitarlo de validated_data
        atributes_data = self.context['request'].data.get('atributes')
        if atributes_data:
            atributes_data = json.loads(atributes_data)
        #crear el item
        print(f'hola {atributes_data}')
        store_item = StoreItem.objects.create(**validated_data)
        for attr_name, attr_value in atributes_data.items():

            attribute, created = Atribute.objects.get_or_create(name=attr_name)

            AtributeValue.objects.create(
                attribute = attribute,
                storeItem = store_item,
                value = attr_value
            )
        return store_item


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

class AtributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributeValue
        fields = '__all__'



