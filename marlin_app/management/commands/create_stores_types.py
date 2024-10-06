from django.core.management.base import BaseCommand
from marlin_app.models import StoreType
import os
from django.conf import settings
from cloudinary.uploader import upload

class Command(BaseCommand):
    help = 'Creacion de tipos de tienda'

    def handle(self, *args, **kwargs):
        types = [
            'Zapateria',
            'Ferreteria',
            'Mascotas',
            'Ropa',
            'Surf',
            'Pesca',
            'Deporte',
            'Bisuteria',
            'Pasamaneria',
            'Floristeria'
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

                # Imprimir las respuestas de Cloudinary para verificar las URLs
                # print(f"Uploaded {stype} image: {image_uploaded}")
                # print(f"Uploaded {stype} selected image: {image_selected_uploaded}")

                # Crear el nuevo StoreType con las URLs correctas
                url1 = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
                url2 = image_selected_uploaded.get('secure_url', image_selected_uploaded.get('url', ''))

                # Usar split para extraer la parte deseada
                extracted_url1 = url1.split('image', 1)[1]
                extracted_url2 = url2.split('image', 1)[1]

                # Si deseas agregar "image" de vuelta al inicio de la cadena extraída
                final_url1 = 'image' + extracted_url1
                final_url2 = 'image' + extracted_url2
                new_type = StoreType(
                    name=stype,
                    image= final_url1,  # Obtener 'secure_url' o 'url'
                    image_selected= final_url2  # Obtener 'secure_url' o 'url'
                )

                new_type.save()

        self.stdout.write(self.style.SUCCESS(f'Se crearon tipos de tienda.'))