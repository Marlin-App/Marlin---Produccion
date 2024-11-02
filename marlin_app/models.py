from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from cloudinary.uploader import upload
from cloudinary.models import CloudinaryField
import os
import cloudinary.uploader
import uuid

# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    def get_default_user_type():
        return UserType.objects.get(id=3)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE, default=get_default_user_type)
    phone = models.CharField(max_length=8, null=True, blank=True)
    # picture = models.ImageField(upload_to='user_pictures/')
    picture = CloudinaryField('image', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.picture and hasattr(self.picture, 'name'):
            ext = os.path.splitext(self.picture.name)[1]
            public_id_picture = f'{self.user.username}_picture'
            image_uploaded = upload(self.picture, folder="userpictures", public_id=public_id_picture, format="webp")
            self.picture = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
        super(UserProfile, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Si hay una imagen, la convertimos a .webp antes de guardar
    #     if self.image:
    #         # Abrir la imagen usando PIL
    #         img = Image.open(self.image)
            
    #         # Convertir la imagen a webp en memoria
    #         webp_image = BytesIO()
    #         img.save(webp_image, format='WEBP', quality=85)  # Ajustar calidad si es necesario
            
    #         # Crear un nuevo archivo en memoria con la imagen .webp
    #         webp_image.seek(0)  # Regresar al inicio del archivo BytesIO
            
    #         # Asignar el nuevo nombre con la extensión .webp basado en el nombre de la tienda
    #         new_filename = f"{self.user.username}.webp"
    #         self.image = ContentFile(webp_image.getvalue(), new_filename)

    #     # Guardar la imagen convertida con el nuevo nombre
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user_id = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    senders = models.CharField(max_length=240)
    message = models.TextField()
    is_active = models.BooleanField(default=True)

class UserDirection(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='directions')
    zip_code = models.CharField(max_length=5)
    direction = models.CharField(max_length=250)
    specific_direction = models.TextField()
    
    def __str__(self):
        return f"{self.direction}, {self.zip_code}"

class StoreType(models.Model):
    name = models.CharField(max_length=250)
    image = CloudinaryField('image')
    image_selected = CloudinaryField('image')
    


    def __str__(self):
        return self.name


class Store(models.Model):
    STATUS_CHOICES = [
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
        ('Pendiente', 'Pendiente'),
        ('Inactivo', 'Inactivo'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_type = models.ManyToManyField(StoreType)
    name = models.CharField(max_length=250)
    description = models.TextField()
    canton = models.CharField(max_length=250)
    district = models.CharField(max_length=250)
    coodernates = models.CharField(max_length=250)
    num_sinpe = models.CharField(max_length=250)
    owner_sinpe = models.CharField(max_length=250)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    picture = CloudinaryField('image')
    banner = CloudinaryField('image')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Pendiente")

    def save(self, *args, **kwargs):
        if self.picture and hasattr(self.picture, 'name'):
            ext = os.path.splitext(self.picture.name)[1]
            public_id_picture = f'{self.name}_picture'
            image_uploaded = upload(self.picture, folder="stores", public_id=public_id_picture, format="webp")
            self.picture = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
        
        if self.banner and hasattr(self.banner, 'name'):
            ext = os.path.splitext(self.banner.name)[1]
            public_id_banner = f'{self.name}_banner'
            banner_uploaded = upload(self.banner, folder="stores", public_id=public_id_banner, format="webp")
            self.banner = banner_uploaded.get('secure_url', banner_uploaded.get('url', ''))

        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ItemTag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class StoreItem(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="items")
    item_type = models.ForeignKey(ItemTag, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
        
    def __str__(self):
        return self.name
    
class ItemImage(models.Model):
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name="item_images")
    picture = CloudinaryField('image')

    def save(self, *args, **kwargs):
        if self.picture and hasattr(self.picture, 'name'):
            # Obtener la extensión del archivo original
            ext = os.path.splitext(self.picture.name)[1]
            
            # Contar cuántas imágenes están asociadas al StoreItem
            image_count = ItemImage.objects.filter(item=self.item).count() + 1
            
            # Generar el nombre con el número secuencial
            public_id_picture = f'{self.item.name}_pic_{image_count}'
            
            # Subir la imagen a Cloudinary con el nombre único y formato webp
            image_uploaded = upload(self.picture, folder="items", public_id=public_id_picture, format="webp")
            
            # Asignar la URL segura de la imagen a la instancia
            self.picture = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
        
        super(ItemImage, self).save(*args, **kwargs)
    
class Atribute(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
class ItemVariation(models.Model):
    store_item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='variations')
    stock = models.IntegerField()

class AtributeValue(models.Model):
    item_variation = models.ForeignKey(ItemVariation, on_delete=models.CASCADE, related_name='item_variations')
    attribute = models.ForeignKey(Atribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Enviada', 'Enviada'),
        ('Entregada', 'Entregada'),
        ('Cancelada', 'Cancelada'),
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_num = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(default='Pendiente', choices=STATUS_CHOICES,  max_length=100)
    direction = models.TextField()
    voucher = CloudinaryField('image', blank=True, null=True)
    def __str__(self):
        return f"Precio: {self.total_price}"
    
    def save(self, *args, **kwargs):
        if self.voucher and hasattr(self.voucher, 'name'):
            ext = os.path.splitext(self.voucher.name)[1]
            public_id_picture = f'{self.name}_voucher'
            image_uploaded = upload(self.voucher, folder="vouchers", public_id=public_id_picture, format="webp")
            self.voucher = image_uploaded.get('secure_url', image_uploaded.get('url', ''))

        super(Order, self).save(*args, **kwargs)
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    item_id = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    item_variation_id = models.ForeignKey(ItemVariation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    #delivery = models.ForeignKey(User, on_delete=models.CASCADE) ver si se puede incluir un atributo mas la tabla de user para identificar un user, delivery o store owner

    def save(self, *args, **kwargs):
        self.total_price = self.item_id.price * self.quantity
        return super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_id
    
class Invoice(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField() #cambiar este por un nuevo modelo tipo PaymentMethod
    issue_date = models.DateTimeField()

    def __str__(self):
        return self.issue_date
    
class DeliveryProfile(models.Model):
    VEHICLE_CHOICES = [
        ('Carga Liviana', 'Carga Liviana'),
        ('Liviano', 'Liviano'),
        ('Bicicleta', 'Bicicleta'),
        ('Motocicleta', 'Motocicleta'),
    ]
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Bloqueado', 'Bloqueado'),
        ('Aprobado', 'Aprobado'),
    ]
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate = models.CharField(max_length=10)
    vehicle = models.CharField(choices=VEHICLE_CHOICES, max_length=20)
    selfie = CloudinaryField('image')
    vehicle_picture = CloudinaryField('image')
    iD_front_picture = CloudinaryField('image')
    iD_back_picture = CloudinaryField('image')
    license_picture = CloudinaryField('image')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pendiente')

    def save(self, *args, **kwargs):
        cloudinary_fields = ['selfie', 'vehicle_picture', 'iD_front_picture', 'iD_back_picture', 'license_picture']
        
        for field in cloudinary_fields:
            image_field = getattr(self, field, None)
            if image_field and hasattr(image_field, 'name'):
                ext = os.path.splitext(image_field.name)[1]
                public_id = f'{self.user_id}_{field}'
                uploaded_image = upload(
                    image_field,
                    folder="stores",
                    public_id=public_id,
                    format="webp"
                )
                setattr(self, field, uploaded_image.get('secure_url', uploaded_image.get('url', '')))
        
        super().save(*args, **kwargs)
   