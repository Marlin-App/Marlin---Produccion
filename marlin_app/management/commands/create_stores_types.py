from django.core.management.base import BaseCommand
from marlin_app.models import StoreType
import os
from django.conf import settings
from cloudinary.uploader import upload

class Command(BaseCommand):
    help = 'Creacion de tipos de tienda'

    def handle(self, *args, **kwargs):
        types = [
            'Pesca',
            'Deporte',
            'Bisuteria',
            'Floristeria',
            'Ferreteria',
            'Mascotas',
            'Ropa',
            'Zapateria',
            'Surf',
            'Pasamaneria',
        ]
        images_dir = os.path.join(settings.MEDIA_ROOT, 'categories')
        image_files = os.listdir(images_dir)
        
        for i, stype in enumerate(types):
            # Cargar imágenes locales
            with open(os.path.join(images_dir, image_files[i * 2]), 'rb') as image_file, \
                 open(os.path.join(images_dir, image_files[i * 2 + 1]), 'rb') as image_selected_file:

                # Subir imágenes a Cloudinary
                image_uploaded = upload(image_file, folder="categories", public_id=f"{stype}_image", format="webp")
                image_selected_uploaded = upload(image_selected_file, folder="categories", public_id=f"{stype}_selected_image", format="webp")

                # Crear el nuevo StoreType con las URLs de Cloudinary
                new_type = StoreType(
                    name=stype,
                    image=image_uploaded['secure_url'],  # Guardar la URL pública de la imagen
                    image_selected=image_selected_uploaded['secure_url']  # Guardar la URL pública de la imagen seleccionada
                )

                new_type.save()

        self.stdout.write(self.style.SUCCESS(f'Se crearon tipos de tienda.'))