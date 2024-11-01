import json
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, OrderItem, UserProfile, Store, StoreItem, StoreType, ItemTag, AtributeValue, Atribute, ItemVariation, ItemImage
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


# Registrar un usuario

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
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
        token['usertype'] = user.userprofile.user_type.name
        
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

    
class AtributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')

    class Meta:
        model = AtributeValue
        fields = ['attribute_name', 'value']


class ItemVariationSerializer(serializers.ModelSerializer):
    item_variations = AtributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ItemVariation
        fields = ['id', 'stock', 'item_variations']

class ItemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        # fields = '__all__'
        fields = ['id', 'picture']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['picture'].startswith('image/upload/'):
            representation['picture'] = representation['picture'].replace('image/upload/', '')
        return representation

class ListStoreItemSerializer(serializers.ModelSerializer):
    item_images = ItemImagesSerializer(many=True, read_only=True)
    class Meta:
        model = StoreItem
        fields = ['id', 'name', 'description', 'price', 'item_images']

class StoreItemSerializer(serializers.ModelSerializer):
    variations = ItemVariationSerializer(many=True, read_only=True)
    item_images = ItemImagesSerializer(many=True, read_only=True)
    class Meta:
        model = StoreItem
        fields = '__all__'  

    def to_representation(self, instance):
        """Devuelve todos los campos para la acción de retrieve"""
        # Aquí puedes agregar lógica adicional para incluir más campos según la acción
        if self.context['view'].action == 'retrieve':
            return super().to_representation(instance)
        else:
            serializer = ListStoreItemSerializer(instance)
            return serializer.data
    def create(self, validated_data):
    
        #extraer los attibutes
        atributes_data = self.context['request'].data.get('attributes')
        if atributes_data:
            atributes_data = json.loads(atributes_data)

        #crear el item
        pictures = self.context['request'].FILES.getlist('pictures')
        store_item = StoreItem.objects.create(**validated_data)
        print(pictures)
        item_variations = []
        attribute_values = []
# Guardar las imágenes
        for picture in pictures:
            ItemImage.objects.create(
                item=store_item,
                picture=picture  # Asumiendo que tu modelo ItemImage tiene un campo llamado 'image'
            )

        for variation_data in atributes_data:
            #por cada objeto dentro de atributes obtener los datos para crear la variacion
            attibute_value_list = variation_data.get('attribute_values')
            stock = variation_data.get('stock')

            #Crear la variacion
            item_variation = ItemVariation(
                store_item = store_item,
                stock = stock
            )

            item_variations.append(item_variation)

            # lista de atributos que llevara esa variacion
            for attr_data in attibute_value_list:
                #obtener la instancia del nombre del attribute
                atribute, created = Atribute.objects.get_or_create(name=attr_data['name'])

                #crear el attribute value
                attribute_value = AtributeValue(
                    item_variation=item_variation,
                    attribute=atribute,
                    value=attr_data['value']
                )
                attribute_values.append(attribute_value)

        ItemVariation.objects.bulk_create(item_variations)
        AtributeValue.objects.bulk_create(attribute_values)
        return store_item

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.price = validated_data.get('price')
        instance.stock = validated_data.get('stock')
        instance.save()

        current_variations = {variation.id: variation for variation in instance.variations.all()}
        current_images = {image.id: image for image in instance.item_images.all()}

        #extraer los attibutes
        variations_data = self.context['request'].data.get('attributes')
        request_images = self.context['request'].data.get('images')
        new_images = self.context['request'].FILES.getlist('new_images')
    

        new_variations = []
        new_attributes_values = []

        for variation_data in variations_data:
            variation_id = variation_data.get('id')
            stock = variation_data.get('stock')
            variation_attributes = variation_data.get('attribute_values')

            if variation_id and variation_id in current_variations:
                item_variation = current_variations.pop(variation_id)
                item_variation.stock = stock
                item_variation.save()

                item_variation.item_variations.all().delete()

                for attr_data in variation_attributes:
                    #obtener la instancia del nombre del attribute
                    atribute, created = Atribute.objects.get_or_create(name=attr_data['name'])

                    #crear el attribute value
                    attribute_value = AtributeValue(
                        item_variation=item_variation,
                        attribute=atribute,
                        value=attr_data['value']
                    )
                    new_attributes_values.append(attribute_value)
            else:
                item_variation = ItemVariation(
                    store_item=instance,
                    stock=stock
                )
                new_variations.append(item_variation)

                for attr_data in variation_attributes:
                    #obtener la instancia del nombre del attribute
                    atribute, created = Atribute.objects.get_or_create(name=attr_data['name'])

                    #crear el attribute value
                    attribute_value = AtributeValue(
                        item_variation=item_variation,
                        attribute=atribute,
                        value=attr_data['value']
                    )
                    new_attributes_values.append(attribute_value)
        for remaining_variations in current_variations.values():
            remaining_variations.delete()

        for request_image in request_images:
            #extrae el id de las foto que llegan
            request_id = request_image.get('id')
            #si el id existe y esta en current lo saca del arreglo
            if request_id and request_id in current_images:
                current_images.pop(request_id)

        #lo que quedo en el arreglo se elimina
        for remaining_images in current_images.values():
            remaining_images.delete()

        if new_images:
            for picture in new_images:
                ItemImage.objects.create(
                    item=instance,
                    picture=picture
                )   


        ItemVariation.objects.bulk_create(new_variations)
        AtributeValue.objects.bulk_create(new_attributes_values)
        return instance
    
class StoreWithItemsSerializer(serializers.ModelSerializer):
    items = StoreItemSerializer(many=True, read_only=True)
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

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)
    total_price = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        total_price = 0
        for product in products:
            order_product = OrderItem.objects.create(order_id=order, **product)
            print(vars(order_product))
            total_price += order_product.total_price

        order.total_price = total_price
        order.save()
        return order

#Proceso de cambio de contraseña
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User 
        fields = ['email']

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('No hay un usuario registrado con este email.')
        return value
    
class PasswordResetSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('El enlace no es valido')
        
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError('El token no es valido')
        
        return data
    
    def save(self):
        uid = urlsafe_base64_decode(self.validated_data['uidb64']).decode()
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()


