from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from cloudinary.uploader import upload
from cloudinary.models import CloudinaryField
import os
import cloudinary.uploader

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

    def save(self, *args, **kwargs):
        if self.picture and hasattr(self.picture, 'name'):
            ext = os.path.splitext(self.picture.name)[1]
            public_id_picture = f'{self.name}_picture'
            image_uploaded = upload(self.picture, folder="stores", public_id=public_id_picture, format="webp")
            self.picture = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
        
        if self.banner and hasattr(self.picture, 'name'):
            ext = os.path.splitext(self.banner.name)[1]
            public_id_banner = f'{self.name}_banner'
            banner_uploaded = upload(self.banner, folder="stores", public_id=public_id_banner, format="webp")
            self.banner = banner_uploaded.get('secure_url', banner_uploaded.get('url', ''))

        super(Store, self).save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     # Si hay una imagen, la convertimos a .webp antes de guardar
    #     if self.picture:
    #         # Abrir la imagen usando PIL
    #         img = Image.open(self.picture)
            
    #         # Convertir la imagen a webp en memoria
    #         webp_image = BytesIO()
    #         img.save(webp_image, format='WEBP', quality=85)  # Ajustar calidad si es necesario
            
    #         # Crear un nuevo archivo en memoria con la imagen .webp
    #         webp_image.seek(0)  # Regresar al inicio del archivo BytesIO
            
    #         # Asignar el nuevo nombre con la extensión .webp basado en el nombre de la tienda
    #         new_filename = f"{self.name}.webp"
    #         self.picture = ContentFile(webp_image.getvalue(), new_filename)

    #     # Guardar la imagen convertida con el nuevo nombre
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     # Eliminar la imagen del sistema de archivos si existe
    #     if self.picture:
    #         self.picture.delete(save=False)
    #     # Llamar al método delete() del padre para eliminar el objeto
    #     super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

class ItemTag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class StoreItem(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemTag, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    picture = CloudinaryField('image')

    def save(self, *args, **kwargs):
        if self.picture and hasattr(self.picture, 'name'):
            ext = os.path.splitext(self.picture.name)[1]
            public_id_picture = f'{self.name}_picture'
            image_uploaded = upload(self.picture, folder="items", public_id=public_id_picture, format="webp")
            self.picture = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
        super(StoreItem, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Atribute(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
class AtributeValue(models.Model):
    attribute = models.ForeignKey(Atribute, on_delete=models.CASCADE)
    storeItem = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField()
    #delivery = models.ForeignKey(User, on_delete=models.CASCADE) ver si se puede incluir un atributo mas la tabla de user para identificar un user, delivery o store owner

    def __str__(self):
        return self.user_id
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    #delivery = models.ForeignKey(User, on_delete=models.CASCADE) ver si se puede incluir un atributo mas la tabla de user para identificar un user, delivery o store owner

    def __str__(self):
        return self.order_id
    
class Invoice(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField() #cambiar este por un nuevo modelo tipo PaymentMethod
    issue_date = models.DateTimeField()

    def __str__(self):
        return self.issue_date
   