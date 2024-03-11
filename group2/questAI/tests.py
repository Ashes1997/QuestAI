from django.test import TestCase
from questAI.models import Products, Baskets, Reviews, Comments, UserProfile, Purchase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

# Create your tests here.
class ProductModelTests(TestCase):
    def test_product_is_added_right(self):
        """
        Tests product given to model is returned correctly when requested
        """

        product = Products(productName='Product', productDescription='Description', price=69.69, category='Category')
        product.save()
        self.assertEqual(Products.objects.get(pk=product.productId).productName, 'Product')
        self.assertEqual(Products.objects.get(pk=product.productId).productDescription, 'Description')

class ReviewModelTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='111')
        product = Products.objects.create(productName='Product', productDescription='Description', price=1.00, category='Category')
        self.review = Reviews.objects.create(username=user, productId=product, review_type='like')

    def test_review_creation(self):
        """
        Test the creation of a review and check its been saved correctly
        """
        self.assertEqual(self.review.review_type, 'like')

    def test_unique_together_constraint(self):
        """
        Test that the unique_together constraint for username and productId is enforced, preventing users from making multiple reviews on one product
        """
        user = User.objects.get(username='user')
        product = Products.objects.get(productName='Product')
        with self.assertRaises(Exception): #this should cause an exception because of unique constraint
            Reviews.objects.create(username=user, productId=product, review_type='dislike')


class BasketUpdateTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='user', password='111')
        self.client.login(username='user', password='111')
        
        # Create a product
        self.product = Products.objects.create(
            productName="Product",
            productDescription="Description",
            price=9.99,
            category="Category",
        )

        # Add a basket item for the user
        self.basket_item = Baskets.objects.create(
            username=self.user,
            productId=self.product,
            price=self.product.price,
            quantity=1
        )

    def test_increase_basket_item_quantity(self):
        """
        Ensure that the basket item quantity increases when an increase action is sent.
        """
        response = self.client.post(reverse('questAI:update_basket'), {'item_id': self.basket_item.basketId, 'action': 'increase'})
        self.basket_item.refresh_from_db()
        self.assertEqual(self.basket_item.quantity, 2)


    def test_decrease_basket_item_quantity(self):
        """
        Ensure that the basket item quantity decreases upon receiving a "decrease" action,
        and if quantity goes below 1, the item is removed.
        """
        
        self.basket_item.quantity = 2
        self.basket_item.save()

        response = self.client.post(reverse('questAI:update_basket'), {'item_id': self.basket_item.basketId, 'action': 'decrease'})
        self.basket_item.refresh_from_db()
        self.assertEqual(self.basket_item.quantity, 1) #checks that its still in the basket afetr initial decrease

        # Test removing the item if quantity becomes less than 1
        response = self.client.post(reverse('questAI:update_basket'), {'item_id': self.basket_item.basketId, 'action': 'decrease'})
        self.assertFalse(Baskets.objects.filter(basketId=self.basket_item.basketId).exists())


