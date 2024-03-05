import os
import django
from django.core.files.base import ContentFile

from group2 import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'group2.settings')
django.setup()

from django.contrib.auth.models import User
from questAI.models import Products, Baskets, Reviews, Comments
from django.core.files import File
from django.core.files.images import ImageFile


def populate():
    product_details = [
        {'productName': 'Sword of Flames', 'productDescription': "A blade forged in the belly of a volcano. It's location has been lost for eons but when a user finds it, they will posess the powers of the inferno", 'price': 19.99, 'category': 'Weapon', 'image': 'product_images/SwordOfFlames.png'},
        {'productName': 'Potion of Giants', 'productDescription': "An elixir that bestows a gigantic size and strength to the user. It was last seen in the kingdom of Aberdeen, being stolen by goblins", 'price': 69.99, 'category': 'Potion', 'image': 'product_images/PotionOfGiants.png'},
        {'productName': 'Cloak of Invisibility', 'productDescription': "Woven from the threads of night itself, this cloak grants its wearer the power to become unseen by mortal eyes. A favorite among spies and thieves.", 'price': 149.99, 'category': 'Apparel', 'image': 'product_images/InvisCloak.png'},
        {'productName': 'Boots of Speed', 'productDescription': "These enchanted boots double the speed of the wearer, making them a valuable asset for messengers and adventurers alike. Just be careful not to run off cliffs.", 'price': 89.99, 'category': 'Apparel', 'image': 'product_images/BootsOfSpeed.png'},
        {'productName': 'Ring of Health', 'productDescription': "A simple band that radiates a soft warmth, slowly healing the wounds of those who wear it. A must-have for any who venture into danger.", 'price': 109.99, 'category': 'Apparel', 'image': 'product_images/RingOfHealth.png'},
        {'productName': 'Staff of Wisdom', 'productDescription': "Carved from an ancient tree, this staff is said to grant wisdom beyond measure to those deemed worthy. Many seek it, but few are chosen.", 'price': 259.99, 'category': 'Weapon', 'image': 'product_images/StaffOfWisdom.png'},
    ]
    for p_detail in product_details:
        add_product(productName=p_detail['productName'], productDescription=p_detail['productDescription'], price=p_detail['price'], category=p_detail['category'], image=p_detail['image'])

    for p in Products.objects.all():
        print(f'{p}')


def add_product(productName, productDescription, price, category, image):
    product, created = Products.objects.get_or_create(
        productName=productName,
        defaults={
            'productDescription': productDescription,
            'price': price,
            'category': category,
        }
    )
    if created:
        image_abs_path = os.path.join(settings.MEDIA_ROOT, image.strip('/'))
        if os.path.exists(image_abs_path):
            if not product.image or os.path.basename(product.image.name) != os.path.basename(image_abs_path):
                with open(image_abs_path, 'rb') as img_file:
                    product.image.save(os.path.basename(image_abs_path), File(img_file), save=True)
            else:
                print(f"Image for '{productName}' is already up to date.")
        else:
            print(f"Image file does not exist: {image_abs_path}")
    else:
        print(f"Product with name '{productName}' already exists. Skipping creation.")

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
