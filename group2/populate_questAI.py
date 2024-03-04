import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'group2.settings')
django.setup()

from django.contrib.auth.models import User
from questAI.models import Products, Baskets, Reviews, Comments


def populate():
    product_details = [
        {'productId': 1, 'productName': 'Sword of Flames', 'productDescription': "A blade forged in the belly of a volcano. It's location has been lost for eons but when a user finds it, they will posess the powers of the inferno", 'price': 19.99, 'category': 'Weapon', 'image_path': '/static/images/SwordOfFlames.png'},
        {'productId': 2, 'productName': 'Potion of Giants', 'productDescription': "An elixir that bestows a gigantic size and strength to the user. It was last seen in the kingdom of Aberdeen, being stolen by goblins", 'price': 69.99, 'category': 'Potion', 'image_path': '/static/images/PotionOfGiants.png'},
        {'productId': 3, 'productName': 'Cloak of Invisibility', 'productDescription': "Woven from the threads of night itself, this cloak grants its wearer the power to become unseen by mortal eyes. A favorite among spies and thieves.", 'price': 149.99, 'category': 'Apparel', 'image_path': '/static/images/InvisCloak.png'},
        {'productId': 4, 'productName': 'Boots of Speed', 'productDescription': "These enchanted boots double the speed of the wearer, making them a valuable asset for messengers and adventurers alike. Just be careful not to run off cliffs.", 'price': 89.99, 'category': 'Apparel', 'image_path': '/static/images/BootsOfSpeed.png'},
        {'productId': 5, 'productName': 'Ring of Health', 'productDescription': "A simple band that radiates a soft warmth, slowly healing the wounds of those who wear it. A must-have for any who venture into danger.", 'price': 109.99, 'category': 'Apparel', 'image_path': '/static/images/RingOfHealth.png'},
        {'productId': 6, 'productName': 'Staff of Wisdom', 'productDescription': "Carved from an ancient tree, this staff is said to grant wisdom beyond measure to those deemed worthy. Many seek it, but few are chosen.", 'price': 259.99, 'category': 'Weapon', 'image_path': '/static/images/StaffOfWisdom.png'},
    ]
    for p_detail in product_details:
        add_product(productID=p_detail['productId'], productName=p_detail['productName'], productDescription=p_detail['productDescription'], price=p_detail['price'], category=p_detail['category'], image_path=p_detail['image_path'])

    for p in Products.objects.all():
        print(f'{p}')

def add_product(productID, productName, productDescription, price, category, image_path):

    p, created = Products.objects.get_or_create(productId=productID, defaults={'productName': productName, 'productDescription': productDescription, 'price': price, 'category': category, 'image_path': image_path})
    p.save()

    return p

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
