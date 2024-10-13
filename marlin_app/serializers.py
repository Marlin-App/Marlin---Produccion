import json
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Store, StoreItem, StoreType, ItemTag, AtributeValue, Atribute, ItemVariation
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
    
        #extraer los attibutes
        atributes_data = self.context['request'].data.get('attributes')
        if atributes_data:
            atributes_data = json.loads(atributes_data)

        #crear el item
        store_item = StoreItem.objects.create(**validated_data)
        
        print(atributes_data)
        for variation_data in atributes_data:
            #por cada objeto dentro de atributes obtener los datos para crear la variacion
            attibute_value_list = variation_data.get('attribute_values')
            stock = variation_data.get('stock')

            #Crear la variacion
            item_variation = ItemVariation.objects.create(
                store_item = store_item,
                stock = stock
            )

            # lista de atributos que llevara esa variacion
            attribute_value_instances = []
            for attr_data in attibute_value_list:
                attr_name = attr_data['name']
                attr_value = attr_data['value']

                #obtener la instancia del nombre del attribute
                atribute, created = Atribute.objects.get_or_create(name=attr_name)

                #crear el attribute value
                attribute_value, created = AtributeValue.objects.get_or_create(
                    attribute=atribute,
                    value=attr_value
                )

                # añadir a la lista de attributos que tendra la variacion 
                attribute_value_instances.append(attribute_value)

            # meterle los atributos a la variacion
            item_variation.attribute_values.set(attribute_value_instances)
        return store_item

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['picture'].startswith('image/upload/'):
            representation['picture'] = representation['picture'].replace('image/upload/', '')
        return representation
    
class AtributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')

    class Meta:
        model = AtributeValue
        fields = ['attribute_name', 'value']


class ItemVariationSerializer(serializers.ModelSerializer):
    attribute_values = AtributeValueSerializer(many=True)

    class Meta:
        model = ItemVariation
        fields = ['id', 'stock', 'attribute_values']


class ItemViewSerializer(serializers.ModelSerializer):
    variations = ItemVariationSerializer(many=True, read_only=True)

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image'].startswith('image/upload/'):
            representation['image'] = representation['image'].replace('image/upload/', '')
        if representation['image_selected'].startswith('image/upload/'):
            representation['image_selected'] = representation['image_selected'].replace('image/upload/', '')
        return representation

class StoreItemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTag
        fields = '__all__'

class AtributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributeValue
        fields = '__all__'



