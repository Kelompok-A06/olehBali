from django import forms
from .models import Wishlist

class AddWishlistStatusForm(forms.Form):
    PRODUCT_STATUS =[
        (1, 'Should Buy'),
        (2, 'Interested'),
        (3, 'Maybe Later'),
    ]
    product_status = forms.ChoiceField(
        label='What’s your interest level in this product?',
        choices=PRODUCT_STATUS,
        widget=forms.RadioSelect
    )

class AddWishlistStatusForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product_status']
        widgets = {
            'product_status': forms.RadioSelect(choices=Wishlist.PRODUCT_STATUS)
        }