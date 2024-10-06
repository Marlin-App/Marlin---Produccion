from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

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
    phone = models.CharField(max_length=8)
    picture = models.ImageField(upload_to='user_pictures/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Si hay una imagen, la convertimos a .webp antes de guardar
        if self.picture:
            # Abrir la imagen usando PIL
            img = Image.open(self.picture)
            
            # Convertir la imagen a webp en memoria
            webp_image = BytesIO()
            img.save(webp_image, format='WEBP', quality=85)  # Ajustar calidad si es necesario
            
            # Crear un nuevo archivo en memoria con la imagen .webp
            webp_image.seek(0)  # Regresar al inicio del archivo BytesIO
            
            # Asignar el nuevo nombre con la extensión .webp basado en el nombre de la tienda
            new_filename = f"{self.user.username}.webp"
            self.picture = ContentFile(webp_image.getvalue(), new_filename)
        
        # Guardar la imagen convertida con el nuevo nombre
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username


class UserPaymentCard(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payment_cards')
    card_number = models.CharField(max_length=16)
    card_date = models.CharField(max_length=5)
    card_holder = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.card_holder} - {self.card_number}"


class UserDirection(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='directions')
    zip_code = models.CharField(max_length=5)
    direction = models.CharField(max_length=250)
    specific_direction = models.TextField()
    
    def __str__(self):
        return f"{self.direction}, {self.zip_code}"

class StoreType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Store(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    store_type = models.ManyToManyField(StoreType)
    name = models.CharField(max_length=250)
    description = models.TextField()
    location = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='store_pictures/')

    def save(self, *args, **kwargs):
        # Si hay una imagen, la convertimos a .webp antes de guardar
        if self.picture:
            # Abrir la imagen usando PIL
            img = Image.open(self.picture)
            
            # Convertir la imagen a webp en memoria
            webp_image = BytesIO()
            img.save(webp_image, format='WEBP', quality=85)  # Ajustar calidad si es necesario
            
            # Crear un nuevo archivo en memoria con la imagen .webp
            webp_image.seek(0)  # Regresar al inicio del archivo BytesIO
            
            # Asignar el nuevo nombre con la extensión .webp basado en el nombre de la tienda
            new_filename = f"{self.name}.webp"
            self.picture = ContentFile(webp_image.getvalue(), new_filename)
        
        # Guardar la imagen convertida con el nuevo nombre
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):

        # Eliminar la imagen del sistema de archivos si existe
        if self.picture:
            self.picture.delete(save=False)
        # Llamar al método delete() del padre para eliminar el objeto
        super().delete(*args, **kwargs)

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
    picture = models.ImageField(upload_to='product_pictures/')

    def save(self, *args, **kwargs):
        # Si hay una imagen, la convertimos a .webp antes de guardar
        if self.picture:
            # Abrir la imagen usando PIL
            img = Image.open(self.picture)
            
            # Convertir la imagen a webp en memoria
            webp_image = BytesIO()
            img.save(webp_image, format='WEBP', quality=85)  # Ajustar calidad si es necesario
            
            # Crear un nuevo archivo en memoria con la imagen .webp
            webp_image.seek(0)  # Regresar al inicio del archivo BytesIO
            
            # Asignar el nuevo nombre con la extensión .webp basado en el nombre de la tienda
            new_filename = f"{self.name}.webp"
            self.picture = ContentFile(webp_image.getvalue(), new_filename)
        
        # Guardar la imagen convertida con el nuevo nombre
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        
        # Eliminar la imagen del sistema de archivos si existe
        if self.picture:
            self.picture.delete(save=False)
        # Llamar al método delete() del padre para eliminar el objeto
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.name
    
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
    quantity = models.FloatField()
    total_price = models.FloatField()
    #delivery = models.ForeignKey(User, on_delete=models.CASCADE) ver si se puede incluir un atributo mas la tabla de user para identificar un user, delivery o store owner

    def __str__(self):
        return self.order_id
    
class Invoice(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField() #cambiar este por un nuevo modelo tipo PaymentMethod
    issue_date = models.DateTimeField()

    def __str__(self):
        return self.issue_date
   
    #metodos de pago
    #catalogo tienda








# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class UserType(models.Model):
#     name = models.CharField(max_length=100)

# class User (models.Model):
#     user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     password = models.CharField(max_length=100)
#     profile_picture = models.CharField()

# class UserDirection(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     zip_code = models.CharField(max_length=5)
#     direction = models.CharField(max_length=100)
#     specific_direction = models.TextField()

# class Store(models.Model):
#     pass
