from django.test import TestCase
from django.urls import reverse
from catalog.models import Product
from .models import Wishlist
from django.contrib.auth.models import User

class WishlistViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username="testuser", password="belajardjango")
        self.product = Product.objects.create(
            nama="Test Product",
            kategori="kerajinan_tangan",
            harga=10000,
            toko="Test Store",
            alamat="Test Address",
            deskripsi="Test Description"
        )
        self.client.login(username='testuser', password='belajardjango')

        # Add product to wishlist for test user
        self.wishlist = Wishlist.objects.create(user=self.user, product=self.product)

    def test_show_wishlist_view(self):
        # Test access to the wishlist view page
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')
        self.assertContains(response, self.product.nama)

    def test_delete_wishlist_view(self):
        # Test deletion of product from wishlist
        response = self.client.post(reverse('wishlist:delete_wishlist', args=[self.product.id]))
        self.assertRedirects(response, reverse('wishlist:show_wishlist'))
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_show_wishlist_json(self):
        # Test JSON response of the wishlist items
        response = self.client.get(reverse('wishlist:show_wishlist_json'))
        self.assertEqual(response.status_code, 200)
        expected_response = [
            {
                'id': self.product.id,
                'nama': self.product.nama,
                'toko': self.product.toko,
                'harga': self.product.harga,
                'gambar': self.product.gambar if self.product.gambar else '',
            }
        ]
        self.assertJSONEqual(response.content, {'wishlist_items': expected_response})

    def test_delete_wishlist_json(self):
        # Test JSON response for successful wishlist item deletion
        response = self.client.post(reverse('wishlist:delete_wishlist_json', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Product removed from wishlist'})
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_delete_wishlist_json_nonexistent_product(self):
        # Test JSON response when deleting a non-existent wishlist item
        response = self.client.post(reverse('wishlist:delete_wishlist_json', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Product not found in wishlist'})

    def test_add_wishlist_view(self):
        # Test adding a product to wishlist through add_wishlist view
        response = self.client.post(reverse('wishlist:add_wishlist', args=[self.product.id]))
        self.assertRedirects(response, reverse('catalog:catalog'))
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_add_wishlist_json(self):
        # Test JSON response for adding a product to wishlist
        response = self.client.post(reverse('wishlist:add_wishlist_json', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        expected_response = {
            'status': 'info',  # If already exists in wishlist
            'message': 'Product is already in your wishlist',
        }
        self.assertJSONEqual(response.content, expected_response)

    def test_unauthorized_access(self):
        # Test redirect to login for unauthorized access to views
        self.client.logout()
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 302)
        response = selfgit.client.get(reverse('wishlist:show_wishlist_json'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('wishlist:delete_wishlist_json', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)