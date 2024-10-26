from django.test import TestCase
from django.urls import reverse
from catalog.models import Product
from .models import Wishlist
from authentication.models import User

class WishlistViewTests(TestCase):
    def setUp(self):
        # Create a test user and a test product
        self.user = User.objects.create_user(username="testuser", password="belajardjango")
        self.product = Product.objects.create(
            nama="Test Product",
            kategori="kerajinan_tangan",
            harga=10000,
            toko="Test Store",
            alamat="Test Address",
            deskripsi="Test Description"
        )
        # Log in the user
        self.client.login(username='testuser', password='belajardjango')

        # Create a wishlist and add the product to it
        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist.product.add(self.product)

    def test_show_wishlist_view(self):
        # Test the show wishlist view for logged-in user
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')
        self.assertContains(response, self.product.nama)

    def test_delete_wishlist_view(self):
        # Test deleting a product from wishlist
        response = self.client.post(reverse('wishlist:delete_wishlist', args=[self.product.id]))
        self.assertRedirects(response, reverse('wishlist:show_wishlist'))
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_show_wishlist_json(self):
        # Test JSON wishlist response for the logged-in user
        response = self.client.get(reverse('wishlist:show_wishlist_json'))
        self.assertEqual(response.status_code, 200)
        expected_response = [
            {
                'id': self.product.id,
                'nama': self.product.nama,
                'toko': self.product.toko,
                'harga': self.product.harga,
                'gambar': self.product.gambar or '',
            }
        ]
        self.assertJSONEqual(response.content, {'wishlist_items': expected_response})

    def test_delete_wishlist_json(self):
        # Test deleting a product from the wishlist using JSON endpoint
        response = self.client.post(reverse('wishlist:delete_wishlist_json', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Product removed from wishlist'})
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_delete_wishlist_json_nonexistent_product(self):
        # Test attempting to delete a product not in wishlist (should return an error)
        response = self.client.post(reverse('wishlist:delete_wishlist_json', args=[999]))  # Using an invalid product ID
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Product not found in wishlist'})

    def test_unauthorized_access(self):
        # Test that unauthorized users cannot access wishlist views
        self.client.logout()
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        response = self.client.get(reverse('wishlist:show_wishlist_json'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        response = self.client.post(reverse('wishlist:delete_wishlist_json', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

